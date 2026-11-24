"""Editable homepage sections based on the supplied layout references."""

SECTIONS = {
    "home-compare": ("Packaging comparison", """
<section class="reference-band"><div class="shell reference-split" data-cups1-comparison>
    <div class="comparison-controls" data-cups1-new-fields hidden>
      <label>Product <select data-comparison-model>
        <option value="double-wall">Double-wall cup</option>
        <option value="single-wall">Single-wall cup</option>
        <option value="ripple-wall">Ripple-wall cup</option>
        <option value="dessert" data-cups1-new-fields="append">Dessert cup</option>
        <option value="bowls" data-cups1-new-fields="append">Kraft food bowl</option>
        <option value="boxes" data-cups1-new-fields="append">Takeaway box</option>
      </select></label>
      <div class="comparison-views" role="group" aria-label="Comparison view">
        <button type="button" data-comparison-view="0" aria-pressed="false">Plain</button>
        <button type="button" data-comparison-view="50" aria-pressed="true">Compare</button>
        <button type="button" data-comparison-view="100" aria-pressed="false">Printed</button>
      </div>
    </div>
    <div class="comparison-upload" data-comparison-upload data-cups1-new-fields="last" hidden>
      <label class="comparison-drop" data-logo-drop>
        <input type="file" accept="image/png,image/jpeg,image/webp" data-comparison-file>
        <strong>Drag your logo here</strong>
        <small>PNG, JPEG, or WebP · Up to 10 MB</small>
      </label>
      <p role="status" data-comparison-status></p>
      <button type="button" data-comparison-remove hidden>Remove logo</button>
    </div>
  <figure class="comparison-figure">
    <div class="reference-comparison">
    <img src="assets/comparison-cup.png" alt="Cream double-wall cup with a matching lid" data-comparison-cup="double-wall">
    <img src="assets/preview-single-wall.png" alt="Cream single-wall cup" data-comparison-cup="single-wall" data-cups1-new-fields hidden>
    <img src="assets/preview-ripple-wall.png" alt="Kraft ripple-wall cup with a cream lid" data-comparison-cup="ripple-wall" data-cups1-new-fields hidden>
    <img src="assets/preview-dessert.png" alt="Blank paper dessert cup" data-comparison-cup="dessert" data-cups1-new-fields="append" hidden>
    <img src="assets/preview-bowls.png" alt="Blank kraft food bowl" data-comparison-cup="bowls" data-cups1-new-fields="append" hidden>
    <img src="assets/preview-boxes.png" alt="Blank kraft takeaway box" data-comparison-cup="boxes" data-cups1-new-fields="append" hidden>
    <div class="reference-comparison-overlay">
      <img src="assets/cups1-logo-final-nav.png" alt="Cups1 branding printed on the cup">
      <canvas width="1536" height="1024" role="img" aria-label="Your logo printed on the product" data-comparison-artwork hidden></canvas>
    </div>
    <span class="reference-comparison-line" aria-hidden="true"><b>↔</b></span>
    <input type="range" min="0" max="100" value="50" aria-label="Compare the product with and without custom printing">
  </div><figcaption>Drag to compare plain and printed</figcaption>
  </figure>
</div><div class="shell"><h2 class="comparison-heading" data-cups1-new-fields="last">Preview your logo on packaging</h2></div><div class="reference-category"><div class="shell">
  <a href="@page/double-wall-paper-cups">Double-wall cups</a><a href="@page/single-wall-paper-cups">Single-wall cups</a>
  <a href="@page/ripple-wall-paper-cups">Ripple-wall cups</a><a href="@page/ice-cream-dessert-cups">Dessert cups</a>
  <a href="@page/kraft-food-salad-bowls">Food bowls</a><a href="@page/custom-takeaway-boxes">Takeaway boxes</a>
</div></div></section>"""),
    "home-business-mosaic": ("Business photo grid", """
<section class="reference-band reference-muted"><div class="shell">
  <div class="reference-mosaic">
    <article class="reference-photo reference-photo-feature"><img src="assets/cafes.webp" alt="Branded cups on a café counter">
      <div><p class="eyebrow">For business</p><h2>Packaging built around how you operate.</h2>
      <p>Plan custom production and recurring supply for cafés, restaurants, venues, and more.</p>
      <div class="actions"><a class="button primary" href="@page/for-business">Explore for business →</a><a class="button outline" href="@page/industries">Coffee shops ↗</a></div></div>
    </article>
    <a class="reference-photo" href="@page/industries"><img src="assets/restaurants.webp" alt=""><div><p class="eyebrow">For</p><h3>Restaurants ↗</h3></div></a>
    <a class="reference-photo" href="@page/location-management"><img src="assets/distributors.webp" alt=""><div><p class="eyebrow">For</p><h3>Venues and multi-location teams ↗</h3></div></a>
  </div>
  <p class="reference-more">Planning for a juice bar, brewery, or food truck? <a href="@page/contact-sales">Talk to sales</a>.</p>
</div></section>"""),
    "home-story-pair": ("Our story photo pair", """
<section class="reference-band reference-tint"><div class="shell reference-split">
  <div class="reference-story-images">
    <figure class="reference-photo"><img src="assets/detail.webp" alt="Printed packaging detail"><figcaption>Design</figcaption></figure>
    <figure class="reference-photo"><img src="assets/boxes.webp" alt="Takeaway packaging concepts"><figcaption>Supply</figcaption></figure>
  </div>
  <div><p class="eyebrow">Our story</p><h2>From your first idea to your next delivery.</h2>
    <p>Cups1 helps food-service businesses bring their brand to everyday packaging, from choosing a format and preparing artwork to coordinating production and delivery.</p>
    <a class="button outline" href="@page/about">Read our story →</a>
  </div>
</div></section>"""),
    "home-service-grid": ("Products and services grid", """
<section class="reference-band reference-muted"><div class="shell">
  <h2 class="reference-centered">Products and supply services for food-service teams.</h2>
  <div class="reference-service-grid">
    <a class="reference-service reference-service-primary" href="@page/products"><strong>See our catalog</strong><span aria-hidden="true">↗</span></a>
    <a class="reference-service" href="@page/warehousing"><div><h3>Warehousing</h3><p>Discuss inventory planning and scheduled delivery.</p></div><span aria-hidden="true">↗</span></a>
    <a class="reference-service" href="@page/business-account"><div><h3>Business account</h3><p>Find your account and ordering information.</p></div><span aria-hidden="true">↗</span></a>
    <a class="reference-service" href="@page/location-management"><div><h3>Location management</h3><p>Plan packaging supply across multiple sites.</p></div><span aria-hidden="true">↗</span></a>
  </div>
</div></section>"""),
    "home-use-carousel": ("Packaging use carousel", """
<section class="reference-band" data-cups1-carousel>
  <div class="shell reference-carousel-heading"><h2>Packaging in use.<br>Find a format for your business.</h2>
    <div class="reference-carousel-buttons" hidden><button type="button" data-carousel-prev aria-label="Previous card">‹</button><button type="button" data-carousel-next aria-label="Next card">›</button></div>
  </div>
  <div class="reference-carousel" tabindex="0" aria-label="Packaging examples">
    <article class="reference-note"><p class="eyebrow">Coffee shops</p><p>Choose a paper cup format and coordinate print artwork for your hot drink service.</p><a href="@page/products?format=beverage">Browse cups →</a></article>
    <a class="reference-photo" href="@page/industries"><img src="assets/cafes.webp" alt=""><div><h3>Cafés</h3></div></a>
    <article class="reference-note"><p class="eyebrow">Food service</p><p>Match bowls and takeaway containers to the way your menu travels.</p><a href="@page/products?format=food">Browse food packaging →</a></article>
    <a class="reference-photo" href="@page/ice-cream-dessert-cups"><img src="assets/dessert.webp" alt=""><div><h3>Dessert cups</h3></div></a>
    <article class="reference-note"><p class="eyebrow">Multiple locations</p><p>Share your delivery destinations and expected quantities for a coordinated supply quote.</p><a href="@page/location-management">Explore multi-location supply →</a></article>
  </div>
</section>"""),
    "home-closing-bands": ("Newsletter and business footer bands", """
<div class="reference-closing">
  <section class="reference-newsletter" id="cups1-newsletter"><img src="assets/restaurants.webp" alt="">
    <div class="shell"><div class="reference-newsletter-copy"><p class="eyebrow">Stay in the loop</p><h2>Get Cups1 packaging updates.</h2>
      <form action="@inquiry" method="post" data-cups1-newsletter>
        <input type="hidden" name="action" value="cups1_inquiry"><input type="hidden" name="intent" value="newsletter">
        <input type="hidden" name="cups1_nonce" value="@nonce"><input type="hidden" name="return_page" value="@current">
        <div hidden><label>Leave blank<input name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="reference-newsletter-fields"><input type="email" name="email" aria-label="Email address" placeholder="Enter your email" maxlength="254" required><button class="button primary" type="submit">Subscribe →</button></div>
        <p class="form-status" role="status"><span data-inquiry-result></span></p>
      </form>
    </div></div>
  </section>
  <section class="reference-footer-cta"><div class="shell">
    <div><p class="eyebrow">For business</p><h2>Build a packaging plan for your team.</h2><p>Tell us what you need printed and where you need it delivered.</p></div>
    <a class="button outline" href="@page/contact-sales">Talk to sales →</a>
  </div></section>
</div>"""),
}
