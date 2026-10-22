"""Build a dependency-free academic portfolio for GitHub Pages."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'content.json').read_text())
e=lambda x:html.escape(str(x),quote=True)
def head(title,prefix=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Sean Lin — robotics, safe control, perception, and mechanical engineering at the University of Michigan."><title>{e(title)} | Sean Lin</title><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}script.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a>'''
def sidebar(prefix=''):
 return f'''<aside class="sidebar"><a class="portrait-link" href="{prefix}index.html"><img class="portrait" src="{prefix}assets/sean-profile.jpg" alt="Sean Lin in London" width="180" height="180"></a><h1>Sean Lin</h1><p class="full-name">Tzu-Hsiang Lin</p><p class="position">Graduate Student<br>Mechanical Engineering (Robotics)<br><strong>University of Michigan</strong></p><nav aria-label="Main navigation"><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#news">News</a><a href="{prefix}index.html#publications">Publications</a><a href="{prefix}index.html#projects">Selected Projects</a><a href="{prefix}index.html#experience">Experience</a><a href="{prefix}assets/Sean-Lin-Robotics-Resume.pdf">CV / Résumé ↗</a></nav><div class="socials"><a href="{e(d['github'])}" aria-label="GitHub"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1-.2-1.8-.8-2.3 3-.3 6-1.5 6-5.6 0-1.2-.4-2.3-1.1-3.1.1-.8.1-1.8-.5-3-1.8-.1-3.2.9-3.8 1.3a13 13 0 0 0-6.8 0C7.4 4.9 6 3.9 4.2 4c-.6 1.2-.6 2.2-.5 3C3 7.8 2.6 8.9 2.6 10.1c0 4.1 3 5.3 6 5.6-.5.5-.8 1.3-.8 2.3v4"/></svg></a><a href="{e(d['linkedin'])}" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7m0-10v.1M11 17v-7m0 3c0-4 6-4 6 0v4"/></svg></a><a href="mailto:{e(d['email'])}" aria-label="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></svg></a></div><a class="email" href="mailto:{e(d['email'])}">{e(d['email'])}</a><p class="location">Ann Arbor, Michigan</p><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false">Dark mode</button></aside>'''
def footer():
 return '<footer>© 2026 Tzu-Hsiang (Sean) Lin<span>Robotics · Control · Perception · Design</span></footer>'
def picture(x,prefix=''):
 if not x.get('image'):return '<div class="image-placeholder">Project image forthcoming</div>'
 note=f'<span class="image-note">{e(x["image_note"])}</span>' if x.get('image_note') else ''
 return f'<img src="{prefix}assets/{e(x["image"])}" alt="{e(x.get("alt",x.get("title",x.get("name","Project image"))))}" loading="lazy">'+note
parts=[head('Robotics & Mechanical Engineering'),'<div class="layout">',sidebar(),'<main id="main">']
parts+=['<section id="about"><h2>About</h2>']+[f'<p>{e(p)}</p>' for p in d['about']]
parts+=['<p class="interest-line"><strong>Research interests</strong> &nbsp; Safe control · Aerial robotics · 3D perception · SLAM · Mechanical design</p></section>']
parts+=['<section id="publications"><h2>Publications &amp; Manuscripts</h2>']
for p in d['publications']:
 parts.append(f'<article class="media-row publication"><a class="media" href="projects/{e(p["project"])}/">'+picture(dict(p,image_note='Online reference image · Illustrative only') if p['project']=='micro-soft-robotics' else p)+f'</a><div><h3><a href="projects/{e(p["project"])}/">{e(p["title"])}</a></h3><p class="authors">{e(p["authors"]).replace("T.-H. Lin","<strong>T.-H. Lin</strong>")}</p><p class="status">{e(p["status"])}</p><a class="text-link" href="projects/{e(p["project"])}/">Project details ↗</a></div></article>')
parts+=['</section><section id="projects"><div class="heading-row"><h2>Selected Projects</h2><span id="project-count">'+str(len(d['projects']))+' projects</span></div><div class="filters" role="group" aria-label="Filter projects"><button data-filter="all" aria-pressed="true">All projects</button><button data-filter="robotics" aria-pressed="false">Robotics</button><button data-filter="mechanical" aria-pressed="false">Mechanical / aerospace</button></div>']
for p in d['projects']:
 parts.append(f'<article class="media-row project-row" data-category="{e(p["group"])}"><a class="media" href="projects/{e(p["slug"])}/">'+picture(p)+f'</a><div><p class="category">{e(p["category"])}</p><h3><a href="projects/{e(p["slug"])}/">{e(p["name"])}</a></h3><p class="project-affiliation">{e(p["affiliation"])}</p><p class="project-time">{e(p["time"])}</p><p>{e(p.get("card_summary",p["summary"]))}</p><div class="tags">'+''.join(f'<span>{e(t)}</span>' for t in p.get('keywords',p['tags']))+'</div></div></article>')
parts+=['</section><section id="experience"><h2>Experience</h2><div class="experience-list">']
for p in d['experience']:
 logo='apple-logo.svg' if p['company']=='Apple' else 'bellwether-logo.png'
 parts.append(f'<article class="media-row experience-row"><div class="media"><img src="assets/{e(p["image"])}" alt="{e(p["company"])} product reference image" loading="lazy"></div><div><p class="dates">{e(p["dates"])}</p><h3 class="company"><img src="assets/{logo}" alt="" aria-hidden="true">{e(p["company"])}</h3><p class="role">{e(p["role"])}</p><ul>'+''.join(f'<li>{e(b)}</li>' for b in p['bullets'])+'</ul></div></article>')
parts+=['</div></section><section id="research"><h2>Research Experience</h2>']
for title,context,date,summary in [('DASC Lab','University of Michigan · Prof. Dimitra Panagou','Jan 2026–present','Safety-critical multi-agent aerial autonomy, hardware deployment and perception-aware exploration.'),('Zoetic Robotics Lab','University of Michigan · Prof. Cameron Aubin','Sep 2025–present','Pneumatic micro-actuation, high-speed experimental measurement and bio-inspired aerial robotics.'),('SAM Lab','University of Michigan · Prof. Steven Ceron','Sep 2025–present','Magnetic microrobot locomotion, experimental systems and high-level field control.'),('Advanced Robotics Laboratory','University of Nottingham','Aug 2024–Jun 2025','Bio-inspired manta-ray locomotion, pneumatic actuator fabrication, kinematic modeling and finite-element analysis.')]:
 parts.append(f'<article class="compact-entry"><div><h3>{e(title)}</h3><p>{e(context)}</p><p>{e(summary)}</p></div><span>{e(date)}</span></article>')
parts+=['</section><section id="education"><h2>Education</h2><article class="compact-entry"><div><h3>University of Michigan</h3><p>M.S. Mechanical Engineering · Robotics</p><p>Ann Arbor, Michigan</p></div><span>2025–2027</span></article><article class="compact-entry"><div><h3>University of Nottingham</h3><p>B.Eng. (Hons) Mechanical Engineering</p><p>GPA 3.90 / 4.00 · Top 1%</p></div><span>2021–2025</span></article></section><section id="resume"><h2>Résumé</h2><div class="resume-links"><a href="assets/Sean-Lin-Robotics-Resume.pdf">Robotics résumé ↗</a><a href="assets/Sean-Lin-Mechanical-Resume.pdf">Mechanical engineering résumé ↗</a></div></section>',footer(),'</main></div></body></html>']
(ROOT/'index.html').write_text(''.join(parts))
for p in d['projects']:
 target=ROOT/'projects'/p['slug'];target.mkdir(parents=True,exist_ok=True)
 body=head(p['name'],'../../')+'<div class="layout">'+sidebar('../../')+'<main id="main" class="project-detail"><a class="back-link" href="../../index.html#projects">← All projects</a><p class="category">'+e(p['category'])+'</p><h2>'+e(p['name'])+'</h2><p class="detail-lead">'+e(p['summary'])+'</p>'
 if p.get('image'):body+='<figure class="detail-image">'+picture(p,'../../')+f'<figcaption>{e(p.get("caption",""))}</figcaption></figure>'
 body+='<section><h3>Project overview</h3>'+''.join('<p>'+e(t)+'</p>' for t in p['paragraphs'])+'</section>'+footer()+'</main></div></body></html>'
 (target/'index.html').write_text(body)
print(f'Built homepage and {len(d["projects"])} project pages.')

# Academic homepage ordering and lightweight News section.
import re
home=ROOT/'index.html';text=home.read_text()
sections={m[1]:m[0] for m in re.finditer(r'<section id="([^"]+)">.*?</section>',text,re.S)}
news='<section id="news"><h2>News</h2><ul class="news">'+''.join('<li><span class="news-date">'+e(n['date'])+'</span><span>'+e(n['text'])+'</span></li>' for n in d.get('news',[]))+'</ul></section>'
exp=sections['experience'].replace('</section>',sections['research'].replace('<section id="research"><h2>Research Experience</h2>','<h3 class="subsection-title">Research Experience</h3>').replace('</section>','')+'</section>')
projects=sections['projects'];projects=re.sub(r'<div class="filters".*?</div>','',projects,count=1,flags=re.S);projects=re.sub(r'<span id="project-count">.*?</span>','',projects,count=1)
projects=re.sub(r'<p class="category">.*?</p>','',projects,flags=re.S)
skills='<section id="skills"><h2>Skills</h2><dl class="skills"><dt>Robotics &amp; Control</dt><dd>ROS / ROS2, SLAM, state estimation, MPC, CBF, trajectory planning</dd><dt>Programming &amp; Simulation</dt><dd>Python, C++, MATLAB, Simulink, PX4, Gazebo, Isaac Sim</dd><dt>Mechanical Design</dt><dd>SolidWorks, CATIA, NX, CFD, FEA, Abaqus, manufacturing and prototyping</dd></dl></section>'
start=text.index('<section id="about">');end=text.index('<footer>',start)
text=text[:start]+sections['about']+news+sections['publications']+exp+projects+sections['education']+skills+sections['resume']+text[end:]
home.write_text(text)
