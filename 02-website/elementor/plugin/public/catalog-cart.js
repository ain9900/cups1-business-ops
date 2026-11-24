/* global cups1CatalogCart, jQuery */
(() => {
  function init() {
    const cartButtons = document.querySelectorAll('[data-catalog-cart-item]');
    const navLinks = document.querySelectorAll('.cups1-nav-tools a[aria-label="Cart"]');
    if ((!cartButtons.length && !navLinks.length) || typeof HTMLDialogElement === 'undefined') return;

    const dialog = document.createElement('dialog');
    dialog.className = 'cups1-catalog-cart';
    dialog.id = 'cups1-cart-drawer';
    dialog.setAttribute('aria-labelledby', 'cups1-cart-heading');
    dialog.innerHTML = `
      <header class="drawer-heading">
        <div><h2 id="cups1-cart-heading">Your cart</h2><p data-cart-count></p></div>
        <form method="dialog"><button class="drawer-close" aria-label="Close cart" autofocus>×</button></form>
      </header>
      <p role="status"></p>
      <ul class="drawer-items"></ul>
      <footer class="drawer-summary">
        <p data-total hidden><span>Subtotal</span><strong></strong></p>
        <a class="button primary" data-full-cart hidden>Review cart &amp; checkout</a>
        <form method="dialog"><button class="button outline">Continue shopping</button></form>
      </footer>`;
    document.body.append(dialog);
    function isOutside(event) {
      const bounds = dialog.getBoundingClientRect();
      return event.target === dialog && (event.clientX < bounds.left || event.clientX >= bounds.right ||
        event.clientY < bounds.top || event.clientY >= bounds.bottom);
    }
    let pressedOutside = false;
    dialog.addEventListener('pointerdown', (event) => { pressedOutside = isOutside(event); });
    dialog.addEventListener('click', (event) => {
      if (pressedOutside && isOutside(event)) dialog.close();
      pressedOutside = false;
    });
    const status = dialog.querySelector('[role=status]');
    const list = dialog.querySelector('ul');
    const total = dialog.querySelector('[data-total]');
    const fullCart = dialog.querySelector('[data-full-cart]');
    const count = dialog.querySelector('[data-cart-count]');
    fullCart.href = cups1CatalogCart.cartUrl;
    const open = document.createElement('button');
    open.type = 'button';
    open.className = 'button outline cups1-cart-open';
    open.textContent = 'View cart';
    const detailActions = document.querySelector('[data-product-detail] .product-details .actions:has([data-catalog-cart-item])');
    const grid = document.querySelector('.catalog-grid:has([data-catalog-cart-item])');
    if (!detailActions && !navLinks.length) grid?.before(open);

    const endpoint = cups1CatalogCart.endpoint;
    let nonce;
    async function request(action = '', body) {
      if (body && !nonce) await request();
      const response = await fetch(endpoint + action, {
        credentials: 'same-origin', cache: 'no-store', method: body ? 'POST' : 'GET',
        headers: body ? { 'Content-Type': 'application/json', Nonce: nonce || '' } : {},
        body: body ? JSON.stringify(body) : undefined
      });
      nonce = response.headers.get('Nonce') || nonce;
      const cart = await response.json();
      if (!response.ok) throw new Error(cart.message || 'WooCommerce could not update your cart.');
      return cart;
    }

    function money(amount, data) {
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: data.currency_code })
        .format(Number(amount) / 10 ** data.currency_minor_unit);
    }

    function updateBadges(quantity) {
      navLinks.forEach((link) => {
        const badge = link.querySelector('.cups1-cart-count');
        badge.textContent = quantity;
        badge.hidden = !quantity;
        link.setAttribute('aria-description', quantity + (quantity === 1 ? ' case in cart' : ' cases in cart'));
      });
    }

    function render(cart) {
      updateBadges(cart.items_count);
      open.textContent = 'View cart (' + cart.items_count + ')';
      count.textContent = cart.items_count ? cart.items_count + (cart.items_count === 1 ? ' case' : ' cases') : 'Your cart is empty.';
      list.replaceChildren();
      fullCart.hidden = false;
      fullCart.textContent = cart.items_count ? 'Review cart & checkout' : 'View full cart';
      cart.items.forEach((item) => {
        const row = document.createElement('li');
        const photo = item.images?.[0];
        if (photo) {
          const image = document.createElement('img');
          image.src = photo.thumbnail || photo.src;
          image.alt = '';
          row.append(image);
        }
        const details = document.createElement('div');
        const name = document.createElement('a');
        name.href = item.permalink;
        name.className = 'drawer-product';
        name.textContent = item.name;
        details.append(name);
        const options = item.variation.map(({ attribute, value }) => {
          if (/units\s+per\s+case/i.test(attribute) && /^\d+$/.test(value)) {
            return Number(value).toLocaleString() + ' units per case';
          }
          return attribute + ': ' + value;
        });
        if (options.length) {
          const specs = document.createElement('p');
          specs.textContent = options.join(' · ');
          details.append(specs);
        }
        const pricing = document.createElement('p');
        pricing.textContent = item.quantity + (item.quantity === 1 ? ' case × ' : ' cases × ') + money(item.prices.price, item.prices);
        const lineTotal = document.createElement('strong');
        lineTotal.textContent = money(item.totals.line_total, item.totals);
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'drawer-remove';
        remove.textContent = '×';
        remove.title = 'Remove item';
        remove.setAttribute('aria-label', 'Remove ' + item.name + (options.length ? ' ' + options.join(', ') : ''));
        remove.addEventListener('click', () => showCart('/remove-item', { key: item.key }));
        const line = document.createElement('div');
        line.className = 'drawer-line';
        const quantity = document.createElement('div');
        quantity.className = 'drawer-quantity';
        const quantityLabel = document.createElement('span');
        quantityLabel.textContent = item.quantity;
        const limits = item.quantity_limits;
        const step = limits?.multiple_of || 1;
        for (const direction of [-1, 1]) {
          const next = item.quantity + direction * step;
          const button = document.createElement('button');
          const label = direction < 0 ? 'Decrease' : 'Increase';
          button.type = 'button';
          button.textContent = direction < 0 ? '−' : '+';
          button.dataset.quantityAction = label;
          button.setAttribute('aria-label', label + ' quantity of ' + item.name + (options.length ? ', ' + options.join(', ') : ''));
          button.disabled = limits?.editable === false || next < (limits?.minimum ?? 1) || next > (limits?.maximum ?? Infinity);
          button.addEventListener('click', () => showCart('/update-item', { key: item.key, quantity: next }));
          quantity.append(button);
          if (direction < 0) quantity.append(quantityLabel);
        }
        line.append(lineTotal, quantity);
        details.append(pricing, line);
        row.dataset.itemKey = item.key;
        row.append(details, remove);
        list.append(row);
      });
      const t = cart.totals;
      total.hidden = !cart.items.length;
      total.querySelector('strong').textContent = money(t.total_items, t);
    }

    let busy = false;
    let cartRevision = 0;
    async function showCart(action = '', body, trigger) {
      if (busy) {
        if (!dialog.open) dialog.showModal();
        return;
      }
      busy = true;
      cartRevision++;
      if (trigger) trigger.disabled = true;
      if (!dialog.open) dialog.showModal();
      status.textContent = action === '/update-item' ? '' : 'Updating cart…';
      const activeControl = document.activeElement;
      list.inert = true;
      try {
        const cart = await request(action, body);
        render(cart);
        if (action && document.querySelector('.wp-block-woocommerce-cart, .wp-block-woocommerce-checkout')) {
          window.wp?.data?.dispatch('wc/store/cart')?.invalidateResolutionForStoreSelector?.('getCartData');
        }
        status.textContent = action === '/add-item' ? 'Added to your cart.' : '';
        if (action === '/add-item') {
          const item = cart.items.find((entry) => Number(entry.id) === body.id);
          if (item) {
            const { price, currency_code: currency, currency_minor_unit: minorUnit } = item.prices;
            const unitPrice = Number(price) / 10 ** minorUnit;
            document.dispatchEvent(new CustomEvent('cups1:measurement', {
              detail: {
                event: 'cups1_cart_add',
                currency,
                value: (Number(price) * body.quantity) / 10 ** minorUnit,
                items: [{ item_id: String(item.id), item_name: item.name, price: unitPrice, quantity: body.quantity }],
              },
            }));
          }
        }
      } catch (error) {
        status.textContent = error.message || 'Cart is unavailable. Please try again.';
      } finally {
        busy = false;
        list.inert = false;
        if (dialog.open && activeControl?.dataset.quantityAction && !activeControl.isConnected) {
          const row = [...list.children].find((item) => item.dataset.itemKey === body?.key);
          const control = row?.querySelector('[data-quantity-action="' + activeControl.dataset.quantityAction + '"]:enabled');
          (control || row?.querySelector('.drawer-remove'))?.focus();
        }
        if (trigger) trigger.disabled = !trigger.dataset.cartId;
      }
    }
    open.addEventListener('click', () => showCart());
    navLinks.forEach((link) => {
      const badge = document.createElement('span');
      badge.className = 'cups1-cart-count';
      badge.hidden = true;
      badge.setAttribute('aria-hidden', 'true');
      link.append(badge);
      link.setAttribute('aria-haspopup', 'dialog');
      link.setAttribute('aria-controls', dialog.id);
      link.addEventListener('click', (event) => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        showCart();
      });
    });

    if (navLinks.length) {
      request().then((cart) => {
        if (!cartRevision) updateBadges(cart.items_count);
      }).catch(() => {});
      if (document.querySelector('.wp-block-woocommerce-cart, .wp-block-woocommerce-checkout') && window.wp?.data) {
        let lastQuantity;
        window.wp.data.subscribe(() => {
          const cart = window.wp.data.select('wc/store/cart')?.getCartData?.();
          const quantity = cart?.itemsCount;
          if (typeof quantity !== 'number' || quantity === lastQuantity) return;
          lastQuantity = quantity;
          cartRevision++;
          updateBadges(quantity);
        }, 'wc/store/cart');
      }
    }

    cartButtons.forEach((button) => {
      if (button.hasAttribute('data-catalog-unavailable')) return;
      const product = button.closest('.catalog-product-card, [data-product-detail]');
      const form = product.querySelector('.variations_form');
      if (form) {
        if (!window.jQuery) return;
        function setVariation(variation, purchasable) {
          button.dataset.cartId = purchasable ? variation.variation_id : '';
          button.disabled = !button.dataset.cartId;
        }
        jQuery(form).on('show_variation', (_event, variation, purchasable) => setVariation(variation, purchasable));
        jQuery(form).on('hide_variation reset_data', () => setVariation(null, false));
        form.addEventListener('change', (event) => {
          if (event.target.matches('.variations select')) setVariation(null, false);
        }, true);
      } else {
        button.dataset.cartId = button.dataset.catalogCartItem;
      }
      button.addEventListener('click', () => {
        const id = Number(button.dataset.cartId);
        if (!id) return;
        const variation = form ? [...form.querySelectorAll('.variations select')].map((select) => ({
          attribute: select.name,
          value: select.value
        })) : [];
        showCart('/add-item', { id, quantity: 1, variation }, button);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();

(() => {
  function initAvailabilityLabels() {
    const $ = window.jQuery;
    if (!$) return;
    document.querySelectorAll('.catalog-product-card .variations_form, [data-product-detail] .variations_form:has(tr[hidden])').forEach((form) => {
      if (form.dataset.cups1AvailabilityLabels) return;
      form.dataset.cups1AvailabilityLabels = 'true';
      const selects = [...form.querySelectorAll('.variations select')];
      const initialOptions = new Map(selects.map((select) => [select, [...select.options].map((option) => option.cloneNode(true))]));
      function refresh() {
        const variations = $(form).data('product_variations');
        if (!Array.isArray(variations)) return;
        const hasAutomaticCase = selects.some((select) => select.closest('tr')?.hidden);
        selects.filter((select) => !select.closest('tr')?.hidden).forEach((select) => {
          const reference = $(select).data('attribute_options') || initialOptions.get(select);
          const current = new Map([...select.options].map((option) => [option.value, option]));
          const matchesOtherChoices = (variation) => selects.every((other) => {
            const value = variation.attributes[other.name];
            return other === select || other.closest('tr')?.hidden || !other.value || !value || other.value === value;
          });
          let next = null;
          [...reference].reverse().forEach((original) => {
            const value = original.value;
            if (!value) return;
            const matches = variations.filter((variation) => matchesOtherChoices(variation) &&
              (!variation.attributes[select.name] || variation.attributes[select.name] === value));
            const outOfStock = matches.length > 0 && matches.every((variation) => !variation.is_in_stock);
            let option = current.get(value);
            if (!option) {
              option = new Option(original.textContent, value);
              option.disabled = true;
              select.insertBefore(option, next);
            }
            if (hasAutomaticCase) option.disabled = !matches.some((variation) => variation.is_in_stock && variation.variation_is_active);
            else if (outOfStock) option.disabled = true;
            const label = original.textContent.trim();
            option.textContent = label + (outOfStock ? ' (Out of stock)' : option.disabled ? ' (Unavailable)' : '');
            next = option;
          });
        });
      }
      $(form).on('woocommerce_update_variation_values.cups1Availability', refresh);
      refresh();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAvailabilityLabels, { once: true });
  else initAvailabilityLabels();
})();
