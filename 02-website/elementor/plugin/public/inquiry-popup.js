(() => {
  const popup = document.querySelector("[data-inquiry-popup]");
  if (!popup || typeof popup.showModal !== "function" || !window.crypto?.getRandomValues) return;

  const form = popup.querySelector("form");
  const contact = form.querySelector('[data-popup-step="contact"]');
  const details = form.querySelector('[data-popup-step="details"]');
  const scrollArea = form.querySelector(".cups1-popup-scroll");
  const status = form.querySelector("[data-popup-status]");
  const advance = form.querySelector('button[type="submit"]');
  const close = popup.querySelector(".cups1-popup-close");
  const title = popup.querySelector("h2");
  const progress = popup.querySelector("[data-popup-progress]");
  const productContext = popup.querySelector("[data-popup-context]");
  const consent = form.querySelector("[data-popup-consent]");
  const postalLabel = form.querySelector("[data-popup-postal]");
  const notesOptional = form.querySelector("[data-popup-notes-optional]");
  const sizes = form.querySelector("datalist");
  const { product: productField, dimensions, country, postal_code: postalCode, artwork } = form.elements;
  const routes = {
    "request-a-quote": "quote",
    "request-a-sample": "sample",
    "contact-sales": "contact",
    contact: "contact",
    "configure-packaging": "customize",
  };
  let trigger;
  let context;
  let step;
  let busy = false;

  async function fetchNonce() {
    const url = new URL(form.action);
    url.searchParams.set("action", "cups1_form_token");
    const response = await fetch(url, {
      cache: "no-store",
      credentials: "same-origin",
      signal: AbortSignal.timeout(6000),
    });
    const result = await response.json();
    if (!result.success || !result.data?.nonce) throw new Error("Form token unavailable");
    return result.data.nonce;
  }

  function showProduct(size = "") {
    const option = productField.selectedOptions[0];
    productContext.hidden = !productField.value;
    productContext.textContent = productField.value ? [option.textContent, size].filter(Boolean).join(" · ") : "";
    const availableSizes = JSON.parse(option?.dataset.sizes || "[]");
    sizes.replaceChildren(...availableSizes.map((value) => new Option(value, value)));
    dimensions.placeholder = availableSizes[0] ? "e.g. " + availableSizes[0] : "Enter a size or dimensions";
  }

  function updatePostalField() {
    postalLabel.textContent = country.value === "Canada" ? "Postal code" : country.value === "United States" ? "ZIP code" : "ZIP or postal code";
    postalCode.placeholder = country.value === "Canada" ? "A1A 1A1" : country.value === "United States" ? "12345" : "";
    postalCode.inputMode = country.value === "United States" ? "numeric" : "text";
  }

  function selectedSize(container) {
    return container?.querySelector('[data-catalog-quote-size], select[name="attribute_size"], select[name="attribute_pa_size"]')?.value || "";
  }

  function startInquiry({ reason, product, size }) {
    form.reset();
    step = "contact";
    status.textContent = "";
    contact.hidden = contact.disabled = false;
    details.hidden = details.disabled = true;
    advance.hidden = false;
    advance.textContent = "Next";
    title.textContent = "Contact details";
    progress.textContent = "Step 1 of 2";
    progress.hidden = false;
    consent.hidden = false;
    artwork.setCustomValidity("");
    artwork.closest("details").open = false;
    updatePostalField();
    form.elements.reason.value = reason;
    productField.value = product;
    showProduct(size);
    context = {
      product,
      size,
      nonce: fetchNonce().catch(() => null),
      token: Array.from(crypto.getRandomValues(new Uint8Array(16)), (byte) => byte.toString(16).padStart(2, "0")).join(""),
    };
    if (!popup.open) popup.showModal();
    title.focus();
  }

  productField.addEventListener("change", () => {
    dimensions.value = "";
    showProduct();
  });
  dimensions.addEventListener("change", () => showProduct(dimensions.value.trim()));
  country.addEventListener("change", updatePostalField);
  artwork.addEventListener("change", () => {
    artwork.setCustomValidity(artwork.files[0]?.size > 5 * 1024 * 1024 ? "Choose a file of 5 MB or less." : "");
    artwork.reportValidity();
  });

  document.addEventListener("click", (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest("a[href]");
    if (!link || link.target && link.target !== "_self" || link.hasAttribute("download")) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin) return;
    const route = url.pathname.split("/").filter(Boolean).pop();
    const homeInquiry = url.pathname === "/" && url.hash === "#quote";
    const reason = link.dataset.inquiryReason || routes[route] || (homeInquiry ? url.searchParams.get("intent") || "quote" : "");
    if (!reason || !Array.from(form.elements.reason.options).some((option) => option.value === reason)) return;
    event.preventDefault();
    trigger = link;
    const currentURL = new URL(location.href);
    const currentInquiry = routes[location.pathname.split("/").filter(Boolean).pop()];
    const product = url.searchParams.get("packaging_product") || url.searchParams.get("product") ||
      (currentInquiry === reason ? currentURL.searchParams.get("packaging_product") : "") || "";
    const size = selectedSize(link.closest(".catalog-product-card, [data-product-detail]")) || url.searchParams.get("packaging_size") ||
      (currentInquiry === reason ? currentURL.searchParams.get("packaging_size") : "") || "";
    startInquiry({ reason, product, size });
  });

  close.addEventListener("click", () => { if (!busy) popup.close(); });
  popup.addEventListener("cancel", (event) => { if (busy) event.preventDefault(); });
  popup.addEventListener("close", () => trigger?.focus());

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy || step === "complete") return;
    busy = close.disabled = advance.disabled = true;
    status.textContent = "";
    const data = new FormData(form);
    data.set("action", "cups1_inquiry_step");
    data.set("step", step);
    data.set("token", context.token);
    if (step === "contact") {
      data.set("product", context.product);
      data.set("selected_size", context.size);
    }
    try {
      const prefetchedNonce = context.nonce;
      context.nonce = null;
      data.set("cups1_nonce", (await prefetchedNonce) || await fetchNonce());
      const response = await fetch(form.action, {
        method: "POST",
        body: data,
        credentials: "same-origin",
        signal: AbortSignal.timeout(step === "contact" ? 10000 : 30000),
      });
      const result = await response.json();
      if (!response.ok || !result.success) {
        status.textContent = result.data?.message || "Could not save. Please try again.";
        return;
      }
      if (step === "contact") {
        step = "details";
        const reason = data.get("reason");
        contact.hidden = contact.disabled = true;
        details.hidden = details.disabled = false;
        details.querySelectorAll("[data-reasons]").forEach((label) => {
          label.hidden = !label.dataset.reasons.split(" ").includes(reason);
          label.querySelector("input, select").disabled = label.hidden;
        });
        productField.value = context.product;
        dimensions.value = context.size;
        showProduct(context.size);
        form.elements.notes.required = reason === "contact";
        notesOptional.hidden = reason === "contact";
        title.textContent = "Request details";
        progress.textContent = "Step 2 of 2";
        consent.hidden = true;
        advance.textContent = "Done";
        status.textContent = "";
        scrollArea.scrollTop = 0;
        title.focus();
      } else {
        step = "complete";
        details.hidden = details.disabled = true;
        advance.hidden = true;
        title.textContent = "Inquiry received";
        progress.hidden = true;
        status.textContent = "Your inquiry was received. Reference: " + result.data.reference + ".";
        close.disabled = false;
        close.focus();
        document.dispatchEvent(new CustomEvent("cups1:measurement", {
          detail: { event: "cups1_inquiry_complete", lead_type: form.elements.reason.value, form_type: "popup" },
        }));
      }
    } catch {
      status.textContent = "Could not confirm the save. Please try again.";
    } finally {
      busy = close.disabled = advance.disabled = false;
    }
  });
})();
