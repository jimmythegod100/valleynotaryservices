# Valley Notary Services

Mobile-only traveling notary public site for Modesto, CA and the Central Valley. We come to you — no walk-in office. A service of Martinez Enterprises.

**Live site:** [https://valleynotaryservices.com](https://valleynotaryservices.com)

`www.valleynotaryservices.com` redirects to the apex canonical URL. GitHub Pages serves the site over HTTPS (custom domain + enforced HTTPS).

Domain audit and DNS checklist: [`docs/CUSTOM-DOMAIN.md`](docs/CUSTOM-DOMAIN.md)

## Stack

- Static HTML/CSS (no build step)
- Hosted on GitHub Pages (`main` / repository root)
- Custom domain via Cloudflare DNS (DNS-only) → GitHub Pages

## Contact

info@valleynotaryservices.com · (209) 315-5702

Booking form posts to FormSubmit (`info@valleynotaryservices.com`) and redirects to `/request-received.html`. Shareable request URL: [valleynotaryservices.com/request.html](https://valleynotaryservices.com/request.html).

**Owner action (once):** submit the live form and click FormSubmit’s first-email confirmation so later customer requests arrive in the inbox.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

## Deploy

Push to `main`. GitHub Pages publishes from the repository root. Do not change `CNAME` or email-related DNS records when editing site files.
