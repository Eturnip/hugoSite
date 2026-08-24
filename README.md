# Eturnip.com

This is the source for the Hugo-based personal blog that uses the Stack theme.

## Local development

Requirements:

- Hugo extended 0.157.0 or newer
- Go 1.24+ if you need module resolution updates

Typical local workflow:

```bash
hugo server --disableFastRender
```

The site is configured to use the Stack theme in [config/_default/hugo.toml](config/_default/hugo.toml), with the active content under [content](content).

## Deployment

This project is built in GitHub Actions using the extended Hugo binary and published to GitHub Pages via the workflow in [.github/workflows/hugo.yml](.github/workflows/hugo.yml).
