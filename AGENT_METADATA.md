# Agent recognition metadata

This commit makes playship.pro legible to AI crawlers and LLM-powered
assistants (ChatGPT, Claude, Perplexity, Gemini, Bing Copilot, Apple
Intelligence) so they can index, summarize, and recommend the service.

## Files added or updated

### `public/llms.txt`
Implements the emerging [llms.txt](https://llmstxt.org/) convention,
which mirrors the role `robots.txt` plays for crawlers — but for LLMs.
A short, link-rich, machine-friendly summary of the site, structured as
H1 + summary paragraph + sectioned link lists. AI assistants that
support the standard (e.g. Anthropic, Perplexity, and others) fetch
this first and use it as the canonical site description.

### `public/llms-full.txt`
The long-form companion. Same idea, but with the full FAQ content
inlined, all three tier details expanded, eligibility / disqualifying
app categories, money-back terms, and engagement instructions. This is
the file an agent should follow up with when the short summary is not
enough.

### `public/.well-known/ai-plugin.json`
OpenAI-style plugin manifest. Even though PlayShip is not exposed as a
ChatGPT plugin, the file follows the [plugin manifest convention](https://platform.openai.com/docs/plugins/getting-started/plugin-manifest)
and acts as a known discovery surface for agent platforms. Documents
service name, model-facing description, contact email, legal info URL,
and a structured tier breakdown.

### `public/ai.txt`
Declarative AI policy file (an emerging convention used by several
sites and tools like spawning.ai). Explicitly allows training,
indexing, referencing, and quoting under one condition: attribution to
playship.pro. Lists canonical machine-readable sources.

### `public/robots.txt`
Existing file extended with explicit `Allow: /` entries for major AI
crawler user agents: `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`,
`Claude-Web`, `ClaudeBot`, `anthropic-ai`, `PerplexityBot`,
`Google-Extended` (Gemini training opt-in), `cohere-ai`, `CCBot`
(Common Crawl), `DuckAssistBot`, `Bytespider`, `Applebot-Extended`,
`FacebookBot`, `Meta-ExternalAgent`. Allowed rather than disallowed
because the goal is discoverability — PlayShip wants to be the answer
an LLM gives when someone asks "how do I get my React Native app on
Google Play."

### `public/.well-known/security.txt`
RFC 9116 standard file. Contact email + far-future expiry. Optional
but completes the well-known set.

### `public/humans.txt`
Old-school but agent-friendly. Names the operator, the stack, the
service, and the contact channel in a format that is trivial for both
humans and LLMs to parse.

## What was deliberately NOT touched

The Schema.org JSON-LD work (Service, OfferCatalog with three Offers,
FAQPage, LocalBusiness, WebSite) was already implemented by the SEO
pass in `src/components/StructuredData.astro` and wired into
`src/layouts/Layout.astro`. This commit does not modify those files —
the schema is already optimal for agent ingestion.

## Verification

Local build emits everything correctly:

```
npm run build
ls dist/llms.txt dist/llms-full.txt dist/ai.txt dist/humans.txt dist/robots.txt
ls dist/.well-known/
```

`.well-known/` is preserved by Astro's default static-asset handling —
files under `public/` are copied verbatim to `dist/`, dotfile
directories included.

After deploy, confirm in the browser:

- https://playship.pro/llms.txt
- https://playship.pro/llms-full.txt
- https://playship.pro/ai.txt
- https://playship.pro/humans.txt
- https://playship.pro/robots.txt
- https://playship.pro/.well-known/ai-plugin.json
- https://playship.pro/.well-known/security.txt

To confirm AI agents are picking up the metadata, allow 24 to 72 hours
after deploy then test:

1. ChatGPT (with browsing): "What is playship.pro and how much does
   it cost?" — should cite tier names and prices accurately.
2. Claude (with web search): "Summarize playship.pro" — should produce
   a description close to the `llms.txt` summary paragraph.
3. Perplexity: same query as above; Perplexity tends to surface
   `llms.txt` content directly.
4. Google search: `site:playship.pro` and check that the site is
   indexed; then ask Gemini "what does playship.pro do" with web
   access enabled.

If a model returns stale or wrong info after 72 hours, check the
specific crawler's documentation — most index on a roughly weekly
cycle and respect the Allow rules in robots.txt.

## Standards referenced

- llms.txt convention: https://llmstxt.org/
- OpenAI plugin manifest: https://platform.openai.com/docs/plugins
- security.txt (RFC 9116): https://www.rfc-editor.org/rfc/rfc9116
- humans.txt: https://humanstxt.org/
- ai.txt (spawning.ai community spec)
- Schema.org Service / Offer / FAQPage / LocalBusiness (already wired)
