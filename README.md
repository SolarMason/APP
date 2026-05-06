# app.

> We build your app. You run your business.

A NEPA-PRO product. Marketing site for **app.nepa-pro.com** — a PWA-as-a-service business.

## Business model

- **Pure subscription. Nothing is one-time.** Setup is always waived.
- **Base PWA: $49/month.** Required, always-on. Includes the custom-built app, hosting, SSL, CDN, save-to-home-screen, offline mode, branding.
- **Every capability is its own stackable subscription.** Email, SMS, payments, accounts, bookings, dispatch, etc. — toggle on what you need.
- **Stripe Checkout via nepa-pro.com** handles all billing.
- **Cancel anytime.** No lock-in. App goes offline when subscription stops (since hosting is part of the sub).

## Add-on subscription catalog (27 items, 7 categories)

| Category | Add-ons | Price range |
|---|---|---|
| Communications | Email, SMS, Push, Live chat, AI chatbot, Newsletter | $15-$39/mo |
| Commerce | Stripe payments, Subscriptions, Catalog, Invoicing, Coupons | $15-$35/mo |
| Users & Accounts | Auth, Social login, Member portal, Roles | $15-$39/mo |
| Data & Content | Database, CRM, Analytics, CMS, Gallery, Search | $15-$35/mo |
| Booking | Appointments, Reservations, Events, Calendar sync | $15-$29/mo |
| Operations | Job dispatch, Quotes, Reviews, Loyalty, Referrals | $15-$35/mo |
| Premium | Custom domain, White-glove, Native wrap, Priority | $9-$99/mo |

Edit pricing/add-ons by changing `data-price` and content of `.sub` cards in `index.html`.

## Files

| File | Purpose |
|---|---|
| `index.html` | Single-page marketing site (all CSS + JS inline, ~100 KB) |
| `manifest.json` | PWA manifest |
| `sw.js` | Service worker (offline cache) |
| `icon.svg` | Master icon source |
| `icon-*.png` | Rendered PWA icons (192, 512, 1024, maskable) |
| `og-card.svg` / `og-card.png` | OG share card source + render |
| `.github/workflows/deploy.yml` | GitHub Actions auto-deploy |
| `CNAME` | Custom domain binding (`app.nepa-pro.com`) |

## Deploy to GitHub Pages

1. Create a new repo (e.g. `app-nepa-pro`)
2. Push all these files to `main`
3. Settings → Pages → Source: **GitHub Actions**
4. DNS: add a CNAME record `app` → `<your-username>.github.io`
5. The included workflow auto-deploys on every push to `main`.
6. The included `CNAME` file binds the custom domain.

First push triggers the workflow (~30-60s). HTTPS cert provisions in 5-15 min.

## Local testing

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

To test PWA installability you need HTTPS — deploy to Pages, or use `ngrok http 8000`.

## Customizing later

- All CSS/JS is inline in `index.html`. Edit one file, redeploy.
- Form currently uses `mailto:` to `hello@app.nepa-pro.com` and includes the customer's selected stack in the email body — so you know exactly what to invoice for.
- When ready, swap the form submit handler to POST to a Cloudflare Worker / SuiteDash / Stripe Checkout URL on nepa-pro.com.
- The base PWA price (`BASE_PRICE = 49`) and all add-on prices live in the cards' `data-price` attributes. Edit there.

## Brand

- Wordmark: **app.** (the period is the signature — gradient orb)
- Palette: iOS system blue `#0a84ff` → indigo `#5e5ce6` → purple `#bf5af2`
- Type: SF Pro Display / Inter Display fallback
- Aesthetic: pure black, Liquid Glass, Lock Screen vibe

—
Built in NEPA. Veteran owned and operated.
