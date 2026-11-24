const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".main-nav");
const dropdown = navigation.querySelector(".dropdown");

function setMenu(open) {
  navigation.classList.toggle("open", open);
  menu.setAttribute("aria-expanded", String(open));
}

menu.addEventListener("click", () => setMenu(menu.getAttribute("aria-expanded") === "false"));
navigation.addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (!link) return;

  if (link.hash && link.pathname === location.pathname && link.search === location.search) {
    const target = document.getElementById(link.hash.slice(1));
    if (target) {
      target.setAttribute("tabindex", "-1");
      target.focus({ preventScroll: true });
    }
  }

  dropdown.open = false;
  setMenu(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;

  if (dropdown.open) {
    dropdown.open = false;
    dropdown.querySelector("summary").focus();
  } else if (menu.getAttribute("aria-expanded") === "true") {
    setMenu(false);
    menu.focus();
  }
});

const galleryImage = document.querySelector("#gallery-image");
if (galleryImage) {
  const caption = document.querySelector("#gallery-caption");
  const controls = document.querySelector(".gallery-controls");

  controls.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;

    controls.querySelector('[aria-pressed="true"]').setAttribute("aria-pressed", "false");
    button.setAttribute("aria-pressed", "true");
    galleryImage.src = button.querySelector("img").src;
    galleryImage.alt = button.dataset.alt;
    caption.textContent = `Concept rendering / ${button.dataset.caption}`;
  });
}

const form = document.querySelector("#inquiry-form");
if (form) {
  const query = new URLSearchParams(location.search);
  const product = form.elements.namedItem("product");
  const artwork = form.elements.namedItem("artwork");
  const quantity = form.elements.namedItem("quantity");
  const submit = document.querySelector("#inquiry-submit");
  const status = form.querySelector(".form-status");
  const sample = query.get("intent") === "sample";

  function setInquiryIntent(isSample) {
    document.querySelector("#inquiry-kicker").textContent = isSample ? "Sample inquiry" : "Get a delivered quote";
    document.querySelector("#inquiry-title").textContent = isSample ? "See the packaging before you order." : "Put your brand on the packaging you serve.";
    document.querySelector("#form-heading").textContent = isSample ? "Request a sample kit" : "Get a delivered quote";
    document.querySelector("#inquiry-copy").textContent = isSample ? "Tell us which formats you’d like to compare." : "Tell us what you need and where it’s going.";
    document.querySelector("#quantity-field").hidden = isSample;
    quantity.required = !isSample;
    quantity.disabled = isSample;
    document.querySelector("#artwork-field").hidden = isSample;
    artwork.disabled = isSample;
    submit.textContent = isSample ? "Preview Sample Request" : "Get My Custom Quote ↗";
    status.textContent = "";
  }

  if (Array.from(product.options).some((option) => option.value === query.get("product"))) {
    product.value = query.get("product");
  }

  setInquiryIntent(sample);
  document.querySelectorAll('a[href="#quote"], a[href="#contact"]').forEach((link) => {
    link.addEventListener("click", () => {
      if (!query.has("intent")) return;
      query.delete("intent");
      const url = new URL(location.href);
      url.search = query.toString();
      if (url.protocol !== "file:") history.replaceState(null, "", url);
      setInquiryIntent(false);
    });
  });

  artwork.addEventListener("change", () => {
    const file = artwork.files[0];
    const allowed = /\.(pdf|png|jpe?g)$/i;
    const valid = !file || (allowed.test(file.name) && file.size <= 10 * 1024 * 1024);
    artwork.setCustomValidity(valid ? "" : "Choose a PDF, PNG, or JPEG file of 10 MB or less.");
    artwork.reportValidity();
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    status.textContent = "Preview complete. Your information was neither sent nor saved.";
  });

  submit.disabled = false;
}
