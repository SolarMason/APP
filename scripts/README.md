# scripts/

One-time bootstrap utilities for `app.nepa-pro.com`. Not deployed — these run on your local machine.

## `setup_stripe.py`

Creates all 35 subscription Products + monthly Prices + Payment Links in your Stripe account in one shot.

### What you need

- Python 3.8+ (you already have this)
- Your Stripe **secret key** (starts with `sk_live_` for live mode or `sk_test_` for test mode (described in Stripe dashboard))
  - Get it at: https://dashboard.stripe.com/apikeys
  - For your first run, **use a test key** to verify everything looks right before flipping to live.

### Run it

```bash
# install Stripe SDK once
pip install stripe --break-system-packages

# go to scripts folder
cd scripts

# set your key (TEST first)
export STRIPE_API_KEY=<YOUR-TEST-SECRET-KEY>

# run
python3 setup_stripe.py
```

### What it produces

Three files in `scripts/`:

| File | What it is |
|---|---|
| `stripe_links.json` | Full mapping of every product/price/payment-link ID and URL. Source of truth. |
| `stripe_links.js` | Copy-paste-ready JS snippet — replace the `STRIPE_LINKS` block in `index.html` with this content. |
| `setup_stripe.log` | Console log of every Stripe call. Useful if something fails partway. |

After running, open `stripe_links.js`, copy the entire `const STRIPE_LINKS = { … };` block, and replace the matching block at the top of the `<script>` section in `../index.html`. Push to GitHub. Live.

### Important notes

- **Re-running creates duplicates.** Stripe doesn't dedupe by name. If you need to re-run, archive the previous products in your Stripe dashboard first (Products → ⋮ → Archive).
- **Switch from test to live** by archiving your test products (or just using a different Stripe account view), then running the script again with your live key.
- **Success URL** is hardcoded to `https://nepa-pro.com/app-thanks?session={CHECKOUT_SESSION_ID}` — change the `SUCCESS_URL` constant near the top of `setup_stripe.py` if your thank-you page lives elsewhere.
- **Webhook handler** for handling successful subscriptions (provisioning the customer's PWA, sending welcome emails, etc.) is a separate next step — you'll want a Cloudflare Worker or SuiteDash automation listening on `checkout.session.completed`. Tell me when you're ready and I'll build it.

### Editing the catalog

If you need to change a product name, description, or price before running: edit the `CATALOG` list in `setup_stripe.py` directly. Each entry is `(key, name, description, monthly_price_in_dollars)`. The `key` MUST match the `data-id` attribute on the corresponding card in `index.html` — that's what links them together.
