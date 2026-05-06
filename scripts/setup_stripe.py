#!/usr/bin/env python3
"""
==============================================================================
app.nepa-pro.com — Stripe Products + Payment Links bootstrap
==============================================================================

ONE-TIME SETUP:
This script creates all 35 subscription products, monthly recurring prices,
and Payment Links in your Stripe account in a single run. It outputs a
ready-to-paste STRIPE_LINKS const block for index.html.

USAGE:
    pip install stripe --break-system-packages
    export STRIPE_API_KEY=<YOUR-LIVE-SECRET-KEY>       # use <test-secret-key> for testing first
    python3 setup_stripe.py

OUTPUTS (in current directory):
    stripe_links.json       — full mapping of every product/price/link
    stripe_links.js         — copy-paste-ready JS snippet for index.html
    setup_stripe.log        — console log of every Stripe call

SAFETY:
    - Run in TEST MODE first (any key from your Stripe test environment) to verify everything looks right
    - Re-running creates DUPLICATES (Stripe doesn't dedupe by name) — only
      run once per environment, or archive previous products in dashboard first
    - Your key is read from STRIPE_API_KEY env var — never hardcoded

==============================================================================
"""

import os
import sys
import json
import time
from datetime import datetime

try:
    import stripe
except ImportError:
    print("ERROR: stripe library not installed.")
    print("Run: pip install stripe --break-system-packages")
    sys.exit(1)

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------

API_KEY = os.environ.get("STRIPE_API_KEY")
if not API_KEY:
    print("ERROR: STRIPE_API_KEY environment variable is not set.")
    print("Set it first:  export STRIPE_API_KEY=<YOUR-LIVE-SECRET-KEY>")
    print("Or for testing: export STRIPE_API_KEY=<YOUR-TEST-SECRET-KEY>")
    sys.exit(1)

stripe.api_key = API_KEY
MODE = "TEST" if API_KEY[:8] == "sk_test_" else "LIVE"

# After-checkout success URL (Stripe will redirect here once payment succeeds).
# Adjust to your actual thank-you / onboarding page on nepa-pro.com.
SUCCESS_URL = "https://nepa-pro.com/app-thanks?session={CHECKOUT_SESSION_ID}"

# -----------------------------------------------------------------------------
# CATALOG — must match index.html data-id values exactly
# -----------------------------------------------------------------------------
# (key, display_name, description, monthly_price_in_dollars)

CATALOG = [
    # Base
    ("base", "app. — Base PWA",
        "A custom Progressive Web App for your business. Hosted, installable on iPhone/Android/desktop, works offline. Setup waived. Cancel anytime.", 49),

    # Communications
    ("email", "app. — Email Backend",
        "Transactional & marketing email infrastructure on a custom domain.", 19),
    ("sms", "app. — SMS / Texting",
        "Two-way SMS for confirmations, reminders, and customer support.", 29),
    ("push", "app. — Push Notifications",
        "Native push notifications to home-screen-installed apps. Segments & campaigns.", 15),
    ("livechat", "app. — Live Chat Widget",
        "Real-time chat inside your app. Multi-agent inbox, mobile-ready.", 25),
    ("ai", "app. — AI Chatbot",
        "24/7 smart chatbot trained on your business and FAQ content.", 39),
    ("newsletter", "app. — Newsletter Signup",
        "List builder, signup forms, double opt-in compliance.", 15),

    # Commerce
    ("stripe", "app. — Stripe Payments",
        "One-time payments, deposits, donations, gift cards.", 25),
    ("subscriptions", "app. — Subscription Billing",
        "Recurring plans, trials, upgrades, prorated changes.", 35),
    ("catalog", "app. — Product Catalog",
        "Items, prices, images, variants — full storefront.", 25),
    ("invoicing", "app. — Invoicing",
        "Send invoices, track paid/unpaid, automatic reminders.", 19),
    ("coupons", "app. — Coupons & Promo Codes",
        "Discount codes, expirations, single-use, BOGO.", 15),

    # Users & Accounts
    ("auth", "app. — User Accounts & Auth",
        "Email/password signup, sessions, password reset.", 29),
    ("social", "app. — Social Login",
        "Sign in with Apple, Google, Facebook — one tap.", 15),
    ("member", "app. — Member Portal",
        "Gated content, profile pages, member dashboards.", 39),
    ("roles", "app. — Roles & Permissions",
        "Admin, manager, staff, customer — granular access.", 20),

    # Data & Content
    ("db", "app. — Database Hosting",
        "Custom data, queries, backups, growing tables.", 29),
    ("crm", "app. — CRM Integration",
        "SuiteDash, HubSpot, Salesforce — bi-directional sync.", 35),
    ("analytics", "app. — Analytics Dashboard",
        "Visitors, conversions, revenue, retention — live.", 15),
    ("cms", "app. — Blog / CMS",
        "Posts, categories, drafts, scheduled publishing.", 19),
    ("gallery", "app. — Photo Gallery",
        "Albums, lightbox, filters — portfolios and products.", 15),
    ("search", "app. — Site Search",
        "Fast in-app search across all your content.", 15),

    # Booking
    ("appts", "app. — Appointments",
        "Bookable time slots, rules, reminders, calendar sync.", 29),
    ("reservations", "app. — Reservations",
        "Tables, rooms, equipment — capacity and deposits.", 29),
    ("events", "app. — Event Tickets",
        "Sell tickets, scan at the door, capacity and tiers.", 25),
    ("calsync", "app. — Calendar Sync",
        "Two-way sync with Google and Apple Calendar.", 15),

    # Operations & Marketing
    ("dispatch", "app. — Job Dispatch",
        "Assign work, track crews, GPS check-ins, signatures.", 35),
    ("quotes", "app. — Quote Builder",
        "Itemized estimates with line items, taxes, e-signature.", 25),
    ("reviews", "app. — Reviews & Ratings",
        "Collect, display, moderate — push to Google and Yelp.", 15),
    ("loyalty", "app. — Loyalty Program",
        "Points, stamps, tiers, push-back rewards.", 25),
    ("referrals", "app. — Referral Tracking",
        "Customer-share links, tracking, payout flows.", 20),

    # Premium
    ("domain", "app. — Custom Domain",
        "yourbrand.com instead of a subdomain. SSL included.", 9),
    ("white", "app. — White-Glove Support",
        "Same-day fixes, dedicated channel, monthly check-ins.", 75),
    ("wrap", "app. — Native App Wrapper",
        "Optional — ship to App Store and Play Store too.", 99),
    ("priority", "app. — Priority Delivery",
        "3-day build instead of 5. Front-of-line builds.", 49),
]


# -----------------------------------------------------------------------------
# RUN
# -----------------------------------------------------------------------------

def main():
    log_lines = []
    def log(msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        log_lines.append(line)

    log(f"Stripe mode: {MODE}")
    log(f"Items to create: {len(CATALOG)}")
    log(f"Success redirect: {SUCCESS_URL}")
    log("")

    if MODE == "LIVE":
        confirm = input("⚠️  You are using a LIVE Stripe key. Real products will be created. Type 'yes' to continue: ")
        if confirm.strip().lower() != "yes":
            log("Aborted.")
            return

    results = {}
    failures = []

    for key, name, desc, price_dollars in CATALOG:
        try:
            log(f"→ {name} (${price_dollars}/mo)")

            # 1. Product
            product = stripe.Product.create(
                name=name,
                description=desc,
                metadata={"app_id": key, "source": "app.nepa-pro.com"}
            )

            # 2. Price (recurring monthly)
            price = stripe.Price.create(
                product=product.id,
                unit_amount=price_dollars * 100,
                currency="usd",
                recurring={"interval": "month"},
                metadata={"app_id": key}
            )

            # 3. Payment Link
            link = stripe.PaymentLink.create(
                line_items=[{"price": price.id, "quantity": 1}],
                after_completion={
                    "type": "redirect",
                    "redirect": {"url": SUCCESS_URL}
                },
                metadata={"app_id": key}
            )

            results[key] = {
                "name": name,
                "price_dollars": price_dollars,
                "product_id": product.id,
                "price_id": price.id,
                "payment_link_id": link.id,
                "url": link.url,
            }
            log(f"   ✓ {link.url}")
            time.sleep(0.15)  # be kind to rate limits

        except Exception as e:
            log(f"   ✗ FAILED: {e}")
            failures.append((key, name, str(e)))

    log("")
    log(f"Created: {len(results)} / {len(CATALOG)}")
    if failures:
        log(f"Failures: {len(failures)}")
        for k, n, err in failures:
            log(f"   - {k} ({n}): {err}")

    # Write JSON
    with open("stripe_links.json", "w") as f:
        json.dump(results, f, indent=2)
    log("")
    log("Wrote stripe_links.json")

    # Write JS snippet (copy-paste ready)
    with open("stripe_links.js", "w") as f:
        f.write("// Auto-generated by setup_stripe.py — paste this into index.html\n")
        f.write(f"// Stripe mode: {MODE}\n")
        f.write(f"// Generated: {datetime.now().isoformat()}\n\n")
        f.write("const STRIPE_LINKS = {\n")
        for key, _, _, _ in CATALOG:
            if key in results:
                f.write(f'  {key + ":":<16}{json.dumps(results[key]["url"])},\n')
            else:
                f.write(f'  {key + ":":<16}"REPLACE_ME_FAILED",\n')
        f.write("};\n")
    log("Wrote stripe_links.js")

    # Write log
    with open("setup_stripe.log", "w") as f:
        f.write("\n".join(log_lines))
    log("Wrote setup_stripe.log")
    log("")
    log("Done. Open stripe_links.js and paste the STRIPE_LINKS block into index.html.")


if __name__ == "__main__":
    main()
