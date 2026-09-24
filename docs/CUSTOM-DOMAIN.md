# Custom domain: valleynotaryservices.com

**Audit date:** 2026-07-24 (Mac valak)

Valley Notary Services custom domain is **live and verified**.

## Live status (public DNS)

| Check | Result |
|-------|--------|
| WHOIS | **ACTIVE** — Registrar Cloudflare, Inc.; created 2026-07-23 |
| NS | `sue.ns.cloudflare.com`, `thaddeus.ns.cloudflare.com` |
| `dig valleynotaryservices.com A` | `185.199.108–111.153` (GitHub Pages) |
| `dig www CNAME` | `jimmythegod100.github.io` |
| `curl -I https://valleynotaryservices.com` | **HTTP/2 200** — `server: GitHub.com` |
| `curl -I https://www.valleynotaryservices.com` | **301 → apex** |
| GitHub Pages API | `cname: valleynotaryservices.com`, `https_enforced: true`, cert approved through 2026-10-21 |

## Cloudflare (Jimmythegod100@gmail.com)

| Setting | Value |
|---------|-------|
| DNS apex | Four **A** records → GitHub Pages IPs — **DNS only** (grey cloud) |
| DNS www | **CNAME** → `jimmythegod100.github.io` — **DNS only** |
| Email | **MX** → Cloudflare Email Routing (`route1/2/3.mx.cloudflare.net`) |
| SPF | `v=spf1 include:_spf.mx.cloudflare.net ~all` |
| SSL/TLS mode | **Full** (records are DNS-only; TLS terminates at GitHub Pages) |

## Checklist

### DONE

- [x] Domain registered at Cloudflare (valleynotaryservices.com)
- [x] Nameservers on Cloudflare
- [x] DNS A + www CNAME → GitHub Pages (DNS only)
- [x] `CNAME` file in repo root
- [x] Canonical URLs, sitemap, robots.txt, `site-config.js` use apex domain
- [x] GitHub Pages custom domain + Enforce HTTPS
- [x] Live site serves Valley Notary Services branding (not Vince Remedia)

### STILL NEEDED

- [ ] **FormSubmit activation** — from production, submit the request form once and click the confirmation email FormSubmit sends to `info@valleynotaryservices.com`. Until that click, the first customer may see FormSubmit’s activation page instead of `/request-received.html`.
- [ ] **Optional:** Cloudflare Email Routing rules for `info@valleynotaryservices.com` if inbox forwarding not yet tested

## Verify

```bash
dig +short valleynotaryservices.com A
dig +short www.valleynotaryservices.com CNAME
curl -sI https://valleynotaryservices.com/ | head -8
gh api repos/jimmythegod100/valleynotaryservices/pages
```

## Project

- **Repo:** [jimmythegod100/valleynotaryservices](https://github.com/jimmythegod100/valleynotaryservices)
- **Local:** `~/Projects/valleynotaryservices`
- **Hosting:** GitHub Pages (`main`, repository root)

## Note: vinceremediaworks.com

The Vince Remedia Works portfolio domain was **not purchased**. That site remains on GitHub Pages at https://jimmythegod100.github.io/vincere-media-works-web/
