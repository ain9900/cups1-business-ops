// Publish local events for consent-aware tags configured separately in Tag Manager.
document.addEventListener("cups1:measurement", ({ detail }) => {
  window.dataLayer ??= [];
  if (Array.isArray(window.dataLayer)) window.dataLayer.push(detail);
});

const menu = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".main-nav");

const productCollections = document.querySelector(".catalog-collections");
if (productCollections && !location.hash && !new URLSearchParams(location.search).has("elementor-preview")
  && performance.getEntriesByType("navigation")[0]?.type === "navigate") {
  window.addEventListener("pageshow", (event) => {
    if (event.persisted || window.scrollY !== 0) return;
    const header = document.querySelector(".cups1-global-header");
    const initialAnchor = document.documentElement.style.overflowAnchor;
    document.documentElement.style.overflowAnchor = "none";
    let frame;
    let timeout;
    const input = new AbortController();
    function stopAligning() {
      cancelAnimationFrame(frame);
      clearTimeout(timeout);
      input.abort();
      document.documentElement.style.overflowAnchor = initialAnchor;
    }
    function alignCollections() {
      const headerOffset = header ? header.offsetHeight + (parseFloat(getComputedStyle(header).top) || 0) : 0;
      const target = window.scrollY + productCollections.getBoundingClientRect().top - headerOffset - 12;
      if (Math.abs(window.scrollY - target) > 1) window.scrollTo({ top: target, behavior: "instant" });
      frame = requestAnimationFrame(alignCollections);
    }
    for (const type of ["wheel", "touchstart", "pointerdown", "keydown", "pagehide"]) {
      window.addEventListener(type, stopAligning, { passive: true, signal: input.signal });
    }
    timeout = setTimeout(stopAligning, 1200);
    alignCollections();
  }, { once: true });
}

const printSurfaces = {
    "double-wall": { top: .34, bottom: .80 },
    "single-wall": { top: .24, bottom: .83 },
    "ripple-wall": { top: .31, bottom: .82 },
    dessert: { top: .38, bottom: .75 },
    bowls: { top: .43, bottom: .69 },
    boxes: { top: .36, bottom: .75 },
  };

function drawLogo(logo, model, artwork, position) {
  const ink = logo.getContext("2d");
  ink.clearRect(0, 0, logo.width, logo.height);
  logo.hidden = !artwork;
  if (!artwork) return;
  const surface = printSurfaces[model];
  const top = logo.height * surface.top + 24;
  const bottom = logo.height * surface.bottom - 24;
  const scale = Math.min(
    logo.width * .15 / Math.max(artwork.naturalWidth, artwork.naturalHeight),
    (bottom - top - 56) / artwork.naturalHeight
  );
  const width = artwork.naturalWidth * scale;
  const height = artwork.naturalHeight * scale;
  const left = (logo.width - width) / 2;
  const y = top + (bottom - top - height) * position;

  ink.drawImage(artwork, left, y, width, height);
}

function bindLogoInput(input, remove, status, render) {
  const state = { artwork: null };
  let pending;
  function clear() {
    pending = null;
    state.artwork = null;
    remove.hidden = true;
    render(null);
  }
  function load(file) {
    if (!file) return;
    pending = null;
    if (!["image/png", "image/jpeg", "image/webp"].includes(file.type) || file.size > 10 * 1024 * 1024) {
      input.value = "";
      status.textContent = "Choose a PNG, JPEG, or WebP file up to 10 MB.";
      return;
    }
    const candidate = new Image();
    const url = URL.createObjectURL(file);
    pending = candidate;
    status.textContent = "Loading your logo…";
    candidate.onload = () => {
      URL.revokeObjectURL(url);
      if (pending !== candidate) return;
      pending = null;
      state.artwork = candidate;
      remove.hidden = false;
      render(candidate);
      status.textContent = "Logo added to the preview.";
    };
    candidate.onerror = () => {
      URL.revokeObjectURL(url);
      if (pending !== candidate) return;
      pending = null;
      input.value = "";
      status.textContent = "This image couldn’t be opened. Try another file.";
    };
    candidate.src = url;
  }
  input.addEventListener("change", () => load(input.files[0]));
  remove.addEventListener("click", () => {
    clear();
    input.value = "";
    status.textContent = "Logo removed.";
    input.focus();
  });
  const drop = input.closest("[data-logo-drop]");
  if (drop) {
    drop.addEventListener("dragover", (event) => {
      if (!event.dataTransfer.types.includes("Files")) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = "copy";
      drop.classList.add("is-dragging");
    });
    drop.addEventListener("dragleave", (event) => {
      if (!drop.contains(event.relatedTarget)) drop.classList.remove("is-dragging");
    });
    drop.addEventListener("drop", (event) => {
      event.preventDefault();
      drop.classList.remove("is-dragging");
      input.value = "";
      load(event.dataTransfer.files[0]);
    });
  }
  return state;
}

document.querySelectorAll("[data-cups1-logo-preview]").forEach((widget) => {
  const fileInput = widget.querySelector("[data-logo-file]");
  const model = widget.querySelector("[data-logo-model]");
  const position = widget.querySelector("[data-print-position]");
  const remove = widget.querySelector("[data-logo-remove]");
  const status = widget.querySelector("[data-logo-status]");
  const logo = widget.querySelector("[data-logo-overlay]");
  const quote = widget.querySelector("[data-logo-quote]");
  const cups = widget.querySelectorAll("[data-preview-cup]");
  function renderPrint(artwork) {
    position.disabled = !artwork;
    drawLogo(logo, model.value, artwork, Number(position.value) / 100);
  }

  function updateModel() {
    cups.forEach((cup) => { cup.hidden = cup.dataset.previewCup !== model.value; });
    const destination = new URL(quote.href);
    destination.searchParams.set("packaging_product", model.value);
    quote.href = destination.href;
    renderPrint(upload.artwork);
  }

  const upload = bindLogoInput(fileInput, remove, status, renderPrint);
  position.addEventListener("input", () => renderPrint(upload.artwork));
  model.addEventListener("change", updateModel);
  const requestedModel = new URLSearchParams(location.search).get("model");
  if (Object.hasOwn(printSurfaces, requestedModel)) model.value = requestedModel;
  updateModel();
});

document.querySelectorAll(".hero-montage").forEach((montage) => {
  const images = Array.from(montage.children);
  const hero = montage.closest(".hero");
  if (!hero || images.length < 2) return;
  const track = document.createElement("div");
  const strip = document.createElement("div");
  track.className = "hero-montage-track";
  strip.className = "hero-montage-strip";
  strip.append(...images);
  const repeat = strip.cloneNode(true);
  repeat.querySelectorAll("[fetchpriority]").forEach((image) => image.removeAttribute("fetchpriority"));
  track.append(strip, repeat);
  montage.append(track);
  montage.classList.add("hero-montage-loop");

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "hero-motion-toggle";
  function updateToggle(paused) {
    hero.classList.toggle("hero-motion-paused", paused);
    toggle.setAttribute("aria-label", paused ? "Play hero images" : "Pause hero images");
    toggle.title = toggle.getAttribute("aria-label");
    toggle.innerHTML = `<svg viewBox="0 0 20 20" width="20" height="20" fill="currentColor" aria-hidden="true">${paused
      ? '<path d="M6 3.5v13l10-6.5z"/>'
      : '<path d="M5 4h3v12H5zm7 0h3v12h-3z"/>'}</svg>`;
  }
  updateToggle(false);
  toggle.addEventListener("click", () => updateToggle(!hero.classList.contains("hero-motion-paused")));
  hero.append(toggle);
});

if (menu && navigation) {
  const dropdowns = [...navigation.querySelectorAll(".dropdown")];
  const closeDropdowns = (except) => {
    dropdowns.forEach((dropdown) => {
      if (dropdown !== except) dropdown.open = false;
    });
  };
  function setMenu(open) {
    navigation.classList.toggle("open", open);
    menu.setAttribute("aria-expanded", String(open));
    if (!open) closeDropdowns();
  }

  menu.addEventListener("click", () => setMenu(menu.getAttribute("aria-expanded") === "false"));
  dropdowns.forEach((dropdown) => {
    const summary = dropdown.querySelector("summary");
    const panel = dropdown.querySelector(".dropdown-panel");
    const canHover = (event) => event.pointerType === "mouse" && matchMedia("(any-hover: hover)").matches
      && getComputedStyle(menu).display === "none";
    dropdown.addEventListener("pointerenter", (event) => {
      if (!canHover(event)) return;
      closeDropdowns(dropdown);
      dropdown.open = true;
    });
    dropdown.addEventListener("pointerleave", (event) => {
      if (canHover(event) && !panel.contains(document.activeElement)) dropdown.open = false;
    });
    summary.addEventListener("click", (event) => {
      if (canHover(event) && dropdown.open) event.preventDefault();
    });
    dropdown.addEventListener("focusout", (event) => {
      if (!dropdown.contains(event.relatedTarget) && !dropdown.matches(":hover")) dropdown.open = false;
    });
    dropdown.addEventListener("toggle", () => {
      if (dropdown.open) closeDropdowns(dropdown);
    });
  });
  navigation.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    setMenu(false);
  });
  document.addEventListener("pointerdown", (event) => {
    if (!navigation.contains(event.target) && !menu.contains(event.target)) closeDropdowns();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const dropdown = dropdowns.find((item) => item.open);
    if (dropdown) {
      dropdown.open = false;
      dropdown.querySelector("summary").focus();
    } else if (menu.getAttribute("aria-expanded") === "true") {
      setMenu(false);
      menu.focus();
    }
  });
}

document.querySelectorAll(".catalog-filters").forEach((filters) => {
  const catalog = filters.closest("section");
  const grid = catalog.querySelector(".catalog-grid");
  const cards = Array.from(grid.querySelectorAll(".product"), (element) => ({
    element,
    title: element.querySelector("h3").textContent.trim(),
    keywords: element.querySelector(".card-body").textContent.toLowerCase(),
  }));
  const search = filters.elements.namedItem("packaging");
  const category = filters.elements.namedItem("format");
  const sort = filters.elements.namedItem("sort");

  function render() {
    const words = search.value.trim().toLowerCase().split(/\s+/);
    const ordered = [...cards];
    if (sort.value) {
      const direction = sort.value === "za" ? -1 : 1;
      ordered.sort((first, second) => direction * first.title.localeCompare(second.title));
    }

    let count = 0;
    ordered.forEach(({ element, keywords }) => {
      const matches = (!category.value || (element.dataset.catalogCategory || "").split(" ").includes(category.value))
        && words.every((word) => keywords.includes(word));
      element.hidden = !matches;
      grid.append(element);
      count += Number(matches);
    });
    catalog.querySelector(".catalog-status").textContent = `${count} ${count === 1 ? "product" : "products"}`;
    catalog.querySelector(".catalog-empty").hidden = count !== 0;
  }

  function readURL() {
    const params = new URLSearchParams(location.search);
    search.value = params.get(search.name) || "";
    category.value = params.get(category.name) || "";
    sort.value = params.get(sort.name) || "";
    render();
  }

  filters.hidden = false;
  readURL();
  window.addEventListener("popstate", readURL);
  filters.addEventListener("submit", (event) => {
    event.preventDefault();
    const url = new URL(location.href);
    for (const [name, value] of new FormData(filters)) {
      if (value.trim()) url.searchParams.set(name, value.trim());
      else url.searchParams.delete(name);
    }
    if (url.href !== location.href) history.pushState(null, "", url);
    render();
  });
});

const galleryImage = document.querySelector("#gallery-image");
const gallery = document.querySelector(".gallery-controls");
if (galleryImage && gallery) {
  gallery.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;

    gallery.querySelector('[aria-pressed="true"]')?.setAttribute("aria-pressed", "false");
    button.setAttribute("aria-pressed", "true");
    galleryImage.removeAttribute("srcset");
    galleryImage.removeAttribute("sizes");
    galleryImage.src = button.dataset.image || button.querySelector("img").src;
    galleryImage.alt = button.dataset.alt;
    document.querySelector("#gallery-caption").textContent = button.dataset.image
      ? button.dataset.caption : `Concept rendering / ${button.dataset.caption}`;
  });
}

function enablePackagingWizard(form) {
  const stages = ["Specification", "Artwork", "Contact", "Review"];
  const panels = Array.from(form.querySelectorAll("[data-packaging-panel]"));
  const progress = form.querySelector("[data-packaging-step]");
  const review = form.querySelector("[data-packaging-review]");
  const back = form.querySelector("[data-packaging-back]");
  const next = form.querySelector("[data-packaging-next]");
  const submit = form.querySelector('button[type="submit"]');
  let current = 0;

  function render() {
    const name = stages[current];
    progress.textContent = `Step ${current + 1} of ${stages.length} · ${name}`;
    panels.forEach((panel) => { panel.hidden = panel.dataset.packagingPanel !== name.toLowerCase(); });
    const reviewing = name === "Review";
    review.hidden = !reviewing;
    submit.hidden = !reviewing;
    next.hidden = reviewing;
    back.hidden = current === 0;
    if (!reviewing) return;
    const summary = review.querySelector("dl");
    summary.replaceChildren();
    const fields = {
      product: "Packaging", dimensions: "Size", print_preference: "Printing",
      quantity: "Quantity", artwork: "Artwork", country: "Delivery country", postal_code: "Postal code",
    };
    for (const [key, label] of Object.entries(fields)) {
      const field = form.elements.namedItem(key);
      if (!field) continue;
      const value = field.type === "file" ? field.files[0]?.name || "Send later"
        : field.value && (field.selectedOptions?.[0]?.textContent || field.value);
      if (!value) continue;
      const term = document.createElement("dt");
      const detail = document.createElement("dd");
      term.textContent = label;
      detail.textContent = value;
      summary.append(term, detail);
    }
  }

  function move(offset) {
    if (offset > 0 && panels.filter((panel) => !panel.hidden).some(
      (panel) => !panel.querySelector("input, select, textarea").reportValidity()
    )) return;
    current += offset;
    render();
    const first = panels.find((panel) => !panel.hidden);
    (first?.querySelector("input, select, textarea") || submit).focus();
  }

  form.querySelector("[data-packaging-steps]").hidden = false;
  form.querySelector("[data-packaging-controls]").hidden = false;
  back.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  form.addEventListener("submit", (event) => {
    if (current === stages.length - 1) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    move(1);
  });
  form.addEventListener("reset", () => {
    current = 0;
    requestAnimationFrame(render);
  });
  render();
}

document.querySelectorAll("[data-catalog-quote-size]").forEach((picker) => {
  const container = picker.closest(".catalog-product-card, [data-product-detail]");
  const links = container.querySelectorAll("[data-catalog-quote-link], [data-catalog-product-link]");
  const size = new URLSearchParams(location.search).get("packaging_size");
  if (container.hasAttribute("data-product-detail") && Array.from(picker.options).some((option) => option.value === size)) {
    picker.value = size;
  }
  function updateQuoteLink() {
    links.forEach((link) => {
      const destination = new URL(link.href);
      if (picker.value) destination.searchParams.set("packaging_size", picker.value);
      else destination.searchParams.delete("packaging_size");
      link.href = destination.href;
    });
  }
  picker.addEventListener("change", updateQuoteLink);
  updateQuoteLink();
});

document.querySelectorAll("#inquiry-form, [data-cups1-newsletter]").forEach((form) => {
  const product = form.elements.namedItem("product");
  const query = new URLSearchParams(location.search);
  const selected = query.get("packaging_product") || query.get("product");
  if (product && Array.from(product.options).some((option) => option.value === selected)) {
    product.value = selected;
    const dimensions = form.elements.namedItem("dimensions");
    const size = query.get("packaging_size");
    if (dimensions && size && !dimensions.value) dimensions.value = size.slice(0, 120);
  }

  const artwork = form.elements.namedItem("artwork");
  artwork?.addEventListener("change", () => {
    const file = artwork.files[0];
    const valid = !file || (/\.(pdf|png|jpe?g)$/i.test(file.name) && file.size <= 5 * 1024 * 1024);
    artwork.setCustomValidity(valid ? "" : "Choose a PDF, PNG, or JPEG file of 5 MB or less.");
    if (!valid) artwork.reportValidity();
  });

  if (form.hasAttribute("data-packaging-wizard")) enablePackagingWizard(form);

  const submitButton = form.querySelector('button[type="submit"]');
  const status = form.querySelector(".form-status");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submitButton.disabled) return;
    submitButton.disabled = true;
    status.textContent = "Submitting…";
    let message;
    let success = false;
    try {
      const action = form.getAttribute("action");
      const tokenURL = new URL("admin-ajax.php", action);
      tokenURL.searchParams.set("action", "cups1_form_token");
      const tokenResponse = await fetch(tokenURL, { cache: "no-store", credentials: "same-origin" });
      if (tokenResponse.ok) {
        const token = await tokenResponse.json();
        if (token.success && token.data.nonce) form.elements.namedItem("cups1_nonce").value = token.data.nonce;
      }
      const body = new FormData(form);
      const response = await fetch(action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body,
        credentials: "same-origin",
      });
      const result = await response.json();
      success = response.ok && result.success === true;
      message = result.data?.message;
      if (success) {
        form.reset();
        const intent = body.get("intent");
        if (["quote", "sample", "contact"].includes(intent)) {
          const leadType = form.hasAttribute("data-packaging-wizard") ? "customize" : intent;
          document.dispatchEvent(new CustomEvent("cups1:measurement", {
            detail: { event: "cups1_inquiry_complete", lead_type: leadType, form_type: "standalone" },
          }));
        }
      }
    } catch {
      message = "We couldn’t confirm receipt. Your details are still here so you can try again.";
    }
    const result = document.createElement("span");
    result.dataset.status = success ? "success" : "error";
    result.textContent = message || "The inquiry could not be sent. Please try again.";
    status.replaceChildren(result);
    submitButton.disabled = false;
  });
});

document.querySelectorAll("[data-cups1-comparison]").forEach((comparison) => {
  const slider = comparison.querySelector('input[type="range"]');
  const model = comparison.querySelector("[data-comparison-model]");
  const views = comparison.querySelectorAll("[data-comparison-view]");
  const update = () => {
    comparison.style.setProperty("--comparison-position", slider.value + "%");
    views.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.comparisonView === slider.value)));
  };
  const canvas = comparison.querySelector("[data-comparison-artwork]");
  const sample = comparison.querySelector(".reference-comparison-overlay img");
  function renderArtwork(artwork) {
    drawLogo(canvas, model.value, artwork, .5);
    sample.hidden = !!artwork;
  }
  const upload = bindLogoInput(
    comparison.querySelector("[data-comparison-file]"),
    comparison.querySelector("[data-comparison-remove]"),
    comparison.querySelector("[data-comparison-status]"),
    (artwork) => {
      renderArtwork(artwork);
      if (artwork) {
        slider.value = slider.max;
        update();
      }
    }
  );
  comparison.querySelector("[data-comparison-upload]").hidden = false;
  function updateModel() {
    comparison.querySelectorAll("[data-comparison-cup]").forEach((cup) => {
      cup.hidden = cup.dataset.comparisonCup !== model.value;
    });
    renderArtwork(upload.artwork);
  }
  views.forEach((button) => button.addEventListener("click", () => {
    slider.value = button.dataset.comparisonView;
    update();
  }));
  model?.addEventListener("change", () => {
    updateModel();
    slider.value = upload.artwork ? slider.max : slider.min;
    update();
  });
  if (model) {
    updateModel();
    model.closest(".comparison-controls").hidden = false;
  }
  slider.addEventListener("input", update);
  update();
});

document.querySelectorAll("[data-cups1-carousel]").forEach((section) => {
  const track = section.querySelector(".reference-carousel");
  const previous = section.querySelector("[data-carousel-prev]");
  const next = section.querySelector("[data-carousel-next]");
  const update = () => {
    previous.disabled = track.scrollLeft <= 1;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
  };
  function move(direction) {
    const distance = track.children[1].offsetLeft - track.children[0].offsetLeft;
    track.scrollBy({ left: direction * distance, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
  previous.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  track.addEventListener("scroll", update, { passive: true });
  new ResizeObserver(update).observe(track);
  previous.parentElement.hidden = false;
  update();
});

if (typeof cups1Navigation !== "undefined") {
  const nav = document.querySelector("#main-nav");
  if (nav) {
    const actions = document.createElement("div");
    actions.className = "cups1-nav-tools";
    actions.innerHTML = '<button type="button" aria-expanded="false" aria-controls="cups1-header-search" aria-label="Search" title="Search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg></button>';
    if (cups1Navigation.cart) {
      const cart = document.createElement("a");
      cart.href = cups1Navigation.cart;
      cart.setAttribute("aria-label", "Cart");
      cart.title = "Cart";
      cart.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 4h2l2.5 11h11l2-8H6"/><circle cx="9" cy="19" r="1"/><circle cx="18" cy="19" r="1"/></svg>';
      actions.append(cart);
    }
    const compactHeader = window.matchMedia("(max-width: 1200px)");
    const mobileActions = document.createElement("div");
    mobileActions.className = "cups1-mobile-header-actions";
    if (menu) menu.before(mobileActions);

    function placeHeaderActions() {
      if (menu && compactHeader.matches) {
        mobileActions.append(actions, menu);
      } else {
        if (menu && menu.parentElement === mobileActions) mobileActions.after(menu);
        nav.append(actions);
      }
    }
    placeHeaderActions();
    compactHeader.addEventListener("change", placeHeaderActions);

    const search = document.createElement("form");
    search.id = "cups1-header-search";
    search.className = "shell cups1-header-search";
    search.setAttribute("role", "search");
    search.hidden = true;
    search.action = cups1Navigation.shop;
    search.innerHTML = '<input aria-label="Search products" type="search" name="packaging" placeholder="Search products…" required><button class="button primary" type="submit">Search</button>';
    nav.closest(".header-inner").after(search);
    const searchToggle = actions.querySelector("button");
    function setSearch(expanded) {
      search.hidden = !expanded;
      searchToggle.setAttribute("aria-expanded", String(expanded));
      if (expanded) search.querySelector("input").focus();
    }
    searchToggle.addEventListener("click", () => {
      if (search.hidden && menu?.getAttribute("aria-expanded") === "true") menu.click();
      setSearch(search.hidden);
    });
    menu?.addEventListener("click", () => setSearch(false));
    search.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      event.preventDefault();
      setSearch(false);
      searchToggle.focus();
    });
  }
}
