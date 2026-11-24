(function (w, d) {
  if (w.cups1EngagementMeasurement) return;
  var path = w.location.pathname.replace(/\/$/, '') || '/';
  var pageTypes = {
    '/': 'home', '/products': 'catalog', '/for-business': 'business', '/industries': 'business',
    '/request-a-quote': 'quote', '/contact-sales': 'contact_sales', '/request-a-sample': 'sample',
    '/configure-packaging': 'customize', '/contact': 'contact', '/custom-printing': 'customize',
    '/how-it-works': 'resource', '/documents': 'resource', '/faq': 'resource', '/resources': 'resource',
    '/help-center': 'resource', '/about': 'about', '/for-distributors': 'business'
  };
  var pageType = pageTypes[path];
  if (/^\/product\/[a-z0-9-]+$/.test(path)) pageType = 'product';
  if (/^\/(for-business|industries)\/[a-z0-9-]+$/.test(path)) pageType = 'business';
  if (!pageType) return;
  w.cups1EngagementMeasurement = true;

  var thresholds = [25, 50, 75, 90];
  var seenDepths = new Set();
  var startedForms = new WeakSet();
  var pendingScroll = false;
  var callsToAction = {
    '/request-a-quote': 'request_quote', '/contact-sales': 'contact_sales',
    '/request-a-sample': 'request_sample', '/contact': 'contact',
    '/configure-packaging': 'customize', '/custom-printing': 'learn_custom_printing',
    '/products': 'browse_catalog', '/for-business': 'explore_business', '/documents': 'view_documents',
    '/cart': 'open_cart', '/checkout': 'open_checkout'
  };

  function hasStatisticsConsent() {
    var layer = w.dataLayer || [];
    for (var i = layer.length - 1; i >= 0; i--) {
      var entry = layer[i];
      if (entry && entry.event === 'wpconsent_consent_processed') {
        return !!(entry.wpconsentPreferences && entry.wpconsentPreferences.statistics === true);
      }
    }
    return false;
  }

  function emit(event, action, depth, formType) {
    w.dataLayer.push({
      event: event,
      engagement_action: action || null,
      engagement_depth: depth || null,
      engagement_form_type: formType || null,
      engagement_page_type: pageType,
      engagement_page_location: w.location.origin + w.location.pathname,
      engagement_page_referrer: d.referrer ? new URL(d.referrer).origin : ''
    });
  }

  d.addEventListener('click', function (event) {
    if (!event.isTrusted || !hasStatisticsConsent() || !event.target.closest) return;
    var control = event.target.closest('a[href], button, [role="button"]');
    if (!control || control.matches(':disabled, [aria-disabled="true"]')) return;

    var action;
    if (control.matches('[data-catalog-cart-item]')) {
      action = 'add_to_cart_cta';
    } else if (control.matches('a[href]')) {
      var destination = new URL(control.href);
      if (destination.protocol === 'mailto:') action = 'email_link';
      if (destination.protocol === 'tel:') action = 'phone_link';
      if (destination.origin === w.location.origin) {
        var destinationPath = destination.pathname.replace(/\/$/, '');
        action = callsToAction[destinationPath];
        if (/^\/product\/[a-z0-9-]+$/.test(destinationPath)) action = 'open_product';
        if (/^\/(for-business|industries)\/[a-z0-9-]+$/.test(destinationPath)) action = 'explore_business';
      }
    }
    if (action) emit('cta_click', action);
  }, true);

  function recordFormStart(event) {
    if (!event.isTrusted || !hasStatisticsConsent()) return;
    var field = event.target;
    if (!field.matches || !field.matches('input:not([type="hidden"]):not([type="submit"]), select, textarea')) return;
    var form = field.form;
    if (!form || startedForms.has(form)) return;
    var formType = form.closest('[data-inquiry-popup]') ? 'popup' : form.matches('form.inquiry-form') ? 'standalone' : '';
    if (!formType) return;
    startedForms.add(form);
    emit('inquiry_start', null, null, formType);
  }
  d.addEventListener('input', recordFormStart, true);
  d.addEventListener('change', recordFormStart, true);

  w.addEventListener('scroll', function () {
    if (pendingScroll || seenDepths.size === thresholds.length) return;
    pendingScroll = true;
    w.requestAnimationFrame(function () {
      pendingScroll = false;
      if (!hasStatisticsConsent()) return;
      var height = d.documentElement.scrollHeight;
      if (height - w.innerHeight < 300 || w.scrollY < 100) return;
      var depth = Math.floor((w.scrollY + w.innerHeight) / height * 100);
      thresholds.forEach(function (threshold) {
        if (depth < threshold || seenDepths.has(threshold)) return;
        seenDepths.add(threshold);
        emit('scroll_depth', null, threshold);
        if (threshold === 75 && ['product', 'catalog', 'business', 'customize'].includes(pageType)) {
          emit('content_engaged', null, threshold);
        }
      });
    });
  }, { passive: true });
})(window, document);
