# MI Mythos

**Source-grounded policy briefs on New York City and New York State, on demand.**

Live site: [danielgolliher.github.io/mi-mythos](https://danielgolliher.github.io/mi-mythos/)

## What this is

New York governance runs on three layers — legislation, agency rule-making, and case law. Most coverage skips two of them.

MI Mythos is a tiny static web app that takes a policy question and emits a self-contained research prompt for Claude. The prompt embodies a methodology for building a research-grade brief that pulls from:

- The cipher MCP server (NYC's legislative graph: bills, votes, committee reports, hearing transcripts, attachments)
- New York State Senate and Assembly (bills, hearings, committee pages)
- City rules (Title 68 RCNY, the NYC Administrative Code, agency rule-makings)
- State rules (18 NYCRR, OTDA ADM directives, HCR rule-makings)
- Case law (Court of Appeals, Appellate Division, NYSCEF dockets)
- Oversight reports (NYS Comptroller audits, NYC IBO, Citizens Budget Commission)

The output is a single-file HTML brief with a floating table-of-contents sidebar, hover-tooltip footnotes for every named person, expandable verbatim transcript blocks, an administrative-and-case-law section, and a print button.

## How to use it

1. Open the [live site](https://danielgolliher.github.io/mi-mythos/).
2. Type a NYC or NYS policy question into the box — a bill ID (`Int 0704-2022`), a law (`LL 64/2023`), a topic ("source-of-income discrimination enforcement"), or a court case (`Vincent v. Adams`) all work.
3. Click **Generate brief prompt**. The page produces a self-contained research prompt.
4. Click **Copy to clipboard** and paste into Claude Code (terminal) or Claude.ai. Or click **Open in Claude.ai** to launch a new chat with the prompt prefilled.

If you have Claude Code installed locally and the `ny-policy-brief` skill registered, you can also invoke it directly with `/ny-policy-brief <topic>`.

## Repository layout

```
mi-mythos/
├── index.html              # the web app
├── skill/
│   └── SKILL.md            # the underlying methodology, formatted as a Claude Code skill
└── examples/
    ├── electronic-rent-payments/      # NYC LL 64/2023 (NYC/NYS scope)
    │   ├── index.html
    │   └── sources/                   # primary-source documents
    └── teacher-cba-student-outcomes/  # US teacher CBAs (national scope)
        └── index.html
```

## The example briefs

### [Electronic rent payments — NYC LL 64 of 2023](https://danielgolliher.github.io/mi-mythos/examples/electronic-rent-payments/)

NYC/NYS scope. The canonical demonstration of the skill applied to a single bill.

- Verbatim hearing exchanges (the December 2022 General Welfare Committee oversight session, including the Abreu/Berry "all the payments to private landlords are currently made by paper check" exchange)
- State Comptroller audit findings (DiNapoli, October 2024 + January 2026)
- The *Vincent v. Adams* litigation timeline (trial → First Department reversal → Mamdani Court of Appeals appeal)
- HAVP as a state-level parallel program
- 22 footnoted people, every one with a hover tooltip and a verified profile link
- A print button that produces a clean, paginated PDF

### [Teacher contracts and student outcomes](https://danielgolliher.github.io/mi-mythos/examples/teacher-cba-student-outcomes/)

National scope. Demonstrates the methodology adapted from a single-bill NYC focus to a broad national-policy question.

- NCTQ Teacher Contract Database synthesis (147 districts + 2 CMOs)
- Federal regulatory arc (Race to the Top → ESSA → COVID-era retreat)
- Four district case studies (DC IMPACT, Denver ProComp, Houston ASPIRE, NY Lederman)
- Active litigation: *Houston Federation of Teachers v. HISD* and *Lederman v. King*
- Calendar/instructional-time analysis (planning periods, school-day length, 30:1 ratio between districts on planning time)
- Teacher-protections analysis (tenure, LIFO, mutual consent, ATR)
- Red-vs-blue partisan breakdown of CBA policy moves
- **130 inline fact citations across 40 unique sources** — every numeric or specific claim has a hover tooltip showing the underlying source
- 10 footnoted people

## Installing the skill locally

If you use Claude Code on macOS or Linux:

```bash
git clone https://github.com/danielgolliher/mi-mythos.git
mkdir -p ~/.claude/skills/ny-policy-brief
cp mi-mythos/skill/SKILL.md ~/.claude/skills/ny-policy-brief/SKILL.md
```

Then in Claude Code: `/ny-policy-brief <your topic>`.

## License

MIT. See `LICENSE`.

## Credits

Built by [Daniel Golliher](https://maximumnewyork.com) — Maximum New York, Manhattan Institute Cities Fellow.

The `ny-policy-brief` skill was iteratively developed while assembling the LL 64 example, in collaboration with Claude (Anthropic).
