# Terms Navigation

The repository keeps `terms/major/` and `terms/minor/` flat on disk.

That is now a deliberate maintenance decision:

- flat directories keep record destinations predictable
- scripts can continue to treat the live dataset uniformly
- human navigation is handled by generated indexes rather than by adding
  subfolders that would complicate existing tooling and editorial conventions

## What Lives Here

`terms/` is the live lexicon, not a scratch area.

- `terms/major/`: policy-bearing entries that govern translation behavior
- `terms/minor/`: lighter live entries for stable, narrower, or supporting vocabulary

If a piece of vocabulary is still only a candidate from source extraction, keep
it in [`../candidates/`](../candidates/README.md) until the repository has made
an editorial decision about it.

Do not store these here:

- extracted candidate reports
- review packets
- speculative half-finished live entries
- generated browsing material

## Major Versus Minor

Use a major entry when the term needs governed translation behavior, such as:

- context-sensitive rendering
- doctrinal contrast management
- compound or formula inheritance
- explicit drift-prevention notes

Use a minor entry when the term is live and useful but does not yet need the
full rule-bearing surface.

## Navigation Layer

Use these generated indexes for browsing:

- [../docs/generated/major-term-index.md](../docs/generated/major-term-index.md)
- [../docs/generated/minor-term-index.md](../docs/generated/minor-term-index.md)

Regenerate them with:

```bash
python scripts/term_directory_navigation.py --write-docs
```

Check that they are current with:

```bash
python scripts/term_directory_navigation.py --check
```

For the field-level and policy expectations behind those records, see:

- [../docs/data-dictionary.md](../docs/data-dictionary.md)
- [../docs/term-entry-standard.md](../docs/term-entry-standard.md)
- [../STYLE_GUIDE.md](../STYLE_GUIDE.md)

For the distinction between live term data and generated browsing surfaces, see
[../docs/generated/generated-docs-guide.md](../docs/generated/generated-docs-guide.md).
