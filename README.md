# Junjie Nian Personal Homepage

This repository contains the source code for Junjie Nian's personal academic homepage. It is a fully static website built with plain HTML, CSS, and vanilla JavaScript, and is designed to be hosted directly on GitHub Pages without any build step.

## Overview

The site is organized as a small multi-page portfolio:

- `index.html` – landing page with hero section and navigation cards
- `academic.html` – publications, new papers, and honors
- `projects.html` – research projects, technical work, and side explorations
- `experience.html` – research experience and education background

## Tech Stack

- **HTML5** for page structure
- **CSS3** for layout, typography, and responsive design
- **Vanilla JavaScript** for page interactions
- **Google Fonts** (`Cormorant Garamond`, `Karla`) for typography
- **GitHub Pages** for deployment

## Repository Structure

```text
.
├── README.md
├── index.html
├── academic.html
├── projects.html
├── experience.html
└── assets/
    ├── avatar.jpg
    ├── cv.html
    ├── cv.pdf
    ├── landing.css
    ├── landing.js
    ├── main.js
    ├── pages.css
    ├── shared.css
    └── *.png / *.jpg / *.gif
```

## Styling and Behavior

- `assets/shared.css` contains shared styles used across all pages
- `assets/landing.css` styles the homepage hero and navigation cards
- `assets/pages.css` styles the internal content pages
- `assets/landing.js` controls landing-page interactions
- `assets/main.js` powers scroll/reveal behaviors on the content pages

In addition, `projects.html` includes a small inline lightbox script for enlarging project images.

## Local Preview

Because the site is fully static, you can preview it with any simple local server.

### Python

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

### VS Code

You can also use the **Live Server** extension and open `index.html` from the workspace root.

## Content Maintenance

### Update profile information

Edit `index.html` to update:

- name and Chinese name
- affiliation and short bio
- contact links such as GitHub, email, and CV
- hero text and homepage entry points

### Update academic content

Edit `academic.html` to maintain:

- new papers
- honors and awards
- publication list
- advisor and lab information

### Update projects

Edit `projects.html` to maintain:

- project descriptions
- screenshots and media under `assets/`
- tags and external links

### Update experience

Edit `experience.html` to maintain:

- research experience
- education timeline
- cross-links to publications and projects

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

No bundler, package manager, or static-site generator is required.

## Customization Notes

- Keep all asset references relative so the site works correctly on GitHub Pages
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

- Make sure the latest changes are pushed to the published branch
- Check **Settings** → **Pages** for the deployment status
- Wait a minute or two for GitHub Pages to finish rebuilding

## License

This repository is intended for personal homepage source management. Reuse the structure if helpful, but please replace personal content, publications, and assets with your own before publishing.
