# Terms Navigation

The repository keeps `terms/major/` and `terms/minor/` flat on disk.

That is now a deliberate maintenance decision:

- flat directories keep record destinations predictable
- scripts can continue to treat the live dataset uniformly
- human navigation is handled by generated indexes rather than by adding
  subfolders that would complicate existing tooling and editorial conventions

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
