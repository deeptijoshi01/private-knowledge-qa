const BASE_URL = "http://127.0.0.1:8000";

/* ==============================
   Upload Document
================================ */
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const status = document.getElementById("uploadStatus");

    status.innerText = "";

    if (!fileInput.files.length) {
        status.innerText = "⚠ Please select a file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`${BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            status.innerText = `❌ ${data.detail}`;
            return;
        }

        status.innerText = `✅ Upload successful! Document ID: ${data.document_id}`;
        fileInput.value = "";

        loadDocuments();

    } catch (error) {
        status.innerText = "❌ Upload failed. Backend not reachable.";
    }
}


/* ==============================
   Load Documents
================================ */
async function loadDocuments() {
    const docBox = document.getElementById("documentsBox");
    docBox.innerHTML = "";

    try {
        const response = await fetch(`${BASE_URL}/documents`);
        const docs = await response.json();

        if (!docs.length) {
            docBox.innerText = "No documents uploaded yet.";
            return;
        }

        docs.forEach(doc => {
            const div = document.createElement("div");
            div.classList.add("doc-item");
            div.innerText = `📄 ${doc.id} - ${doc.name}`;
            docBox.appendChild(div);
        });

    } catch (error) {
        docBox.innerText = "Failed to load documents.";
    }
}


/* ==============================
   Clear Documents
================================ */
async function clearDocuments() {
    if (!confirm("Delete ALL documents?")) return;

    try {
        const response = await fetch(`${BASE_URL}/documents`, {
            method: "DELETE"
        });

        if (!response.ok) {
            alert("Failed to delete documents.");
            return;
        }

        alert("All documents deleted.");
        loadDocuments();

    } catch (error) {
        alert("Backend not reachable.");
    }
}


/* ==============================
   Ask Question
================================ */
async function askQuestion() {
    const questionInput = document.getElementById("questionInput");
    const answerBox = document.getElementById("answerBox");
    const sourcesBox = document.getElementById("sourcesBox");

    const question = questionInput.value.trim();

    answerBox.innerText = "";
    sourcesBox.innerHTML = "";

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    answerBox.innerText = "⏳ Processing...";

    try {
        const response = await fetch(
            `${BASE_URL}/ask?question=${encodeURIComponent(question)}`,
            { method: "POST" }
        );

        const data = await response.json();

        if (!response.ok) {
            answerBox.innerText = `❌ ${data.detail}`;
            return;
        }

        answerBox.innerText = data.answer;

        if (data.sources?.length) {
            data.sources.forEach(src => {
                const div = document.createElement("div");
                div.classList.add("doc-item");
                div.innerText = `📄 Document ${src.document_id}: ${src.snippet}`;
                sourcesBox.appendChild(div);
            });
        } else {
            sourcesBox.innerText = "No sources found.";
        }

    } catch (error) {
        answerBox.innerText = "❌ Backend not reachable.";
    }
}


/* ==============================
   System Status
================================ */
async function checkStatus() {
    const statusBox = document.getElementById("statusBox");
    statusBox.innerText = "Checking...";

    try {
        const response = await fetch(`${BASE_URL}/status`);
        const data = await response.json();

        statusBox.innerText = JSON.stringify(data, null, 2);

    } catch (error) {
        statusBox.innerText = "❌ Backend not reachable.";
    }
}


window.onload = function () {
    loadDocuments();
};
