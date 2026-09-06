# Agalmic Research

Minimal static website for **Agalmic Research**, an open research programme studying abundance, epistemic scarcity, innovation as search, representation, coordination, and institutions after the cost of generating candidate knowledge falls.

## Design goals

- **Minimal:** no framework islands, no client JavaScript, no external font or UI dependency.
- **Open:** the website source is part of the publication record.
- **Durable:** plain Astro components and CSS, suitable for long-lived research pages.
- **Cheap to host:** static build with a GitHub Pages workflow included.
- **Expandable:** the current pages establish the research programme without committing to a CMS or complex publishing stack.

## Pages

- `/`: thesis, programme, Nemosyne relationship, operating model
- `/research`: six research tracks and research method
- `/publications`: publication architecture and initial paper sequence
- `/principles`: open-research, provenance, versioning and IP principles

## Local development

```sh
npm install
npm run dev
```

Build the production site:

```sh
npm run build
npm run preview
```

## GitHub Pages

The included `.github/workflows/deploy.yml` uses Astro's official GitHub Pages action. In the repository settings, set **Pages → Source** to **GitHub Actions**.

The site is configured for `https://agalmicresearch.org` and includes `public/CNAME`. Point the domain's DNS to GitHub Pages before enabling the custom domain. Remove `public/CNAME` and adjust `astro.config.mjs` if a different host is preferred.

## Content strategy

The website is the canonical index, not the only publication surface. Each research object can be projected into a working paper, journal article, public essay, policy brief, talk, model, dataset, or software artefact. Stable versions can be archived with persistent identifiers while the living source remains public and versioned here.

## Next sensible additions

Only add these when there is real content for them:

1. Markdown/content collections for papers and essays.
2. RSS when publication cadence begins.
3. DOI / archive metadata for stable research releases.
4. A small `people` or `about` page if collaborators join.
5. Search only after the corpus is large enough to need it.
