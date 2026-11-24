(function (w) {
  if (w.cups1CatalogMeasurement) return;

  var requests = new Map();
  var departments = new Set(['cups', 'lids', 'containers', 'ware']);

  function getProduct(id) {
    id = String(id || '');
    if (!/^\d+$/.test(id)) return Promise.resolve(null);
    if (!requests.has(id)) {
      var controller = new AbortController();
      var timer = w.setTimeout(function () { controller.abort(); }, 2500);
      var request = w.fetch('/wp-json/wc/store/v1/products/' + id, {
        credentials: 'same-origin',
        signal: controller.signal
      }).then(function (response) {
        return response.ok ? response.json() : null;
      }).then(function (product) {
        return product && String(product.id) === id ? product : null;
      }).catch(function () {
        return null;
      }).finally(function () {
        w.clearTimeout(timer);
      });
      requests.set(id, request);
    }
    return requests.get(id);
  }

  function detail(id, knownParent) {
    return Promise.all([
      getProduct(id),
      String(knownParent) === String(id) ? Promise.resolve(null) : getProduct(knownParent)
    ]).then(function (resolved) {
      var product = resolved[0];
      var parent = resolved[1];
      return parent || !product || !product.parent ? resolved : getProduct(product.parent).then(function (fallback) {
        return [product, fallback];
      });
    }).then(function (resolved) {
      var product = resolved[0];
      var parent = resolved[1];
      if (!product && !parent) return {};

      var categoryProduct = parent || product;
      var terms = categoryProduct.categories || [];
      var primary = terms.find(function (term) { return departments.has(term.slug); }) || terms[0];
      var secondary = terms.find(function (term) { return term !== primary; });
      var fields = {};
      if (primary) fields.item_category = primary.name;
      if (secondary) fields.item_category2 = secondary.name;
      if (product && product.sku) fields.item_sku = product.sku;
      if (product && product.variation) fields.item_variant = product.variation;

      var result = { fields: fields };
      if (!product) return result;

      var priceData = product.prices || {};
      var minor = priceData.currency_minor_unit;
      var amount = /^\d+$/.test(String(priceData.price)) && Number.isInteger(minor) && minor >= 0 && minor <= 6
        ? Number(priceData.price) / Math.pow(10, minor) : NaN;
      if (!Number.isFinite(amount) || !/^[A-Z]{3}$/.test(priceData.currency_code || '') || !product.price_html) {
        result.pricing_mode = !product.price_html ? 'quote_only' : 'unknown';
      } else if (product.type === 'variable' || product.type === 'grouped') {
        result.pricing_mode = 'variant_required';
      } else {
        result.pricing_mode = product.is_purchasable && product.is_in_stock ? 'priced' : 'unavailable';
        result.price = amount;
        result.currency = priceData.currency_code;
        result.price_band = amount < 100 ? 'under_100' : amount < 250 ? '100_to_249' : amount < 500 ? '250_to_499' : '500_plus';
      }
      return result;
    });
  }

  function decorate(items) {
    return Promise.all(items.map(function (item, index) {
      if (index >= 15) return Promise.resolve(item);
      return detail(item.item_id).then(function (metadata) {
        return Object.assign({}, item, metadata.fields || {});
      });
    }));
  }

  w.cups1CatalogMeasurement = { detail: detail, decorate: decorate };
})(window);
