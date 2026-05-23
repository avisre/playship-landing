# PlayShip

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

## Swap the Formspree endpoint

The intake form at `src/components/IntakeForm.astro` currently POSTs to a placeholder:

```html
<form action="https://formspree.io/f/PLACEHOLDER" method="POST">
```

To wire it up:

1. Create a form at https://formspree.io and copy the endpoint (looks like `https://formspree.io/f/abcd1234`).
2. Replace `PLACEHOLDER` in `IntakeForm.astro`.
3. Optionally configure Formspree to forward submissions to `avinashsreekumar007@gmail.com`.
4. Rebuild and redeploy.

No JavaScript handler — Formspree handles the redirect natively after a POST.

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
