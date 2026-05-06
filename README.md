# app.

> We build your app. You run your business.

PWA-as-a-service marketing site for **app.nepa-pro.com** — a NEPA-PRO product.

## Files

| File | Purpose |
|---|---|
| `index.html` | Single-page marketing site (all CSS + JS inline) |
| `manifest.json` | PWA manifest — makes the site installable |
| `sw.js` | Service worker — offline cache, install prompt support |
| `icon.svg` | Master icon (vector source) |
| `icon-192.png` | PWA icon, 192×192 |
| `icon-512.png` | PWA icon, 512×512 |
| `icon-1024.png` | High-res icon (Apple Touch, app store wrappers) |
| `icon-maskable.png` | Android maskable icon |
| `og-card.svg` | Open Graph share card (vector source) |
| `og-card.png` | Open Graph share card, 1200×630 (referenced in `<meta>`) |

## Deploy to GitHub Pages

1. Create a new repo (e.g. `app-nepa-pro`)
2. Drop all these files at the **root** of the repo
3. Settings → Pages → Source: `main` branch, `/` (root)
4. Add a custom domain: `app.nepa-pro.com`
5. In your DNS, add a CNAME: `app` → `<username>.github.io`
6. Wait for SSL (5-15 min)

## Deploy via GitHub Actions (recommended for production)

If you want to use the same workflow pattern as `Solar-Mason-Dev`:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
```

Then in repo Settings → Pages → Source: **GitHub Actions**.

## Local testing

```bash
# any static server — python is easiest
python3 -m http.server 8000
# then open http://localhost:8000
```

To test PWA installability you need HTTPS — either deploy to Pages, or use `ngrok http 8000`.

## Customizing later

- All CSS/JS is inline in `index.html`. Edit one file, redeploy.
- Form currently uses `mailto:` fallback to `hello@app.nepa-pro.com`. Swap to a real backend (Cloudflare Worker, SuiteDash, Formspree, etc.) by replacing the submit handler near the bottom of the `<script>` block.
- Pricing tiers live in the `tiers` object inside the pricing IIFE. Edit there to change names/prices/features.
- Add-ons are `<div class="addon-row">` elements with `data-price` attributes. Add/remove rows; the totals recompute automatically.

## Brand

- Wordmark: **app.** (the period is the signature — gradient orb)
- Palette: iOS system blue `#0a84ff` → indigo `#5e5ce6` → purple `#bf5af2`
- Type: SF Pro Display / Inter Display fallback
- Aesthetic: pure black, Liquid Glass, Lock Screen vibe

—
Built in NEPA. Veteran owned and operated.
