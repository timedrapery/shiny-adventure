# Reader hosting and Brickwall styling

## Website structure

The reader remains in this repository.
The Brickwall Unlimited homepage remains in `timedrapery/cuddly-octo-waffle`.

- Homepage: <https://brickwallunlimited.com/>
- Reader domain: <https://readings.brickwallunlimited.com/>
- Previous reader address: <https://timedrapery.github.io/shiny-adventure/>

The owner confirmed that the reader domain is ready.
The homepage link now uses the reader domain.
GitHub Pages redirects the previous reader address after custom-domain activation.
The execution network could not reach the domain for an independent live check.

## Shared appearance

The reader uses the Brickwall white wordmark, black and white brick photograph,
charcoal surfaces, Arial text, and white links.
The brick photograph appears in the masthead.
The reading panel has a plain background.
Navigation, search, glossary panels, feedback forms, and print styles remain available.
Reading routes use full-width rows rather than narrow columns.
Page headings appear within the left navigation instead of a second sidebar.
The text has a bounded line length, generous line spacing, and separated list items.
The Brickwall stylesheet URL includes a content hash to avoid stale cached layouts.
After a stylesheet change, update its hash in `mkdocs.yml`.
The translations and editorial attribution are unchanged.

The presentation files are:

- `../overrides/main.html`: shared masthead and links
- `../reader-src/stylesheets/brickwall.css`: reader colors and layout
- `../reader-src/assets/brickwall/`: local wordmark, photograph, icon, and licenses
- `../mkdocs.yml`: palette, assets, template directory, and canonical reader URL

The wordmark and photograph come from the Brickwall website repository.
Their source notices are included with the copied assets.
The photograph comes from three.js under its MIT License.
The wordmark uses DejaVu Sans outlines with the included font notice.

## Activate the reader domain

Repository changes do not configure the GitHub Pages custom-domain setting.
This site uses a custom GitHub Actions workflow.
A CNAME file alone does not configure its domain.

1. Open this repository's Settings, then Pages.
2. Enter `readings.brickwallunlimited.com` under Custom domain.
3. Save the setting before adding the DNS record.
4. In Cloudflare DNS, add this record:

| Field | Value |
| --- | --- |
| Type | CNAME |
| Name | readings |
| Target | timedrapery.github.io |
| Proxy status | DNS only |
| TTL | Auto |

The target is a hostname, with no repository path.
Keep the existing root, www, and email records.
Wait for GitHub's domain check and certificate provisioning.
Enable Enforce HTTPS in GitHub Pages when available.
Test the reader home, a nested sutta page, search, glossary, and EPUB download.
Then update the Brickwall homepage link to the new reader domain.

See [GitHub's custom domain procedure](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## Builds and checks

The existing deployment workflow remains the publication gate.
It runs full repository verification, reader generation checks, a strict MkDocs
build, rendered browser checks, and EPUB validation before deployment.
Changes to `overrides/` also trigger this workflow.

Use these local checks after presentation changes:

```bash
python scripts/run_checks.py
mkdocs build --strict
pnpm install --frozen-lockfile
pnpm test:a11y
```

Examine desktop, phone, keyboard, 200% zoom, and print output.
Keep translation changes separate from presentation changes.
