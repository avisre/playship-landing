# PlayShip

![Auto-deploy](https://github.com/avisre/playship-landing/actions/workflows/deploy.yml/badge.svg)

<!-- autodeploy-test: 2026-05-24 -->

Landing page for PlayShip, a Google Play submission service. Static one-pager built with Astro 6, Tailwind v4, and self-hosted Geist fonts.

## Stack

- Astro 6 (static output)
- Tailwind CSS v4 (via `@tailwindcss/vite`)
- Fontsource Geist Sans + Geist Mono (no Google Fonts CDN)
- `@astrojs/sitemap`
- Formspree for the intake form
- Zero JavaScript on the client beyond Astro's bundle

## Local development

```sh
npm install
npm run dev
```

Dev server: http://localhost:4321/

```sh
npm run build      # static build into dist/
npm run preview    # serve dist/ locally
```

Node version is pinned via `.node-version` (currently `22.12.0`).

## Project structure

```
src/
  pages/
    index.astro       # main landing page
    404.astro         # not-found page
  layouts/
    Layout.astro      # HTML scaffold, meta tags, font imports, favicon
  components/
    Hero.astro
    PainPoints.astro
    Process.astro
    Pricing.astro
    Credibility.astro
    FAQ.astro
    IntakeForm.astro
    Footer.astro
  styles/
    global.css        # design tokens (CSS custom properties), base type, .container
public/
  favicon.svg         # custom monochrome favicon
  favicon.ico         # fallback
  robots.txt
astro.config.mjs      # site URL + sitemap integration
.node-version         # 22.12.0
```

## Design system

All colors live as CSS custom properties on `:root` in `src/styles/global.css`. Components reference them via `var(--token)`. Do not re-declare these tokens in component scoped styles.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#FAFAF7` | Page background |
| `--soft` | `#F4F4F0` | Card / section break background |
| `--ink` | `#0A0A0A` | Primary text |
| `--muted` | `#4B5563` | Secondary text (tuned for WCAG AA on `--soft`) |
| `--line` | `rgba(10,10,10,0.08)` | Default borders |
| `--line-strong` | `rgba(10,10,10,0.18)` | Emphasis borders |
| `--approved` | `#15803D` | Trust / success / check icons |
| `--approved-soft` | `#DCFCE7` | Badge backgrounds |
| `--cta` | `#C2410C` | Primary action background |
| `--cta-hover` | `#9A3412` | Hover state |

Typography rules:

- Sentence case everywhere. No Title Case. No ALL CAPS except `.eyebrow` (mono uppercase).
- Weights `400` and `500` only. Never bold.
- Headings and body in Geist Sans. Numbers, prices, eyebrows, and buttons in Geist Mono.

## Intake form delivery (FormSubmit)

The intake form at `src/components/IntakeForm.astro` POSTs directly to FormSubmit, which forwards every submission to `avinashsreekumar007@gmail.com`. No account, no API key, no dashboard — just an email address in the form action.

```html
<form action="https://formsubmit.co/b391c6f131759b7d0723b3185e4e658d" method="POST">
  <input type="hidden" name="_subject" value="New PlayShip intake" />
  <input type="hidden" name="_template" value="table" />
  <input type="hidden" name="_captcha" value="false" />
  <input type="text" name="_honey" class="botcheck" ... />
  ...
</form>
```

The action URL uses FormSubmit's hashed alias rather than the naked email address — this keeps `avinashsreekumar007@gmail.com` out of the page's HTML source, reducing scraper-driven spam. The hash forwards to the original email; to change the destination, generate a new hash by activating a fresh email with FormSubmit.

### Activation status

The form was activated on first submission (May 2026). Submissions deliver immediately, no further setup needed.

### Hidden field reference

- `_subject` — email subject line in your inbox
- `_template=table` — formats the submission as a clean HTML table
- `_captcha=false` — skips the FormSubmit captcha page (the honeypot below handles spam)
- `_honey` — invisible honeypot field; bots fill it, real users don't

### Limits

FormSubmit is free with no published submission cap. If volume becomes a concern, switch to a self-hosted backend later.

## Production site URL

`astro.config.mjs` is set to `https://playship-landing.onrender.com`. Update the `site` field there once a custom domain is wired up; sitemap and canonical links derive from it.

## Deploying to Render

This is a static site. Render configuration:

- **Service type:** Static Site
- **Build command:** `npm run build`
- **Publish directory:** `dist`
- **Node version:** `22.12.0` (read automatically from `.node-version`, or set `NODE_VERSION` env var on Render to override)
- **Auto-deploy:** Enable on `main` branch
- **Pull request previews:** Optional, recommended

After the first deploy:

1. Update `astro.config.mjs` `site:` field with the real Render URL.
2. Update `public/robots.txt` sitemap URL with the real Render URL.
3. Rebuild.

## SEO

Meta tags and four JSON-LD blocks (Service, LocalBusiness, FAQPage, WebSite) are wired into `src/layouts/Layout.astro` and `src/components/StructuredData.astro`.

Two verification meta tags in `src/layouts/Layout.astro` ship with placeholder values and need real tokens before the consoles will accept them:

- `<meta name="google-site-verification" content="GOOGLE_VERIFICATION_PLACEHOLDER" />` — swap with the token from Google Search Console (URL-prefix property, HTML-tag method).
- `<meta name="msvalidate.01" content="BING_VERIFICATION_PLACEHOLDER" />` — swap with the key from Bing Webmaster Tools (Meta-tag method), or import directly from Search Console after step 1.

After swapping either token, rebuild and redeploy, then click **Verify** in the corresponding console.

The OG image at `public/og-image.png` is rasterised from `public/og-image.svg` via `sharp`. To regenerate after editing the SVG, run sharp against the SVG at 1200x630 and overwrite the PNG.

## Lighthouse scores (mobile, production build)

- Performance: 97
- Accessibility: 100
- Best Practices: 100
- SEO: 100

Re-run locally with:

```sh
npm run build
cd dist && python3 -m http.server 4321 &
CHROME_PATH=/path/to/chrome lighthouse http://localhost:4321/ \
  --form-factor=mobile --screenEmulation.mobile=true \
  --chrome-flags="--headless=new --no-sandbox"
```

## Contributing notes

- No JavaScript on the client unless a section explicitly needs it. The FAQ uses native `<details>` and the disclosure toggle is pure CSS.
- No external CDNs beyond the Formspree POST endpoint.
- All borders are `0.5px` or `1px`. The sole `2px` border is the featured pricing card — intentional.
- All hover states use `150ms ease` transitions on color/border only. No transforms, no shadows, no scale.
