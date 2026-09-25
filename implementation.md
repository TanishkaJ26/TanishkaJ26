# GitHub Profile README — Implementation Guide

**Owner:** Tanishka Jangir (`TanishkaJ26`)
**Deliverables:** `README.md`, `.github/workflows/snake.yml`
**Theme:** Security-engineer terminal. Palette: `#0D1117` background, `#00E5A0` accent, `#C9D1D9` text.

---

## 1. How a Profile README Works

GitHub shows a repository's `README.md` at the top of your profile page when **all** of these are true:

| Requirement | Value |
|---|---|
| Repo name | Exactly your username: `TanishkaJ26` (the case must match) |
| Visibility | **Public** |
| File location | `README.md` at the repo **root** |
| Default branch | `main` |

---

## 2. Final Repository Structure

```
TanishkaJ26/                      ← repo name = username
├── README.md                     ← the profile page
└── .github/
    └── workflows/
        └── snake.yml             ← GitHub Action (generates the snake SVGs)

Branch: output (auto-created by the Action)
├── github-snake.svg              ← light-mode snake
└── github-snake-dark.svg         ← dark-mode snake
```

---

## 3. Setup — Step by Step

### Option A: Browser only (no Git)

1. Go to **github.com → + → New repository**.
2. Set the name to `TanishkaJ26`. GitHub will show a "✨ special repository" notice.
3. Select **Public** and tick **Add a README file**. Then click **Create repository**.
4. Open `README.md` and click ✏️ **Edit**. Replace everything with the contents of the provided `README.md`, then **Commit changes**.
5. Click **Add file → Create new file**. Type the file name `.github/workflows/snake.yml`; the slashes create the folders automatically. Paste in `snake.yml` and commit.
6. Open the **Actions** tab. If prompted, enable workflows. Then choose **Generate contribution snake → Run workflow → Run**.
7. Wait about 1 minute for a ✅. Refresh your profile at `github.com/TanishkaJ26`.

### Option B: Git CLI

```bash
# 1. Create the empty public repo "TanishkaJ26" on github.com first (no README), then:
mkdir TanishkaJ26 && cd TanishkaJ26
git init -b main

# 2. Add files
cp /path/to/README.md .
mkdir -p .github/workflows
cp /path/to/snake.yml .github/workflows/snake.yml

# 3. Commit & push
git add .
git commit -m "feat: terminal-themed profile README + snake workflow"
git remote add origin https://github.com/TanishkaJ26/TanishkaJ26.git
git push -u origin main
```

Pushing to `main` triggers the workflow automatically, because it has an `on: push` trigger.

### Required Actions permission (only if the workflow fails with a 403)

Go to **Repo → Settings → Actions → General → Workflow permissions**. Select **Read and write permissions** and click **Save**. The workflow already declares `permissions: contents: write`, but some accounts have a stricter default.

---

## 4. Pre-Publish Checklist

- [ ] **Spotlight card:** Replace `https://github.com/TanishkaJ26/spotlight` with the real repo URL, and the Live `#` with the deployed URL.
- [ ] **WanderLust card:** Replace `https://github.com/TanishkaJ26/wanderlust` with the real repo URL, and the Live `#` with the deployed URL.
- [ ] **Placeholders:** Search the file for `TODO`. Nothing should remain.
- [ ] **LinkedIn link:** Confirm it resolves to `linkedin.com/in/tanishka-jangir`.
- [ ] **Pipeline section:** Remove any project you don't want shown as in progress.
- [ ] **Personal data:** Confirm no phone number or personal address is included (intentionally excluded).
- [ ] **Rendering:** Check the profile in both light and dark mode (GitHub → Settings → Appearance).
- [ ] **Mobile:** Check it in the GitHub mobile app. Tables stack vertically, which is expected.

---

## 5. Section-by-Section Reference

| # | Section | What it is | Powered by | Needs setup? |
|---|---|---|---|---|
| 1 | Header wave | Animated gradient banner with name and tagline | `capsule-render.vercel.app` | No |
| 2 | Typing line | Four rotating headline lines | `readme-typing-svg.demolab.com` | No |
| 3 | Badges | LinkedIn, Email, Profile views | `shields.io`, `komarev.com` | No |
| 4 | `whoami` | Short intro and internship call-to-action | Plain Markdown | No |
| 5 | `nmap` scan | Tech stack as an nmap service-detection output | Plain code block | No |
| 6 | Skill icons | Two rows of 10 icons | `skillicons.dev` | No |
| 7 | Featured Deployments | Two-column project cards (Spotlight, WanderLust) | HTML `<table>` + shields badges | **Yes** — real links |
| 8 | In the Pipeline | Colour-coded project status | ` ```diff ` highlighting | Keep updated |
| 9 | `git log` | Career timeline as a commit graph | Plain code block | Keep updated |
| 10 | Telemetry | Stats, top languages, streak, activity graph | See §7 | No (may rate-limit) |
| 11 | Packet Capture | Contribution snake, light/dark aware | `Platane/snk` Action | **Yes** — run Action |
| 12 | Footer | Motto and inverted wave | `capsule-render` | No |

### How the `diff` block colours work

In the "In the Pipeline" section, the first character of each line sets its colour:

| Prefix | Colour | Used for |
|---|---|---|
| `+` | Green | `[BUILDING]` — active work |
| `!` | Orange | `[RESEARCH]` / notes |
| `-` | Red | `[QUEUED]` — not started |

To promote a project, change its prefix and tag. For example, a finished project becomes `+ [SHIPPED]`.

---

## 6. Customisation Reference

### 6.1 Change the accent colour globally

Replace every `00E5A0` in `README.md` with your new hex code (no `#`). In VS Code, **Ctrl+H** does this in one pass. Also update `color_snake=#00E5A0` in `snake.yml`.

| Alternative palettes | Accent | Vibe |
|---|---|---|
| Matrix | `39FF14` | Classic hacker green |
| Cyber blue | `00B4FF` | Clean, corporate-security |
| Violet | `A78BFA` | Modern, softer |
| Amber | `FFB000` | Retro terminal |

### 6.2 Edit the typing lines

Lines live in the `lines=` parameter and are separated by `;`. Characters must be URL-encoded:

| Character | Encoded |
|---|---|
| space | `+` |
| `\|` | `%7C` |
| `&` | `%26` |
| `,` | `%2C` |
| `·` | `%C2%B7` |
| `@` | `%40` |

For example, to add the line "Open to Summer 2027 internships":
```
;Open+to+Summer+2027+internships
```
Other parameters you can change: `size` (font px), `pause` (ms between lines), `width` (widen it if lines get cut off), and `font` (any Google Font).

### 6.3 Edit skill icons

Icon IDs go in `?i=` as a comma-separated list, and `perline=` sets the wrap point. The full ID list is at `skillicons.dev`. Useful additions:

| Skill | ID |
|---|---|
| Docker | `docker` |
| AWS | `aws` |
| Redis | `redis` |
| Socket.io | `socketio` |
| FastAPI | `fastapi` |
| scikit-learn | `sklearn` |
| Postman | `postman` |
| VS Code | `vscode` |

### 6.4 Add a project card

Copy one `<td width="50%" valign="top"> … </td>` block. To keep two cards per row, open a new `<tr>` for the 3rd and 4th cards:
```html
  </tr>
  <tr>
    <td width="50%" valign="top"> …card 3… </td>
    <td width="50%" valign="top"> …card 4… </td>
  </tr>
```
Badge format: `https://img.shields.io/badge/<Label>-<HEX>?style=flat-square&logo=<simpleicons-slug>&logoColor=white`. Logo slugs come from `simpleicons.org`. In `<Label>`, `_` renders as a space and `--` renders as a literal `-`.

### 6.5 Update the `nmap` block

- Keep the columns aligned with **spaces, not tabs**, because GitHub renders tabs as 8 characters.
- `open` means you are proficient. `filtered` means you are learning it.
- To add a row, pick a plausible port: `6379` Redis, `27017` MongoDB, `9200` search, `2375` Docker.

### 6.6 Update the `git log` block

Add new milestones **at the top** and move `(HEAD -> main)` to the newest line. Hashes are decorative: any 7 hex characters work.

Verb conventions used:

| Verb | Meaning |
|---|---|
| `ship:` | A project was released |
| `feat:` | A role or experience |
| `lead:` | A leadership role |
| `init:` | A start point |
| `win:` | An award or hackathon win |
| `pub:` | A paper was published |

---

## 7. Stats Services & Reliability

| Card | Service | Reliability | Fallback |
|---|---|---|---|
| Stats + Top languages | `github-readme-stats.vercel.app` | ⚠️ Public instance is often rate-limited or shows errors | Self-host (below) |
| Streak | `streak-stats.demolab.com` | Generally stable | Self-host `DenverCoder1/github-readme-streak-stats` |
| Activity graph | `github-readme-activity-graph.vercel.app` | Occasionally slow | Remove the section |
| Snake | Your own Action | ✅ Fully under your control | — |

### Self-hosting github-readme-stats (free, about 5 minutes)

1. Fork `github.com/anuraghazra/github-readme-stats`.
2. Create a GitHub **Personal Access Token (classic)** with no scopes; the default read-only access is enough.
3. Go to **vercel.com → Add New → Project** and import the fork.
4. Add the environment variable `PAT_1 = <your token>` and deploy.
5. In `README.md`, replace `github-readme-stats.vercel.app` with `<your-project>.vercel.app` in both stats URLs.

**Note on `count_private=true`:** It only counts private contributions if **Settings → Public profile → "Include private contributions on my profile"** is enabled. On a self-hosted instance, it counts your private work when the PAT has `repo` scope.

---

## 8. The Snake Workflow Explained

```yaml
on:
  schedule: - cron: "0 */12 * * *"   # regenerates every 12h (UTC)
  workflow_dispatch:                   # manual "Run workflow" button
  push: branches: [main]               # regenerates whenever README changes
```

| Step | Action | Output |
|---|---|---|
| 1 | `Platane/snk@v3` reads your contribution graph | `dist/github-snake.svg` and `dist/github-snake-dark.svg` |
| 2 | `crazy-max/ghaction-github-pages@v4` force-pushes `dist/` | `output` branch |

The README loads the images from `raw.githubusercontent.com/TanishkaJ26/TanishkaJ26/output/…`. The `<picture>` tag then serves the dark or light version to match the viewer's GitHub theme.

**Snake palette options:** `palette=github` (light), `github-dark`, or `github-light`. You can override individual colours with `&color_snake=#HEX&color_dots=#c1,#c2,#c3,#c4,#c5`, where the dots run from the fewest to the most contributions.

---

## 9. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| README doesn't appear on profile | Repo name mismatch or private repo | Rename the repo to exactly `TanishkaJ26` and make it Public |
| Snake image broken | Action hasn't run yet | Actions → Run workflow; wait for ✅ |
| Action fails: `403` / `Permission denied` | Workflow token is read-only | Settings → Actions → General → Read and write permissions |
| Action fails: `output branch not found` | First-run race | Re-run the workflow once |
| Stats card shows an error or blank | Public instance rate-limited | Self-host (§7) or wait an hour |
| Top languages shows HTML/CSS/EJS first | Templates are counted as code | Add `&hide=html,css,ejs` to the top-langs URL |
| Typing SVG text cut off | `width` too small | Increase `width=620` to `700` or more |
| `nmap` / `git log` columns misaligned | Tabs or proportional font | Use spaces only; keep the block fenced |
| Old image still shows after an edit | GitHub image cache (camo) | Wait 5–30 minutes, or add `&v=2` to the image URL |
| Profile-views counter reset | Username param changed | Keep `username=TanishkaJ26` fixed |

---

## 10. Maintenance Cadence

| When | Do |
|---|---|
| A project ships | Move it from Pipeline to Featured Deployments; add a `ship:` line to `git log` |
| New role or internship | Add a `feat:` line to `git log`; update the `whoami` CTA |
| Paper submitted or published | Change `! [RESEARCH]` to `+ [PUBLISHED]`; add a `pub:` line with the DOI link |
| New skill used in a real project | Add it to `nmap` (as `open`) and to the skill icons |
| Each semester | Update the CGPA in `whoami` |
| Internship season ends | Change the CTA (e.g. to "Open to full-time roles from 2028") |

**Rule of thumb:** Only list a skill as `open` if a pinned repo demonstrates it. Recruiters and admissions reviewers click through, and a stack claim with no code behind it undermines your credibility more than a shorter list does.

---

## 11. Complementary Profile Settings

1. **Pin 4–6 repos** (Profile → Customize your pins): Spotlight, WanderLust, the scanner, and the trading engine once it's presentable.
2. Give **every pinned repo** a description, topics/tags, a live link in the About panel, and its own README with screenshots.
3. Fill in your **profile bio**: *"Full-stack dev · Network Security undergrad @ DSEU · Next.js / Node / Python"*.
4. Enable **Settings → Public profile → Include private contributions** so the contribution graph and snake reflect all your work.
5. Upload a **profile photo** that matches your LinkedIn one, so you're consistent across platforms.
