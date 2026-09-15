const messages = document.getElementById("messages");
const questionInput = document.getElementById("question");
const sendButton = document.getElementById("sendButton");


function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}


function cleanText(text) {

    // Normalize escaped Markdown
    text = text.replace(/\\#/g, "#");
    text = text.replace(/\\\-/g, "-");
    text = text.replace(/\\\*/g, "*");

    // Remove stray Markdown-only lines
    text = text.replace(/^\s*[-*]\s*$/gm, "");

    // Remove stray escaped star lines
    text = text.replace(/^\s*\\?\*+\s*$/gm, "");

    // Convert "1)" style numbering to "1."
    text = text.replace(/^(\d+)\)\s+/gm, "$1. ");

    // Remove escaped numbering
    text = text.replace(/^\\(\d+)\.\s+/gm, "$1. ");

    // Remove excessive blank lines
    text = text.replace(/\n{3,}/g, "\n\n");

    return text.trim();
}


function inlineMarkdown(text) {

    let html = escapeHtml(text);

    // Bold
    html = html.replace(
        /\*\*([^*\n]+)\*\*/g,
        "<strong>$1</strong>"
    );

    // Italic
    html = html.replace(
        /(?<!\*)\*([^*\n]+)\*(?!\*)/g,
        "<em>$1</em>"
    );

    // Inline code
    html = html.replace(
        /`([^`\n]+)`/g,
        "<code>$1</code>"
    );

    return html;
}


function formatMarkdown(text) {

    text = cleanText(text);

    const lines = text.split("\n");

    let html = "";
    let inList = false;
    let listType = null;


    function closeList() {

        if (inList) {

            html += listType === "ordered"
                ? "</ol>"
                : "</ul>";

            inList = false;
            listType = null;
        }
    }


    for (let i = 0; i < lines.length; i++) {

        let line = lines[i].trim();


        // Empty line
        if (!line) {

            closeList();

            continue;
        }


        // Horizontal rule
        if (/^---+$/.test(line)) {

            closeList();

            html += "<hr>";

            continue;
        }


        // H3
        if (/^###\s+/.test(line)) {

            closeList();

            const heading = line.replace(/^###\s+/, "");

            html += `<h3>${inlineMarkdown(heading)}</h3>`;

            continue;
        }


        // H2
        if (/^##\s+/.test(line)) {

            closeList();

            const heading = line.replace(/^##\s+/, "");

            html += `<h2>${inlineMarkdown(heading)}</h2>`;

            continue;
        }


        // H1
        if (/^#\s+/.test(line)) {

            closeList();

            const heading = line.replace(/^#\s+/, "");

            html += `<h1>${inlineMarkdown(heading)}</h1>`;

            continue;
        }


        // Numbered list
        const numberedMatch = line.match(
            /^\d+\.\s+(.+)$/
        );

        if (numberedMatch) {

            if (!inList || listType !== "ordered") {

                closeList();

                html += "<ol>";

                inList = true;

                listType = "ordered";
            }

            html += `<li>${inlineMarkdown(numberedMatch[1])}</li>`;

            continue;
        }


        // Bullet list
        const bulletMatch = line.match(
            /^[-*]\s+(.+)$/
        );

        if (bulletMatch) {

            if (!inList || listType !== "unordered") {

                closeList();

                html += "<ul>";

                inList = true;

                listType = "unordered";
            }

            html += `<li>${inlineMarkdown(bulletMatch[1])}</li>`;

            continue;
        }


        // Normal paragraph
        closeList();

        html += `<p>${inlineMarkdown(line)}</p>`;
    }


    closeList();

    return html;
}


function addMessage(text, type, route = null) {

    const message = document.createElement("div");

    message.className = `message ${type}`;


    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        type === "user" ? "You" : "AI";


    const bubble = document.createElement("div");

    bubble.className = "bubble";


    if (type === "assistant" && route) {

        const routeBadge = document.createElement("div");

        routeBadge.className = "route-badge";

        routeBadge.textContent = route;

        bubble.appendChild(routeBadge);
    }


    const content = document.createElement("div");


    if (type === "assistant") {

        content.innerHTML = formatMarkdown(text);

    } else {

        content.textContent = text;
    }


    bubble.appendChild(content);

    message.appendChild(avatar);

    message.appendChild(bubble);

    messages.appendChild(message);


    messages.scrollTop = messages.scrollHeight;
}


function getRouteLabel(route) {

    const routes = {

        rag: "🔍 RAG · Knowledge Base",

        web: "🌐 Web Search",

        mcp: "⚙ MCP · Calculator",

        direct: "✨ Direct Reasoning"
    };


    return routes[route] || null;
}


async function sendMessage() {

    const question = questionInput.value.trim();


    if (!question) {
        return;
    }


    addMessage(
        question,
        "user"
    );


    questionInput.value = "";

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";


    try {

        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Backend request failed"
            );
        }


        const data = await response.json();


        addMessage(
            data.answer,
            "assistant",
            getRouteLabel(data.route)
        );


    } catch (error) {

        console.error(error);


        addMessage(
            "Sorry, I couldn't connect to the AgentFlow backend.",
            "assistant"
        );


    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send";

        questionInput.focus();
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


questionInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);