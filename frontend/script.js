async function check() {
    const spec = document.getElementById("specFile").files[0];
    const vectors = document.getElementById("vectorFile").files[0];

    if (!spec || !vectors) {
        alert("Please select both JSON files");
        return;
    }

    const formData = new FormData();
    formData.append("spec", spec);
    formData.append("vectors", vectors);

    const response = await fetch("http://127.0.0.1:5000/check", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    document.getElementById("output").textContent =
        JSON.stringify(data, null, 2);
}

async function analyze() {
    const log = document.getElementById("log").files[0];

    if(!log){
        alert("Please select both JSON files");
        return;
    }

     const formData = new FormData();
    formData.append("log", log);

    const response = await fetch("http://127.0.0.1:5000/api/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    document.getElementById("output_analyze").textContent =
        JSON.stringify(data, null, 2);
}
