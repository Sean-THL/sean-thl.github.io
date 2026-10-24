"""Build the dependency-free portfolio from content.json."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
escape = lambda value: html.escape(str(value), quote=True)


def inline(value):
    """Escape content, then support Markdown-style links and **bold** spans."""
    text = escape(value)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def page_head(title, prefix=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(data['meta_description'])}"><title>{escape(title)} | {escape(data['short_name'])}</title><link rel="stylesheet" href="{prefix}style.css?v=20261024-3"><script src="{prefix}script.js?v=20261024-2" defer></script></head><body><a class="skip" href="#main">Skip to content</a>'''


def sidebar(prefix=""):
    nav = f'<a href="{prefix}about/">Beyond Research</a><a href="{prefix}index.html#research">Research</a><a href="{prefix}projects/">Projects</a><a href="{prefix}assets/Sean-Lin-Robotics-Resume.pdf">CV</a>'
    previous_role = f'<p class="previous-role"><a href="{prefix}{escape(data["previous_role_url"])}">{escape(data["previous_role"])}</a></p>'
    return f'''<aside class="sidebar"><a class="portrait-link" href="{prefix}index.html"><img class="portrait" src="{prefix}assets/{escape(data['profile_image'])}" alt="{escape(data['profile_image_alt'])}" width="200" height="200"></a><h1>{escape(data['short_name'])}</h1><p class="full-name">{escape(data['name'])}</p><p class="position"><span>{escape(data['role'])}</span><span>{escape(data['program'])}</span><strong>{escape(data['university'])}</strong></p>{previous_role}<nav aria-label="Main navigation">{nav}</nav><div class="socials"><a href="{escape(data['github'])}" aria-label="GitHub"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1-.2-1.8-.8-2.3 3-.3 6-1.5 6-5.6 0-1.2-.4-2.3-1.1-3.1.1-.8.1-1.8-.5-3-1.8-.1-3.2.9-3.8 1.3a13 13 0 0 0-6.8 0C7.4 4.9 6 3.9 4.2 4c-.6 1.2-.6 2.2-.5 3C3 7.8 2.6 8.9 2.6 10.1c0 4.1 3 5.3 6 5.6-.5.5-.8 1.3-.8 2.3v4"/></svg></a><a href="{escape(data['linkedin'])}" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7m0-10v.1M11 17v-7m0 3c0-4 6-4 6 0v4"/></svg></a><a href="mailto:{escape(data['email'])}" aria-label="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></svg></a></div><a class="email" href="mailto:{escape(data['email'])}">{escape(data['email'])}</a><p class="location">{escape(data['location'])}</p><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false">Dark mode</button></aside>'''


def footer():
    return f'<footer>{escape(data["footer"]["copyright"])}<span>{escape(data["footer"]["tagline"])}</span></footer>'


def picture(item, prefix="", cover=False):
    if cover and item.get("cover_video"):
        poster_name = item.get("video_poster", item.get("cover_image", item.get("image", "")))
        poster = f' poster="{prefix}assets/{escape(poster_name)}"' if poster_name else ""
        return f'<video class="project-cover-video" autoplay muted loop playsinline preload="metadata"{poster} aria-hidden="true"><source src="{prefix}videos/{escape(item["cover_video"])}" type="video/mp4"></video>'
    image_name = item.get("cover_image", item.get("image")) if cover else item.get("image")
    if not image_name:
        return '<div class="image-placeholder">Project image forthcoming</div>'
    note = f'<span class="image-note">{escape(item["image_note"])}</span>' if item.get("image_note") else ""
    zoom = f' class="cover-zoom" style="--cover-zoom:{float(item["cover_zoom"]):.2f}"' if cover and item.get("cover_zoom") else ""
    alt = item.get("cover_alt", item.get("alt", item.get("title", item.get("name", "Project image")))) if cover else item.get("alt", item.get("title", item.get("name", "Project image")))
    return f'<img{zoom} src="{prefix}assets/{escape(image_name)}" alt="{escape(alt)}" loading="lazy">{note}'


def gallery_item(item, prefix="../../"):
    caption = f'<figcaption>{escape(item["caption"])}</figcaption>' if item.get("caption") else ""
    if item.get("video"):
        poster = f' poster="{prefix}assets/{escape(item["poster"])}"' if item.get("poster") else ""
        media = f'<video controls muted loop playsinline preload="metadata"{poster}><source src="{prefix}videos/{escape(item["video"])}" type="video/mp4"></video>'
    else:
        media = f'<img src="{prefix}assets/{escape(item["image"])}" alt="{escape(item.get("alt", "Project media"))}" loading="lazy">'
    return f'<figure>{media}{caption}</figure>'


def logo_entry(item, css_class="entry-row"):
    bullets = "<ul>" + "".join(f"<li>{inline(line)}</li>" for line in item.get("bullets", [])) + "</ul>" if item.get("bullets") else ""
    summary = f'<p class="entry-summary">{inline(item["summary"])}</p>' if item.get("summary") else ""
    detail = f'<p class="entry-detail">{inline(item["detail"])}</p>' if item.get("detail") else ""
    company_href = f'companies/{escape(item["company_slug"])}/' if item.get("company_slug") else ""
    logo = f'<img src="assets/{escape(item["logo"])}" alt="{escape(item["logo_alt"])}" loading="lazy">'
    logo = f'<a href="{company_href}" aria-label="View project work at {escape(item["name"])}">{logo}</a>' if company_href else logo
    name = f'<a href="{company_href}">{escape(item["name"])}</a>' if company_href else escape(item["name"])
    prompt = f'<a class="company-project-hint" href="{company_href}">View project work from this company →</a>' if company_href else ""
    return f'''<article class="{css_class}"><div class="logo-frame">{logo}</div><div class="entry-content"><div class="entry-heading"><div><h3>{name}</h3><p class="role">{escape(item['role'])}</p>{prompt}</div><span class="dates">{escape(item['dates'])}</span></div>{detail}{summary}{bullets}</div></article>'''


def ordered_projects():
    projects_by_slug = {project["slug"]: project for project in data["projects"]}
    ordered_slugs = data.get("project_order", [])
    projects = [projects_by_slug[slug] for slug in ordered_slugs if slug in projects_by_slug]
    projects += [project for project in data["projects"] if project["slug"] not in ordered_slugs]
    return projects


def project_card(project, prefix="", href_prefix="projects/"):
    tags = "".join(f"<span>{escape(tag)}</span>" for tag in project["keywords"])
    categories = " ".join(project["categories"])
    time = f'<p class="project-time">{escape(project["time"])}</p>' if project.get("time") else ""
    href = f'{href_prefix}{escape(project["slug"])}/'
    return f'<article class="media-row project-row" data-categories="{escape(categories)}"><a class="media" href="{href}" aria-label="View {escape(project["name"])} project">{picture(project, prefix, cover=True)}</a><div><h3><a href="{href}">{escape(project["name"])}</a></h3><p class="project-affiliation">{escape(project["affiliation"])}</p>{time}<p>{inline(project.get("card_summary", project["summary"]))}</p><div class="tags">{tags}</div></div></article>'


def project_section(title, content):
    if not content:
        return ""
    if isinstance(content, list):
        body = '<ul class="contribution-list">' + "".join(f'<li>{inline(item)}</li>' for item in content) + '</ul>'
    else:
        body = f'<p>{inline(content)}</p>'
    return f'<section class="project-evidence"><h3>{escape(title)}</h3>{body}</section>'


parts = [page_head("Robotics & Mechanical Engineering"), '<div class="layout">', sidebar(), '<main id="main">']
parts += ['<section id="about"><h2>About</h2>'] + [f'<p>{inline(text)}</p>' for text in data["about"]]
parts += [f'<p class="interest-line"><strong>Research interests</strong> &nbsp; {escape(" · ".join(data["research_interests"]))}</p></section>']
parts += ['<section id="news"><h2>News</h2><ul class="news">'] + [f'<li><span class="news-date">{escape(item["date"])}</span><span>{inline(item["text"])}</span></li>' for item in data["news"]]
parts += ['</ul></section><section id="research"><h2>Research &amp; Publications</h2>']
for publication in data["publications"]:
    authors = escape(publication["authors"]).replace("T.-H. Lin", "<strong>T.-H. Lin</strong>")
    publication_href = escape(publication.get("url", f'projects/{publication["project"]}/'))
    external = ' target="_blank" rel="noopener noreferrer"' if publication.get("url") else ""
    parts.append(f'<article class="media-row publication"><a class="media" href="{publication_href}"{external}>{picture(publication)}</a><div><h3><a href="{publication_href}"{external}>{escape(publication["title"])}</a></h3><p class="authors">{authors}</p><p class="status">{escape(publication["status"])}</p></div></article>')
project_filters = (("all", "All"), ("control", "Control & Planning"), ("perception", "Perception & Sensing"), ("mechatronics", "Mechanical Design & Mechatronics"))
filter_buttons = "".join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{escape(label)}</button>' for key, label in project_filters)
featured_slugs = data.get("featured_projects", [])
projects_by_slug = {project["slug"]: project for project in data["projects"]}
featured_projects = [projects_by_slug[slug] for slug in featured_slugs if slug in projects_by_slug]
parts += [f'</section><section id="projects"><div class="heading-row"><h2>Selected Projects</h2><span id="project-count">{len(featured_projects)} projects</span></div><div class="filters" role="group" aria-label="Filter selected projects">{filter_buttons}</div>']
parts += [project_card(project) for project in featured_projects]
parts += [f'<p class="all-projects-link"><a href="projects/">View all {len(data["projects"])} projects →</a></p>']
parts += ['</section><section id="experience"><h2>Experience</h2><h3 class="subsection-title">Work Experience</h3>'] + [logo_entry(item, "entry-row experience-row") for item in data["experience"]]
parts += ['<h3 class="subsection-title">Research Experience</h3>'] + [logo_entry(item, "entry-row research-row") for item in data["research"]]
parts += ['</section><section id="education"><h2>Education</h2>'] + [logo_entry(item, "entry-row education-row") for item in data["education"]]
parts += ['</section><section id="skills"><h2>Skills</h2><dl class="skills">']
for skill in data["skills"]:
    parts.append(f'<dt>{escape(skill["category"])}</dt><dd>{escape(skill["items"])}</dd>')
parts += ['</dl></section><section id="resume"><h2>Résumé</h2><div class="resume-links">'] + [f'<a href="assets/{escape(item["file"])}">{escape(item["label"])} ↗</a>' for item in data["resumes"]]
parts += ['</div></section>', footer(), '</main></div></body></html>']
(ROOT / "index.html").write_text("".join(parts), encoding="utf-8")

about_target = ROOT / "about"
about_target.mkdir(parents=True, exist_ok=True)
about_body = page_head("About", "../") + '<div class="layout">' + sidebar("../") + '<main id="main" class="about-page"><header class="personal-header"><p class="about-eyebrow">Beyond engineering</p><h2>' + escape(data["name"]) + '</h2>' + "".join(f'<p>{inline(text)}</p>' for text in data.get("personal_about", [])) + '</header>'
for index, interest in enumerate(data.get("personal_interests", [])):
    images = "".join(f'<img src="../assets/{escape(image["file"])}" alt="{escape(image["alt"])}" loading="lazy">' for image in interest.get("images", []))
    about_body += f'<section class="personal-interest{" reverse" if index % 2 else ""}"><div class="personal-interest-media count-{len(interest.get("images", []))}">{images}</div><div class="personal-interest-copy"><h3>{escape(interest["title"])}</h3><p>{inline(interest["summary"])}</p></div></section>'
other_interests = "".join(f'<li>{escape(interest)}</li>' for interest in data.get("other_interests", []))
about_body += '<section class="other-interests"><h3>Other interests</h3><ul>' + other_interests + '</ul></section>' + footer() + '</main></div></body></html>'
(about_target / "index.html").write_text(about_body, encoding="utf-8")

projects_target = ROOT / "projects"
projects_target.mkdir(parents=True, exist_ok=True)
all_projects = ordered_projects()
catalog = page_head("Projects", "../") + '<div class="layout">' + sidebar("../") + '<main id="main" class="project-catalog"><header class="catalog-header"><p class="about-eyebrow">Complete portfolio</p><div class="heading-row"><h2>Projects</h2><span id="project-count">' + str(len(all_projects)) + ' projects</span></div><p>Research and engineering work across planning and control, perception, and mechanical design.</p></header><div class="filters" role="group" aria-label="Filter all projects">' + filter_buttons + '</div>'
catalog += "".join(project_card(project, "../", "") for project in all_projects)
catalog += footer() + '</main></div></body></html>'
(projects_target / "index.html").write_text(catalog, encoding="utf-8")

for company in data.get("company_projects", []):
    target = ROOT / "companies" / company["slug"]
    target.mkdir(parents=True, exist_ok=True)
    company_body = page_head(f'{company["name"]} project work', "../../") + '<div class="layout">' + sidebar("../../") + '<main id="main" class="company-detail"><a class="back-link" href="../../index.html#experience">← Work experience</a><header class="company-detail-header"><img src="../../assets/' + escape(company["logo"]) + '" alt="' + escape(company["logo_alt"]) + '"><div><p class="about-eyebrow">Selected internship work</p><h2>' + escape(company["name"]) + '</h2><p class="company-detail-role">' + escape(company["role"]) + ' · ' + escape(company["dates"]) + '</p><p>' + inline(company["intro"]) + '</p><p class="company-confidentiality">' + inline(company["note"]) + '</p></div></header><section class="company-project-list"><h3>Project work</h3>'
    for index, project in enumerate(company["projects"], 1):
        company_body += f'<article class="company-project"><span>{index:02d}</span><div><h3>{escape(project["title"])}</h3><p>{inline(project["summary"])}</p></div></article>'
    company_body += '</section>' + footer() + '</main></div></body></html>'
    (target / "index.html").write_text(company_body, encoding="utf-8")

for project in data["projects"]:
    target = ROOT / "projects" / project["slug"]
    target.mkdir(parents=True, exist_ok=True)
    body = page_head(project["name"], "../../") + '<div class="layout">' + sidebar("../../") + '<main id="main" class="project-detail"><a class="back-link" href="../">← All projects</a><p class="category">' + escape(project["category"]) + '</p><h2>' + escape(project["name"]) + '</h2><p class="detail-lead">' + inline(project["summary"]) + '</p>'
    if project.get("image"):
        body += '<figure class="detail-image">' + picture(project, "../../") + f'<figcaption>{escape(project.get("caption", ""))}</figcaption></figure>'
    if project.get("gallery"):
        body += '<div class="project-gallery">' + "".join(gallery_item(item) for item in project["gallery"]) + '</div>'
    if project.get("research_question"):
        body += project_section("Research question", project.get("research_question"))
        body += project_section("My contribution", project.get("my_contribution"))
        body += project_section("Results & current status", project.get("results_status"))
    else:
        body += '<section><h3>Project overview</h3>' + "".join(f'<p>{inline(text)}</p>' for text in project["paragraphs"]) + '</section>'
    body += footer() + '</main></div></body></html>'
    (target / "index.html").write_text(body, encoding="utf-8")

print(f'Built homepage, {len(data["projects"])} project pages and {len(data.get("company_projects", []))} company pages.')
