---
name: ny-policy-brief
description: Generate a serious, source-grounded HTML policy brief on any NYC or NYS issue — pulling from the cipher legislative graph (NYC), state Senate/Assembly archives, agency rule-makings, comptroller audits, and case law. Produces a print-ready, JS-enabled brief with TOC sidebar, expandable transcript blocks, hover-tooltip footnotes for every named person, and an administrative-and-case-law section. Use when the user invokes `/ny-policy-brief` with a topic (e.g. "Int 0894-2023" or "NYC composting law" or "NY housing voucher payment timing") or asks for a "policy brief" on a NYC/NYS topic. Output: `~/projects/<slug>/index.html` with sources/ alongside.
---

# Generate an NYC/NYS policy brief

This skill produces a research-grade HTML brief on a single NYC or New York State policy issue. Briefs are durable, source-grounded, and styled for print.

## When to use

- User invokes `/ny-policy-brief <topic>` or "/policy-brief".
- User asks for a "research brief," "policy brief," "writeup," or "report" on an NYC or NYS bill, law, agency action, court ruling, or policy fight.
- User references a specific bill ID (`Int 0704-2022`, `S.72`, `LL 64/2023`) or topic ("electronic rent payments," "CityFHEPS reform," "congestion pricing litigation").

## When **not** to use

- Federal-level questions (no cipher data, different sources entirely).
- News summaries — this skill is for legislative/regulatory deep dives, not breaking-news roundups.
- The user wants only a quick answer in chat. Briefs are heavy artifacts; ask before generating one if unclear.

## Output location

Always durable. Default: `~/projects/<topic-slug>/index.html`. Never `/tmp/` — the user has been burned by `/tmp` clearing.

Inside the project directory:
- `index.html` — the brief
- `sources/` — every primary source you fetched, saved as plain text or PDF for posterity

## Mandatory steps

### 1. Confirm scope before pulling sources

If the user gave a vague topic ("housing vouchers"), ask: which bill, law, or specific question? If the topic is concrete (a bill ID, a specific law, a specific court ruling), proceed.

### 2. Pull NYC legislative material from the cipher MCP server

The cipher MCP server (`mcp__cipher__*`) has NYC's complete legislative graph: bills, local laws, council members, committees, votes, hearings, attachments. Use it first.

Pattern:
- `search_nodes` for specific bill IDs (`"Int 0704-2022"`) or keywords.
- `get_node` for full metadata + edges + attachment list.
- `get_node_attachments` for hearing transcripts, committee reports, fiscal impact, bill text.
- `get_edges` for sponsorship, hearings, votes, ENACTED_AS relationships.
- `semantic_search` for natural-language exploration ("source-of-income discrimination housing voucher").

**Critical:** `get_node_attachments` output is often >100KB. When that happens it gets saved to a temp file. **Delegate the chunked read to a subagent** rather than blowing your own context. Brief the subagent: read in 36-line chunks, save each document to `sources/<short_name>.txt`, return a tight summary of key findings + verbatim load-bearing quotes.

### 3. Pull state legislative material

- NYS Senate: `https://www.nysenate.gov/legislation/bills/<year>/<bill>` — full bill text, sponsors, status, history. Use `WebFetch` then `WebSearch` for hearing pages.
- NYS Assembly: `https://nyassembly.gov/leg/?bn=<bill>` and `https://nyassembly.gov/comm/?id=<comm-id>&sec=hearings`.
- Joint hearings: `https://www.nysenate.gov/calendar/public-hearings/...` — these often 403 on direct WebFetch; use `WebSearch` with the hearing date as a fallback.
- LegiScan and the state's bill archive can fill gaps when official pages are slow.

### 4. Pull administrative law (always, when relevant)

This is non-negotiable for a serious brief — the legislative story is half-true without it.

**City admin law:**
- NYC Rules and rule-makings: `https://rules.cityofnewyork.us/`
- Title 68 RCNY: HRA / DSS rules. CityFHEPS lives in 68 RCNY ch. 10.
- The administrative code itself: `https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/`
- Mayoral office and agency directives: `nyc.gov/site/<agency>/news/...`

**State admin law:**
- 18 NYCRR (social services): `https://www.law.cornell.edu/regulations/new-york/18-NYCRR-Part-352` (Cornell LII has clean copies).
- OTDA directives (`ADM` series): `https://otda.ny.gov/policy/directives/`
- DOS rule-makings.
- HCR (Homes and Community Renewal): `https://hcr.ny.gov/`

**Note rule promulgation authority.** When city rules cite their statutory authority (e.g. "Sections 603 and 1043 of the City Charter and Sections 34, 56, 61, 62, 77, and 131-a of the New York Social Services Law"), include this in the brief — it shows where state law is the floor on city rule-making.

### 5. Pull case law (always, when relevant)

- NY Court of Appeals decisions: `https://www.nycourts.gov/ctapps/`
- Appellate Division decisions: NY Slip Opinion Service (`law.justia.com/cases/new-york/`).
- Trial-court matters: `https://iapps.courts.state.ny.us/nyscef/CaseSearch` (NYSCEF — public docket).
- For active cases: WebSearch the case name and check Gothamist, The City, City & State for plain-language coverage; cite the underlying decision when possible.

If a bill has been the subject of litigation (and many controversial ones have — voucher expansion, congestion pricing, rent stabilization, source-of-income discrimination cases), include a `<table class="timeline">` of the litigation history.

### 6. Pull oversight and audit material

- NYS Comptroller (DiNapoli): `https://www.osc.ny.gov/state-agencies/audits/` — file naming pattern is `sga-<year>-<n>n1.pdf`. Audits are often more concrete than committee reports.
- NYC Comptroller: `https://comptroller.nyc.gov/reports/`
- NYC IBO (Independent Budget Office): `https://www.ibo.nyc.ny.us/`
- Citizens Budget Commission: `https://cbcny.org/research`
- City Council Finance Division reports.
- Mayor's Management Report (MMR): `nyc.gov/site/operations/performance/mmr.page`

### 7. Process binary PDFs locally

`WebFetch` returns compressed PDF binary on `nyc.legistar1.com` and many state hearing PDFs. Don't try to parse it directly. Pattern:
1. WebFetch the PDF — it auto-saves to a tool-results path.
2. Run `pdftotext -layout <saved-pdf> /Users/<user>/projects/<slug>/sources/<doc>.txt`.
3. Read or grep the converted file.
4. For long transcripts, **delegate verbatim quote extraction to a subagent**. Tell the subagent specifically what to find: speaker exchanges, on-the-record numbers, council member questions, agency concessions. Demand verbatim quotes with speaker labels in `ALL CAPS` and approximate line numbers.

### 8. Verify URLs before linking

Never fabricate URLs. For named people:
- Council members: search for `<name> NYC council district <N> official` — landing page is at `council.nyc.gov/<slug>/` or `council.nyc.gov/district-<N>/`.
- State legislators: `nysenate.gov/senators/<slug>` or `nyassembly.gov/mem/<First-M-Last>`.
- City officials: NYC Green Book Online (`a856-gbol.nyc.gov`) and NYC.gov agency pages.
- Advocates: organization homepages (legalaidnyc.org, neighborhooddefender.org, hsunited.org, cccnewyork.org, neighborstogether.org, etc.).
- For private citizens / witnesses with no public profile: do not link. State this explicitly in the footnote.
- For people who've left their roles: link to the role announcement / press release archive that documents their tenure, not a personal URL that may not exist anymore.

## HTML structure (do not deviate without reason)

The output `index.html` is a single self-contained file. CSS embedded in `<head>`, JS embedded at end of `<body>`. No external dependencies. Print-ready.

### Required sections (in this order)

1. **Print row** — a single right-aligned `Print this brief` button at the very top.
2. **Header** — `<header class="report">` with kicker, h1, deck, and meta block (bill IDs, prime sponsor, compiled date).
3. **What it does** — plain-English summary of the law/rule/case in 2–4 paragraphs. Quote the operative statutory text in a `<blockquote>`.
4. **Why it mattered** — the motivating fact, ideally a verbatim hearing exchange. Use `<div class="exchange">` blocks for speaker dialogue.
5. **The fiscal logic** — `<div class="stat-grid">` with 2–4 dollar figures, sourced from testimony or fiscal impact statements.
6. **The agency context** — what the executive branch was already doing, what they said about the bill.
7. **How it moved through Council/Legislature** — `<table class="timeline">` of dates and actions.
8. **How it was narrowed/amended** — substantive changes between intro and enacted version.
9. **Companion bills / package** — if the bill was part of a package.
10. **Hearing transcripts: what was said** — `<details class="transcript">` blocks with verbatim quotes.
11. **The pattern** — broader cross-bill or cross-administration framing if relevant.
12. **Where the state fits in** — comptroller audits, state hearings, parallel state programs, state preemption.
13. **Administrative and case law** — RCNY/NYCRR rules, court history, parallel enforcement statutes.
14. **Why this is interesting** — 3–5 bullet observations the rest of the brief earned.
15. **Where things stand now** — current implementation status with verifiable numbers.
16. **People mentioned in this report** — `<section class="footnotes">` with one numbered entry per named person.
17. **Sources** — local files saved + primary URLs, organized by category.

### Required interactive features

- **Floating TOC sidebar**: `<nav class="toc">` fixed-position on the left, with one entry per H2. Active section highlighting via IntersectionObserver. "↑ Back to top" at the bottom of the TOC. Hide on viewports < 1180px.
- **Floating back-to-top FAB**: shown after 400px scroll on narrow viewports.
- **Person tooltips**: every named person wrapped as `<a class="person" href="#fn-<id>" data-fn="<id>">Name</a>`. JavaScript on `DOMContentLoaded` reads a `PEOPLE` dictionary and injects the tooltip content. Footnote section provides the no-JS fallback.
- **Expandable transcripts**: `<details class="transcript">` for each verbatim quote block. The first one has `open` so readers see at least one example without clicking.
- **Print button**: `<button class="print-btn" onclick="window.print()">Print this brief</button>` at the top right of the page.

### Required print stylesheet

`@media print` must:
- Hide `nav.toc`, `.toc-fab`, `.print-row`.
- Force `details.transcript[open]` style on all transcripts so they expand for paper.
- Print URLs after external links (`a[href^="http"]::after { content: " <" attr(href) ">"; }`) **except** for TOC links, footnote refs, and tooltip anchors (those would clutter the page).
- Use `@page { margin: 0.75in; }`.
- Remove tooltip dotted underlines from names.

### Required CSS palette (parchment + accent)

```
:root {
  --ink: #1a1a1a;
  --muted: #555;
  --rule: #d8d4cc;
  --bg: #fbfaf6;
  --accent: #6b3410;
  --quote-bg: #f3efe5;
}
```

Body font: `"Iowan Old Style", "Charter", Georgia, "Times New Roman", serif`. Sans-serif for kickers, captions, and TOC: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.

## Voice and editorial standards

- **Lead with verifiable facts.** Numbers from on-the-record testimony, dates from official action histories, dollar figures from fiscal impact statements or audits.
- **Verbatim quotes win over paraphrase.** Find the smoking-gun exchange and quote it. Reserve narrative for the connective tissue between quotes.
- **Flag what you don't know.** A "Where things stand now → What we still don't know" subsection is honest and useful.
- **No editorializing about partisanship.** Describe the legal architecture (vetoes vs. returned-unsigned; trial court vs. appellate ruling). Let the reader form opinions.
- **Names: full name on first reference; short form in subsequent uses; both wrapped as person spans where unambiguous.** Speaker labels inside `<div class="exchange">` dialog blocks should NOT be wrapped — they repeat too often and clutter the rhythm. Wrap names in narrative paragraphs and citation lines instead.

## Common pitfalls to avoid

- **Don't trust memory for current state.** Any project memory more than a few weeks old needs verification before claims are restated. Re-pull active facts (e.g. "is this person still in this role?", "is the case still pending?").
- **Don't fabricate URLs.** If you can't verify a profile page, don't link it. Footnote without a URL is fine.
- **Don't paraphrase agency testimony in a way that smooths over its concessions.** If a witness said "all the payments to private landlords are currently made by paper check," quote that. Don't write "the agency described existing payment mechanics."
- **Don't skip 18 NYCRR / state preemption analysis** when the bill carves out a state-funded payment stream. That carve-out is where the city/state jurisdictional seam lives.
- **Don't conflate a bill's first hearing with its enactment.** Track the full action history; the politics often live in the gap.
- **Don't omit cases.** If there's litigation, include it — even if only one paragraph. Readers need to know which provisions are operative and which are contested.

## Example output

The canonical example is `~/projects/electronic-rent-payments/index.html` (NYC LL 64/2023, the EFT-for-landlords bill). It demonstrates:
- 17 named-person tooltips with verified URLs
- Verbatim Abreu/Berry exchange from the 12/15/22 General Welfare hearing
- DiNapoli audit findings as state-level oversight echo
- LL 102 Vincent v. Adams litigation timeline
- HAVP as state-level parallel program
- 22-entry footnotes section
- Floating TOC + print button

## Implementation order

When generating a new brief from scratch, work in this order to avoid backtracking:

1. Decide topic and create durable directory: `mkdir -p ~/projects/<slug>/sources`
2. Pull cipher data first (cheapest, richest signal).
3. Pull state legislative pages and bill text.
4. Pull admin law (RCNY, NYCRR, agency rule-makings).
5. WebSearch for relevant case law and audits.
6. Convert any binary PDFs locally with `pdftotext`.
7. Delegate transcript extraction to a subagent if any single document is >50KB.
8. Compile a `transcript_highlights.md` working file.
9. Verify URLs for every name you'll cite.
10. Write the HTML in this order: header → core narrative → transcripts → state context → admin/case law → "where things stand now" → footnotes → sources.
11. Run a names-wrapper script that turns "Shaun Abreu" → `<a class="person" href="#fn-abreu" data-fn="abreu">Shaun Abreu</a>` everywhere outside `<a>`/`<script>`/`<style>`/footnotes section.
12. Validate: every `data-fn` resolves to a footnote ID; every `href="#sec-..."` resolves to a heading ID; no nested anchors.
13. Open in browser; test print preview.
