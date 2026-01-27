# Personal Academic Homepage

A clean, academic-style personal homepage built with pure HTML, CSS, and vanilla JavaScript. No frameworks required. Perfect for researchers, academics, and professionals who want a modern, responsive personal website.

## Features

✨ **Clean & Academic Design** - Minimalist white background with professional layout
📱 **Fully Responsive** - Two-column layout on desktop, single column on mobile
⚡ **No Dependencies** - Pure HTML, CSS, and vanilla JavaScript
🎯 **Smart Navigation** - Automatic section highlighting using IntersectionObserver
🔗 **Easy Customization** - Simple placeholder system for quick personalization
📄 **GitHub Pages Ready** - Works out of the box with GitHub Pages

## Directory Structure

```
your-username.github.io/
├── index.html           # Main HTML file
├── .nojekyll           # Tells GitHub Pages to not use Jekyll
├── README.md           # This file
├── assets/
│   ├── style.css       # All styling (responsive, no dependencies)
│   ├── main.js         # Navigation highlighting with IntersectionObserver
│   ├── avatar.jpg      # Your profile picture (replace this!)
│   └── cv.pdf          # Your CV file (optional, replace this!)
```

## Setup Instructions

### Step 1: Create Your GitHub Pages Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. **Repository name:** `<your-username>.github.io` (replace `<your-username>` with your actual GitHub username)
   - For example: if your username is `john-doe`, the repo should be named `john-doe.github.io`
4. Make sure the repository is **Public**
5. Click "Create repository"

### Step 2: Clone Your Repository

```bash
git clone https://github.com/<your-username>/<your-username>.github.io.git
cd <your-username>.github.io
```

### Step 3: Add the Homepage Files

Copy all the files from this template:
- `index.html`
- `.nojekyll`
- `README.md`
- `assets/` directory (with `style.css`, `main.js`, `avatar.jpg`, `cv.pdf`)

### Step 4: Add Your Profile Picture

1. Prepare your profile picture (JPG or PNG format, recommended size: 200x200px or larger, preferably square)
2. Save it as `avatar.jpg` in the `assets/` folder
3. If you use a different filename or format (e.g., `avatar.png`), update line in `index.html`:
   ```html
   <img src="assets/avatar.jpg" alt="Profile Picture" class="avatar">
   ```

### Step 5: Add Your CV (Optional)

1. Prepare your CV as a PDF file
2. Save it as `cv.pdf` in the `assets/` folder
3. If you use a different filename, update the link in `index.html`:
   ```html
   <a href="assets/cv.pdf" target="_blank" class="social-link">CV</a>
   ```

### Step 6: Customize Your Content

Edit `index.html` and replace all placeholder text:

#### Profile Section (Left Sidebar):
```html
<h1 class="name">YOUR_NAME</h1>                    <!-- Replace with your name -->
<p class="affiliation">YOUR_AFFILIATION</p>        <!-- Replace with your university/organization -->
<p class="bio">A brief one-line introduction about yourself.</p>  <!-- Your tagline -->

<p><strong>Location:</strong> Your_City, Country</p>
<p><strong>Email:</strong> <a href="mailto:your.email@example.com">your.email@example.com</a></p>

<a href="https://github.com/yourname" target="_blank" class="social-link">GitHub</a>
```

#### Content Sections:
Replace the placeholder content in each section:
- **About Me** - `<section id="home" class="section-home">`
- **New Papers** - `<section id="papers" class="section-papers">`
- **Experience** - `<section id="experience" class="section-experience">`
- **Honors and Awards** - `<section id="honors" class="section-honors">`
- **Publications** - `<section id="publications" class="section-publications">`

**Timeline Item Example:**
```html
<li class="timeline-item">
    <span class="date">2024</span>
    <span class="content">
        Your achievement or position title
        <br>
        <em>Organization or Company Name</em>
    </span>
</li>
```

### Step 7: Push to GitHub

```bash
git add .
git commit -m "Initial commit: Set up personal homepage"
git push -u origin main
```

### Step 8: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/<your-username>/<your-username>.github.io`
2. Click the **Settings** tab
3. In the left sidebar, click **Pages**
4. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` and `/(root)`
   - Click **Save**
5. Wait a few minutes for GitHub to build and deploy your site
6. Your homepage will be live at: `https://<your-username>.github.io`

## Local Development

To test your homepage locally before pushing to GitHub:

### Option 1: Using Python (Recommended)

```bash
cd <your-username>.github.io

# Python 3.x
python -m http.server 8000

# Python 2.x
python -m SimpleHTTPServer 8000
```

Then open your browser to `http://localhost:8000`

### Option 2: Using Node.js

```bash
# Install http-server globally (one-time)
npm install -g http-server

# Run in your project directory
http-server
```

### Option 3: Using VS Code

Install the "Live Server" extension and right-click `index.html` → "Open with Live Server"

## Customization Tips

### Change Colors

Edit `assets/style.css` and modify:
```css
a {
    color: #0066cc;      /* Link color */
}

.nav-link.active {
    color: #0066cc;      /* Active nav color */
    border-bottom-color: #0066cc;
}
```

### Add More Sections

1. Add a new navigation link in the navbar:
```html
<a href="#mysection" class="nav-link" data-section="mysection">My Section</a>
```

2. Add a new section in the main content:
```html
<section id="mysection" class="section-mysection">
    <h2>My Section</h2>
    <!-- Your content here -->
</section>
```

3. Add CSS for the new section if needed:
```css
.section-mysection {
    margin-bottom: 50px;
    scroll-margin-top: 80px;
}
```

### Adjust Layout Width

Edit `assets/style.css`, find `.container`:
```css
.container {
    max-width: 1200px;  /* Change this value */
}
```

### Change Font

Edit `assets/style.css`, find the `body` selector:
```css
body {
    font-family: 'Your Font Name', sans-serif;
}
```

## Browser Support

- Chrome/Edge (all modern versions)
- Firefox (all modern versions)
- Safari 12+
- Mobile browsers (iOS Safari, Chrome Android)

## Performance

- No external dependencies or CDNs
- Minimal CSS and JavaScript
- Fast loading time
- Mobile-optimized

## Navigation Highlighting

The homepage uses the **Intersection Observer API** to automatically highlight the navigation item corresponding to the section currently in view. The `main.js` file handles this automatically—no configuration needed!

## Troubleshooting

### Styles not loading on GitHub Pages?
- Make sure you're using relative paths (e.g., `assets/style.css`)
- Clear your browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
- Check that all files are committed and pushed to GitHub

### Images not showing?
- Verify the image path is correct: `assets/avatar.jpg`
- Ensure the image file exists in the `assets/` folder
- Use relative paths, not absolute URLs

### Navigation not highlighting?
- Make sure `main.js` is loaded correctly
- Open browser DevTools (F12) and check for JavaScript errors in the Console tab

### GitHub Pages not deploying?
- Make sure you pushed to the `main` branch (or your default branch)
- Check Settings → Pages for deployment status
- Verify that `.nojekyll` file exists in the root directory

## License

Free to use and modify for personal use.

## Questions or Issues?

For detailed GitHub Pages setup, visit: https://docs.github.com/en/pages

---

**Happy blogging! 🚀**
