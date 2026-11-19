import os, sys, json

OUT = sys.argv[1]
EMAIL = "post@learnorg.global"
PHONE = "+47 48 28 70 00"
PHONE_TEL = "+4748287000"
ADDRESS = "Kongens gate 20A, 3717 Skien, Norway"

NAV = [
    ("Home", ""),
    ("About ILO", "about-us/"),
    ("Services", "services/", [
        ("Sensei Mentorship", "sensei-mentorship/"),
        ("Learning Culture", "learning-culture/"),
        ("E-learning Services", "e-learning-services/"),
        ("Courses", "courses/"),
    ]),
    ("Open Resources", "open-resources/", [
        ("Book Resources", "book-resources/"),
    ]),
    ("eStore", "estore/"),
    ("Events", None, [
        ("Upcoming Webinars", "upcoming-webinars/"),
        ("Workshops and Seminars", "workshops-and-webinars/"),
        ("Past Events", "past-events/"),
    ]),
]


def nav_html(r, current):
    items = []
    for entry in NAV:
        label, href = entry[0], entry[1]
        subs = entry[2] if len(entry) > 2 else None
        if subs:
            sub_active = any(h == current for _, h in subs) or href == current
            sub = "".join(
                f'<li><a href="{r}{h}"{" class=active" if h == current else ""}>{l}</a></li>' for l, h in subs
            )
            if href is not None:
                sub = f'<li><a href="{r}{href}"{" class=active" if href == current else ""}>All {label.lower()}</a></li>' + sub
            items.append(
                f'<li><button class="sub-toggle{" active" if sub_active else ""}" aria-expanded="false">{label}<span class="caret">▾</span></button>'
                f'<ul class="sub">{sub}</ul></li>'
            )
        else:
            items.append(f'<li><a href="{r}{href}"{" class=active" if href == current else ""}>{label}</a></li>')
    return "<ul>" + "".join(items) + "</ul>"


def page(path, title, description, body, lang="en"):
    depth = path.count("/")
    r = "../" * depth
    full_title = "Institute for Learning Organizations (ILO)" if not path else f"{title} | Institute for Learning Organizations"
    html = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{r}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css">
<script src="{r}assets/js/main.js" defer></script>
</head>
<body>
<div class="topbar"><div class="container">
  <a href="mailto:{EMAIL}">{EMAIL}</a>
  <a href="tel:{PHONE_TEL}">{PHONE}</a>
  <span>{ADDRESS}</span>
</div></div>
<header class="site-header"><div class="container">
  <a class="brand" href="{r or './'}">
    <span class="brand-mark">ILO</span>
    <span class="brand-text"><strong>Learn</strong><span>Institute for Learning Organizations</span></span>
  </a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="nav" aria-label="Main">
    {nav_html(r, path)}
    <a class="btn nav-cta" href="{r}contact/">Contact Us</a>
  </nav>
</div></header>
<main>
{body.replace("{r}", r)}
</main>
<footer class="site-footer"><div class="container">
  <div class="cols">
    <div>
      <img class="footer-logo" src="{r}assets/img/logo-ilo.png" alt="ILO – Institute for Learning Organizations">
      <p>In a rapidly changing world, thriving begins with the ability to learn and improve continuously. In learning organizations, individuals and teams unite to master the art of improvement.</p>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul>
        <li><a href="{r or './'}">Home</a></li>
        <li><a href="{r}about-us/">About ILO</a></li>
        <li><a href="{r}open-resources/">Open Resources</a></li>
        <li><a href="{r}estore/">eStore</a></li>
        <li><a href="{r}contact/">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>
        <li><a href="{r}sensei-mentorship/">Sensei Mentorship</a></li>
        <li><a href="{r}e-learning-services/">E-learning</a></li>
        <li><a href="{r}courses/">Courses</a></li>
        <li><a href="{r}upcoming-webinars/">Webinars</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in Touch</h4>
      <ul>
        <li>{ADDRESS}</li>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <div class="bottom">
    <span>© <span id="year">2025</span> Institute for Learning Organizations. All rights reserved.</span>
    <span>learnorg.global</span>
  </div>
</div></footer>
</body>
</html>
"""
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(html)


def page_hero(title, sub, img, crumb=None):
    c = f'<a href="{{r}}">Home</a> / {crumb + " / " if crumb else ""}{title}'
    return f"""<section class="page-hero" style="background-image:url('{{r}}assets/img/{img}')"><div class="container">
  <div class="crumbs">{c}</div>
  <h1>{title}</h1>
  <p>{sub}</p>
</div></section>"""


CTA = """<section class="section"><div class="container">
  <div class="cta-band">
    <div><h2>Let's start the conversation</h2><p>Want to learn more about our offerings, or have specific challenges to address? Reach out.</p></div>
    <a class="btn light" href="{r}contact/">Contact Us</a>
  </div>
</div></section>"""

AFFILIATES = [
    ("ALIOS", "ILO is a founder and projects manager of ALIOS – Accelerated Learning in Organizations and Society."),
    ("Leonardo Group Americas", "Obeya for Operations – online training and coaching."),
    ("Obeya Association", "Knowledge creation and sharing."),
    ("Obeya.Global", "Founding member of Obeya.Global."),
    ("DigiLEAN", "Exclusive representative for digiLEAN.tools in the Middle East."),
    ("Process Excellence Systems", "Business development."),
    ("LOS Norge", "Initiated by Bjarne Berg Wig in 2015. Knowledge sharing with ILO on Lean and learning culture maturity."),
    ("World Climate School", "Collaboration agreement. ILO assists WCS in using systems thinking to teach regenerative agriculture and circular economy."),
]


def affiliates_section(alt=True):
    cards = "".join(
        f'<div class="mini-card"><div class="num">{i:02d}</div><h3>{n}</h3><p>{d}</p></div>'
        for i, (n, d) in enumerate(AFFILIATES, 1)
    )
    return f"""<section class="section{' alt' if alt else ''}"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Affiliates</span>
    <h2>Affiliates &amp; Collaborators</h2>
    <p class="lead">We collaborate with globally recognized organizations like Leonardo Group Americas, Process Excellence, DigiLEAN, Obeya Association and Cabrera Research Lab to help organizations develop Lean, learning and innovation culture.</p>
  </div>
  <div class="grid cols-4">{cards}</div>
</div></section>"""


CLIENTS = [
    ("UDI (The Directorate of Immigration)", "Implemented a learning-organization plan based on the Norwegian co-operation model, involving top management and unions. UDI manages applications from foreigners wishing to visit or reside in Norway."),
    ("Delta Group Jobb og Kompetanse", "Assisted in adopting the Everyday Learning framework through training and sensei dialogue, focusing on job placement, skills development and work training."),
    ("Equinor Mongstad", "Known for its refinery and oil supply base, Mongstad has developed good Lean practices, enhanced by sensei dialogue and training provided by Bjarne Berg Wig."),
    ("Avinor (with Flowit)", "Manages Norway's main airports and has developed effective Lean practices in recent years, with training for top and middle managers."),
    ("Eramet Norway", "The world's leading manganese producer aims to be a true learning organization, with improvement direction through sensei dialogue with Bjarne Berg Wig."),
    ("Yara ASA", "A leading global fertilizer company, engaged in an ambitious improvement program developing its management system based on Lean thinking."),
    ("Stavne KF (Trondheim Kommune)", "Helps people return to work, supported by Bjarne Berg Wig in its Everyday Learning practices."),
    ("Vestre Toten Kommune", "Considered a leader in Lean and continuous improvement; developed video training material for internal management development."),
    ("Hennig-Olsen Is", "An ice cream manufacturer known for quality products and values, assisted in team development and Everyday Learning."),
    ("Sophies Minde Ortopedi", "Norway's leading orthopedic institution, developing a deep learning culture through long-term cooperation: sensei dialogue, training and e-resources."),
    ("Kristiansand Dyrepark", "Norway's leading amusement park, integrating Lean and learning-organization practices with management training and dialogue."),
]


PDF_GROUPS = [
    ("Lean ledelse – Del I: Lederskap og kultur", "Kursmateriell på norsk fra programmet «Lean ledelse for lærende organisasjoner».", [
        ("del-1-innhold", "Innhold Del I – Lederskap og kultur"),
        ("forelesningsnotat-1-kap-1-3", "Forelesningsnotat #1, kap. 1–3"),
        ("hva-er-lean", "Hva er Lean?"),
        ("lean-ledelse-historisk-bakgrunn", "Lean ledelse – historisk bakgrunn"),
        ("intro-til-lean-ledelse", "Intro til Lean ledelse"),
        ("oppbygging-av-lean-ledelse-programmet", "Oppbygging av Lean ledelse-programmet"),
        ("planlegging-for-gjennombrudd", "Planlegging for gjennombrudd"),
        ("masterplan-og-hoshin-ledelse", "Masterplan og Hoshin-ledelse"),
        ("lean-speilet", "Lean-speilet"),
        ("lean-speil-mal", "Mal: Lean-speil"),
        ("mal-for-selvvurdering", "Mal for selvvurdering (basis)"),
        ("det-uslaaelige-arbeidslaget", "Det uslåelige arbeidslaget"),
    ]),
    ("Systems Thinking with Obeya – chapter resources", "Articles and templates that accompany the book.", [
        ("masterplan-obeya-og-hoshin-ledelse", "Masterplan, Obeya og hoshin-ledelse (Bjarne Berg Wig)"),
        ("a3-laerende-system-og-systemtenkning", "A3 lærende system og systemtenkning"),
        ("los-diagnose-a3-mal", "LOS-diagnose – A3-mal"),
        ("obeya-sources-articles.docx", "Scientific articles about Obeya"),
        ("obeya-assessment.docx", "Obeya self-assessment sheet"),
        ("vsm-obeya.pptx", "Value stream mapping and Obeya"),
        ("obeya-hoshin-vmcl.pptx", "VMCL og Hoshin kanri (norsk)"),
    ]),
    ("Lean ledelse – Del II og III", "Arbeidsdokumenter og maler fra boka.", [
        ("lean-ledelse-del-ii.docx", "Del II"),
        ("lean-ledelse-del-iii.docx", "Del III"),
        ("lean-speil-mal.xlsx", "Mal for selvvurdering – Lean-speil"),
    ]),
    ("Recommended reading", "Articles and reports by other authors that the book pages refer to.", [
        ("laloux-reinventing-organizations-summary-changefactory", "Summary of Laloux, Reinventing Organizations"),
        ("vmcl-build-an-adaptive-organization", "VMCL: build an adaptive organization"),
        ("tanaka-obeya-pdma-visions-2009", "Tanaka: the Obeya room (PDMA Visions, 2009)"),
        ("cabrera-why-you-should-map", "Derek Cabrera: why you should map systems"),
        ("systems-thinking-skills-map", "A3 notes: System of Profound Knowledge"),
        ("rother-toyota-practice-article", "Mike Rother: study of Toyota Kata practice"),
        ("digital-obeya-rooms-paper", "Exploring digital Obeya rooms (research paper)"),
        ("vint-fourth-industrial-revolution", "VINT: the fourth industrial revolution"),
    ]),
]
FILE_KIND = {".docx": "Word", ".pptx": "PowerPoint", ".xlsx": "Excel"}


def pdf_library():
    groups = ""
    for title, intro, files in PDF_GROUPS:
        items = ""
        for slug, label in files:
            ext = os.path.splitext(slug)[1]
            path, kind, tab = (f"assets/files/{slug}", FILE_KIND[ext], "") if ext else (f"assets/pdf/{slug}.pdf", "PDF", ' target="_blank" rel="noopener"')
            kb = os.path.getsize(os.path.join(OUT, path)) / 1024
            size = f"{kb / 1024:.1f} MB" if kb >= 1024 else f"{kb:.0f} KB"
            items += f'<li><a href="{{r}}{path}"{tab}>{label}</a><span>{kind} · {size}</span></li>'
        groups += f'<div class="pdf-group"><h3>{title}</h3><p class="note">{intro}</p><ul class="pdf-list">{items}</ul></div>'
    return f"""<section class="section alt" id="library"><div class="container">
  <div class="section-head">
    <span class="eyebrow">Library</span>
    <h2>Downloadable resources</h2>
    <p class="lead">Lecture notes, templates and articles from our courses and books – free to download.</p>
  </div>
  <div class="grid cols-2">{groups}</div>
</div></section>"""


PAST_EVENTS = [
    # (day, month-year, title, meta, description, image or None)
    ("17", "Oct 2024", "Obeya dagseminaret i Bergen", "17 October 2024 · 08:30–18:00 · Høgskulen på Vestlandet, Inndalsveien 28, Bergen",
     "Obeya – raskere felles læring. Obeya er et visuelt rom for samarbeid mellom ulike funksjoner i en virksomhet, og arkitektur for radikalt bedre samspill på tvers. Ved å visualisere (se sammen), reflektere og prøve ut løsninger skapes raskere læring. På fagseminaret lærte vi om Obeya og delte erfaringer mellom ulike virksomheter.", "obeya-day-seminar.jpg"),
    ("9", "May 2024", "ALIOS Seminar in Piedmont", "9–13 May 2024 · Albergo del Vino, Castelnuovo Calcea, Italy",
     "Accelerated Learning in Organizations and Society: the annual R&amp;D programme team meeting of ILO COEX, following up the ALIOS project.", "events/alios-seminar.png"),
    ("Dec", "2023", "Lærende lederskap (Trippel L)", "December 2023 – June 2024 · Online and in Drammen, Bergen and Haugesund",
     "Course programme run by Institute for Learning Organizations and Flowit, in three modules: Lean and systems thinking, learning culture and Obeya, and learning leadership. Sessions were held at Aker Tranby near Drammen, Toyota Jæger Automobil in Bergen and Flowit in Haugesund, with certificates awarded at the Lean conference in Stavanger in September 2024.", None),
    ("10", "Nov 2023", "Obeya Summit presentation", "November 10, 2023 · 09:00–11:00 · Utrecht, the Netherlands",
     "Bjarne Berg Wig presented the book <em>Systems Thinking with Obeya</em> at the 2023 symposium in Utrecht.", None),
    ("23", "Nov 2021", "Manufacturing and Supply Chain Conference", "November 23, 2021 · 10:00–13:00 · Dublin, Ireland",
     "Samer Hamadeh spoke on learning culture transformation.", None),
    ("4", "May 2021", "Studietur Piemonte – FlowIT", "4–8 May 2021 · Via Toetto 5, Castelnuovo Calcea, Italy",
     "FlowIT and TPM Lean brukernettverket, together with Institute for Learning Organizations, invited participants on a study trip focused on systems leadership and coaching.", "piemonte.jpg"),
    ("23", "Sep 2020", "Studietur Piemonte – Samarbeidsutvikling", "23–27 September 2020 · Albergo del Vino, Castelnuovo Calcea, Italy",
     "Samarbeidsutvikling Norge and TPM Lean brukernettverket, together with Institute for Learning Organizations, invited participants on a study trip focused on coaching and systems thinking, for everyone who wants to develop in leadership and Lean.", None),
    ("4", "Feb 2020", "LOS-studiet 2020 – Lærende organisasjon, lærende system", "4–6 February 2020 (first of three sessions) · Norway",
     "A new course with three sessions, 12 days in total, during 2020.", None),
]


def past_events():
    out = ""
    for day, my, title, meta, desc, img in PAST_EVENTS:
        pic = f'<img class="event-img" src="{{r}}assets/img/{img}" alt="" loading="lazy">' if img else ""
        out += f'<div class="event"><div class="date"><b>{day}</b><span>{my}</span></div><div><h3>{title}</h3><div class="meta">{meta}</div><p>{desc}</p>{pic}</div></div>'
    return out


BOOKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content", "books")


def fragment(name):
    with open(os.path.join(BOOKS_DIR, name + ".html")) as f:
        return f.read()


LO_PARTS = [
    ("Del I – Fortid", "Del I ser bakover og utfordrer de mentale modellene som hindrer ny kunnskap.", range(1, 7)),
    ("Del II – Nåtid", "Lærende organisasjoner i praksis.", range(7, 13)),
    ("Del III – Framtid: Organisasjon 5.0", "Ressursene til del III ble aldri publisert på det gamle nettstedet.", range(13, 16)),
]
LO_LATE = {13: "Morgengry eller solnedgang?", 14: "Organisasjon som levende systemer", 15: "Om å lede fra framtida"}


def book_pages():
    lo_titles = {int(k): v for k, v in json.load(open(os.path.join(BOOKS_DIR, "_chapters.json"))).items()}
    base = "book-resources/"

    hub = f"""
{page_hero("Book Resources", "Companion pages for Bjarne Berg Wig's books.", "desk-laptop.jpg", "Open Resources")}
<section class="section"><div class="container">
  <div class="section-head"><p class="lead">Videos, links, templates and reading that go with each chapter. These pages were first published on the earlier learnorg.global site and have been restored here. Most of the material is in Norwegian.</p></div>
  <div class="grid cols-3">
    <article class="card"><img class="card-img" src="{{r}}assets/img/book-obeya.jpg" alt="Systems Thinking with Obeya cover" loading="lazy" style="object-fit:contain;background:var(--bg-alt);padding:20px"><div class="card-body">
      <span class="tag">English · Norsk</span><h3>Systems Thinking with Obeya</h3>
      <p>Chapter resources for the English edition and the Norwegian edition, <em>Systemtenkning med Obeya</em>.</p>
      <a class="more" href="{{r}}{base}systems-thinking-with-obeya/">English pages</a>
      <a class="more" href="{{r}}{base}systemtenkning-med-obeya/" style="margin-top:8px">Norske sider</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/book-laerende-organisasjoner.jpg" alt="Lærende organisasjoner cover" loading="lazy" style="object-fit:contain;background:var(--bg-alt);padding:20px"><div class="card-body">
      <span class="tag">Norsk</span><h3>Lærende organisasjoner</h3>
      <p>Ressurser kapittel for kapittel: videoer, artikler og refleksjonsspørsmål.</p>
      <a class="more" href="{{r}}{base}laerende-organisasjoner/">Til ressurssidene</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/book-lean-ledelse.jpg" alt="LEAN – Ledelse for lærende organisasjoner cover" loading="lazy" style="object-fit:contain;background:var(--bg-alt);padding:20px"><div class="card-body">
      <span class="tag">Norsk</span><h3>LEAN – Ledelse for lærende organisasjoner</h3>
      <p>Del I Lederskap og kultur: forelesningsnotater, maler og kursmateriell.</p>
      <a class="more" href="{{r}}{base}lean-ledelse/">Til ressurssidene</a></div></article>
  </div>
</div></section>
{CTA}
"""
    page(base, "Book Resources", "Companion resources for the books by Bjarne Berg Wig: Systems Thinking with Obeya, Lærende organisasjoner and LEAN – Ledelse for lærende organisasjoner.", hub)

    def prose_page(path, title, sub, img, crumb, desc, frag, lang, extra=""):
        body = f"""
{page_hero(title, sub, img, crumb)}
<section class="section"><div class="container"><div class="prose">
{frag}
</div>{extra}</div></section>
{CTA}
"""
        page(path, title, desc, body, lang)

    order = f'<div class="btn-row"><a class="btn" href="https://www.amazon.com/Systems-Thinking-Obeya-Bjarne-Berg/dp/826932891X" target="_blank" rel="noopener">Order the English book</a><a class="btn ghost" href="https://www.amazon.com/Systemtenkning-Obeya-Norwegian-Bjarne-Berg-ebook/dp/B0CG67C74W" target="_blank" rel="noopener">Norsk e-bok</a></div>'
    prose_page(base + "systems-thinking-with-obeya/", "Systems Thinking with Obeya", "Resources for the book, chapter by chapter.", "obeya-wall.jpg", "Book Resources",
               "Links, videos, tools and templates for Systems Thinking with Obeya by Bjarne Berg Wig.",
               '<p class="lead">Welcome to the resource pages for the book. Here you will find links, videos, tools and templates that will speed up your learning. The pages are continually improved with new resources, and an e-course with a 9-step guide to developing Obeya in your organization is in the works. Questions, ideas or resources to share: <a href="mailto:post@learnorg.global">post@learnorg.global</a>.</p>' + order + fragment("obeya-en"), "en")
    prose_page(base + "systemtenkning-med-obeya/", "Systemtenkning med Obeya", "Ressurser til boka, kapittel for kapittel.", "obeya-wall.jpg", "Book Resources",
               "Videoer, lenker, maler og læreeksempler til Systemtenkning med Obeya av Bjarne Berg Wig.",
               '<p class="lead">Her finner du videoer, lenker til vitenskapelige publikasjoner, maler og læreeksempler. Tips og spørsmål: <a href="mailto:post@learnorg.global">post@learnorg.global</a>.</p>' + order + fragment("obeya-no"), "nb")
    prose_page(base + "lean-ledelse/", "LEAN – Ledelse for lærende organisasjoner", "Ressurser til boka.", "gemba-team.jpg", "Book Resources",
               "Kursmateriell og ressurser til LEAN – Ledelse for lærende organisasjoner av Bjarne Berg Wig.",
               fragment("lean-ledelse"), "nb")

    # Lærende organisasjoner hub + chapters
    parts = ""
    for ptitle, pintro, chs in LO_PARTS:
        items = ""
        for n in chs:
            if n in lo_titles:
                items += f'<li><a href="{{r}}{base}laerende-organisasjoner/kapittel-{n}/"><b>{n}</b>{lo_titles[n]}</a></li>'
            else:
                items += f'<li><a aria-disabled="true" style="pointer-events:none"><b>{n}</b>{LO_LATE[n]}<span class="soon">ikke publisert</span></a></li>'
        parts += f'<div><h2>{ptitle}</h2><p class="note">{pintro}</p><ul class="chapter-list">{items}</ul></div>'
    lo_hub = f"""
{page_hero("Lærende organisasjoner", "Ressurser til boka, kapittel for kapittel.", "training-session.jpg", "Book Resources")}
<section class="section"><div class="container">
  <div class="split" style="margin-bottom:56px">
    <img src="{{r}}assets/img/book-laerende-organisasjoner.jpg" alt="Lærende organisasjoner" loading="lazy" style="max-width:300px;justify-self:center;box-shadow:none">
    <div>
      <p class="lead">Boka gir ledere, tillitsvalgte og andre endringsledere kunnskapen som trengs for å gå fra mål- og resultatstyring til ekte lærende organisasjoner. En rød tråd gjennom boka er systemtenkning.</p>
      <p>Velg et kapittel for å se videoer, artikler og refleksjoner som hører til. Noen av sidene var bare i versjon 1.0 på det gamle nettstedet.</p>
      <div class="btn-row"><a class="btn" href="https://www.gyldendal.no/Faglitteratur/OEkonomi-og-administrasjon/Samfunnsoekonomi/Laerende-organisasjoner" target="_blank" rel="noopener">Kjøp boka</a></div>
    </div>
  </div>
  <div class="grid cols-3">{parts}</div>
</div></section>
{CTA}
"""
    page(base + "laerende-organisasjoner/", "Lærende organisasjoner – ressurser", "Ressurser kapittel for kapittel til boka Lærende organisasjoner av Bjarne Berg Wig.", lo_hub, "nb")

    nums = sorted(lo_titles)
    for i, n in enumerate(nums):
        prev = f'<a href="{{r}}{base}laerende-organisasjoner/kapittel-{nums[i-1]}/">← Kapittel {nums[i-1]}</a>' if i else '<span></span>'
        nxt = f'<a href="{{r}}{base}laerende-organisasjoner/kapittel-{nums[i+1]}/">Kapittel {nums[i+1]} →</a>' if i + 1 < len(nums) else f'<a href="{{r}}{base}laerende-organisasjoner/">Alle kapitler</a>'
        prose_page(f"{base}laerende-organisasjoner/kapittel-{n}/", f"Kapittel {n}: {lo_titles[n]}", "Lærende organisasjoner – ressurser", "desk-laptop.jpg", "Book Resources",
                   f"Ressurser til kapittel {n} i Lærende organisasjoner: {lo_titles[n]}.", fragment(f"lo-kapittel-{n}"), "nb",
                   extra=f'<nav class="chapter-nav">{prev}{nxt}</nav>')


def build():
    book_pages()

    # ---------- Home ----------
    services = [
        ("training-session.jpg", "Sensei Mentorship", "Transformation through dialogue.", "sensei-mentorship/"),
        ("team-laptops.jpg", "Books and e-learning", "What you need, when you need it, how you need it.", "e-learning-services/"),
        ("gemba-team.jpg", "Courses and seminars", "Make your own workplace your campus.", "courses/"),
    ]
    svc = "".join(
        f'<article class="card"><img class="card-img" src="{{r}}assets/img/{img}" alt="" loading="lazy"><div class="card-body"><h3>{t}</h3><p>{d}</p><a class="more" href="{{r}}{h}">Learn more</a></div></article>'
        for img, t, d, h in services
    )
    partners = [
        ("logo-flowit.png", "Flowit", "<p>We cooperate in the following areas:</p><ul><li>Forbedringslederskolen (School)</li><li>Black Belt Lean and continuous improvement program</li><li>Conferences</li><li>Leadership seminar in Piemonte, Italy</li></ul>"),
        (None, "Obeya.Global", "<p>ILO is a founding member of Obeya.Global, the international community for Obeya practice.</p>"),
        ("logo-digilean.png", "DigiLEAN", '<p>We cooperate with Kaizen Solutions to develop DigiLEAN LEARNING. ILO provides DigiLEAN with digital learning resources. <a href="https://www.digilean.com/" target="_blank" rel="noopener">digilean.com</a></p>'),
        ("logo-leonardo.png", "Leonardo Group Americas", "<p>Affiliated for the UK, Spain, Italy, Sweden and Norway. Online training and certification in Mixed Model Line Design and Mixed Model Material Management. Consulting in advanced Lean for healthcare and manufacturing.</p>"),
    ]
    pcards = "".join(
        f'<div class="card logo-card"><div class="logo-box">'
        + (f'<img src="{{r}}assets/img/{logo}" alt="{name}" loading="lazy">' if logo else f'<span class="wordmark">{name}</span>')
        + f"</div><h3>{name}</h3>{body}</div>"
        for logo, name, body in partners
    )
    clients = "".join(f'<div class="mini-card"><h3>{n}</h3><p>{d}</p></div>' for n, d in CLIENTS)
    home = f"""
<section class="hero" style="background-image:url('{{r}}assets/img/hero-laptop.jpg')"><div class="container">
  <span class="eyebrow">Institute for Learning Organizations</span>
  <h1>Shaping the Future with Better Learning</h1>
  <p>Order the book <em>Systems Thinking with Obeya</em> – now available in English.</p>
  <div class="btn-row">
    <a class="btn light" href="{{r}}estore/">Get Your Copy Today</a>
    <a class="btn ghost" style="color:#fff;border-color:#fff" href="{{r}}services/">Our Services</a>
  </div>
</div></section>

<section class="section"><div class="container mission">
  <div>
    <span class="eyebrow">Our Mission</span>
    <h2>Our purpose: millions of improvement culture leaders</h2>
    <p class="lead">In a rapidly changing world, thriving begins with the ability to learn and improve continuously. In learning organizations, individuals and teams unite to master the art of improvement – building the foundation for adaptability and lasting success.</p>
    <p>Through Systems Thinking and Obeya, we help leaders and teams transform challenges into opportunities, fostering collaboration, innovation and growth.</p>
    <div class="stat"><strong>30+</strong><span>years of expertise in sensei mentorship, e-courses and on-site training, supporting leaders and teams to build cultures of improvement and innovation.</span></div>
  </div>
  <img class="media" src="{{r}}assets/img/obeya-wall.jpg" alt="Obeya room with visual management boards" loading="lazy">
</div></section>

<section class="section alt"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">How We Help</span>
    <h2>How we contribute</h2>
  </div>
  <div class="grid cols-3">{svc}</div>
</div></section>

<section class="section"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Partners</span>
    <h2>Our Partners</h2>
  </div>
  <div class="grid cols-4">{pcards}</div>
</div></section>

{affiliates_section()}

<section class="section"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Our Clients</span>
    <h2>Organizations we work with</h2>
  </div>
  <div class="grid cols-3">{clients}</div>
</div></section>

<section class="section alt"><div class="container split">
  <img src="{{r}}assets/img/bjarne-and-samer.jpg" alt="Bjarne Berg Wig and Samer Hamadeh" loading="lazy">
  <div>
    <span class="eyebrow">Meet ILO</span>
    <h2>Making systems thinking affordable and accessible</h2>
    <p>The Institute for Learning Organizations (ILO) was created to make the knowledge of systems thinking affordable and accessible. It evolved from TQM Center Norway.</p>
    <p>ILO has two resident experts, Bjarne Berg Wig and Samer Hamadeh. Together they offer over 30 years of experience in continuous improvement and developing real learning organizations. Their focus is to help employees and leaders become systems thinkers, and to apply this thinking in practice within their organizations – through a combination of mentorship, on-site training and e-learning.</p>
    <div class="btn-row"><a class="btn" href="{{r}}about-us/">About ILO</a></div>
  </div>
</div></section>
{CTA}
"""
    page("", "Home", "The Institute for Learning Organizations helps leaders and teams build cultures of improvement through systems thinking, Obeya, sensei mentorship, e-learning and training.", home)

    # ---------- About ----------
    about = f"""
{page_hero("About ILO", "Future-prepared systems thinkers.", "obeya-wall.jpg")}
<section class="section"><div class="container split">
  <div>
    <span class="eyebrow">Our Story</span>
    <h2>Since 1998</h2>
    <p class="lead">The Institute for Learning Organizations was established in 1998 under the name TQM Center Norway, as a collaboration between researchers, industry and consulting environments.</p>
    <p>We have been developing courses on TQM and Lean management for Norwegian universities, municipalities and international businesses. Our founder Bjarne Berg Wig has published eight books on improvement leadership and Obeya.</p>
    <p>ILO is part of an R&amp;D program supported by the Research Council of Norway: ALIOS – Accelerated Learning in Organizations and Society.</p>
    <div class="btn-row"><a class="btn" href="{{r}}services/">Our Services</a></div>
  </div>
  <img src="{{r}}assets/img/training-session.jpg" alt="Systems thinking training session" loading="lazy">
</div></section>

<section class="section alt"><div class="container">
  <div class="section-head">
    <span class="eyebrow">Our Team</span>
    <h2>Meet our experts</h2>
  </div>
  <div class="grid cols-2">
    <div class="person">
      <img src="{{r}}assets/img/bjarne-berg-wig.jpg" alt="Bjarne Berg Wig" loading="lazy">
      <div>
        <h3>Bjarne Berg Wig</h3>
        <div class="role">Founder · Author · Sensei</div>
        <p>Bjarne Berg Wig is an author and sensei with over three decades of experience in quality management, Lean and systems thinking. He has collaborated with Bergen University of Applied Sciences, authored eight professional books, and pioneered programs on leadership and learning organizations. He leads the ALIOS R&amp;D program and is a certified systems thinking trainer.</p>
        <p>He was Quality and Innovation Manager at Hydro Agri Europe (now Yara), and for the last 20 years has helped many Norwegian and international private and public organizations transform into learning organizations. Bjarne is a founder of LOS Norge, the Society for Learning Organizations in Norway.</p>
      </div>
    </div>
    <div class="person">
      <img src="{{r}}assets/img/bjarne-and-samer.jpg" alt="Samer Hamadeh with Bjarne Berg Wig" loading="lazy" style="object-position:30% center">
      <div>
        <h3>Samer Hamadeh</h3>
        <div class="role">Co-founder · Systems Thinking Expert</div>
        <p>Samer Hamadeh, co-founder of ILO, is a systems thinking expert who helps organizations and communities cultivate actionable cultures of learning and innovation that drive meaningful change.</p>
      </div>
    </div>
  </div>
</div></section>

{affiliates_section(alt=False)}
{CTA}
"""
    page("about-us/", "About ILO", "ILO was established in 1998 as TQM Center Norway. Meet our experts Bjarne Berg Wig and Samer Hamadeh.", about)

    # ---------- Services ----------
    svc_rows = [
        ("hero-coffee.jpg", "Sensei Mentorship", "Transformation through dialogue", "Our sensei mentorship helps leaders develop systems thinking, discover hidden drivers of improvement, and foster innovation. Whether you are an advanced practitioner or just starting, our tailored approach accelerates your journey to becoming a practicing systems thinker and agent of change.", "sensei-mentorship/"),
        ("piemonte.jpg", "Training Programs", "Tailored training for real impact", "From Gemba learning trips at leading Norwegian organizations to immersive off-site retreats in Italy, our training programs are customized to address your organization's unique challenges and foster a learning culture.", "courses/"),
        ("logo-digilean.png", "DigiLEAN", "Empowering through digital tools", "Through our partnership with DigiLEAN, we provide innovative digital learning solutions to streamline Lean management and process optimization.", "e-learning-services/"),
    ]
    rows = ""
    for i, (img, t, sub, d, h) in enumerate(svc_rows):
        style = ' style="background:#fff;padding:48px;object-fit:contain"' if img.endswith(".png") else ""
        rows += f"""<div class="split{' reverse' if i % 2 else ''}" style="margin-bottom:80px">
  <img src="{{r}}assets/img/{img}" alt="" loading="lazy"{style}>
  <div><span class="eyebrow">{sub}</span><h2>{t}</h2><p class="lead">{d}</p><div class="btn-row"><a class="btn" href="{{r}}{h}">Learn more</a></div></div>
</div>"""
    services_page = f"""
{page_hero("Services", "Mentorship, training and digital learning for organizations that want to learn faster.", "gemba-team.jpg")}
<section class="section"><div class="container">{rows}</div></section>
{CTA}
"""
    page("services/", "Services", "Sensei mentorship, training programs and DigiLEAN digital learning from the Institute for Learning Organizations.", services_page)

    # ---------- Sensei ----------
    sensei = f"""
{page_hero("Sensei Mentorship", "Transformation through challenge and dialogue.", "hero-coffee.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container split">
  <div>
    <span class="eyebrow">What is a sensei?</span>
    <h2>Look beyond the borders of your first understanding</h2>
    <p class="lead">A sensei encourages you to look beyond the borders of your first understanding of the current situation, toward a deeper meaning.</p>
    <p>Whether you are advanced in systems thinking or just starting to use the method, we recommend you enlist the expertise of our sensei mentor to help you learn and grow through your journey.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Talk to a sensei</a></div>
  </div>
  <img src="{{r}}assets/img/pdca-sketch.jpg" alt="Hand-drawn Plan–Do–Study–Act learning cycle" loading="lazy">
</div></section>
{CTA}
"""
    page("sensei-mentorship/", "Sensei Mentorship", "Sensei mentorship from ILO: transformation through challenge and dialogue for leaders becoming systems thinkers.", sensei)

    # ---------- Learning Culture (restored from the old Wix "coaching" and "about" pages) ----------
    videos = [
        ("fYoppX3VHIY", "Toyota Kata – Mike Rother", "Mike Rother, author of <em>Toyota Kata</em>, at the Lean Summit 2012."),
        ("zDZFcDGpL4U", "Changing Education Paradigms", "RSA Animate of a talk by Sir Ken Robinson."),
        ("STTwZGNvLmM", "Applying the Lens of Profound Knowledge", "Robert Lloyd, PhD, from the IHI Open School course QI101."),
        ("xKv--YA8XJE", "Deming's System of Profound Knowledge", "Robert Lloyd, PhD, from the IHI Open School course QI101."),
    ]
    video_cards = "".join(f'<div><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v}" title="{t}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><h3>{t}</h3><p class="note">{d}</p></div>' for v, t, d in videos)
    culture = f"""
{page_hero("Learning Culture Transformation", "From seeing work as execution to seeing work as continuous learning and improvement.", "training-session.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container"><div class="prose">
  <p class="lead">Learning Culture Transformation (LCT) is the shift from seeing work as execution to seeing work as continuous learning and improvement – seeing the organization as a complex adaptive system that adapts to change through learning.</p>
  <h2>Learning culture</h2>
  <p>LCT is a breakaway from Taylor's "scientific management" model of centralized command-and-control organizations: from command and control to challenging and developing learners. LCT is about deep respect for people and building on people's innate capacity to learn. Dr W. Edwards Deming (1900–1993) put it this way in <em>The New Economics</em>:</p>
  <blockquote>"One is born with a natural inclination to learn. Learning is a source of innovation. One inherits a right to enjoy his work. Good management helps us to nurture these positive innate attributes of people."</blockquote>
  <h2>What is learning?</h2>
  <p>Learning is the process of developing and improving our mental models – how we see and understand – so we navigate the real world better. It requires a good understanding of the thinking process and of how we acquire knowledge through seeing, dialogue and practical trials. Two insights are key:</p>
  <ul>
    <li>People are born with learning capacity. Present management practice has reduced these skills, so they have to be nurtured.</li>
    <li>We all have biases in how we see and interpret the real world (mental models). We need to understand these biases and use that understanding to become better thinkers.</li>
  </ul>
  <h2>Complex adaptive systems</h2>
  <p>A complex adaptive system (CAS) is able to adapt to change for better interaction with the real world. In an environment of rapid technological, social, geographical and environmental change, the capacity for real learning is crucial for survival. Nature itself is the best teacher of complex adaptive systems.</p>
  <h2>What is a learning organization?</h2>
  <p>An organization that acquires, creates, interprets, transmits, shares and retains knowledge, and consciously adapts its behaviour to reflect new knowledge and insights.</p>
</div></div></section>
<section class="section alt"><div class="container">
  <div class="section-head"><span class="eyebrow">Video library</span><h2>Recommended videos</h2></div>
  <div class="video-grid">{video_cards}</div>
</div></section>
{CTA}
"""
    page("learning-culture/", "Learning Culture Transformation", "Learning Culture Transformation: seeing work as continuous learning and the organization as a complex adaptive system. With a video library.", culture)

    # ---------- E-learning ----------
    books = [
        ("book-laerende-organisasjoner.jpg", "Lærende organisasjoner", "Norwegian · Gyldendal", """<p>The book gives leaders, union representatives and other change leaders the knowledge needed to move from an outdated system of goal management, bureaucracy and hierarchy – to a society that removes waste of all forms and frees the vast and often hidden resources in all people.</p>
<p>It describes the necessary shift from goal and result management to real learning organizations and learning systems, in three parts: <em>Past</em> asks why we ended up in this disorder and how we get out of it; <em>Present</em> is about going from “introducing Lean” and continuous improvement to becoming a true learning organization; <em>Future</em> asks how we develop self-organizing and open, participatory organizations.</p>
<p>A red thread throughout the book is systems thinking – awareness of how systems work and how we think about them. To transform organizations, we must change how we think. The book is for people who want to become better thinkers.</p>""",
         '<a class="btn" href="https://www.gyldendal.no/Faglitteratur/OEkonomi-og-administrasjon/Samfunnsoekonomi/Laerende-organisasjoner" target="_blank" rel="noopener">Buy</a>'),
        ("book-lean-ledelse.jpg", "LEAN – Ledelse for lærende organisasjoner", "Norwegian · Gyldendal", """<p>Lean is about creating products and services with the most value and least possible loss of resources, by focusing on flow, transparent processes and continuous improvement.</p>
<p>This book and its digital resources are designed for a breakthrough for Lean: a turning point where continuous improvement and learning in the workplace become commonplace, and all managers and employees in municipalities and businesses are active in improvement and renewal. It is about moving from work as effective execution to seeing work as a learning process.</p>
<p><strong>Part I</strong> explains how to develop a breakthrough strategy. <strong>Part II</strong> covers the methods and tools for introducing and developing Lean in a municipal or private enterprise. <strong>Part III</strong>, new in this edition, covers real learning organizations: learning leadership and the use of guidance, coaching and problem-solving dialogue – what remains after the term Lean goes into history.</p>""",
         '<a class="btn" href="https://www.gyldendal.no/Faglitteratur/Arbeidsliv/Ledelse/Lean2" target="_blank" rel="noopener">Buy</a>'),
        ("book-quality-craft.jpg", "Quality Improvement as a Craft", "English · Handbook for practitioners", """<p><em>Quality Improvement as a Craft</em> (Hydro Media, 1996) was the main training material for continuous improvement teams in Norway for many years. It is still very valid and gives an overview of many of the methods and tools we know today under the name Lean. The book is still used in teaching at academic courses.</p>
<p>Please contact us with your name and e-mail address and we will follow up on your book order.</p>""",
         '<a class="btn" href="{r}contact/">Contact Us</a>'),
        ("book-det-er-ledelse.jpg", "Det er ledelse", "Norwegian · E-book", """<p>E-bok «Det er ledelse» – kvalitetsledelse for det 21. århundret. Dette er læreboka i TKL/TQM ved flere høgskoler og universiteter. Her finner du også en mengde ressurser knyttet til opplæring i kvalitetsledelsesfaget.</p>""",
         '<a class="btn" href="https://issuu.com/tqm2/docs/det_er_ledelse_8" target="_blank" rel="noopener">Kjøp boka og last den ned</a>'),
    ]
    book_html = "".join(
        f'<div class="book"><img src="{{r}}assets/img/{img}" alt="Cover of {t}" loading="lazy"><div><span class="lang">{lang}</span><h3 style="font-size:1.6rem">{t}</h3>{d}<div class="btn-row">{btn}</div></div></div>'
        for img, t, lang, d, btn in books
    )
    elearn = f"""
{page_hero("E-learning Services", "Key learning resources: what you need, when you need it, and how you need it.", "team-laptops.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container">
  <div class="grid cols-3">
    <article class="card"><img class="card-img" src="{{r}}assets/img/desk-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">E-courses</span><h3>From beginner to advanced</h3>
      <p>We offer e-courses from beginners to advanced systems thinkers. After completing the e-book and e-course, you will be equipped to implement concrete actions to achieve faster learning and improved interaction throughout your organization. Contact Bjarne Berg Wig to hear more about the course.</p>
      <a class="more" href="https://educate.potential.com/courses/laerende-hverdag/" target="_blank" rel="noopener">Register now</a>
    </div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/butterflies.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">E-books</span><h3>Lærende hverdag</h3>
      <p>Read and download our e-books online.</p>
      <a class="more" href="https://issuu.com/tqm2/docs/l_rende_hverdag_e-bok_versjon_1.0" target="_blank" rel="noopener">View e-book</a>
    </div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/cafe-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">Webinars</span><h3>Everyday Learning</h3>
      <p>Next webinar: how to frame the transformation to a learning culture. Hosts: Bjarne Berg Wig and Samer Hamadeh. Date to be announced – send us your name and e-mail address and we will follow up with details.</p>
      <a class="more" href="{{r}}contact/">Contact us</a>
    </div></article>
  </div>
</div></section>
<section class="section alt" id="books"><div class="container">
  <div class="section-head">
    <span class="eyebrow">Books</span>
    <h2>Books by Bjarne Berg Wig</h2>
  </div>
  {book_html}
</div></section>
{CTA}
"""
    page("e-learning-services/", "E-learning Services", "E-courses, e-books, webinars and books on Lean, systems thinking and learning organizations by Bjarne Berg Wig.", elearn)

    # ---------- Courses ----------
    courses = f"""
{page_hero("Courses", "Make your own workplace your campus.", "training-session.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container">
  <div class="split" style="margin-bottom:96px">
    <img src="{{r}}assets/img/training-session.jpg" alt="On-site training" loading="lazy">
    <div><span class="eyebrow">On-site Training</span><h2>Bring an expert to your company</h2>
      <p class="lead">Book an expert to come to your company for hands-on training.</p>
      <p>We believe the best way to learn is through a combination of learning together, e-learning and practical application. Our experts provide custom courses tailored to the needs of your company and team members.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact Us</a></div></div>
  </div>
  <div class="split reverse" style="margin-bottom:96px">
    <img src="{{r}}assets/img/piemonte.jpg" alt="Vineyards in Piemonte, Italy" loading="lazy">
    <div><span class="eyebrow">Off-site Training</span><h2>A change of scenery opens the mind</h2>
      <p class="lead">Take your team off-site to ILO's Albergo del Vino, surrounded by the vineyards of Piemonte, Italy.</p>
      <p>Here your team can fully focus on “learning how to learn together”. Programs are tailored to the needs of your organization and cover all key concepts to help participants become systems thinkers. The off-site program is excellent for team building too.</p>
      <p>Before your visit we discuss the goals and needs of your team, and create a custom program so your team receives exactly what it needs.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Plan an off-site</a></div></div>
  </div>
  <div class="split">
    <img src="{{r}}assets/img/gemba-team.jpg" alt="Team at a Gemba visit" loading="lazy">
    <div><span class="eyebrow">Gemba Learning Trips</span><h2>Go and see</h2>
      <p class="lead">Crucial to learning is to go and see, communicate and learn from practitioners.</p>
      <p>We provide training and learning in partnership with leading companies and municipalities in Norway, Italy and the UK in the field of Lean and learning culture. We organize visits to relevant organizations so participants can see how improvement and change are made, and discuss case studies with the transformation leaders behind them. Combined training and gemba walks provide the ultimate learning experience.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact Us</a></div></div>
  </div>
</div></section>
{CTA}
"""
    page("courses/", "Courses", "On-site training, off-site training in Piemonte, Italy, and Gemba learning trips from ILO.", courses)

    # ---------- Open resources ----------
    res = f"""
{page_hero("Open Resources", "Knowledge at your fingertips.", "desk-laptop.jpg")}
<section class="section"><div class="container">
  <div class="section-head">
    <p class="lead">Explore our library of e-books, webinars and video resources designed for learning organizations. Gain insights on topics like systems thinking, learning leadership and Lean practices – available anytime, anywhere.</p>
  </div>
  <div class="grid cols-3">
    <article class="card"><img class="card-img" src="{{r}}assets/img/book-obeya.jpg" alt="Systems Thinking with Obeya cover" loading="lazy" style="object-fit:contain;background:var(--bg-alt);padding:20px"><div class="card-body">
      <span class="tag">Featured</span><h3>Systems Thinking with Obeya</h3>
      <p>A comprehensive guide for leaders adopting Lean principles.</p>
      <a class="more" href="{{r}}estore/">Get the book</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/learning-culture-diagram.png" alt="Learning culture model" loading="lazy" style="object-fit:contain;background:#fff;padding:12px"><div class="card-body">
      <span class="tag">Popular</span><h3>Everyday Learning</h3>
      <p>Frameworks for building continuous improvement practices.</p>
      <a class="more" href="https://issuu.com/tqm2/docs/l_rende_hverdag_e-bok_versjon_1.0" target="_blank" rel="noopener">Read the e-book</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/cafe-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">Webinars</span><h3>Webinars</h3>
      <p>On leadership, learning teams and continuous improvement.</p>
      <a class="more" href="{{r}}upcoming-webinars/">See webinars</a></div></article>
  </div>
  <div class="cta-band" style="margin-top:48px">
    <div><h2>Book resources</h2><p>Chapter-by-chapter videos, links and templates for Systems Thinking with Obeya, Lærende organisasjoner and LEAN – Ledelse for lærende organisasjoner.</p></div>
    <a class="btn light" href="{{r}}book-resources/">Open book resources</a>
  </div>
</div></section>
{pdf_library()}
{CTA}
"""
    page("open-resources/","Open Resources", "Open e-books, webinars and resources on systems thinking, learning leadership and Lean.", res)

    # ---------- eStore ----------
    estore = f"""
{page_hero("eStore", "Digital and print resources.", "butterflies.jpg")}
<section class="section"><div class="container">
  <div class="section-head">
    <span class="eyebrow">Shop our resources</span>
    <h2>Practical tools and in-depth insight</h2>
    <p class="lead">Access a curated collection of e-books, training materials and guides tailored to help leaders and organizations excel.</p>
  </div>
  <div class="split" style="margin-bottom:72px">
    <img src="{{r}}assets/img/book-obeya.jpg" alt="Systems Thinking with Obeya" loading="lazy" style="max-width:340px;justify-self:center">
    <div><span class="eyebrow">New in English</span><h2>Systems Thinking with Obeya</h2>
      <p class="lead">By Bjarne Berg Wig. A comprehensive guide for leaders adopting Lean principles and building learning organizations with Obeya.</p>
      <div class="btn-row"><a class="btn" href="mailto:post@learnorg.global?subject=Order%3A%20Systems%20Thinking%20with%20Obeya">Order your copy</a></div></div>
  </div>
  <div class="grid cols-3">
    <article class="card"><img class="card-img" src="{{r}}assets/img/pdca-sketch.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">Featured</span><h3>How-to Summaries</h3><p>Practical guides for implementing Lean and systems thinking.</p>
      <a class="more" href="{{r}}contact/">Ask about summaries</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/desk-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">Featured</span><h3>Online Courses</h3><p>Self-paced modules designed to meet organizational needs.</p>
      <a class="more" href="https://educate.potential.com/courses/laerende-hverdag/" target="_blank" rel="noopener">Browse courses</a></div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/book-laerende-organisasjoner.jpg" alt="" loading="lazy" style="object-fit:contain;background:var(--bg-alt);padding:16px"><div class="card-body">
      <span class="tag">Books</span><h3>Books by Bjarne Berg Wig</h3><p>Lærende organisasjoner, LEAN – Ledelse for lærende organisasjoner, Quality Improvement as a Craft and more.</p>
      <a class="more" href="{{r}}e-learning-services/#books">See all books</a></div></article>
  </div>
</div></section>
{CTA}
"""
    page("estore/", "eStore", "Books, e-books, how-to summaries and online courses from the Institute for Learning Organizations.", estore)

    # ---------- Events ----------
    upcoming = f"""
{page_hero("Upcoming Webinars", "Learn and grow.", "cafe-laptop.jpg", "Events")}
<section class="section"><div class="container">
  <div class="section-head"><p class="lead">Join our webinars to explore systems thinking, Lean methodologies and real-life applications of learning culture. Gain actionable insights directly from industry experts.</p></div>
  <div class="event">
    <div class="date"><b>TBA</b><span>Date</span></div>
    <div><h3>Everyday Learning</h3>
      <div class="meta">Online · Hosts: Bjarne Berg Wig and Samer Hamadeh</div>
      <p>How to frame the transformation to a learning culture. Send us your name and e-mail address and we will follow up with information about the webinar.</p>
      <a class="btn" href="{{r}}contact/">Register interest</a></div>
  </div>
</div></section>
{CTA}
"""
    page("upcoming-webinars/", "Upcoming Webinars", "Upcoming ILO webinars on systems thinking, Lean and learning culture.", upcoming)

    workshops = f"""
{page_hero("Workshops and Seminars", "Collaborate and transform.", "obeya-day-seminar.jpg", "Events")}
<section class="section"><div class="container split">
  <div>
    <p class="lead">Attend hands-on workshops that offer practical tools, real-world applications and networking opportunities.</p>
    <h2>Obeya Day Seminar</h2>
    <p>Our Obeya Day seminars focus on rapid collective learning through visual collaboration – Obeya as an architecture for better cooperation.</p>
    <p class="note">No workshops are scheduled right now. Contact us to hear about the next one, or to arrange a seminar for your organization.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact Us</a></div>
  </div>
  <img src="{{r}}assets/img/obeya-day-seminar.jpg" alt="Obeya Day seminar in Bergen" loading="lazy">
</div></section>
{CTA}
"""
    page("workshops-and-webinars/", "Workshops and Seminars", "Hands-on ILO workshops and Obeya Day seminars.", workshops)

    past = f"""
{page_hero("Past Events", "Look back at recent symposiums, conferences and seminars.", "obeya-wall.jpg", "Events")}
<section class="section"><div class="container">
  {past_events()}
</div></section>
{CTA}
"""
    page("past-events/", "Past Events", "Past ILO events, conferences and presentations.", past)

    # ---------- Contact ----------
    contact = f"""
{page_hero("Contact", "Connect with us.", "hero-coffee.jpg")}
<section class="section"><div class="container">
  <div class="section-head"><p class="lead">Want to learn more about our offerings? Have specific challenges to address? Reach out to us, and let's start the conversation.</p></div>
  <div class="contact-grid">
    <div class="contact-item"><div class="label">Post address</div><p>Kongens gate 20A<br>3717 Skien, Norway</p></div>
    <div class="contact-item"><div class="label">Phone</div><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="contact-item"><div class="label">Email</div><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  <div class="btn-row" style="margin-top:40px"><a class="btn" href="mailto:{EMAIL}">Send us an email</a></div>
</div></section>
"""
    page("contact/", "Contact", "Contact the Institute for Learning Organizations in Skien, Norway.", contact)


build()
print("built")
