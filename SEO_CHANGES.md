# SEO changes — what was added and why

One-pass SEO upgrade to `src/layouts/Layout.astro` plus a new structured-data component and a real OG image. Everything is build-verified (`npm run build` passes, all four JSON-LD blocks emit into `dist/index.html`).

## Files touched

- `src/layouts/Layout.astro` — meta-tag expansion (see below)
- `src/components/StructuredData.astro` — new, four JSON-LD blocks
- `public/og-image.svg` — 1200x630 source (editable)
- `public/og-image.png` — rasterised at build-time from the SVG via `sharp` (25 KB)

## What's new in `<head>`

### Crawl directives
- `<meta name="robots" content="index,follow">`
- `<meta name="googlebot" content="index,follow">` (explicit, redundant but defensive)
- `<link rel="alternate" hreflang="en" ...>` and `hreflang="x-default"` pointing at the same canonical (single-locale site, but flags the language so search engines stop guessing)

### Author / publisher
- `<meta name="author" content="Avinash Sreekumar">`
- `<meta property="og:site_name" content="PlayShip">`
- `<meta property="og:locale" content="en_US">`
- Publisher is also wired into the WebSite JSON-LD via `@id` references

### Open Graph
- `og:image` now points at the real `/og-image.png` (was 404'ing before)
- Added `og:image:type`, `og:image:width` (1200), `og:image:height` (630), `og:image:alt`

### Twitter
- Upgraded `twitter:card` from `summary` to `summary_large_image`
- Added `twitter:image` and `twitter:image:alt`

### Keywords
- Added the deprecated-but-harmless `<meta name="keywords">` per spec request: `google play submission, play store rejection recovery, android app submission service, expo react native play store, data safety form, play console help`

### Search Console / Bing verification placeholders
- `<meta name="google-site-verification" content="GOOGLE_VERIFICATION_PLACEHOLDER">`
- `<meta name="msvalidate.01" content="BING_VERIFICATION_PLACEHOLDER">`

Both are dummy strings. Swap them with the real tokens once Avi claims the site in each console (steps below). They sit at the bottom of the meta block so they're easy to find.

## Structured data (JSON-LD)

Four discrete `<script type="application/ld+json">` blocks rendered from `src/components/StructuredData.astro`. Keeping them in a separate component keeps Layout readable; Astro inlines them at build time, no client JS cost.

1. **Service** — `@type: Service`, name "PlayShip", `serviceType: "Google Play Store submission"`, provider is a Person (Avinash Sreekumar, Trivandrum, Kerala, India), `areaServed` covers both India and Worldwide, and the three pricing tiers live under `hasOfferCatalog.itemListElement` as `Offer` nodes with `price`, `priceCurrency: "USD"`, and `availability: InStock`.
2. **LocalBusiness** — because Avi operates a freelance service from a specific city, this gives Google a hook for local-pack visibility on India-targeted queries. Includes `priceRange: "$149–$799"`, the same Trivandrum address, and `@id`-references the Person node so the knowledge graph dedupes.
3. **FAQPage** — wraps all six Q/A pairs from `src/components/FAQ.astro` verbatim. Eligible for FAQ rich results in Google Search.
4. **WebSite** — minimal but lets Google associate the publisher Person with the domain.

All four blocks share `@id` URIs (`https://playship.pro/#service`, `#avinash`, `#localbusiness`, etc.) so a crawler can resolve them as a single graph rather than four loose objects.

## OG image

`public/og-image.svg` is the source of truth (1200x630, sentence-case, uses the project's design tokens: `#FAFAF7` background, `#0A0A0A` ink, `#15803D` approved-green badge). The PNG is generated from it via `sharp` — already a transitive Astro dependency, so no new package needed.

To regenerate the PNG after editing the SVG, from the project root:

```sh
node -e "
const sharp = require('sharp');
const fs = require('fs');
sharp(fs.readFileSync('public/og-image.svg'), { density: 150 })
  .resize(1200, 630, { fit: 'fill' })
  .png({ quality: 95 })
  .toFile('public/og-image.png')
  .then(i => console.log(i.width + 'x' + i.height));
"
```

Fallback if `sharp` is ever removed: any 1200x630 PNG at `public/og-image.png` works — the SVG is a layout reference, nothing depends on it being the source.

## What Avi needs to do next

### 1. Google Search Console verification

1. Go to https://search.google.com/search-console and add `https://playship.pro` as a **URL prefix** property (not Domain — that would need a DNS TXT record).
2. Pick the **HTML tag** verification method. Google will show a string like `content="abc123XYZ..."`.
3. Open `src/layouts/Layout.astro`, find the line:
   ```html
   <meta name="google-site-verification" content="GOOGLE_VERIFICATION_PLACEHOLDER" />
   ```
   Replace `GOOGLE_VERIFICATION_PLACEHOLDER` with the token Google gave you.
4. `npm run build`, push to `master`, wait for Render to redeploy (~60s).
5. Click **Verify** in Search Console.
6. Submit the sitemap: in Search Console -> Sitemaps -> add `sitemap-index.xml`.

### 2. Bing Webmaster Tools verification

1. Go to https://www.bing.com/webmasters and add `https://playship.pro`. Bing will offer to import directly from Search Console — if you've already done step 1, that's the fastest path and you can skip the rest of this section.
2. Otherwise, pick **Meta tag** verification. Bing returns a key for `msvalidate.01`.
3. In `src/layouts/Layout.astro`, replace `BING_VERIFICATION_PLACEHOLDER` with that key.
4. Build and push. Click **Verify**.
5. Submit the same sitemap (`sitemap-index.xml`).

### 3. Validate the structured data

After deploy:

- https://search.google.com/test/rich-results — paste `https://playship.pro` and confirm all four schemas parse (Service, LocalBusiness, FAQPage, WebSite).
- https://validator.schema.org — same URL, looks for raw JSON-LD errors.
- https://cards-dev.twitter.com/validator — confirm Twitter renders the large image.
- https://www.opengraph.xyz or Facebook's Sharing Debugger — confirm OG metadata.

### 4. Optional follow-ups (not done in this pass)

- Replace the placeholder OG image with a designed 1200x630 PNG if you want something prettier than text-on-paper.
- Once you have testimonials, add a `Review` / `AggregateRating` block under the Service schema (Google requires real, verifiable reviews — don't fake this).
- If you ever target a second locale, expand the `hreflang` block.

## Build verification

```
$ npm run build
✓ 2 page(s) built in 1.25s
$ grep -c application/ld+json dist/index.html
4
$ ls -la dist/og-image.png
-rw-r--r-- 25165  dist/og-image.png
```

All four JSON-LD blocks, the PNG, the verification placeholders, `summary_large_image`, and `robots index,follow` are confirmed present in the built HTML.
