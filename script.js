// ===== Hospital Heart Disease Prediction: front-end logic =====
// 1. Asks the API (GET) which fields the model needs and builds the form.
// 2. Sends the filled-in form to the API (POST) and shows the result.

const API_URL = "/api/predict";

const statusBox = document.getElementById("status");
const form = document.getElementById("predict-form");
const fieldsBox = document.getElementById("fields");
const submitBtn = document.getElementById("submit-btn");
const resultCard = document.getElementById("result");
const resultIcon = document.getElementById("result-icon");
const resultLabel = document.getElementById("result-label");
const resultProb = document.getElementById("result-prob");
const barFill = document.getElementById("bar-fill");

// ---------- Step 1: build the form from the model's schema ----------
async function loadForm() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Server error");
    }
    buildFields(data.features);
    statusBox.hidden = true;
    form.hidden = false;
  } catch (error) {
    showStatus("Could not load the form. " + error.message, true);
  }
}

function buildFields(features) {
  fieldsBox.innerHTML = "";

  features.forEach((feature) => {
    const wrapper = document.createElement("div");
    wrapper.className = "field";

    const label = document.createElement("label");
    label.htmlFor = "f-" + feature.name;
    label.textContent = feature.label;
    wrapper.appendChild(label);

    let input;

    if (feature.type === "categorical") {
      input = document.createElement("select");
      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Select…";
      input.appendChild(placeholder);

      feature.options.forEach((option) => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        input.appendChild(opt);
      });
    } else {
      input = document.createElement("input");
      input.type = "number";
      input.step = feature.step;
      input.value = feature.default;
      input.inputMode = "decimal";

      const hint = document.createElement("span");
      hint.className = "hint";
      hint.textContent = "Typical range: " + feature.min + " to " + feature.max;
      wrapper.appendChild(input);
      wrapper.appendChild(hint);
    }

    input.id = "f-" + feature.name;
    input.name = feature.name;
    input.required = true;

    if (feature.type === "categorical") {
      wrapper.appendChild(input);
    }

    fieldsBox.appendChild(wrapper);
  });
}

// ---------- Step 2: send the values and show the answer ----------
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const inputs = {};
  new FormData(form).forEach((value, key) => {
    inputs[key] = value;
  });

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting…";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction failed");
    }
    showResult(data);
  } catch (error) {
    resultCard.hidden = true;
    showStatus("Prediction failed. " + error.message, true);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict";
  }
});

form.addEventListener("reset", () => {
  resultCard.hidden = true;
  statusBox.hidden = true;
});

function showResult(data) {
  statusBox.hidden = true;

  const positive = data.prediction === 1;
  const percent = Math.round(data.probability * 1000) / 10;

  resultCard.hidden = false;
  resultCard.classList.toggle("positive", positive);
  resultCard.classList.toggle("negative", !positive);
  resultIcon.textContent = positive ? "!" : "✓";
  resultLabel.textContent = data.label;
  resultProb.textContent = "Probability of heart disease: " + percent + "%";

  // Restart the bar animation from zero
  barFill.style.width = "0%";
  requestAnimationFrame(() => {
    barFill.style.width = percent + "%";
  });

  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showStatus(message, isError) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", Boolean(isError));
  statusBox.hidden = false;
}

loadForm();
