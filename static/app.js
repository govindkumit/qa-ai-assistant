const SESSION_KEY = "qa_ai_session_id";


function getSessionId() {

    let sessionId =
        localStorage.getItem(
            SESSION_KEY
        );

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


const sessionId =
    getSessionId();


// ==================================================
// CHAT
// ==================================================

async function sendMessage() {

    const input =
        document.getElementById(
            "user-input"
        );

    const message =
        input.value.trim();

    if (!message) {
        return;
    }


    addMessage(
        "You",
        message,
        "user"
    );


    input.value = "";


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            session_id:
                                sessionId,

                            message:
                                message
                        }
                    )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Chat request failed"
            );
        }


        addMessage(
            "AI",
            data.response,
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
            error
        );


        addMessage(
            "AI",
            "Sorry, something went wrong.",
            "assistant"
        );
    }
}


// ==================================================
// REQUIREMENT ANALYSIS
// ==================================================

async function analyzeRequirement() {

    const input =
        document.getElementById(
            "user-input"
        );


    const requirement =
        input.value.trim();


    if (!requirement) {

        addMessage(
            "AI",
            "Please enter a requirement first.",
            "assistant"
        );

        return;
    }


    addMessage(
        "You",
        "Analyze this requirement: " +
        requirement,
        "user"
    );


    input.value = "";


    const dashboard =
        document.getElementById(
            "requirement-analysis"
        );


    dashboard.style.display =
        "none";


    try {

        const response =
            await fetch(
                "/analyze-requirement",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            requirement:
                                requirement
                        }
                    )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Requirement analysis failed"
            );
        }


        displayRequirementAnalysis(
            data.requirement_analysis
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
            error
        );


        addMessage(
            "AI",
            "Requirement analysis failed: " +
            error.message,
            "assistant"
        );
    }
}


// ==================================================
// DISPLAY REQUIREMENT ANALYSIS
// ==================================================

function displayRequirementAnalysis(
    analysis
) {

    const dashboard =
        document.getElementById(
            "requirement-analysis"
        );


    dashboard.style.display =
        "block";


    document.getElementById(
        "requirement-quality"
    ).textContent =
        analysis.quality || "-";


    document.getElementById(
        "clarity-score"
    ).textContent =
        analysis.clarity_score || 0;


    document.getElementById(
        "completeness-score"
    ).textContent =
        analysis.completeness_score || 0;


    document.getElementById(
        "testability-score"
    ).textContent =
        analysis.testability_score || 0;


    const content =
        document.getElementById(
            "analysis-content"
        );


    content.innerHTML = "";


    addAnalysisSection(
        content,
        "📝 Summary",
        analysis.requirement_summary
    );


    addAnalysisList(
        content,
        "✅ Explicit Requirements",
        analysis.explicit_requirements
    );


    addAnalysisList(
        content,
        "❓ Ambiguities",
        analysis.ambiguities
    );


    addAnalysisList(
        content,
        "⚠ Missing Information",
        analysis.missing_information
    );


    addAnalysisList(
        content,
        "📋 Missing Acceptance Criteria",
        analysis.missing_acceptance_criteria
    );


    addAnalysisList(
        content,
        "✅ Positive Scenarios",
        analysis.positive_scenarios
    );


    addAnalysisList(
        content,
        "❌ Negative Scenarios",
        analysis.negative_scenarios
    );


    addAnalysisList(
        content,
        "🔢 Boundary Conditions",
        analysis.boundary_conditions
    );


    addAnalysisList(
        content,
        "⚠ Edge Cases",
        analysis.edge_cases
    );


    addAnalysisList(
        content,
        "🚨 QA Risks",
        analysis.qa_risks
    );


    addAnalysisList(
        content,
        "❓ Questions for Product Owner",
        analysis.questions_for_product_owner
    );


    addAnalysisList(
        content,
        "💡 Recommendations",
        analysis.recommendations
    );


    dashboard.scrollIntoView({
        behavior: "smooth"
    });
}


// ==================================================
// ANALYSIS SECTION
// ==================================================

function addAnalysisSection(
    parent,
    title,
    value
) {

    if (!value) {
        return;
    }


    const section =
        document.createElement(
            "div"
        );


    section.style.marginTop =
        "20px";


    const heading =
        document.createElement(
            "h3"
        );


    heading.textContent =
        title;


    section.appendChild(
        heading
    );


    const text =
        document.createElement(
            "div"
        );


    text.textContent =
        value;


    section.appendChild(
        text
    );


    parent.appendChild(
        section
    );
}


// ==================================================
// ANALYSIS LIST
// ==================================================

function addAnalysisList(
    parent,
    title,
    items
) {

    if (
        !items ||
        items.length === 0
    ) {

        return;
    }


    const section =
        document.createElement(
            "div"
        );


    section.style.marginTop =
        "20px";


    const heading =
        document.createElement(
            "h3"
        );


    heading.textContent =
        title;


    section.appendChild(
        heading
    );


    const list =
        document.createElement(
            "ul"
        );


    for (
        const item of items
    ) {

        const listItem =
            document.createElement(
                "li"
            );


        listItem.textContent =
            item;


        listItem.style.marginBottom =
            "8px";


        list.appendChild(
            listItem
        );
    }


    section.appendChild(
        list
    );


    parent.appendChild(
        section
    );
}


// ==================================================
// GENERATE TEST CASES
// ==================================================

async function generateTestCases() {

    const input =
        document.getElementById(
            "user-input"
        );


    const requirement =
        input.value.trim();


    if (!requirement) {

        addMessage(
            "AI",
            "Please enter a requirement first.",
            "assistant"
        );

        return;
    }


    addMessage(
        "You",
        "Generate test cases for: " +
        requirement,
        "user"
    );


    input.value = "";


    try {

        const response =
            await fetch(
                "/generate-test-cases",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            requirement:
                                requirement
                        }
                    )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Test case generation failed"
            );
        }


        displayTestCases(
            data.test_cases
        );


        displayCoverage(
            data.coverage,
            data.coverage_gaps,
            data.validation
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
            error
        );


        addMessage(
            "AI",
            "Test case generation failed: " +
            error.message,
            "assistant"
        );
    }
}


// ==================================================
// DISPLAY TEST CASES
// ==================================================

function displayTestCases(
    testCases
) {

    const chatBox =
        document.getElementById(
            "chat-box"
        );


    const container =
        document.createElement(
            "div"
        );


    container.classList.add(
        "message",
        "assistant"
    );


    const title =
        document.createElement(
            "strong"
        );


    title.textContent =
        "🧪 Generated Test Cases";


    container.appendChild(
        title
    );


    container.appendChild(
        document.createElement(
            "br"
        )
    );


    for (
        const testCase of testCases
    ) {

        const block =
            document.createElement(
                "div"
            );


        block.style.marginTop =
            "20px";


        const heading =
            document.createElement(
                "strong"
            );


        heading.textContent =
            `${testCase.test_case_id} - ` +
            `${testCase.scenario}`;


        block.appendChild(
            heading
        );


        const details = [

            [
                "Requirement ID",
                testCase.requirement_id
            ],

            [
                "Requirement",
                testCase.requirement
            ],

            [
                "Type",
                testCase.test_type
            ],

            [
                "Priority",
                testCase.priority
            ],

            [
                "Risk",
                testCase.risk
            ],

            [
                "Preconditions",
                Array.isArray(
                    testCase.preconditions
                )
                    ? testCase.preconditions.join(
                        " | "
                    )
                    : testCase.preconditions
            ],

            [
                "Steps",
                Array.isArray(
                    testCase.test_steps
                )
                    ? testCase.test_steps.join(
                        " → "
                    )
                    : testCase.test_steps
            ],

            [
                "Test Data",
                testCase.test_data
            ],

            [
                "Expected Result",
                testCase.expected_result
            ],

            [
                "Traceability",
                testCase.traceability
            ]
        ];


        for (
            const [label, value]
            of details
        ) {

            const line =
                document.createElement(
                    "div"
                );


            line.style.marginTop =
                "8px";


            const labelElement =
                document.createElement(
                    "strong"
                );


            labelElement.textContent =
                `${label}: `;


            line.appendChild(
                labelElement
            );


            const valueElement =
                document.createElement(
                    "span"
                );


            valueElement.textContent =
                value || "";


            line.appendChild(
                valueElement
            );


            block.appendChild(
                line
            );
        }


        container.appendChild(
            block
        );
    }


    chatBox.appendChild(
        container
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// ==================================================
// COVERAGE
// ==================================================

function displayCoverage(
    coverage,
    coverageGaps,
    validation
) {

    const dashboard =
        document.getElementById(
            "coverage-dashboard"
        );


    dashboard.style.display =
        "block";


    document.getElementById(
        "total-tests"
    ).textContent =
        coverage.total_test_cases;


    document.getElementById(
        "valid-tests"
    ).textContent =
        validation.valid;


    document.getElementById(
        "invalid-tests"
    ).textContent =
        validation.invalid;


    document.getElementById(
        "coverage-score"
    ).textContent =
        coverage.overall_coverage_percentage +
        "%";


    const counts =
        coverage.test_type_counts;


    document.getElementById(
        "positive-count"
    ).textContent =
        counts.Positive || 0;


    document.getElementById(
        "negative-count"
    ).textContent =
        counts.Negative || 0;


    document.getElementById(
        "boundary-count"
    ).textContent =
        counts.Boundary || 0;


    document.getElementById(
        "edge-count"
    ).textContent =
        counts.Edge || 0;


    const gapsElement =
        document.getElementById(
            "coverage-gaps"
        );


    gapsElement.innerHTML = "";


    const heading =
        document.createElement(
            "h3"
        );


    heading.textContent =
        "Coverage Gaps";


    gapsElement.appendChild(
        heading
    );


    if (
        !coverageGaps ||
        coverageGaps.length === 0
    ) {

        const message =
            document.createElement(
                "div"
            );


        message.textContent =
            "✅ No test-type coverage gaps detected.";


        gapsElement.appendChild(
            message
        );

    } else {

        for (
            const gap of coverageGaps
        ) {

            const element =
                document.createElement(
                    "div"
                );


            element.textContent =
                "⚠ Missing coverage: " +
                gap;


            gapsElement.appendChild(
                element
            );
        }
    }
}


// ==================================================
// UPLOAD
// ==================================================

async function uploadDocument() {

    const fileInput =
        document.getElementById(
            "document-file"
        );


    const status =
        document.getElementById(
            "upload-status"
        );


    if (
        !fileInput.files ||
        fileInput.files.length === 0
    ) {

        status.textContent =
            "Please select a file.";

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        fileInput.files[0]
    );


    status.textContent =
        "Uploading and indexing...";


    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Upload failed"
            );
        }


        status.textContent =
            data.message;


        fileInput.value = "";


    } catch (error) {

        console.error(
            error
        );


        status.textContent =
            "Upload failed: " +
            error.message;
    }
}


// ==================================================
// SOURCES
// ==================================================

function addSources(
    sources
) {

    const chatBox =
        document.getElementById(
            "chat-box"
        );


    const sourceElement =
        document.createElement(
            "div"
        );


    sourceElement.classList.add(
        "message",
        "assistant"
    );


    const title =
        document.createElement(
            "strong"
        );


    title.textContent =
        "📚 Sources:";


    sourceElement.appendChild(
        title
    );


    sourceElement.appendChild(
        document.createElement(
            "br"
        )
    );


    for (
        const source of sources
    ) {

        const line =
            document.createElement(
                "div"
            );


        line.textContent =
            `• ${source.source} ` +
            `(chunk ${source.chunk_id}, ` +
            `distance ${source.distance})`;


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


// ==================================================
// ENTER
// ==================================================

function handleKeyDown(
    event
) {

    if (
        event.key === "Enter"
    ) {

        sendMessage();
    }
}


// ==================================================
// HISTORY
// ==================================================

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


        for (
            const message of data.messages
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
            "Failed to load history:",
            error
        );
    }
}


window.addEventListener(
    "load",
    loadHistory
);