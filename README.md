# Junjie Nian Personal Homepage

Source for [Junjie Nian's academic homepage](https://junjienian.com), built with HTML, CSS, and vanilla JavaScript and published through GitHub Pages. The academic pages are plain static HTML; GitHub Pages uses Jekyll to render the synchronized exchange journal from Markdown.

## Overview

The site is organized as a small multi-page portfolio:

- `index.html` — biography and research focus, News, selected research, and exchange notes
- `academic.html` — complete publication list, honors, and awards
- `projects.html` — core research, related / adjacent research, and technical work
- `research/*.html` — project questions, methods, results, and paper / source links
- `experience.html` — research experience and education background
- `assets/cv.html` and `assets/cv.pdf` — browser and downloadable CV
- `exchange.md` and `exchange-pages/*.md` — generated journal chapters at `/exchange/` and `/exchange/N/`

## Tech Stack

- **HTML5** for page structure
- **CSS3** for layout, typography, and responsive design
- **Vanilla JavaScript** for page interactions
- **Google Fonts** (`Newsreader`, `DM Sans`) for typography
- **GitHub Pages / Jekyll** for publication and journal rendering
- **GitHub Actions / Python** for exchange-journal synchronization

## Repository Structure

```text
.
├── README.md
├── index.html
├── academic.html
├── projects.html
├── experience.html
├── exchange.md
├── exchange-pages/
├── _layouts/
│   └── exchange.html
├── _config.yml
├── scripts/
│   └── sync_exchange_notes.py
├── research/
│   └── *.html
└── assets/
    ├── avatar.jpg
    ├── cv.html
    ├── cv.pdf
    ├── landing.css
    ├── landing.js
    ├── main.js
    ├── pages.css
    ├── research.css
    ├── exchange.css
    ├── shared.css
    └── *.png / *.jpg / *.gif
```

## Styling and Behavior

- `assets/shared.css` contains shared styles used across all pages
- `assets/landing.css` styles the homepage biography, News, selected research, and exchange note
- `assets/pages.css` styles the internal content pages
- `assets/research.css` styles the project detail and technical-story pages
- `assets/exchange.css` styles the chapter navigation and journal reading layout
- The homepage uses native HTML navigation and an expandable News archive; it does not require JavaScript
- `assets/main.js` enables content-page reveal states and keyboard-accessible project image previews

The site uses an ivory background, burgundy accents, Newsreader headings, and DM Sans body text. Primary navigation is shared across pages; internal pages also provide section links and a skip-to-content link.

## Local Preview

Use any simple local server to preview the plain HTML pages.

### Python

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

This previews the academic pages and assets. It does not render the Markdown journal or Jekyll permalinks. Preview those with a Jekyll environment, or verify the generated pages after GitHub Pages builds them.

### VS Code

You can also use the **Live Server** extension and open `index.html` from the workspace root.

## Content Maintenance

### Update profile information

Edit `index.html` to update:

- name and Chinese name
- affiliation and short bio
- contact links such as GitHub, email, and CV
- research focus, selected research summaries, and paper / source links
- News and its expandable archive
- the compact exchange-journal entry point

### Update academic content

Edit `academic.html` to maintain:

- honors and awards
- publication list
- advisor and lab information

Keep publication titles, author order, contribution marks, dates, and venue/status information consistent with their sources. News belongs on the homepage; do not duplicate it as a separate “New Papers” list. The homepage selects work for orientation, while the Academic page keeps the complete publication record.

### Update projects

Edit `projects.html` to maintain:

- project descriptions
- screenshots and media under `assets/`
- tags and external links
- links to the corresponding project stories under `research/`

Keep the distinction between core research, related / adjacent research, and technical work. The core research entries link directly to their papers and source repositories; detail pages provide the fuller account of each project.

### Update experience

Edit `experience.html` to maintain:

- research experience
- education timeline
- cross-links to publications and projects

### Update the exchange journal

Edit the canonical [`myUCSDexchange/README.md`](https://github.com/JunjieNian/myUCSDexchange/blob/main/README.md). Do not maintain a second copy in this repository's generated chapter files.

`scripts/sync_exchange_notes.py` splits the source at numbered `## 第N章：...` headings, writes the first chapter to `exchange.md`, and writes later chapters to `exchange-pages/`. The displayed update time comes from the source README's latest commit.

The `Sync UCSD exchange notes` workflow runs on the `exchange-notes-updated` repository event, on a six-hour fallback schedule, and by manual dispatch. When generated content changes, it commits the reading copy and requests a GitHub Pages rebuild.

### Update images and files

Store static assets in `assets/`, then reference them with relative paths such as:

```html
<img src="assets/avatar.jpg" alt="Junjie Nian">
<a href="assets/cv.pdf" download>CV</a>
```

## Deployment

This repository is suitable for direct deployment on GitHub Pages:

1. Push changes to the default branch
2. Open the repository on GitHub
3. Go to **Settings** → **Pages**
4. Set the source to **Deploy from a branch**
5. Select the default branch and the repository root

No JavaScript bundler or npm build is required. Leave Jekyll enabled for the journal's Markdown, `_layouts/exchange.html`, and permalink generation. The `CNAME` file records the custom domain.

## Customization Notes

- Use paths appropriate to page depth: relative paths in standalone HTML and root-relative paths in the journal layout
- If you rename files in `assets/`, update every related reference in the HTML files
- Shared layout changes should usually go into `assets/shared.css`
- Page-specific tweaks should stay in `assets/landing.css` or `assets/pages.css`
- If you add a new page, remember to update the navbar links on the internal pages

## Troubleshooting

### Images not showing

- Verify the referenced path matches the actual file under `assets/`
- Keep image paths relative instead of using local absolute paths
- Make sure the filename case matches exactly, especially on GitHub Pages

### Interactions not working

- Confirm `assets/landing.js` or `assets/main.js` is loaded on the relevant page
- Open browser DevTools and check for JavaScript errors

### GitHub Pages not updating

- Confirm the latest changes reached the published branch
- Check the GitHub Pages build and deployment status
- Verify the published page after deployment finishes
- For journal changes, check the source README commit, synchronization workflow, generated chapter commit, and Pages build in that order

## License

This repository is intended for personal homepage source management. Reuse the structure if helpful, but please replace personal content, publications, and assets with your own before publishing.
