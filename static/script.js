async function summarizeText() {
    const input = document.getElementById("inputText").value;
    const response = await fetch("/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: input })
    });

    const data = await response.json();
    document.getElementById("output").innerText = data.summary || data.error;
}
