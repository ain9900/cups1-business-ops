# Cup1 Business Operations

Cup1 is a B2B sourcing and custom-printed food-service packaging business: cups, lids, bowls and takeaway boxes carrying the client's logo. It is made in certified Asian factories and delivered to café groups, chains and distributors in the **USA & Canada**.

> **Tagline:** Your brand. Every cup. Fully documented.

This repository is the single source of truth for the project: phase tracker, research, decisions, brand assets and deliverables. It is set up so any teammate, on any computer, can continue the work with Claude.

## Current status (5 Nov 2026)

| # | Phase | Status |
|---|---|---|
| 1 | Product Research | ✅ Done |
| 2 | Supplier Sourcing | 🟡 Research done; RFQs not yet sent |
| 3 | Branding | ✅ Completed, awaiting approval |
| 4–8 | Website → Clients → Onboarding → Fulfillment → Finance | ⏳ Not started |

Full detail: **[docs/00-master-phase-tracker.md](docs/00-master-phase-tracker.md)**

## Repository structure

```
cup1-business-ops/
├── CLAUDE.md                     # Project instructions Claude Code loads automatically
├── README.md
├── docs/
│   ├── 00-master-phase-tracker.md   # Project memory: read first, update at every phase change
│   ├── business-model-and-revenue.md
│   ├── suppliers-sourcing-links.md
│   ├── phases/                      # Phase-by-phase decisions and deliverable sources
│   └── research/                    # Competitor intelligence, website design teardown
├── brand/
│   ├── logos/                       # SVG + PNG logos
│   ├── design-system/               # tokens.json, brand book README, cover preview
│   ├── brand-sheet.png
│   └── homepage-blueprint.png
├── deliverables/                    # PDF / DOCX / XLSX for sharing
│   ├── phase2/ · phase3/ · research/
└── scripts/                         # Rebuild the Excel model and styled Word/PDF files
```

## Using this on another computer with Claude

1. Install [Git](https://git-scm.com/) and [Claude Code](https://docs.claude.com/en/docs/claude-code/overview).
2. Clone the repository:
   ```bash
   git clone <your-repo-url> cup1-business-ops
   cd cup1-business-ops
   claude
   ```
3. Claude reads `CLAUDE.md` automatically. Type **STATUS** to get a summary of where the project stands, or give the next command (e.g. **APPROVE**, **NEXT**).
4. When work is done, commit and push so the next person (and the next Claude) sees it:
   ```bash
   git add -A
   git commit -m "Phase 4: website plan"
   git push
   ```

**Using claude.ai instead of Claude Code:** upload `CLAUDE.md` into the project instructions and add `docs/00-master-phase-tracker.md` as a project file.

## Notes

- Links to claude.ai docs inside the files are private to their owner unless shared from claude.ai.
- Keep supplier prices and client data in this repo **private** (use a private GitHub repository).
