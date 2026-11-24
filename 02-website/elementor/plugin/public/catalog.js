/* global jQuery */
document.querySelectorAll(".cups1-variation-purchase").forEach((purchase) => {
  const form = purchase.querySelector(".variations_form");
  if (!form) return;

  const price = purchase.querySelector("[data-catalog-price]");
  const caseLabel = purchase.querySelector("[data-catalog-case]");
  const stock = purchase.querySelector("[data-catalog-stock]");
  const initialPrice = price.innerHTML;
  const initialCase = caseLabel.textContent;
  const card = purchase.closest(".catalog-product-card");
  const product = purchase.closest("[data-product-detail]");
  const links = card?.querySelectorAll("[data-catalog-product-link]") ?? [];
  const inquiryLinks = (card || purchase.closest("[data-product-detail]"))?.querySelectorAll("[data-catalog-quote-link]") ?? [];
  const image = card?.querySelector("[data-catalog-product-link] img") ?? product?.querySelector("#gallery-image");
  const caption = product?.querySelector("#gallery-caption");
  const attributes = ["src", "srcset", "sizes", "alt"];
  let previousImage;
  let previousCaption;
  let previousThumbnail;

  function updateImage(variationImage) {
    if (!image) return;
    if (variationImage?.src) {
      if (!previousImage) {
        previousImage = attributes.map((name) => image.getAttribute(name));
        previousCaption = caption?.textContent;
        previousThumbnail = product?.querySelector('.gallery-controls [aria-pressed="true"]');
      }
      attributes.forEach((name) => {
        if (variationImage[name] || name === "alt") image.setAttribute(name, variationImage[name] ?? "");
        else image.removeAttribute(name);
      });
      product?.querySelector('.gallery-controls [aria-pressed="true"]')?.setAttribute("aria-pressed", "false");
      if (caption) caption.textContent = variationImage.title || "";
    } else if (previousImage) {
      attributes.forEach((name, index) => {
        const value = previousImage[index];
        if (value === null) image.removeAttribute(name);
        else image.setAttribute(name, value);
      });
      if (caption) caption.textContent = previousCaption;
      previousThumbnail?.setAttribute("aria-pressed", "true");
      previousImage = null;
    }
  }

  function updateSummary(variation, fallbackPrice = initialPrice) {
    price.innerHTML = variation?.cups1_price_html || fallbackPrice;
    caseLabel.textContent = variation?.cups1_case_label ?? initialCase;
    caseLabel.hidden = !caseLabel.textContent;
    stock.textContent = variation?.cups1_stock_label || "";
    if (variation?.availability_html) {
      const availability = new DOMParser().parseFromString(variation.availability_html, "text/html");
      stock.textContent = availability.body.textContent.trim();
    }
    stock.hidden = !stock.textContent;
    updateImage(variation?.image);
  }

  const options = [...form.querySelectorAll(".variations select")];

  // Keep legacy variation attributes available to WooCommerce and the cart.
  const caseOption = options.find(({ name }) => /^attribute_(?:pa_)?units-per-case$/.test(name));
  const choices = options.filter((option) => option !== caseOption);
  const variations = jQuery(form).data("product_variations");
  if (caseOption && choices.length && Array.isArray(variations) && variations.length &&
      !variations.some((variation, index) => variations.slice(0, index).some((other) =>
        choices.every(({ name }) => {
          const a = variation.attributes[name];
          const b = other.attributes[name];
          return !a || !b || a === b;
        })
      ))) {
    const caseRow = caseOption.closest("tr");
    caseRow.hidden = true;
    caseRow.style.display = "none";
    const caseChoices = [...caseOption.options].map((option) => option.cloneNode(true));
    function selectCaseCount() {
      caseOption.replaceChildren(...caseChoices.map((option) => option.cloneNode(true)));
      const match = variations.find(({ attributes }) => choices.every(({ name, value }) =>
        value && (!attributes[name] || attributes[name] === value)
      ));
      caseOption.value = match?.attributes[caseOption.name] || "";
      // WooCommerce requires every select to have a value, including wildcard attributes.
      if (match && !caseOption.value) {
        caseOption.value = [...caseOption.options].find((option) => option.value)?.value || "";
      }
    }
    selectCaseCount();
    form.addEventListener("change", selectCaseCount, true);
  }

  function updateProductLinks() {
    inquiryLinks.forEach((link) => {
      const destination = new URL(link.href);
      const size = form.querySelector('select[name="attribute_size"], select[name="attribute_pa_size"]');
      if (size?.value) destination.searchParams.set("packaging_size", size.value);
      else destination.searchParams.delete("packaging_size");
      link.href = destination.href;
    });
    links.forEach((link) => {
      const destination = new URL(link.href);
      options.filter((option) => !option.closest("tr")?.hidden).forEach(({ name, value }) => {
        if (value) destination.searchParams.set(name, value);
        else destination.searchParams.delete(name);
      });
      link.href = destination.href;
    });
  }

  product?.querySelector(".gallery-controls")?.addEventListener("click", (event) => {
    if (event.target.closest("button[data-image]")) previousImage = null;
  });
  form.addEventListener("change", (event) => {
    if (event.target.matches(".variations select")) {
      updateSummary(undefined, options.every((option) => option.value) ? "" : initialPrice);
      updateProductLinks();
    }
  }, true);
  jQuery(form).on("found_variation", (_event, variation) => updateSummary(variation));
  jQuery(form).on("reset_data", () => updateSummary());
  jQuery(form).on("woocommerce_variation_has_changed", updateProductLinks);
  updateProductLinks();
});
