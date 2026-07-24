# Valley Notary Services

Professional mobile notary public site for Modesto, CA and the Central Valley. A service of Martinez Enterprises.

**Live site:** [https://valleynotaryservices.com](https://valleynotaryservices.com)

`www.valleynotaryservices.com` redirects to the apex canonical URL. GitHub Pages serves the site over HTTPS (custom domain + enforced HTTPS).

Domain audit and DNS checklist: [`docs/CUSTOM-DOMAIN.md`](docs/CUSTOM-DOMAIN.md)

## Stack

- Static HTML/CSS (no build step)
- Hosted on GitHub Pages (`main` / repository root)
- Custom domain via Cloudflare DNS (DNS-only) → GitHub Pages

## Contact

info@valleynotaryservices.com

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

## Deploy

Push to `main`. GitHub Pages publishes from the repository root. Do not change `CNAME` or email-related DNS records when editing site files.
