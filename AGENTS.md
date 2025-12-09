# AGENTS.md

This repository is automated by two agents:

- Gemini CLI (via GitHub Actions): edits recipes in small batches following `GEMINI.md`.
- Jules (GitHub App): picks up issues labeled `jules` and opens PRs autonomously.

## Gemini CLI

- Workflow: `.github/workflows/gemini-recipes.yml`
- Inputs: batch size, whether to run embeddings.
- Obeys: `GEMINI.md` style, licensing and sources.
- Only edit files listed by the batch selector output.

Recommended settings:

```json
{"model":"gemini-1.5-flash","temperature":0.2}
```

Project variables/secrets:

- `vars.GCP_PROJECT_ID`, `vars.GCP_LOCATION` (only needed when using Vertex AI auth)
- `secrets.GEMINI_API_KEY` (for Gemini API from AI Studio)

## Jules

- Install the Jules GitHub App and grant access to this repo.
- Create an issue using "Jules Task" template or add the `jules` label to any issue.
- Jules will plan, run, and open a PR. Keep tasks small and clear.

Include context for Jules:

- Goal, acceptance criteria, constraints (languages, licenses), file paths.
- Link to prior PRs or examples.

### Jules Task History

#### Completed Tasks

- ✅ **Security fixes** (Dec 9, 2025): Updated `js-yaml` (3.14.1 → 3.14.2) and `glob` to fix CVE-2025-64718 (moderate) and CVE-2025-64756 (high severity).

#### In Progress

- 🔄 **Translation Script Fix** (Issue #37): Update Gemini model to `gemini-2.5-flash` for better free tier support
- 🔄 **Astro Site Structure** (Issue #38): Create basic `site/` directory with Astro configuration files
- 🔄 **GitHub Pages Deployment** (Issue #36): Add workflow for automatic Astro site deployment (blocked by #38)

#### Failed Tasks (Limitations Identified)

- ❌ **Recipe Translation** (Issue #32, PR #34): Jules cannot create multiple new files due to environment restrictions. Error: "Unable to create files".
  - **Recommendation**: Create file structure manually first, then let Jules handle content translation.
  
- ❌ **GitHub Pages with Astro/Svelte** (Issue #33, PR #35): Empty PR with "known build issue". Task too complex for single iteration.
  - **Recommendation**: Break into smaller sub-tasks (setup Astro → add Svelte → configure GitHub Actions).

### Best Practices for Jules (Updated Dec 9, 2025)

#### ✅ What Works Well

1. **Single-file modifications**: Editing existing files with clear instructions
2. **Specific line changes**: "Change line X from Y to Z"
3. **Configuration updates**: Updating constants, config values, dependencies
4. **Bug fixes**: Well-defined errors with specific solutions
5. **Provided content**: Copy-paste exact file contents in issue description

#### ❌ What Doesn't Work

1. **Multiple new files**: Creating 5+ new files in one task fails
2. **Complex scaffolding**: Framework setup (Astro + Svelte + Actions)
3. **Ambiguous tasks**: "Set up authentication system"
4. **Large refactors**: Restructuring entire codebases
5. **Research-heavy**: Tasks requiring exploration and decisions

#### 📋 Issue Template for Success

```markdown
## Goal
[One sentence: what should be accomplished]

## Context
[Why this is needed, what problem it solves]

## Acceptance Criteria
- [ ] Specific measurable outcome 1
- [ ] Specific measurable outcome 2

## File(s) to Create/Modify
- `path/to/file.ext` (line X or new file)

## Specific Changes Needed
[Exact content or code snippets]

## Testing
[How to verify the changes work]

## Important Constraints
- [Language requirements]
- [Don't modify X]
- [Must preserve Y]
```

#### 🎯 Task Breakdown Strategy

**Bad** (too broad):
> "Create a recipe translation system with API integration and batch processing"

**Good** (atomic tasks):

1. Issue: "Fix script to use gemini-2.5-flash model (1 line change)"
2. Issue: "Create site/ directory structure (5 config files, exact content provided)"
3. Issue: "Add GitHub Actions workflow (1 file, exact YAML provided)"

#### 🔗 Dependencies Between Issues

When tasks depend on each other:

- Mark with `**BLOCKED BY**: Issue #XYZ` in description
- Jules will wait or inform you if dependency isn't met
- Order: structure → content → automation

### New Issues (Dec 9, 2025)

Following improved practices, created:

- **#37**: Translation script model fix (atomic, 1-line change)
- **#38**: Astro site structure (5 files, all content provided)
- **#36**: GitHub Pages workflow (1 file, blocked by #38)

## Batch selection

- Script: `automation/queue/select_batch.py`
- Reads `recipes_metadata.json` and supports filters.
- Excludes already-processed files (e.g., `recipes_vectors.jsonl`).

Example:

```bash
python automation/queue/select_batch.py \
  --metadata recipes_metadata.json \
  --processed recipes_vectors.jsonl \
  --count 10 \
  --output-files automation/queue/selected_files.txt
```

## Embeddings

- Default batch vectorization script: `.github/scripts_ts/vectorize_selected.ts` (embeds only selected files).
- You can switch to Vertex AI (text-embedding-004) later using a Python script and WIF auth.

## Conventions

- Branch protection: changes go via PR. Actions and agents create PRs.
- Keep prompts short. Limit batches to avoid rate limits.
- Favor idempotent scripts and append-only JSONL artifacts.

## Auto-approve & Auto-merge

- PRs labeled `automation` are auto-approved by a bot and auto-merge is enabled (squash).
- Self-approval by the author is blocked by GitHub; the bot handles approval when the label is present.
- Auto-merge only completes when all required checks are green, respecting branch protection.
- Workflows: `/.github/workflows/auto-merge.yml` and PR-side helper if needed.
