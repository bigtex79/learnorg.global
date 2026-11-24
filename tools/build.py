import os, sys, json

OUT = sys.argv[1]
EMAIL = "gabi@learnorg.global"
PHONE = "+47 48 28 70 00"
PHONE_TEL = "+4748287000"
ADDRESS = "Kongens gate 20A, 3717 Skien, Norway"
# Public address of the site, used for link previews. Change to https://learnorg.global/ once the domain points here.
SITE_URL = "https://bigtex79.github.io/learnorg.global/"

ICON_PIN = '<svg viewBox="0 0 24 24" width="14" height="14" fill="#078586" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" width="14" height="14" fill="#078586" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4.4 7H4v.6l8 5.5 8-5.5V7h-.4L12 12.2z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" width="14" height="14" fill="#078586" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1l-2.2 2.2z"/></svg>'

# Bump when style.css changes so browsers fetch the new file
CSS_VERSION = "33"
TAGLINE = "Lean · Learning · Leadership"

NAV = [
    # The logo links home, so there is no Home item (saves room for the longer menu labels)
    ("Services", "services/", [
        ("Sensei Mentorship", "sensei-mentorship/"),
        ("Training", "training/"),
        ("Learning Culture", "learning-culture/"),
        ("Obeya", "obeya/"),
    ]),
    ("Books & Resources", "resources/", [
        ("Systems Thinking with Obeya", "book-resources/systems-thinking-with-obeya/"),
        ("Lærende organisasjoner", "book-resources/laerende-organisasjoner/"),
        ("LEAN Ledelse", "book-resources/lean-ledelse/"),
        ("Det er Ledelse", "book-resources/det-er-ledelse/"),
        ("Download library", "resources/#library"),
        ("Video library", "resources/#videos"),
    ]),
    ("Courses & Events", "events/", [
        ("E-learning & webinars", "e-learning/"),
        ("Trippel L", "events/trippel-l/"),
        ("Obeya Day Seminar", "events/obeya-day-seminar/"),
    ]),
    ("About", "about/", [
        ("Bjarne Berg Wig", "about/#bjarne-berg-wig"),
        ("Samer Hamadeh", "about/#samer-hamadeh"),
        ("Clients", "about/#clients"),
    ]),
]


ICONS = {
    "mentoring": '<path d="M4 5h11a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M19 9h1a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-1v3l-4-3h-3"/>',
    "training": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20l4-4 4 4M7 9h6M7 12h4"/>',
    "offsite": '<path d="M3 19l6-10 4 6 3-4 5 8z"/><circle cx="17" cy="6" r="2"/>',
    "elearning": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20M10 9l4 1.5-4 1.5z"/>',
    "culture": '<path d="M20 12a8 8 0 1 1-3-6.2"/><path d="M20 4v5h-5"/><path d="M12 8v4l3 2"/>',
    "obeya": '<rect x="3" y="4" width="18" height="15" rx="1.5"/><path d="M3 9h18M9 9v10M15 9v10"/>',
    "resources": '<path d="M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h6"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="1.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15 20a5 5 0 0 1 7-4.5"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


# First item in a dropdown that links to the section page; default "All <section>"
OVERVIEW_LABELS = {"Books & Resources": "All books & resources", "Courses & Events": "Upcoming & past events", "About": "About ILO"}


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
                sub = f'<li><a href="{r}{href}"{" class=active" if href == current else ""}>{OVERVIEW_LABELS.get(label, "All " + label.lower())}</a></li>' + sub
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
<meta property="og:type" content="website">
<meta property="og:site_name" content="Institute for Learning Organizations">
<meta property="og:title" content="{title if path else full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:locale" content="{"nb_NO" if lang == "nb" else "en_GB"}">
<meta property="og:image" content="{SITE_URL}assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Institute for Learning Organizations: shaping the future with better learning">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE_URL}{path}">
<link rel="icon" href="{r}assets/img/favicon.png?v=6">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css?v={CSS_VERSION}">
<script src="{r}assets/js/main.js?v={CSS_VERSION}" defer></script>
</head>
<body>
<div class="topbar"><div class="container">
  <div class="group">
    <span class="item hide-sm">{ICON_PIN}<b>Location</b> Skien, Norway</span>
    <span class="item">{ICON_MAIL}<b>Email</b> <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
  <div class="group">
    <span class="item">{ICON_PHONE}<b>Phone</b> <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
  </div>
</div></div>
<header class="site-header"><div class="container">
  <a class="brand" href="{r or './'}">
    <img class="brand-mark-img" src="{r}assets/img/ilo-mark.png" alt="ILO" width="136" height="44">
    <span class="brand-name">Institute for Learning<br>Organizations</span>
  </a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="nav" aria-label="Main">
    {nav_html(r, path)}
    <a class="btn nav-cta" href="{r}contact/">Get In Touch</a>
  </nav>
  <!--LANGSWITCH-->
</div></header>
<main>
{body.replace("{r}", r)}
</main>
<footer class="site-footer"><div class="container">
  <div class="cols">
    <div>
      <img class="footer-logo" src="{r}assets/img/logo-ilo-light.png" alt="ILO – Institute for Learning Organizations">
      <p>Better learning shapes the future. We challenge and train leaders, giving them new lenses to build a lasting culture of improvement.</p>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul>
        <li><a href="{r or './'}">Home</a></li>
        <li><a href="{r}about/">About ILO</a></li>
        <li><a href="{r}resources/">Books &amp; Resources</a></li>
        <li><a href="{r}events/">Courses &amp; Events</a></li>
        <li><a href="{r}contact/">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>
        <li><a href="{r}sensei-mentorship/">Sensei Mentorship</a></li>
        <li><a href="{r}training/">Training</a></li>
        <li><a href="{r}learning-culture/">Learning Culture</a></li>
        <li><a href="{r}obeya/">Obeya</a></li>
        <li><a href="{r}e-learning/">E-learning</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in Touch</h4>
      <ul>
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


# Old URLs (from the WordPress version) and where they now live
REDIRECTS = {
    "open-resources/": "resources/",
    "courses/": "training/",
    "upcoming-webinars/": "events/",
    "workshops-and-webinars/": "events/",
    "estore/": "e-learning/",
    # Nov 2026 information architecture: pages that moved or merged
    "about-us/": "about/",
    "off-site-training/": "training/#off-site",
    "e-learning-services/": "e-learning/",
    "e-resources/": "resources/",
    "book-resources/": "resources/#books",
    "det-er-ledelse/": "book-resources/det-er-ledelse/",
    "trippel-l/": "events/trippel-l/",
    "obeya-dagseminar/": "events/obeya-day-seminar/",
    "past-events/": "events/",
}


def redirect(old, new):
    target = "../" * old.count("/") + new
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Page moved | Institute for Learning Organizations</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}")</script>
</head>
<body><p>This page has moved. <a href="{target}">Continue to the new page</a>.</p></body>
</html>
"""
    d = os.path.join(OUT, old)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(html)


def page_hero(title, sub, img, crumb=None, cta=True):
    c = f'<a href="{{r}}">Home</a> / {"<span>" + crumb + "</span> / " if crumb else ""}<span>{title}</span>'
    button = '<div class="btn-row"><a class="btn light" href="{r}contact/">Book a free consultation</a></div>' if cta else ""
    return f"""<section class="page-hero" style="background-image:url('{{r}}assets/img/{img}')"><div class="container">
  <div class="crumbs">{c}</div>
  <h1>{title}</h1>
  <p>{sub}</p>
  {button}
</div></section>"""


CTA = """<section class="cta-full"><div class="container">
  <div class="cta-band cta-v2">
    <img class="cta-petals" src="{r}assets/img/ilo-petals.png" alt="" aria-hidden="true">
    <div class="cta-text"><h2>Ready to build a learning organisation?</h2><p>Tell us where you are today, and we will suggest the next step for your team.</p></div>
    <div class="cta-actions">
      <a class="btn cta-btn" href="{r}contact/">Book a free consultation</a>
      <p class="cta-alt">or contact us directly: <a href="mailto:gabi@learnorg.global">gabi@learnorg.global</a> · <a href="tel:+4748287000">+47 48 28 70 00</a></p>
    </div>
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
    <p class="lead">We collaborate with globally recognized organisations like Leonardo Group Americas, Process Excellence, DigiLEAN, Obeya Association and Cabrera Research Lab to help organisations develop Lean, learning and innovation culture.</p>
  </div>
  <div class="grid cols-4">{cards}</div>
</div></section>"""


CLIENTS = [
    ("UDI (The Directorate of Immigration)", "Implemented a learning-organisation plan based on the Norwegian co-operation model, involving top management and unions. UDI manages applications from foreigners wishing to visit or reside in Norway."),
    ("Delta Group Jobb og Kompetanse", "Assisted in adopting the Everyday Learning framework through training and sensei dialogue, focusing on job placement, skills development and work training."),
    ("Equinor Mongstad", "Known for its refinery and oil supply base, Mongstad has developed good Lean practices, enhanced by sensei dialogue and training provided by Bjarne Berg Wig."),
    ("Avinor (with Flowit)", "Manages Norway's main airports and has developed effective Lean practices in recent years, with training for top and middle managers."),
    ("Eramet Norway", "The world's leading manganese producer aims to be a true learning organisation, with improvement direction through sensei dialogue with Bjarne Berg Wig."),
    ("Yara ASA", "A leading global fertilizer company, engaged in an ambitious improvement program developing its management system based on Lean thinking."),
    ("Stavne KF (Trondheim Kommune)", "Helps people return to work, supported by Bjarne Berg Wig in its Everyday Learning practices."),
    ("Vestre Toten Kommune", "Considered a leader in Lean and continuous improvement; developed video training material for internal management development."),
    ("Hennig-Olsen Is", "An ice cream manufacturer known for quality products and values, assisted in team development and Everyday Learning."),
    ("Sophies Minde Ortopedi", "Norway's leading orthopedic institution, developing a deep learning culture through long-term cooperation: sensei dialogue, training and e-resources."),
    ("Kristiansand Dyrepark", "Norway's leading amusement park, integrating Lean and learning-organisation practices with management training and dialogue."),
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
        ("vmcl-build-an-adaptive-organization", "VMCL: build an adaptive organisation"),
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
    prose_page(base + "systems-thinking-with-obeya/", "Systems Thinking with Obeya", "Resources for the book, chapter by chapter.", "obeya-wall.jpg", '<a href="{r}resources/">Books &amp; Resources</a>',
               "Links, videos, tools and templates for Systems Thinking with Obeya by Bjarne Berg Wig.",
               '<p class="lead">Welcome to the resource pages for the book. Here you will find links, videos, tools and templates that will speed up your learning. The pages are continually improved with new resources, and an e-course with a 9-step guide to developing Obeya in your organisation is in the works. Questions, ideas or resources to share: <a href="mailto:post@learnorg.global">post@learnorg.global</a>.</p>' + order + fragment("obeya-en"), "en")
    prose_page(base + "systemtenkning-med-obeya/", "Systemtenkning med Obeya", "Ressurser til boka, kapittel for kapittel.", "obeya-wall.jpg", '<a href="{r}resources/">Books &amp; Resources</a>',
               "Videoer, lenker, maler og læreeksempler til Systemtenkning med Obeya av Bjarne Berg Wig.",
               '<p class="lead">Her finner du videoer, lenker til vitenskapelige publikasjoner, maler og læreeksempler. Tips og spørsmål: <a href="mailto:post@learnorg.global">post@learnorg.global</a>.</p>' + order + fragment("obeya-no"), "nb")
    prose_page(base + "lean-ledelse/", "LEAN – Ledelse for lærende organisasjoner", "Ressurser til boka.", "gemba-team.jpg", '<a href="{r}resources/">Books &amp; Resources</a>',
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
{page_hero("Lærende organisasjoner", "Ressurser til boka, kapittel for kapittel.", "training-session.jpg", '<a href="{r}resources/">Books &amp; Resources</a>')}
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
        prose_page(f"{base}laerende-organisasjoner/kapittel-{n}/", f"Kapittel {n}: {lo_titles[n]}", "Lærende organisasjoner – ressurser", "desk-laptop.jpg", '<a href="{r}resources/">Books &amp; Resources</a>',
                   f"Ressurser til kapittel {n} i Lærende organisasjoner: {lo_titles[n]}.", fragment(f"lo-kapittel-{n}"), "nb",
                   extra=f'<nav class="chapter-nav">{prev}{nxt}</nav>')


def build():
    pdsa_svg = """<svg class="pdsa" viewBox="0 0 320 320" role="img" aria-labelledby="pdsa-title">
  <title id="pdsa-title">The Plan–Do–Study–Act learning cycle</title>
  <defs><marker id="pdsa-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#078586"/></marker></defs>
  <circle cx="160" cy="160" r="112" fill="none" stroke="#e5f2f2" stroke-width="36"/>
  <path d="M175 49 A112 112 0 0 1 271 145" fill="none" stroke="#078586" stroke-width="6" marker-end="url(#pdsa-arrow)"/>
  <path d="M271 175 A112 112 0 0 1 175 271" fill="none" stroke="#078586" stroke-width="6" marker-end="url(#pdsa-arrow)"/>
  <path d="M145 271 A112 112 0 0 1 49 175" fill="none" stroke="#078586" stroke-width="6" marker-end="url(#pdsa-arrow)"/>
  <path d="M49 145 A112 112 0 0 1 145 49" fill="none" stroke="#078586" stroke-width="6" marker-end="url(#pdsa-arrow)"/>
  <g font-family="League Spartan, Inter, sans-serif" font-weight="700" text-anchor="middle" fill="#282f3b" font-size="16">
    <text x="198" y="122">Plan</text>
    <text x="198" y="212">Do</text>
    <text x="122" y="212">Study</text>
    <text x="122" y="122">Act</text>
  </g>
  <text x="160" y="164" text-anchor="middle" font-family="League Spartan, Inter, sans-serif" font-weight="700" font-size="24" fill="#078586">PDSA</text>
  </svg>"""
    book_pages()

    # ---------- Home (text from the old Wix site, learnorg-backup.zip; redesigned layout Nov 2026) ----------
    tiles = [
        ("sensei-mentorship/", "Sensei Mentorship", "Leadership through dialogue", "mentoring"),
        ("training/", "Training", "On-site and off-site programs", "training"),
        ("obeya/", "Obeya", "See the whole system together", "obeya"),
        ("resources/", "Books & Resources", "Books, videos and downloads", "resources"),
        ("e-learning/", "E-learning", "E-courses, e-books, webinars", "elearning"),
        ("events/", "Courses & Events", "Seminars and programmes", "calendar"),
    ]
    tile_html = "".join(f'<a class="tile" href="{{r}}{h}">{icon(ic, "tile-icon")}<b>{t}</b><span>{d}</span><i>Explore →</i></a>' for h, t, d, ic in tiles)
    services = [
        ("training-session.jpg|mentoring", "Sensei Mentorship", "Leaders learn faster through challenge and dialogue with an experienced sensei mentor.", "sensei-mentorship/"),
        ("gemba-team.jpg|training", "Training", "Site training linked to the practical challenges of developing a learning and improvement culture, with Gemba learning trips.", "training/"),
        ("piemonte.jpg|offsite", "Off-site Training", "A change of scenery opens the mind: bring your team to our countryside retreat in Piemonte, Italy.", "training/#off-site"),
        ("team-laptops.jpg|elearning", "Books and e-learning", "E-books, e-courses and webinars that are affordable, available 24/7 and can be tailored to your organisation.", "e-learning/"),
        ("pdsa|culture", "Learning Culture", "Coaching and a video library to build a culture where everyone learns and improves every day.", "learning-culture/"),
    ]
    def card_img(img):
        img, ic = img.split("|")
        badge = f'<span class="card-icon">{icon(ic)}</span>'
        if img == "pdsa":
            return '<div class="card-media"><div class="card-img card-art">' + pdsa_svg + '</div>' + badge + '</div>'
        return f'<div class="card-media"><img class="card-img" src="{{r}}assets/img/{img}" alt="" loading="lazy">{badge}</div>'
    home_services = services
    def svc_card(n, img, t, d, h):
        return (f'<article class="card svc-card"><span class="card-num" aria-hidden="true">{n:02d}</span>{card_img(img)}'
                f'<div class="card-body"><h3><a href="{{r}}{h}">{t}</a></h3><p>{d}</p><a class="more" href="{{r}}{h}">Learn more</a></div></article>')
    svc = "".join(svc_card(n, *row) for n, row in enumerate(services, 1))
    svc += '<article class="card card-cta"><div class="card-body"><h3>Not sure where to start?</h3><p>Book a free consultation and we will help you find the right path.</p><a class="btn light" href="{r}contact/">Get in touch</a></div></article>'
    books = [
        ("book-resources/systems-thinking-with-obeya/", "book-obeya.jpg", "Systems Thinking with Obeya", "English", "Chapter resources, articles and templates.", "green"),
        ("book-resources/laerende-organisasjoner/", "book-laerende-organisasjoner.jpg", "Lærende organisasjoner", "Norsk", "Resources for chapters 1–12.", "teal"),
        ("book-resources/lean-ledelse/", "book-lean-ledelse.jpg", "LEAN Ledelse", "Norsk", "Course material and templates.", "red"),
        ("book-resources/det-er-ledelse/", "book-det-er-ledelse.jpg", "Det er Ledelse", "Norsk · e-bok", "Quality management for the 21st century.", "blue"),
    ]
    book_html = "".join(
        f'<a class="book-card tint-{tint}" href="{{r}}{h}"><span class="book-cover"><img src="{{r}}assets/img/{img}" alt="" loading="lazy"></span>'
        f'<div class="book-info"><small class="book-lang">{l}</small><b>{t}</b><p class="book-desc">{d}</p><small class="book-go">View resources →</small></div></a>'
        for h, img, t, l, d, tint in books)
    # Client logos: drop a file named <slug>.svg or <slug>.png into assets/img/clients/
    # and it replaces the name tile on the next build.
    clients_wall = [
        ("udi", "UDI", "Immigration"),
        ("equinor", "Equinor Mongstad", "Energy"),
        ("yara", "Yara", "Fertilizer"),
        ("avinor", "Avinor", "Airports"),
        ("eramet", "Eramet Norway", "Manganese"),
        ("delta-group", "Delta Group", "Work and skills"),
        ("trondheim-kommune", "Trondheim Kommune", "Municipality"),
        ("vestre-toten-kommune", "Vestre Toten Kommune", "Municipality"),
        ("hennig-olsen", "Hennig-Olsen Is", "Ice cream"),
        ("sophies-minde", "Sophies Minde Ortopedi", "Orthopedics"),
        ("kristiansand-dyrepark", "Kristiansand Dyrepark", "Amusement park"),
    ]
    def logo_tile(slug, name, sector):
        for ext in ("svg", "png", "webp", "jpg"):
            if os.path.exists(os.path.join(OUT, "assets", "img", "clients", f"{slug}.{ext}")):
                return f'<figure class="logo-tile"><img src="{{r}}assets/img/clients/{slug}.{ext}" alt="{name}" loading="lazy"><figcaption>{sector}</figcaption></figure>'
        return f'<figure class="logo-tile no-logo"><span class="wordmark">{name}</span><figcaption>{sector}</figcaption></figure>'
    logo_html = "".join(logo_tile(*c) for c in clients_wall)
    # Testimonials: add real client quotes here as (quote, name, role and organisation).
    # Until there are quotes, the preview shows marked placeholder slots; set SHOW_TESTIMONIAL_SLOTS = False before launch.
    TESTIMONIALS = []
    SHOW_TESTIMONIAL_SLOTS = True
    quote_mark = '<svg class="quote-mark" viewBox="0 0 48 36" aria-hidden="true"><path fill="currentColor" d="M0 36V21C0 9 6 2 18 0l2 5C13 7 10 11 10 17h9v19H0zm28 0V21c0-12 6-19 18-21l2 5c-7 2-10 6-10 12h9v19H28z"/></svg>'
    if TESTIMONIALS:
        t_cards = "".join(f'<figure class="testimonial">{quote_mark}<blockquote>{q}</blockquote><figcaption><b>{n}</b><span>{r_}</span></figcaption></figure>' for q, n, r_ in TESTIMONIALS)
    elif SHOW_TESTIMONIAL_SLOTS:
        t_cards = "".join(f'<figure class="testimonial is-placeholder">{quote_mark}<blockquote>Client quote to come: two or three sentences about what changed after working with ILO.</blockquote><figcaption><b>Client name</b><span>Role, organisation</span></figcaption></figure>' for _ in range(3))
    else:
        t_cards = ""
    testimonials_html = f"""<section class="section alt testimonials"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Testimonials</span>
    <h2>What our clients say</h2>
  </div>
  <div class="grid cols-3">{t_cards}</div>
</div></section>""" if t_cards else ""
    home = f"""
<section class="hero hero-home" style="background-image:url('{{r}}assets/img/obeya-wall.jpg')"><div class="container">
  <span class="eyebrow">INSTITUTE FOR LEARNING ORGANIZATIONS · NORWAY</span>
  <h1>We help organisations learn faster and improve every day</h1>
  <p>Sensei mentoring, hands-on training and e-learning in Lean and systems thinking, for leaders and teams in businesses and municipalities.</p>
  <div class="btn-row">
    <a class="btn light" href="{{r}}services/">Explore our services</a>
    <a class="btn ghost" style="color:#fff;border-color:#fff" href="{{r}}contact/">Free consultation</a>
  </div>
</div></section>

<div class="container"><nav class="tiles" aria-label="Explore the site">{tile_html}</nav></div>

<section class="section purpose"><div class="container mission">
  <div>
    <span class="eyebrow">Our Purpose</span>
    <h2>Change is faster than ever. Learning has to be faster still.</h2>
    <p class="lead">Organisations that want to survive complex, rapid change need to become real learning organisations: systems of people who master the art of learning together. That’s what we help leaders build.</p>
    <blockquote class="purpose-quote"><p>“Learning is a source of innovation.”</p><cite>W. Edwards Deming</cite></blockquote>
    <ul class="purpose-points">
      <li>{icon("obeya")}<span>See the whole system</span></li>
      <li>{icon("culture")}<span>Learn by doing</span></li>
      <li>{icon("mentoring")}<span>Lead through dialogue</span></li>
    </ul>
    <div class="btn-row"><a class="btn ghost" href="#meet-ilo">Meet the team</a></div>
  </div>
  <figure class="purpose-figure"><img src="{{r}}assets/img/training-session.jpg" alt="Bjarne Berg Wig teaching systems thinking" loading="lazy"><figcaption>Bjarne Berg Wig teaching systems thinking</figcaption></figure>
</div></section>

<section class="numbers"><div class="container numbers-row">
  <div><strong>30+</strong><span>years in continuous improvement and learning organisations</span></div>
  <div><strong>7</strong><span>professional books, used in industry and universities</span></div>
  <div><strong>100s</strong><span>of leaders trained through practical programs</span></div>
  <div><strong>11</strong><span>major Norwegian organisations as clients</span></div>
</div></section>

<section class="section alt svc-section"><img class="svc-petals" src="{{r}}assets/img/ilo-petals.png" alt="" aria-hidden="true"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">How we help</span>
    <h2>We challenge your thinking and transform your organisation</h2>
  </div>
  <div class="grid cols-3">{svc}</div>
</div></section>

<section class="section feature-band"><div class="container feature">
  <img src="{{r}}assets/img/book-obeya.jpg" alt="Systems Thinking with Obeya book cover" loading="lazy">
  <div>
    <span class="eyebrow">Featured book</span>
    <h2>Systems Thinking with Obeya</h2>
    <p>Bjarne Berg Wig's guide to using the Obeya room to see the whole system, align leaders and learn faster together. Chapter resources, articles and templates are free online.</p>
    <div class="btn-row">
      <a class="btn light" href="https://www.amazon.com/Systems-Thinking-Obeya-Bjarne-Berg/dp/826932891X" target="_blank" rel="noopener">Order the book</a>
      <a class="btn ghost" href="{{r}}book-resources/systems-thinking-with-obeya/">Chapter resources</a>
      <a class="btn ghost" href="{{r}}obeya/">Obeya for your organisation</a>
    </div>
  </div>
</div></section>

<section class="section books-section"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">E-resources</span>
    <h2>Free companion resources for Bjarne's books</h2>
    <p class="lead">Chapter notes, templates, videos and downloads.</p>
  </div>
  <div class="books-row">{book_html}</div>
  <p class="center"><a class="more-link" href="{{r}}resources/#library">Browse the download library →</a></p>
</div></section>

<section class="section" id="meet-ilo"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Meet ILO</span>
    <h2>Making systems thinking affordable and accessible</h2>
    <p class="lead">ILO evolved from the Total Quality Management Center Norway. Our two resident experts help employees and leaders become systems thinkers through mentorship, on-site training and e-learning.</p>
  </div>
  <div class="people">
    <article class="person-card"><img src="{{r}}assets/img/bjarne-berg-wig.jpg" alt="Bjarne Berg Wig" loading="lazy"><div><span class="role">Author · Sensei</span><h3>Bjarne Berg Wig</h3><p>More than 30 years in quality management and Lean, including as Quality and Innovation Manager at Hydro Agri Europe (now Yara). He has written 7 professional books and is a founder of LOS Norge, the Society for Learning Organizations in Norway.</p><a class="more-link" href="{{r}}about/#bjarne-berg-wig">Read full bio →</a></div></article>
    <article class="person-card"><img src="{{r}}assets/img/samer-hamadeh.jpg" alt="Samer Hamadeh" loading="lazy"><div><span class="role">Resident expert</span><h3>Samer Hamadeh</h3><p>Specialist in learning culture transformation. Samer works alongside Bjarne on ILO's mentorship, training and seminars, helping organisations build a culture where everyone learns and improves.</p><a class="more-link" href="{{r}}about/#samer-hamadeh">Read full bio →</a></div></article>
  </div>
</div></section>

{testimonials_html}
<section class="section trust"><div class="container">
  <p class="trust-label">Trusted by leading Norwegian organisations</p>
  <div class="logo-wall">{logo_html}</div>
</div></section>
{CTA}
"""
    page("", "Home", "The Institute for Learning Organizations helps leaders and organisations become learning organisations through sensei mentorship, e-learning, training and Obeya.", home)

    # ---------- Services ----------
    svc_rows = [
        ("hero-coffee.jpg", "Sensei Mentorship", "Transformation through challenge and dialogue", "Our sensei partnership is helping leaders to learn faster through challenging and dialogue. Leadership for complex systems needs systems thinking and deep understanding of the hidden drivers of improvement and innovation. Whether you are advanced in systems thinking or have just started, enlist the expertise of our sensei mentor to help you with learning and growing through your journey.", "sensei-mentorship/"),
        ("team-laptops.jpg", "E-learning", "What you need, when you need it, how you need it.", "ILO provides e-books, e-courses and webinars for learning organisations. These digital resources reflect the best knowledge available on learning leadership. It's affordable and available 24/7. We can also create customized e-learning programs and webinars for learning organisations.", "e-learning/"),
        ("piemonte.jpg", "Training", "Make your workplace the primary campus.", "We tailor site training linked to the practical challenges of developing a learning and improvement culture. We also do training with gemba learning trips to leading Norwegian companies and municipalities. A change of scenery helps open the mind to new ways of thinking: we can also bring your team to our countryside retreat in Italy for our off-site program.", "training/"),
    ]
    svc_cards = "".join(svc_card(n, *row) for n, row in enumerate(home_services, 1)) + svc_card(
        len(home_services) + 1, "obeya-wall.jpg|obeya", "Obeya", "Use the Obeya room to see the whole system, align leaders and learn faster together.", "obeya/")
    services_page = f"""
{page_hero("Services", "Sensei mentorship, e-learning and training for learning organisations.", "gemba-team.jpg")}
<section class="section"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">What we offer</span>
    <h2>Ways to work with us</h2>
    <p class="lead">Every programme is tailored to your organisation, from a single sensei conversation to a full learning-culture transformation.</p>
  </div>
  <div class="grid cols-3">{svc_cards}</div>
</div></section>
{CTA}
"""
    page("services/", "Services", "Sensei mentorship, e-learning and training from the Institute for Learning Organizations.", services_page)

    # ---------- Sensei ----------
    pdsa_steps = [
        ("Plan", "Plan a change or a test aimed at improvement."),
        ("Do", "Carry it out, preferably on a small scale."),
        ("Study", "Study the results. What did we learn?"),
        ("Act", "Adopt the change, abandon it, or run through the cycle again."),
    ]
    steps_html = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in pdsa_steps)
    process = [
        ("Talk", "A free consultation: tell us where you are today and what you want to change."),
        ("Plan", "Together we agree the goals, the people involved and how we will learn."),
        ("Mentor", "Regular sensei sessions: challenge, dialogue and practice in your own workplace."),
        ("Review", "We study the results together and decide the next step."),
    ]
    process_html = "".join(f'<li><span class="process-num">{n}</span><b>{t}</b><p>{d}</p></li>' for n, (t, d) in enumerate(process, 1))
    sensei = f"""
{page_hero("Sensei Mentorship", "Transformation through challenge and dialogue.", "hero-coffee.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container split">
  <div>
    <span class="eyebrow">Sensei</span>
    <h2>Look beyond the borders of your first understanding</h2>
    <p class="lead">Sensei is encouragement to look beyond the borders of your first understanding of the current situation, toward a deeper meaning.</p>
    <p>Whether you are advanced in systems thinking or just now starting to use the method, we recommend you enlist the expertise of our sensei mentor to help you with learning and growing through your journey.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Let us know how we can help you</a></div>
  </div>
  <figure class="pdsa-card">
    {pdsa_svg}
    <ol class="pdsa-steps">{steps_html}</ol>
  </figure>
</div></section>
<section class="section alt"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">How we work</span>
    <h2>From first conversation to lasting change</h2>
  </div>
  <ol class="process">{process_html}</ol>
</div></section>
{CTA}
"""
    page("sensei-mentorship/", "Sensei Mentorship", "Sensei mentorship from ILO: transformation through challenge and dialogue.", sensei)

    # ---------- Training ----------
    training = f"""
{page_hero("Training", "Make your workplace the primary campus.", "training-session.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container">
  <div class="split" style="margin-bottom:96px">
    <img src="{{r}}assets/img/training-session.jpg" alt="On-site training" loading="lazy">
    <div><span class="eyebrow">On-site Training</span><h2>Book an expert to come to your company</h2>
      <p class="lead">Book an expert to come to your company for hands-on training.</p>
      <p>We believe that the best way to learn is through a combination of learning together, e-learning and practical application. Our experts provide custom courses that are tailored to the needs of your company and team members.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact us</a></div></div>
  </div>
  <div class="split reverse" id="off-site" style="margin-bottom:96px;scroll-margin-top:120px">
    <img src="{{r}}assets/img/piemonte.jpg" alt="Vineyards in Piemonte, Italy" loading="lazy">
    <div><span class="eyebrow">Off-site Training</span><h2>A change of scenery helps open the mind</h2>
      <p class="lead">Take your team off-site to ILO's Albergo del Vino, surrounded by the vineyards of Piemonte, Italy.</p>
      <p>Here your team can fully focus on "learning how to learn together". Training programs are tailored to the needs of your organisation and cover all key concepts to help participants become systems thinkers. This off-site program is excellent for team building too.</p>
      <p>In advance of your visit we will discuss the goals and needs of your team. From this we will create a custom program so that your team receives exactly what it needs.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Plan an off-site programme</a></div></div>
  </div>
  <div class="split">
    <img src="{{r}}assets/img/gemba-team.jpg" alt="Team on a Gemba visit" loading="lazy">
    <div><span class="eyebrow">Gemba Learning Trips</span><h2>Learn from the people who make the change</h2>
      <p class="lead">Crucial to learning is to go and see, communicate and learn from practitioners.</p>
      <p>We provide training and learning in partnership with leading companies and municipalities in Norway, Italy and the UK in the field of Lean and learning culture. We organize visits to relevant organisations so participants get a chance to see how improvement and change are made, and discuss specific case studies with the transformation leaders behind them. This combined training and gemba walks provide the ultimate learning experience.</p>
      <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact us</a></div></div>
  </div>
</div></section>
{CTA}
"""
    page("training/", "Training", "On-site training, off-site training in Piemonte, Italy, and Gemba learning trips from ILO.", training)

    # ---------- Learning Culture (restored from the old Wix "coaching" and "about" pages) ----------
    videos = [
        ("fYoppX3VHIY", "Toyota Kata – Mike Rother", "Mike Rother, author of <em>Toyota Kata</em>, at the Lean Summit 2012."),
        ("zDZFcDGpL4U", "Changing Education Paradigms", "RSA Animate of a talk by Sir Ken Robinson."),
        ("STTwZGNvLmM", "Applying the Lens of Profound Knowledge", "Robert Lloyd, PhD, from the IHI Open School course QI101."),
        ("xKv--YA8XJE", "Deming's System of Profound Knowledge", "Robert Lloyd, PhD, from the IHI Open School course QI101."),
    ]
    _unused = "".join(f'<div><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v}" title="{t}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><h3>{t}</h3><p class="note">{d}</p></div>' for v, t, d in videos)
    culture = f"""
{page_hero("Learning Culture Transformation", "From seeing work as execution to seeing work as continuous learning and improvement.", "training-session.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container"><div class="prose">
  <p class="lead">Learning Culture Transformation (LCT) is the shift from seeing work as execution to seeing work as continuous learning and improvement – seeing the organisation as a complex adaptive system that adapts to change through learning.</p>
  <h2>Learning culture</h2>
  <p>LCT is a breakaway from Taylor's "scientific management" model of centralized command-and-control organisations: from command and control to challenging and developing learners. LCT is about deep respect for people and building on people's innate capacity to learn. Dr W. Edwards Deming (1900–1993) put it this way in <em>The New Economics</em>:</p>
  <blockquote>"One is born with a natural inclination to learn. Learning is a source of innovation. One inherits a right to enjoy his work. Good management helps us to nurture these positive innate attributes of people."</blockquote>
  <h2>What is learning?</h2>
  <p>Learning is the process of developing and improving our mental models – how we see and understand – so we navigate the real world better. It requires a good understanding of the thinking process and of how we acquire knowledge through seeing, dialogue and practical trials. Two insights are key:</p>
  <ul>
    <li>People are born with learning capacity. Present management practice has reduced these skills, so they have to be nurtured.</li>
    <li>We all have biases in how we see and interpret the real world (mental models). We need to understand these biases and use that understanding to become better thinkers.</li>
  </ul>
  <h2>Complex adaptive systems</h2>
  <p>A complex adaptive system (CAS) is able to adapt to change for better interaction with the real world. In an environment of rapid technological, social, geographical and environmental change, the capacity for real learning is crucial for survival. Nature itself is the best teacher of complex adaptive systems.</p>
  <h2>What is a learning organisation?</h2>
  <p>An organisation that acquires, creates, interprets, transmits, shares and retains knowledge, and consciously adapts its behaviour to reflect new knowledge and insights.</p>
</div></div></section>
{CTA}
"""
    page("learning-culture/", "Learning Culture Transformation", "Learning Culture Transformation: seeing work as continuous learning and the organisation as a complex adaptive system. With a video library.", culture)

    # ---------- E-learning ----------
    books = [
        ("book-laerende-organisasjoner.jpg", "Lærende organisasjoner", "Norwegian · Gyldendal", """<p>The book gives leaders, union representatives and other change leaders the knowledge needed to move from an outdated system of goal management, bureaucracy and hierarchy – to a society that removes waste of all forms and frees the vast and often hidden resources in all people.</p>
<p>It describes the necessary shift from goal and result management to real learning organisations and learning systems, in three parts: <em>Past</em> asks why we ended up in this disorder and how we get out of it; <em>Present</em> is about going from “introducing Lean” and continuous improvement to becoming a true learning organisation; <em>Future</em> asks how we develop self-organizing and open, participatory organisations.</p>
<p>A red thread throughout the book is systems thinking – awareness of how systems work and how we think about them. To transform organisations, we must change how we think. The book is for people who want to become better thinkers.</p>""",
         '<a class="btn" href="https://www.gyldendal.no/Faglitteratur/OEkonomi-og-administrasjon/Samfunnsoekonomi/Laerende-organisasjoner" target="_blank" rel="noopener">Buy</a><a class="btn ghost" href="{r}book-resources/laerende-organisasjoner/">Chapter resources</a>'),
        ("book-lean-ledelse.jpg", "LEAN – Ledelse for lærende organisasjoner", "Norwegian · Gyldendal", """<p>Lean is about creating products and services with the most value and least possible loss of resources, by focusing on flow, transparent processes and continuous improvement.</p>
<p>This book and its digital resources are designed for a breakthrough for Lean: a turning point where continuous improvement and learning in the workplace become commonplace, and all managers and employees in municipalities and businesses are active in improvement and renewal. It is about moving from work as effective execution to seeing work as a learning process.</p>
<p><strong>Part I</strong> explains how to develop a breakthrough strategy. <strong>Part II</strong> covers the methods and tools for introducing and developing Lean in a municipal or private enterprise. <strong>Part III</strong>, new in this edition, covers real learning organisations: learning leadership and the use of guidance, coaching and problem-solving dialogue – what remains after the term Lean goes into history.</p>""",
         '<a class="btn" href="https://www.gyldendal.no/Faglitteratur/Arbeidsliv/Ledelse/Lean2" target="_blank" rel="noopener">Buy</a><a class="btn ghost" href="{r}book-resources/lean-ledelse/">Course material</a>'),
        ("book-quality-craft.jpg", "Quality Improvement as a Craft", "English · Handbook for practitioners", """<p><em>Quality Improvement as a Craft</em> (Hydro Media, 1996) was the main training material for continuous improvement teams in Norway for many years. It is still very valid and gives an overview of many of the methods and tools we know today under the name Lean. The book is still used in teaching at academic courses.</p>
<p>Please contact us with your name and e-mail address and we will follow up on your book order.</p>""",
         '<a class="btn" href="{r}contact/">Contact Us</a>'),
        ("book-det-er-ledelse.jpg", "Det er ledelse", "Norwegian · E-book", """<p>E-bok «Det er ledelse» – kvalitetsledelse for det 21. århundret. Dette er læreboka i TKL/TQM ved flere høgskoler og universiteter. Her finner du også en mengde ressurser knyttet til opplæring i kvalitetsledelsesfaget.</p>""",
         '<a class="btn" href="https://issuu.com/tqm2/docs/det_er_ledelse_8" target="_blank" rel="noopener">Kjøp boka og last den ned</a><a class="btn ghost" href="{r}book-resources/det-er-ledelse/">Read more</a>'),
    ]
    books.insert(0, ("book-obeya.jpg", "Systems Thinking with Obeya", "English · Norwegian edition: Systemtenkning med Obeya", """<p>Bjarne Berg Wig's guide to using the Obeya room to see the whole system, align leaders and learn faster together. The free companion pages follow the book chapter by chapter, with videos, articles, tools and templates.</p>""",
         '<a class="btn" href="https://www.amazon.com/Systems-Thinking-Obeya-Bjarne-Berg/dp/826932891X" target="_blank" rel="noopener">Order the book</a><a class="btn ghost" href="{r}book-resources/systems-thinking-with-obeya/">Chapter resources</a><a class="btn ghost" href="{r}book-resources/systemtenkning-med-obeya/">Norsk utgave</a>'))
    book_html = "".join(
        f'<div class="book"><img src="{{r}}assets/img/{img}" alt="Cover of {t}" loading="lazy"><div><span class="lang">{lang}</span><h3 style="font-size:1.6rem">{t}</h3>{d}<div class="btn-row">{btn}</div></div></div>'
        for img, t, lang, d, btn in books
    )
    elearn = f"""
{page_hero("E-learning and Webinars", "Key learning resources: what you need, when you need it, and how you need it.", "team-laptops.jpg", '<a href="{r}events/">Courses &amp; Events</a>')}
<section class="section"><div class="container">
  <div class="grid cols-3">
    <article class="card"><img class="card-img" src="{{r}}assets/img/desk-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">E-courses</span><h3>From beginner to advanced</h3>
      <p>We offer e-courses from beginners to advanced systems thinkers. After completing the e-book and e-course, you will be equipped to implement concrete actions to achieve faster learning and improved interaction throughout your organisation. Contact Bjarne Berg Wig to hear more about the course.</p>
      <a class="more" href="https://educate.potential.com/courses/laerende-hverdag/" target="_blank" rel="noopener">Register now</a>
    </div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/butterflies.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">E-books</span><h3>Lærende hverdag: Everyday Learning</h3>
      <p>A practical e-book by Bjarne Berg Wig on making learning part of the working day. Available in Norwegian.</p>
      <a class="more" href="https://issuu.com/tqm2/docs/l_rende_hverdag_e-bok_versjon_1.0" target="_blank" rel="noopener">View e-book</a>
    </div></article>
    <article class="card"><img class="card-img" src="{{r}}assets/img/cafe-laptop.jpg" alt="" loading="lazy"><div class="card-body">
      <span class="tag">Webinars</span><h3>Everyday Learning</h3>
      <p>Next webinar: how to frame the transformation to a learning culture. Hosts: Bjarne Berg Wig and Samer Hamadeh. Date to be announced – send us your name and e-mail address and we will follow up with details.</p>
      <a class="more" href="{{r}}contact/">Contact us</a>
    </div></article>
  </div>
</div></section>
<section class="section alt"><div class="container center">
  <span class="eyebrow">Books</span>
  <h2>Looking for Bjarne's books?</h2>
  <p class="lead">All of the books, with their chapter resources and downloads, are together under Books &amp; Resources.</p>
  <div class="btn-row" style="justify-content:center"><a class="btn" href="{{r}}resources/#books">Go to Books &amp; Resources</a></div>
</div></section>
{CTA}
"""
    page("e-learning/", "E-learning and Webinars", "E-courses, e-books, webinars and books on Lean, systems thinking and learning organisations by Bjarne Berg Wig.", elearn)

    # ---------- E-resources (videos from the old Wix "E-resources" page) ----------
    vids = "".join(f'<div><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v}" title="{t}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><h3>{t}</h3><p class="note">{d}</p></div>' for v, t, d in videos)
    eres = f"""
{page_hero("Books & Resources", "Bjarne Berg Wig's books, with free companion pages, videos and downloads.", "desk-laptop.jpg")}
<section class="section" id="books" style="scroll-margin-top:120px"><div class="container">
  <div class="section-head">
    <span class="eyebrow">Books</span>
    <h2>Books by Bjarne Berg Wig</h2>
    <p class="lead">Each book has free companion pages: chapter notes, videos, templates and downloads. Most of the material is in Norwegian.</p>
  </div>
  {book_html}
</div></section>
<section class="section alt" id="videos" style="scroll-margin-top:120px"><div class="container">
  <div class="section-head"><span class="eyebrow">Video library</span><h2>Recommended videos</h2></div>
  <div class="video-grid">{vids}</div>
</div></section>
{pdf_library().replace('section alt', 'section')}
{CTA}
"""
    page("resources/", "Books & Resources", "Books by Bjarne Berg Wig with free companion resources, a video library and downloadable material on learning organisations, Lean and systems thinking.", eres)

    det = f"""
{page_hero("Det er Ledelse", "Kvalitetsledelse for det 21. århundret.", "desk-laptop.jpg", '<a href="{r}resources/">Books &amp; Resources</a>')}
<section class="section"><div class="container split">
  <img src="{{r}}assets/img/book-det-er-ledelse.jpg" alt="Det er Ledelse" loading="lazy" style="max-width:320px;justify-self:center;box-shadow:none">
  <div>
    <span class="eyebrow">E-bok</span>
    <h2>Seize the opportunity</h2>
    <p class="lead">E-bok «Det er Ledelse» – Kvalitetsledelse for det 21. århundret.</p>
    <p>Dette er læreboka i TKL/TQM ved flere høgskoler og universitet. Her vil du også finne en mengde ressurser som er knyttet til opplæring i kvalitetsledelsesfaget.</p>
    <div class="btn-row"><a class="btn" href="https://issuu.com/tqm2/docs/det_er_ledelse_8" target="_blank" rel="noopener">Kjøp boka og last den ned</a></div>
  </div>
</div></section>
{CTA}
"""
    page("book-resources/det-er-ledelse/", "Det er Ledelse", "E-boka Det er Ledelse – kvalitetsledelse for det 21. århundret, av Bjarne Berg Wig.", det, "nb")

    # ---------- Obeya ----------
    obeya = f"""
{page_hero("Obeya", "A room for seeing the whole system and learning faster together.", "obeya-wall.jpg", '<a href="{r}services/">Services</a>')}
<section class="section"><div class="container split">
  <div>
    <span class="eyebrow">Obeya for your organisation</span>
    <h2>See together, think together, try together</h2>
    <p class="lead">Obeya is a visual room for collaboration between the different functions of an organisation, and an architecture for radically better collaboration across boundaries.</p>
    <p>By visualising (seeing together), reflecting and trying out solutions, we learn faster and waste less time on papers sent back and forth. Obeya is also the room for developing a better understanding of systems: better systems thinking.</p>
    <p>ILO helps leadership teams set up and run their own strategic Obeya, through mentoring, training and day seminars where organisations share experience. We are also working on an e-course with a 9-step guide to developing Obeya in your organisation or community.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Talk to us about Obeya</a><a class="btn ghost" href="{{r}}events/obeya-day-seminar/">Obeya Day Seminar</a></div>
  </div>
  <img src="{{r}}assets/img/obeya-day-seminar.jpg" alt="Obeya day seminar in Bergen" loading="lazy">
</div></section>
<section class="section alt"><div class="container">
  <a class="video-block" href="https://www.youtube.com/watch?v=Vy8tfaOHzAo" target="_blank" rel="noopener">
    <img src="{{r}}assets/img/obeya-wall.jpg" alt="" loading="lazy">
    <span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M8 5v14l11-7z"/></svg></span>
    <div class="video-caption"><span class="eyebrow">Watch on YouTube</span><b>The building blocks of systems thinking (DSRP)</b></div>
  </a>
</div></section>
<section class="section"><div class="container split">
  <img src="{{r}}assets/img/book-obeya.jpg" alt="Systems Thinking with Obeya book cover" loading="lazy" style="max-width:300px;justify-self:center;box-shadow:none">
  <div>
    <span class="eyebrow">The book</span>
    <h2>Systems Thinking with Obeya</h2>
    <p>Bjarne Berg Wig's book explains the method chapter by chapter, and its free companion pages add videos, articles, tools and templates. It is also available in Norwegian as <em>Systemtenkning med Obeya</em>.</p>
    <div class="btn-row"><a class="btn" href="{{r}}book-resources/systems-thinking-with-obeya/">Chapter resources</a><a class="btn ghost" href="https://www.amazon.com/Systems-Thinking-Obeya-Bjarne-Berg/dp/826932891X" target="_blank" rel="noopener">Order the book</a></div>
  </div>
</div></section>
{CTA}
"""
    page("obeya/", "Obeya", "Obeya for your organisation: ILO helps leadership teams set up and run a strategic Obeya room to see the whole system and learn faster together.", obeya)

    # ---------- Trippel L ----------
    cal = [
        ("Modul 1. Lean og systemtenkning", ["Januar – selvstudier", "1. februar – nettbasert oppstartsamling", "27. februar – nettbasert samling", "13.–14. mars – lunsj-til-lunsj-samling på Aker Tranby ved Drammen"]),
        ("Modul 2. Læringskultur og Obeya", ["20. mars – nettbasert samling", "4. april – nettbasert samling", "17. og 18. april – samling hos Toyota Jæger Automobil i Bergen", "Utvikling av egen strategisk Obeya"]),
        ("Modul 3. Lærende lederskap", ["22. mai – nettbasert samling", "13.–14. juni – fysisk samling hos Flowit i Haugesund", "Oppgaveinnlevering", "12.–13. september – offisiell utdeling av sertifikater på Lean-konferansen i Stavanger (frivillig)"]),
    ]
    calhtml = "".join(f'<div class="pdf-group"><h3>{m}</h3><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>" for m, items in cal)
    trippel = f"""
{page_hero("Trippel L – Lærende lederskap", "Et kurs i samarbeid mellom Institute for Learning Organizations og Flowit.", "training-session.jpg", '<a href="{r}events/">Kurs og arrangementer</a>')}
<section class="section"><div class="container"><div class="prose">
  <p class="note">Kurset ble gjennomført fra desember 2023 til juni 2024. Ta kontakt for å høre om neste gjennomføring.</p>
  <p class="lead">Mer enn noen gang trenger vi å forbedre kvalitet i vårt lederskap. Lærende lederskap utløser en kjedereaksjon av forbedringer og læring. Alle virksomheter er «komplekse tilpasningssystemer» der raskere felles læring er nøkkelen til suksess. Det starter med hvordan vi tenker: utvikling av mentale modeller som er tettere på hvordan virkeligheten egentlig er. Dette kurset handler om å forstå systemer og å forstå og forbedre vår tenkning.</p>
  <p>Programmet er et samarbeid mellom Institute for Learning Organizations og Flowit. Det faglige innholdet er blant annet utviklet som del av et «PhD»-program som Bjarne Berg Wig har gått i regi av Cabrera Research Lab i Boston, og som del av to F&amp;U-programmer støttet av Norges forskningsråd. Det første programmet (2020–2022) resulterte i metodikk for å identifisere sterke adaptive læringskulturer (LOS-speilet). Det andre F&amp;U-programmet, ALIOS (akselerert læring i organisasjoner og samfunn), skal utvikle metoder for bedre tenkemodenhet, systemtenkning og systemledelse, der vi knytter an til verdens ledende forskning på området. Gjesteforelesere kommer fra F&amp;U-teamet i ALIOS: Sidsel W. Storaas, Johannes Borge, Kari Heggholmen, Einar Jørgensen og John Richard Hansen.</p>
  <p>Kurset gir deg et betydelig løft videre, både individuelt ved at du tenker bedre og mer bevisst, og for din virksomhet ved at ditt lederskap får langt større virkning. Som på tidligere Lean-kurs knytter vi læring til de konkrete utfordringene dere står i, så kurset gir dobbel virkning. Alle deltakerne har flere år med Lean og kontinuerlig forbedring i egen virksomhet. Trippel L-programmet skal utløse potensial i deg og dine medarbeidere som du nesten ikke trodde var mulig.</p>
  <p>En vesentlig nytteverdi for deg vil være å studere sammen med noen av Norges beste på området.</p>
  <h2>Kalender</h2>
</div>
  <div class="grid cols-3" style="margin-top:24px">{calhtml}</div>
  <div class="prose" style="margin-top:32px">
  <p>Lærebøker sendes ut når dere har meldt dere på. Alt materiell er tilgjengelig på egen kursportal 24/7. Sertifikat deles ut på Lean-konferansen i september.</p>
  <p><strong>Bjarne Berg Wig</strong>, Institute for Learning Organizations · <strong>Thorleif K. Sire</strong>, Flowit</p>
  </div>
</div></section>
{CTA}
"""
    page("events/trippel-l/", "Trippel L – Lærende lederskap", "Trippel L – Lærende lederskap: kurs i systemtenkning, læringskultur og Obeya fra Institute for Learning Organizations og Flowit.", trippel, "nb")

    # ---------- Obeya dagseminar ----------
    seminar = f"""
{page_hero("Obeya dagseminar", "Obeya – raskere felles læring.", "obeya-day-seminar.jpg", '<a href="{r}events/">Kurs og arrangementer</a>')}
<section class="section"><div class="container split">
  <div>
    <p class="note">Seminaret ble holdt i Bergen 17. oktober 2024. Ta kontakt for å høre om neste Obeya-seminar.</p>
    <h2>Obeya – raskere felles læring</h2>
    <p class="lead">Obeya er et visuelt rom for samarbeid mellom ulike funksjoner i en virksomhet. Obeya er arkitektur for radikalt bedre samspill på tvers.</p>
    <p>Ved å visualisere (se sammen), reflektere og prøve ut løsninger skapes raskere læring, og vi reduserer tidssløsing med papirer som sendes hit og dit. Obeya er også rommet for å utvikle bedre forståelse for systemer, bedre systemtenkning.</p>
    <p>På fagseminarer lærer vi om Obeya og deler erfaringer mellom ulike virksomheter. Vi er bare i begynnelsen på denne neste Lean-reisen, som vil gi oss dramatisk bedre læring.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Kontakt oss</a></div>
  </div>
  <img src="{{r}}assets/img/obeya-day-seminar.jpg" alt="Obeya dagseminar i Bergen" loading="lazy">
</div></section>
{CTA}
"""
    page("events/obeya-day-seminar/", "Obeya dagseminar", "Obeya dagseminar: Obeya – raskere felles læring. Fagseminar om Obeya fra Institute for Learning Organizations.", seminar, "nb")

    # ---------- Past events ----------
    # Upcoming events: add (date, title, place, text, link) here; the section only shows when the list is not empty.
    UPCOMING = []
    upcoming_html = ""
    if UPCOMING:
        upcoming_html = '<section class="section"><div class="container"><div class="section-head"><span class="eyebrow">Upcoming</span><h2>Coming up</h2></div>' + "".join(
            f'<div class="event"><div class="date"><b>{d}</b></div><div><h3>{t}</h3><div class="meta">{pl}</div><p>{tx}</p><a class="more-link" href="{lk}">Read more →</a></div></div>' for d, t, pl, tx, lk in UPCOMING) + '</div></section>'
    past = f"""
{page_hero("Courses & Events", "Seminars, programmes and conferences from ILO.", "obeya-wall.jpg")}
{upcoming_html}
<section class="section"><div class="container">
  <div class="grid cols-3 event-links">
    <article class="card"><div class="card-body"><span class="tag">E-learning</span><h3><a href="{{r}}e-learning/">E-learning and webinars</a></h3><p>E-courses, e-books and webinars, available when you need them.</p><a class="more" href="{{r}}e-learning/">Learn more</a></div></article>
    <article class="card"><div class="card-body"><span class="tag">Programme · 2023–2024</span><h3><a href="{{r}}events/trippel-l/">Trippel L – Learning Leadership</a></h3><p>A course in systems thinking, learning culture and Obeya, run with Flowit.</p><a class="more" href="{{r}}events/trippel-l/">Learn more</a></div></article>
    <article class="card"><div class="card-body"><span class="tag">Seminar · Bergen 2024</span><h3><a href="{{r}}events/obeya-day-seminar/">Obeya Day Seminar</a></h3><p>Obeya – faster learning together. Ask us about the next seminar.</p><a class="more" href="{{r}}events/obeya-day-seminar/">Learn more</a></div></article>
  </div>
</div></section>
<section class="section alt" id="past"><div class="container">
  <div class="section-head"><span class="eyebrow">Past events</span><h2>Seminars, study trips and conferences</h2></div>
  {past_events()}
</div></section>
{CTA}
"""
    page("events/", "Courses & Events", "Courses, seminars and events from the Institute for Learning Organizations, with past events, seminars and study trips.", past)

    # ---------- About Us ----------
    about = f"""
{page_hero("About ILO", "The people behind the Institute for Learning Organizations.", "obeya-wall.jpg")}
<section class="section"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Who we are</span>
    <h2>Making systems thinking affordable and accessible</h2>
    <p class="lead">The Institute for Learning Organizations (ILO) was created to make the knowledge of systems thinking affordable and accessible. It evolved from the Total Quality Management Center Norway. ILO has two resident experts, Bjarne Berg Wig and Samer Hamadeh. Together they offer over 30 years of experience in continuous improvement and developing real learning organisations.</p>
    <p class="lead">Their focus is to help employees and leaders become systems thinkers, and to practically apply this thinking within their organisations, through a combination of mentorship, on-site training and e-learning.</p>
  </div>
</div></section>

<section class="section alt" id="bjarne-berg-wig"><div class="container split bio">
  <figure class="team-photo"><img src="{{r}}assets/img/bjarne-berg-wig.jpg" alt="Bjarne Berg Wig" loading="lazy"><figcaption><span><b>30+</b> years in Lean</span><span><b>7</b> books</span></figcaption></figure>
  <div>
    <span class="eyebrow">Author · Sensei</span>
    <h2>Bjarne Berg Wig</h2>
    <p>Author and sensei Bjarne Berg Wig has more than 30 years of experience in quality management and Lean. He was Quality and Innovation Manager at Hydro Agri Europe (now Yara).</p>
    <p>For the last 20 years, Bjarne has helped many Norwegian and international private and public companies transform into learning organisations. He has developed academic programs with Bergen University College in Quality Management and Lean leadership. Several hundred leaders have gone through his practical training, with high impact on many companies and municipalities in Norway.</p>
    <p>He has written 7 professional books, which are used both in industry and in academic programs. Bjarne is a founder of LOS Norge, the Society for Learning Organizations in Norway, and is regarded as one of the "gurus" of learning organisations in Europe.</p>
    <div class="btn-row"><a class="btn" href="mailto:bjarne@learnorg.global">Email Bjarne</a><a class="btn ghost" href="{{r}}resources/#books">His books</a></div>
  </div>
</div></section>

<section class="section" id="samer-hamadeh"><div class="container split reverse bio">
  <figure class="team-photo"><img src="{{r}}assets/img/samer-hamadeh.jpg" alt="Samer Hamadeh" loading="lazy"><figcaption><span>Learning culture specialist</span></figcaption></figure>
  <div>
    <span class="eyebrow">Resident expert</span>
    <h2>Samer Hamadeh</h2>
    <p>Samer Hamadeh is a specialist in learning culture transformation: the shift from seeing work as execution to seeing work as continuous learning and improvement.</p>
    <p>Samer works alongside Bjarne on ILO's mentorship, training and seminars, helping organisations build a culture where everyone learns and improves every day. He has spoken on learning culture transformation at the Manufacturing and Supply Chain Conference in Dublin, and co-hosts ILO's webinars on how to frame the transformation to a learning culture.</p>
    <div class="btn-row"><a class="btn" href="{{r}}contact/">Contact ILO</a><a class="btn ghost" href="{{r}}learning-culture/">Learning Culture</a></div>
  </div>
</div></section>

<section class="section alt trust" id="clients" style="scroll-margin-top:120px"><div class="container">
  <div class="section-head center">
    <span class="eyebrow">Clients</span>
    <h2>Organisations we have worked with</h2>
  </div>
  <div class="logo-wall">{logo_html}</div>
</div></section>
{testimonials_html.replace('section alt testimonials', 'section testimonials')}
{CTA}
"""
    page("about/", "About ILO", "Meet the Institute for Learning Organizations: Bjarne Berg Wig and Samer Hamadeh.", about)

    # ---------- Contact ----------
    contact = f"""
{page_hero("Contact", "Let us know how we can help you.", "hero-coffee.jpg", cta=False)}
<section class="section"><div class="container">
  <div class="section-head"><p class="lead">Schedule a complimentary consultation with Institute for Learning Organizations, or ask us about mentorship, e-learning, training and books.</p></div>
  <div class="contact-grid">
    <div class="contact-item"><div class="label">Email</div><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div class="contact-item"><div class="label">Phone</div><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="contact-item"><div class="label">Books and resources</div><a href="mailto:post@learnorg.global">post@learnorg.global</a></div>
  </div>
  <div class="btn-row" style="margin-top:40px"><a class="btn" href="mailto:{EMAIL}">Send us an email</a></div>
</div></section>
"""
    page("contact/", "Contact", "Contact the Institute for Learning Organizations.", contact)

    # ---------- Redirects for pages the Wix rebuild renamed or removed ----------
    for old, new in REDIRECTS.items():
        redirect(old, new)


build()
print("built")
