async function check() {
  const spec = document.getElementById("specFile").files[0];
  const vectors = document.getElementById("vectorFile").files[0];

  if (!spec || !vectors) {
    showError("checkError", "Please select both JSON files.");
    return;
  }

  const btn = document.getElementById("checkBtn");

  setLoading(btn, true, "Checking...");

  hide("checkError");

  try {
    const formData = new FormData();

    formData.append("spec", spec);
    formData.append("vectors", vectors);

    const response = await fetch(
      "http://127.0.0.1:5000/check",
      {
        method: "POST",
        body: formData
      }
    );

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();

    renderCheckResult(data);

  } catch (error) {
    showError(
      "checkError",
      `Check failed: ${error.message}`
    );
  } finally {
    setLoading(btn, false);
  }
}


function renderCheckResult(data) {
  const summary = data.summary;

  if (!summary) {
    showError(
      "checkError",
      "Invalid response: summary data is missing."
    );

    return;
  }

  const total = summary.total || 0;
  const pass = summary.pass || 0;
  const fail = summary.fail || 0;

  const failRate = summary.fail_rate || 0;

  // 0.75 = 75%
  const passRate =
    total > 0
      ? pass / total
      : 0;

  document.getElementById("checkTotal").textContent =
    total;

  document.getElementById("checkPass").textContent =
    pass;

  document.getElementById("checkFail").textContent =
    fail;

  document.getElementById("checkFailRate").textContent =
    formatPercent(failRate);

  document.getElementById("passPercent").textContent =
    formatPercent(passRate);

  document.getElementById("passProgress").style.width =
    `${passRate * 100}%`;

  document.getElementById("failProgress").style.width =
    `${(1 - passRate) * 100}%`;

  document.getElementById("generatedLogFile").textContent =
    data.log_file || "No log file generated";

  const status =
    document.getElementById("checkerStatus");

  if (fail === 0) {
    status.textContent = "ALL PASS";
    status.className = "result-status status-pass";
  } else {
    status.textContent = `${fail} FAILED`;
    status.className = "result-status status-fail";
  }

  show("checkerResult");
}

async function analyze() {
  const log = document.getElementById("log").files[0];

  if (!log) {
    showError(
      "analyzeError",
      "Please select a CSV log file."
    );

    return;
  }

  const btn = document.getElementById("analyzeBtn");

  setLoading(btn, true, "Analyzing...");

  hide("analyzeError");

  try {
    const formData = new FormData();

    formData.append("log", log);

    const response = await fetch(
      "http://127.0.0.1:5000/api/analyze",
      {
        method: "POST",
        body: formData
      }
    );

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();

    renderAnalyzeResult(data);

  } catch (error) {
    showError(
      "analyzeError",
      `Analysis failed: ${error.message}`
    );
  } finally {
    setLoading(btn, false);
  }
}


function renderAnalyzeResult(data) {
  const summary = data.summary;

  if (!summary) {
    showError(
      "analyzeError",
      "Invalid response: summary data is missing."
    );

    return;
  }

  document.getElementById("analyzeTotal").textContent =
    summary.total || 0;

  document.getElementById("analyzePass").textContent =
    summary.pass || 0;

  document.getElementById("analyzeFail").textContent =
    summary.fail || 0;

  document.getElementById("analyzeFailRate").textContent =
    formatPercent(summary.fail_rate || 0);

  renderSignals(data.signals || []);

  renderErrorDistribution(
    data.error_distribution || {}
  );

  renderRootCauses(
    data.root_causes || []
  );

  show("analyzeResult");
}

function renderSignals(signals) {
  const table =
    document.getElementById("signalTable");

  table.innerHTML = "";

  signals.forEach(signal => {

    const rate = signal.fail_rate || 0;

    let status = "PASS";
    let statusClass = "signal-ok";

    if (rate > 0 && rate < 0.5) {
      status = "WARNING";
      statusClass = "signal-warning";
    }

    if (rate >= 0.5) {
      status = "FAIL";
      statusClass = "signal-fail";
    }

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>
        <strong>${escapeHtml(signal.signal)}</strong>
      </td>

      <td class="signal-rate">
        ${formatPercent(rate)}
      </td>

      <td class="${statusClass}">
        ${status}
      </td>
    `;

    table.appendChild(row);
  });
}

function renderErrorDistribution(errors) {
  const container =
    document.getElementById("errorDistribution");

  container.innerHTML = "";

  const entries =
    Object.entries(errors);

  if (entries.length === 0) {
    container.innerHTML = `
      <div class="cause">
        No failures detected.
      </div>
    `;

    return;
  }

  entries.forEach(([name, count]) => {

    const item =
      document.createElement("div");

    item.className = "error-item";

    item.innerHTML = `
      <span class="error-name">
        ${escapeHtml(name)}
      </span>

      <span class="error-count">
        ${count}
      </span>
    `;

    container.appendChild(item);
  });
}

function renderRootCauses(rootCauses) {
  const container =
    document.getElementById("rootCauseList");

  container.innerHTML = "";

  if (rootCauses.length === 0) {
    container.innerHTML = `
      <div class="cause">
        No root causes detected.
      </div>
    `;

    return;
  }

  rootCauses.forEach(root => {

    const cases =
      root.cases || [];

    const caseInfo =
      cases.length > 0
        ? cases
            .map(item =>
              `${item.case_id} · ${item.signal}`
            )
            .join(", ")
        : "N/A";

    const element =
      document.createElement("div");

    element.className = "root-cause";

    element.innerHTML = `
      <div class="root-cause-top">

        <span class="reason">
          ${escapeHtml(root.fail_reason)}
        </span>

        <span class="count">
          ${root.count || 0} occurrence(s)
        </span>

      </div>

      <div class="root-cause-grid">

        <div class="root-field">
          <span>Test case</span>
          <strong>
            ${escapeHtml(caseInfo)}
          </strong>
        </div>

        <div class="root-field">
          <span>Signal</span>
          <strong>
            ${escapeHtml(
              cases[0]?.signal || "N/A"
            )}
          </strong>
        </div>

        <div class="root-field">
          <span>Suspected cause</span>
          <div class="cause">
            ${escapeHtml(
              root.suspected_cause || "N/A"
            )}
          </div>
        </div>

      </div>
    `;

    container.appendChild(element);
  });
}

function setupFileInput(inputId) {
  const input =
    document.getElementById(inputId);

  const label =
    input.closest(".file-input");

  const text =
    label.querySelector(".file-text");

  input.addEventListener("change", () => {

    if (input.files.length > 0) {

      text.textContent =
        input.files[0].name;

      label.classList.add("active");

    } else {

      text.textContent =
        "Click to upload";

      label.classList.remove("active");
    }

  });
}

function setLoading(
  btn,
  loading = true,
  text = "Processing..."
) {
  if (loading) {
    btn.dataset.original =
      btn.innerText;

    btn.disabled = true;
    btn.innerText = text;

  } else {

    btn.disabled = false;

    btn.innerText =
      btn.dataset.original;
  }
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}


function show(id) {
  document
    .getElementById(id)
    .classList.remove("hidden");
}


function hide(id) {
  document
    .getElementById(id)
    .classList.add("hidden");
}


function showError(id, message) {
  const element =
    document.getElementById(id);

  element.textContent = message;

  element.classList.remove("hidden");
}


function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setupDragAndDrop(inputId) {
  const input = document.getElementById(inputId);
  const dropZone = input.closest(".file-input");

  if (!input || !dropZone) return;

  dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("drag-over");

    const files = event.dataTransfer.files;

    if (!files || files.length === 0) return;

    input.files = files;

    // Cập nhật tên file trên UI
    const fileText = dropZone.querySelector(".file-text");

    if (fileText) {
      fileText.textContent = files[0].name;
    }
  });

  // Khi click chọn file bình thường
  input.addEventListener("change", () => {
    const fileText = dropZone.querySelector(".file-text");

    if (fileText && input.files.length > 0) {
      fileText.textContent = input.files[0].name;
    }
  });
}

setupDragAndDrop("specFile");
setupDragAndDrop("vectorFile");
setupDragAndDrop("log");
