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

## Swap the Web3Forms access key

The intake form at `src/components/IntakeForm.astro` POSTs to Web3Forms, which forwards every submission to your email. The form currently uses a placeholder access key:

```html
<input type="hidden" name="access_key" value="WEB3FORMS_ACCESS_KEY_PLACEHOLDER" />
```

To wire it up (30-second flow, free, no real signup):

1. Go to https://web3forms.com
2. Enter `avinashsreekumar007@gmail.com` — Web3Forms sends you a verification email containing your access key (a UUID).
3. Copy the access key.
4. Replace `WEB3FORMS_ACCESS_KEY_PLACEHOLDER` in `src/components/IntakeForm.astro` with that key.
5. Rebuild (`npm run build`) and redeploy.

After that, every submission arrives in `avinashsreekumar007@gmail.com` as an email with subject `New PlayShip intake` and all form fields in the body.

The form includes a honeypot field (`botcheck`) which Web3Forms uses for spam filtering — leave it in place.

Free tier: 250 submissions/month. If you grow past that, upgrade or switch to a self-hosted backend.

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
