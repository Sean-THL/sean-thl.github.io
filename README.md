# Sean Lin — GitHub Pages portfolio

A clean academic portfolio inspired by https://ycsun2113.github.io/, independently implemented with no third-party template code. Left sidebar, publications, image-and-text project rows, work experience, research, education, résumé links, responsive layout and dark mode.

## Publish at https://sean-thl.github.io/

1. Create a public repository named **sean-thl.github.io** in your **Sean-THL** account. If one already exists, review and merge these files rather than replacing its contents blindly.
2. Upload the contents of this folder into the repository root (not the outer folder). Include `.github/workflows/pages.yml` and `.nojekyll`.
3. Open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Push to `main`. The **Build and deploy portfolio** workflow builds and publishes the site. The repository name alone does not publish it; wait for a successful workflow run.

Alternatively, because the generated HTML is included, choose **Deploy from a branch → main → /(root)**. With branch deployment, regenerate HTML after changing `content.json`.

## Edit your content

- Edit **content.json** using GitHub's pencil button. Commit the change to `main`; the Actions workflow regenerates every page and publishes automatically.
- `about`: biography paragraphs. `news`: dated updates. `publications`: titles, authors and manuscript status. `projects`: cards and detailed project paragraphs. `experience` and `research`: work and research entries. `education`, `skills`, and `resumes`: the remaining homepage sections.
- Use paired Markdown-style markers such as `**important text**` to bold specific words in narrative text and bullet points.
- Upload a project image to `assets/`, then add `image`, `alt`, `caption`, `width`, `height` to its project record. `image` is just the filename; use `fit: contain`.
- Keep the online-reference note on the micro-soft aerial robotics image.
- Change design in `style.css`; interactions in `script.js`; page structure in `build.py`.
- Rebuild locally with `python3 build.py`, then preview with `python3 -m http.server 8000` and visit http://localhost:8000.

## Content notes

Publication statuses use the supplied résumés and are marked **in preparation**. Update those fields when a public paper URL/status is confirmed. TEG-SLAM attribution follows the corrected project description. BR-MPPI, Apple, Bellwether, Soft Pneumatic Robotics and Pneumatic Micro-muscle Modeling are excluded from the project catalog; Apple and Bellwether remain under employment.

The supplied Apple image is a product reference, and the Bellwether image is a concept rendering. Neither represents a photograph of the individual engineering work. Some projects await images.

This static GitHub Pages version uses GitHub content editing and deployment. It does not include the previous site's server-based inline editor or its draft database.

## Files

`index.html`, `projects/*/index.html`: generated static pages; `content.json`: editable content; `build.py`: standard-library generator; `assets/`: supplied project media and résumés; `.github/workflows/pages.yml`: GitHub Pages deployment.
# sean-portfolio
