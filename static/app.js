// ============================================================
// QA AI ASSISTANT - COMPLETE FRONTEND
// ============================================================

const SESSION_KEY = "qa_ai_session_id";


// ============================================================
// SESSION
// ============================================================

function getSessionId() {

    let sessionId =
        localStorage.getItem(SESSION_KEY);

    if (!sessionId) {

        sessionId =
            crypto.randomUUID();

        localStorage.setItem(
            SESSION_KEY,
            sessionId
        );
    }

    return sessionId;
}


const sessionId = getSessionId();


// ============================================================
// DOM HELPERS
// ============================================================

function getInput() {
    return document.getElementById("user-input");
}


function getChatBox() {
    return document.getElementById("chat-box");
}


// ============================================================
// MESSAGE DISPLAY
// ============================================================

function addMessage(sender, message, type) {

    const chatBox = getChatBox();

    if (!chatBox) {
        console.error("chat-box not found");
        return;
    }


    const messageElement =
        document.createElement("div");

    messageElement.classList.add(
        "message",
        type
    );


    const senderElement =
        document.createElement("strong");

    senderElement.textContent =
        sender + ":";


    const contentElement =
        document.createElement("div");

    contentElement.textContent =
        typeof message === "string"
            ? message
            : JSON.stringify(
                message,
                null,
                2
            );


    messageElement.appendChild(
        senderElement
    );


    messageElement.appendChild(
        document.createElement("br")
    );


    messageElement.appendChild(
        contentElement
    );


    chatBox.appendChild(
        messageElement
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// ============================================================
// LOADING
// ============================================================

function addLoadingMessage() {

    removeLoadingMessage();


    const chatBox =
        getChatBox();


    const loading =
        document.createElement("div");


    loading.id =
        "loading-message";


    loading.classList.add(
        "message",
        "assistant"
    );


    loading.textContent =
        "AI is thinking...";


    chatBox.appendChild(
        loading
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function removeLoadingMessage() {

    const loading =
        document.getElementById(
            "loading-message"
        );


    if (loading) {
        loading.remove();
    }
}


// ============================================================
// BUTTON STATE
// ============================================================

function setButtonsDisabled(disabled) {

    const buttonIds = [
        "send-button",
        "analyze-button",
        "generate-button",
        "upload-button"
    ];


    for (const id of buttonIds) {

        const button =
            document.getElementById(id);


        if (button) {
            button.disabled =
                disabled;
        }
    }
}


// ============================================================
// GENERIC API REQUEST
// ============================================================

async function postJson(
    endpoint,
    body
) {

    const response =
        await fetch(
            endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(body)
            }
        );


    if (!response.ok) {

        let errorMessage =
            `HTTP ${response.status}`;


        try {

            const errorData =
                await response.json();


            if (errorData.detail) {
                errorMessage =
                    errorData.detail;
            }

        } catch (error) {
            // Keep HTTP status message.
        }


        throw new Error(
            errorMessage
        );
    }


    return await response.json();
}


// ============================================================
// SEND CHAT MESSAGE
// ============================================================

async function sendMessage() {

    const input =
        getInput();


    if (!input) {
        console.error(
            "user-input not found"
        );
        return;
    }


    const message =
        input.value.trim();


    if (!message) {

        alert(
            "Please enter a question."
        );

        return;
    }


    addMessage(
        "You",
        message,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/chat",
                {
                    session_id:
                        sessionId,

                    message:
                        message
                }
            );


        removeLoadingMessage();


        addMessage(
            "AI",
            data.response ||
            "No response received.",
            "assistant"
        );


        if (
            data.sources &&
            data.sources.length > 0
        ) {

            addSources(
                data.sources
            );
        }


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Chat request failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// SOURCES
// ============================================================

function addSources(sources) {

    const chatBox =
        getChatBox();


    const sourceElement =
        document.createElement("div");


    sourceElement.classList.add(
        "message",
        "assistant"
    );


    const title =
        document.createElement("strong");


    title.textContent =
        "📚 Sources:";


    sourceElement.appendChild(
        title
    );


    sourceElement.appendChild(
        document.createElement("br")
    );


    for (
        const source of sources
    ) {

        const line =
            document.createElement("div");


        const sourceName =
            source.source ||
            "Unknown source";


        const chunk =
            source.chunk_id ??
            "N/A";


        // ChromaDB normally returns distance.
        // Older search code may return score.
        const relevance =
            source.score ??
            source.distance ??
            "N/A";


        line.textContent =
            `• ${sourceName} ` +
            `(chunk ${chunk}, ` +
            `distance/score ${relevance})`;


        sourceElement.appendChild(
            line
        );
    }


    chatBox.appendChild(
        sourceElement
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// ============================================================
// ANALYZE REQUIREMENT
// ============================================================

async function analyzeRequirement() {

    const input =
        getInput();


    const requirement =
        input.value.trim();


    if (!requirement) {

        alert(
            "Please enter a requirement first."
        );

        return;
    }


    addMessage(
        "You",
        requirement,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        // IMPORTANT:
        // Backend endpoint is /analyze-requirement

        const data =
            await postJson(
                "/analyze-requirement",
                {
                    requirement:
                        requirement
                }
            );


        removeLoadingMessage();


        let result;


        if (
            typeof data.response ===
            "string"
        ) {

            result =
                data.response;

        } else if (
            typeof data.analysis ===
            "string"
        ) {

            result =
                data.analysis;

        } else if (
            typeof data.result ===
            "string"
        ) {

            result =
                data.result;

        } else {

            result =
                JSON.stringify(
                    data,
                    null,
                    2
                );
        }


        addMessage(
            "AI - Requirement Analysis",
            result,
            "assistant"
        );


    } catch (error) {

        console.error(
            "Requirement analysis error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Requirement analysis failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// GENERATE TEST CASES
// ============================================================

async function generateTestCases() {

    const input =
        getInput();


    const requirement =
        input.value.trim();


    if (!requirement) {

        alert(
            "Please enter a requirement first."
        );

        return;
    }


    addMessage(
        "You",
        requirement,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/generate-test-cases",
                {
                    requirement:
                        requirement
                }
            );


        removeLoadingMessage();


        let result;


        if (
            typeof data.response ===
            "string"
        ) {

            result =
                data.response;

        } else if (
            typeof data.test_cases ===
            "string"
        ) {

            result =
                data.test_cases;

        } else {

            result =
                JSON.stringify(
                    data,
                    null,
                    2
                );
        }


        addMessage(
            "AI - Generated Test Cases",
            result,
            "assistant"
        );


    } catch (error) {

        console.error(
            "Test generation error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Test case generation failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// UPLOAD DOCUMENT
// ============================================================

async function uploadDocument() {

    const fileInput =
        document.getElementById(
            "file-input"
        );


    if (!fileInput) {

        alert(
            "File input not found."
        );

        return;
    }


    const file =
        fileInput.files[0];


    if (!file) {

        alert(
            "Please choose a document first."
        );

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",

                    body:
                        formData
                }
            );


        if (!response.ok) {

            let message =
                `HTTP ${response.status}`;


            try {

                const errorData =
                    await response.json();


                if (errorData.detail) {
                    message =
                        errorData.detail;
                }

            } catch (error) {
                // Keep HTTP error.
            }


            throw new Error(
                message
            );
        }


        const data =
            await response.json();


        removeLoadingMessage();


        addMessage(
            "AI",
            data.message ||
            data.response ||
            "Document uploaded successfully.",
            "assistant"
        );


        fileInput.value = "";


    } catch (error) {

        console.error(
            "Upload error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Document upload failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// API TESTING
// ============================================================

async function runApiTest() {

    const input =
        getInput();


    const apiDescription =
        input.value.trim();


    if (!apiDescription) {

        alert(
            "Please enter an API description first."
        );

        return;
    }


    addMessage(
        "You",
        apiDescription,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/api-test",
                {
                    api_description:
                        apiDescription
                }
            );


        removeLoadingMessage();


        addMessage(
            "AI - API Testing",
            data.response ||
            data.result ||
            JSON.stringify(
                data,
                null,
                2
            ),
            "assistant"
        );


    } catch (error) {

        console.error(
            "API testing error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `API testing failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// UI TESTING
// ============================================================

async function runUiTest() {

    const input =
        getInput();


    const requirement =
        input.value.trim();


    if (!requirement) {

        alert(
            "Please enter a UI testing requirement."
        );

        return;
    }


    addMessage(
        "You",
        requirement,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/ui-test",
                {
                    requirement:
                        requirement
                }
            );


        removeLoadingMessage();


        addMessage(
            "AI - UI Testing",
            data.response ||
            data.result ||
            JSON.stringify(
                data,
                null,
                2
            ),
            "assistant"
        );


    } catch (error) {

        console.error(
            "UI testing error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `UI testing failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// FAILURE ANALYSIS
// ============================================================

async function analyzeFailure() {

    const input =
        getInput();


    const failureText =
        input.value.trim();


    if (!failureText) {

        alert(
            "Please enter failure information."
        );

        return;
    }


    addMessage(
        "You",
        failureText,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/analyze-failure",
                {
                    test_type:
                        "UI/API",

                    execution_result:
                        failureText
                }
            );


        removeLoadingMessage();


        addMessage(
            "AI - Failure Analysis",
            data.response ||
            data.result ||
            JSON.stringify(
                data,
                null,
                2
            ),
            "assistant"
        );


    } catch (error) {

        console.error(
            "Failure analysis error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Failure analysis failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// AI AGENT
// ============================================================

async function runAgent() {

    const input =
        getInput();


    const message =
        input.value.trim();


    if (!message) {

        alert(
            "Please enter a task for the AI agent."
        );

        return;
    }


    addMessage(
        "You",
        message,
        "user"
    );


    input.value = "";


    addLoadingMessage();

    setButtonsDisabled(true);


    try {

        const data =
            await postJson(
                "/agent",
                {
                    message:
                        message
                }
            );


        removeLoadingMessage();


        addMessage(
            "AI Agent",
            data.response ||
            data.result ||
            JSON.stringify(
                data,
                null,
                2
            ),
            "assistant"
        );


    } catch (error) {

        console.error(
            "Agent error:",
            error
        );


        removeLoadingMessage();


        addMessage(
            "AI",
            `Agent request failed: ${error.message}`,
            "assistant"
        );


    } finally {

        setButtonsDisabled(false);

    }
}


// ============================================================
// ENTER KEY
// ============================================================

function handleKeyDown(event) {

    if (
        event.key === "Enter"
    ) {

        event.preventDefault();

        sendMessage();
    }
}


// ============================================================
// LOAD HISTORY
// ============================================================

async function loadHistory() {

    try {

        const response =
            await fetch(
                `/history/${sessionId}`
            );


        if (!response.ok) {
            return;
        }


        const data =
            await response.json();


        if (
            !data.messages
        ) {
            return;
        }


        for (
            const message
            of data.messages
        ) {

            const sender =
                message.role === "user"
                    ? "You"
                    : "AI";


            const type =
                message.role === "user"
                    ? "user"
                    : "assistant";


            addMessage(
                sender,
                message.content,
                type
            );
        }


    } catch (error) {

        console.error(
            "History loading error:",
            error
        );
    }
}


// ============================================================
// INITIALIZE
// ============================================================

window.addEventListener(
    "DOMContentLoaded",
    function () {

        const input =
            getInput();


        if (input) {

            input.addEventListener(
                "keydown",
                handleKeyDown
            );
        }


        loadHistory();

    }
);