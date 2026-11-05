# Cup1 – B2B Sourcing & Custom Packaging

Cup1 is a B2B sourcing company that resells custom-printed paper food packaging (cups, lids, bowls, boxes, plates)
under its own name. We source from checked Asian factories and handle samples, artwork, inspection and shipping.
Worldwide B2B; **USA & Canada is the launch market.**

> **Your brand. Every cup. Fully documented.**

This repository is the **single source of truth**: decisions, status, research, brand files and deliverables.
It is used from two computers (home and office), and Claude on both reads the same `CLAUDE.md`, so both work the same way.

## Start here
| File | Read it for |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | How Claude works on this project (three experts, rules) |
| [`DECISIONS.md`](DECISIONS.md) | What is decided, what the owner still has to decide |
| [`PROJECT-STATUS.md`](PROJECT-STATUS.md) | Where every work area stands, open tasks |

## Folders
```
CLAUDE.md · DECISIONS.md · PROJECT-STATUS.md · README.md
experts/        business-expert.md · web-developer.md · marketing-expert.md
01-business/    business model, supplier audits & master list, USA/Canada sourcing pack, policies/
02-website/     website plan, design teardown (later: site code)
03-marketing/   brand strategy & decisions, competitor research
brand/          logo/ (svg, png, favicon, palette, guidelines), design-system/, brand sheet, homepage blueprint
deliverables/   PDF / DOCX / XLSX copies for sharing
scripts/        rebuild the Excel model, styled Word files, logo files
archive/        superseded files (reference only)
```

## Daily workflow (home PC and office PC)
**Before you start working:**
```bash
cd "<your Cup1 folder>"
git pull
claude            # Claude reads CLAUDE.md automatically; type STATUS for a summary
```
**When you finish:**
```bash
git add -A
git commit -m "Short description of what changed"
git push
```
Rules: always `git pull` before you start and `git push` when you stop, so the other computer is never behind.
If Git reports a conflict, don't guess: ask Claude to help resolve it.

## First-time setup on a new computer
1. Install [Git](https://git-scm.com/) and [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) (or the Claude desktop app).
2. Accept the GitHub collaborator invite (office account) and sign in to GitHub on that computer.
3. Clone:
   ```bash
   git clone https://github.com/ain9900/cup1-business-ops.git "Cup1 B2B"
   ```
4. Open that folder in Claude and type **STATUS**.

## Keeping both Claudes the same
- **Claude Code / Cowork with the folder:** nothing extra; `CLAUDE.md` + `experts/` load from the repo.
- **claude.ai Projects (each account):** paste `CLAUDE.md` into the project instructions and upload `DECISIONS.md`,
  `PROJECT-STATUS.md`, `01-business/business-model.md` and the expert files as project knowledge. Re-upload after big changes,
  or ask Claude to sync them.
- Personal skills (e.g. `logo-favicon-designer`) live in each Claude account, not in Git: add them on both accounts if needed.
- claude.ai artifact links in the docs are private to the owner's account until shared.

## Notes
- Keep this repo **private** (supplier prices, margins, client data).
- Never commit passwords, API keys or `.env` files (see `.gitignore`).
