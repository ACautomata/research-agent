# TOOLS.md - Local Notes

This workspace mainly uses the `idea-generate` skill workflow.

## Conventions

- Default paper input folder: `paper/`.
- Default generated run folder: `idea-runs/YYYYMMDD-HHMMSS-<topic-slug>/`.
- Final human-readable output: `recommended-ideas.md`.
- Preserve intermediate `paper-context.md`, `paper-analysis.md`, and JSON idea files inside the run folder.

## Workspace Skill

- `idea-generate`: extracts paper context, synthesizes opportunity buckets, deduplicates candidate idea cards, validates required fields, and writes recommended ideas to Markdown.

