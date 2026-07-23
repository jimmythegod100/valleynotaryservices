# Valley Notary Services

Professional mobile notary public site for Modesto, CA and the Central Valley.

**Live now:** [https://jimmythegod100.github.io/valleynotaryservices/](https://jimmythegod100.github.io/valleynotaryservices/)

**Custom domain (pending DNS):** [https://valleynotaryservices.com](https://valleynotaryservices.com) — intended hostname is in `CNAME.cloudflare-pending`. Public nameservers still advertise `sue`/`thaddeus` (empty zone); Cloudflare zone records live on `brit`/`phil` and need registrar NS alignment before GitHub Pages can issue the apex certificate.

## Stack

- Static HTML/CSS (no build step)
- Hosted on GitHub Pages (`main` / root)
- Custom domain via Cloudflare DNS → GitHub Pages (blocked until NS mismatch is fixed)

## Contact

info@valleynotaryservices.com

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

## Deploy

Push to `main`. GitHub Pages publishes from the repository root.

After Cloudflare nameservers are `brit.ns.cloudflare.com` and `phil.ns.cloudflare.com` and the apex resolves to GitHub Pages IPs, restore the root `CNAME` from `CNAME.cloudflare-pending` and set Pages:

```bash
gh api -X PUT repos/jimmythegod100/valleynotaryservices/pages --input - <<'EOF'
{"cname":"valleynotaryservices.com","https_enforced":true}
EOF
```
