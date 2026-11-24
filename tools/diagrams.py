"""Redrawn diagrams for the Obeya book companion pages, in English (en) and Norwegian (nb).

Each diagram replaces an old screenshot. DIAGRAMS maps the old image file name to a function
that returns the new <figure> for a language. build.py swaps them in when it loads the page text.
"""
import random

DEEP, TEAL, TEAL2, AMBER, AMBER_L = "#0b4f5c", "#078586", "#0b6f73", "#b9741a", "#f0a23b"
INK, MUTED, LINE, SOFT, CARD = "#23303b", "#5b6b76", "#9cc3c4", "#eef6f6", "#ffffff"
HEAD = "League Spartan, Inter, sans-serif"
BODY = "Inter, system-ui, sans-serif"
_uid = [0]


def _id():
    _uid[0] += 1
    return f"dg{_uid[0]}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, lines, size=16, weight=600, fill=INK, anchor="middle", family=BODY, lh=1.25, italic=False):
    if isinstance(lines, str):
        lines = [lines]
    top = y - (len(lines) - 1) * size * lh / 2
    spans = "".join(f'<tspan x="{x}" y="{top + i * size * lh:.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    st = ' font-style="italic"' if italic else ""
    return (f'<text text-anchor="{anchor}" dominant-baseline="middle" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}"{st}>{spans}</text>')


def card(x, y, w, h, fill, stroke=None, r=16, shadow=None, sw=2, dash=None):
    """Box with the site's corner shape: rounded top-left and bottom-right."""
    d = (f"M{x + r},{y} H{x + w} V{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} "
         f"H{x} V{y + r} Q{x},{y} {x + r},{y} Z")
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash:
        st += f' stroke-dasharray="{dash}"'
    f = f' filter="url(#{shadow})"' if shadow else ""
    return f'<path d="{d}" fill="{fill}"{st}{f}/>'


def pill(x, y, label, size=14, fill=CARD, stroke="#cfe2e3", color=INK, weight=600):
    w = 22 + len(label) * size * 0.56
    return (f'<rect x="{x - w / 2:.1f}" y="{y - size}" width="{w:.1f}" height="{size * 2}" rx="{size}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            + text(x, y + 1, label, size, weight, color))


def badge(x, y, n, color, r=17):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{color}" stroke-width="3"/>'
            + text(x, y + 1, str(n), r - 1, 700, color))


def defs(i, arrow=TEAL):
    return (f'<defs><marker id="{i}a" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{arrow}"/></marker>'
            f'<marker id="{i}g" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            f'<filter id="{i}s" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="{DEEP}" flood-opacity=".18"/></filter></defs>')


def line(d, i, color=LINE, w=3, dash=None, end=True, start=False, marker="a"):
    m = (f' marker-end="url(#{i}{marker})"' if end else "") + (f' marker-start="url(#{i}{marker})"' if start else "")
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{ds}{m}/>'


def figure(w, h, body, caption, label):
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">{body}</svg>'
            + (f"<figcaption>{caption}</figcaption>" if caption else "") + "</figure>")


# ---------- 1. VMCL: each element exists to serve the one before it ----------
def vmcl_steps(lang):
    T = {"en": [("V", "Vision", ["To reach the", "desired state"]), ("M", "Mission", ["To carry out", "the mission"]),
                ("C", "Capacity", ["To improve our", "capacity and culture"]), ("L", "Learning", ["To develop", "knowledge"])],
         "nb": [("V", "Visjon", ["For å nå", "ønsket tilstand"]), ("M", "Oppdrag", ["For å utføre", "oppdraget"]),
                ("K", "Kapasitet", ["For å forbedre vår", "kapasitet og kultur"]), ("L", "Læring", ["Utvikle", "kunnskap"])]}[lang]
    cap = {"en": "VMCL: learning improves capacity, capacity carries out the mission, the mission reaches the vision",
           "nb": "VMCL: læring forbedrer kapasiteten, kapasiteten utfører oppdraget, oppdraget når visjonen"}[lang]
    i = _id()
    cols = [DEEP, TEAL2, TEAL, AMBER]
    xs = [120, 340, 560, 780]
    b = defs(i)
    for k, ((letter, word, sub), c, x) in enumerate(zip(T, cols, xs)):
        b += card(x - 80, 30, 160, 110, c, shadow=f"{i}s")
        b += text(x, 70, letter, 40, 800, "#fff", family=HEAD) + text(x, 112, word.upper(), 14, 700, "#e6f3f3")
        b += text(x, 186, sub, 16, 600, INK)
    for k in range(3):
        x1, x2 = xs[k + 1] - 35, xs[k] + 35
        b += line(f"M{x1},228 V262 Q{x1},282 {x1 - 20},282 H{x2 + 20} Q{x2},282 {x2},262 V232", i, TEAL, 6)
    return figure(900, 300, b, cap, cap)


# ---------- 2. Mental models loop ----------
def mental_loop(lang):
    T = {"en": ("The real world", "Our mental models", ["Feedback on what", "actually happens"],
                ["What we believe, want,", "think and plan: our theory", "of what has happened", "and what will happen"], "We act", "We see"),
         "nb": ("Den virkelige verden", "Våre mentale modeller", ["Tilbakemelding om", "hva som faktisk skjer"],
                ["Hva vi tror, ønsker,", "tenker og planlegger: vår", "teori om hva som har", "skjedd og skal skje"], "Vi handler", "Vi ser")}[lang]
    i = _id()
    b = defs(i)
    b += line("M300,135 C330,40 570,40 600,135", i, TEAL, 4)
    b += line("M600,245 C570,340 330,340 300,245", i, TEAL, 4)
    b += pill(450, 64, T[5]) + pill(450, 318, T[4])
    b += card(200, 135, 200, 110, "#5b6b76", shadow=f"{i}s") + text(300, 190, T[0].split(" ", 1) if lang == "en" else T[0].split(" ", 1), 19, 700, "#fff", family=HEAD)
    b += card(500, 135, 200, 110, TEAL, shadow=f"{i}s") + text(600, 190, T[1].split(" ", 1), 19, 700, "#fff", family=HEAD)
    b += card(10, 150, 170, 80, SOFT, "#cfe2e3", sw=1.5) + text(95, 190, T[2], 14, 600, DEEP)
    b += card(720, 120, 175, 140, SOFT, "#cfe2e3", sw=1.5) + text(807, 190, T[3], 13.5, 600, DEEP)
    b += line("M180,190 H196", i, LINE, 2, end=False) + line("M704,190 H718", i, LINE, 2, end=False)
    label = " ".join(T[0:2])
    return figure(900, 370, b, None, label)


# ---------- 3. See together, think together, try together ----------
def three_rules(lang):
    T = {"en": ("See together", "Think together", "Try together"), "nb": ("Se sammen", "Tenke sammen", "Prøve sammen")}[lang]
    i = _id()
    b = defs(i)
    import math
    cx, cy, R = 450, 293, 173
    def pt(a):
        return cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
    for a1, a2 in ((-66, -8), (43, 137), (188, 246)):
        x1, y1 = pt(a1); x2, y2 = pt(a2)
        b += line(f"M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}", i, LINE, 4)
    nodes = [((450, 120), DEEP, T[0], "eye"), ((615, 345), TEAL, T[1], "talk"), ((285, 345), AMBER, T[2], "test")]
    icons = {
        "eye": '<path d="M-30,0 Q0,-26 30,0 Q0,26 -30,0 Z" fill="none" stroke="#fff" stroke-width="4"/><circle r="10" fill="#fff"/>',
        "talk": '<path d="M-30,-20 h34 a6,6 0 0 1 6,6 v18 a6,6 0 0 1 -6,6 h-20 l-10,9 v-9 h-4 a6,6 0 0 1 -6,-6 v-18 a6,6 0 0 1 6,-6z" fill="none" stroke="#fff" stroke-width="4"/>'
                '<path d="M16,-4 h12 a6,6 0 0 1 6,6 v16 a6,6 0 0 1 -6,6 h-2 v8 l-9,-8 h-12 a6,6 0 0 1 -6,-6" fill="none" stroke="#fff" stroke-width="4"/>',
        "test": '<path d="M-8,-28 v18 l-18,30 a6,6 0 0 0 5,9 h42 a6,6 0 0 0 5,-9 l-18,-30 v-18" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
                '<path d="M-12,-28 h24" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M-17,12 h34" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
    }
    for (x, y), c, lab, ic in nodes:
        b += f'<circle cx="{x}" cy="{y}" r="66" fill="{c}" filter="url(#{i}s)"/><g transform="translate({x},{y})">{icons[ic]}</g>'
    b += text(450, 32, T[0], 26, 700, INK, family=HEAD)
    b += text(700, 345, T[1].split(" "), 24, 700, INK, anchor="start", family=HEAD)
    b += text(200, 345, T[2].split(" "), 24, 700, INK, anchor="end", family=HEAD)
    return figure(900, 490, b, None, ", ".join(T))


# ---------- 4. Value stream map ----------
def value_stream(lang):
    en = lang == "en"
    L = dict(sup=["Ingot", "internal supplier"] if en else ["Ingot", "intern leverandør"],
             cus=["Internal customer", "wafer"] if en else ["Intern kunde", "wafer"],
             order="Daily order" if en else "Daglig ordre", qr="Quality report" if en else "Kvalitetsrapport",
             wh="Ingot warehouse" if en else "Ingot-lager", cont="Continuous delivery" if en else "Kontinuerlig levering",
             ct="Cycle time" if en else "Syklustid", pt="Process time" if en else "Prosesstid", blocks="5 blocks" if en else "5 blokker",
             va="Processing time" if en else "Bearbeidingstid", wait="Waiting time" if en else "Ventetid")
    steps = [("Gluing station" if en else "Limestasjon", "120 min", "100 min"),
             ("PSQ saw" if en else "PSQ-sag", "666 min", "600 min"),
             ("Block saw / grinding" if en else "Blokksag / sliping", "57 min", "30 min"),
             ("Testing", "2 min", "per slug" if en else "pr. slug"),
             ("Gluing centre" if en else "Limesenter", "12 hours" if en else "12 timer", "11.9 hours" if en else "11,9 timer")]
    i = _id()
    b = defs(i, DEEP)
    # supplier and customer
    for x, lab in ((30, L["sup"]), (740, L["cus"])):
        b += card(x, 24, 180, 74, SOFT, "#9fbfc2", sw=1.5) + f'<path d="M{x + 12},52 l9,-8 v8 l9,-8 v8 l9,-8 v8" fill="none" stroke="{TEAL}" stroke-width="2.2"/>'
        b += text(x + 112, 62, lab, 13, 700, DEEP)
    b += line("M732,60 H218", i, DEEP, 2.5, dash="8 6") + pill(492, 60, L["order"], 13)
    # quality report from testing back to supplier
    b += line("M640,232 C560,160 300,170 150,104", i, DEEP, 2.5, dash="8 6") + pill(400, 158, L["qr"], 13)
    # warehouse and continuous delivery
    b += card(40, 140, 130, 46, "#fff", "#9fbfc2", sw=1.5) + text(105, 164, L["wh"], 13, 700, MUTED)
    b += line("M105,104 V134", i, MUTED, 3, marker="g") + line("M105,190 V226", i, MUTED, 3, marker="g")
    b += card(750, 140, 160, 46, "#fff", "#9fbfc2", sw=1.5) + text(830, 164, L["cont"], 13, 700, MUTED)
    b += line("M860,232 V194", i, MUTED, 3, marker="g") + line("M860,134 V104", i, MUTED, 3, marker="g")
    # process boxes
    x0, w, gap = 40, 150, 32
    for k, (name, ct, pt) in enumerate(steps):
        x = x0 + k * (w + gap)
        b += card(x, 232, w, 64, TEAL if k != 3 else DEEP, shadow=f"{i}s") + text(x + w / 2, 264, name.split(" / ") if " / " in name else name, 14.5, 700, "#fff")
        b += card(x, 304, w, 58, "#fff", "#cfe2e3", sw=1.5, r=10)
        b += text(x + 10, 322, f"{L['ct']}: {ct}", 12.5, 600, INK, anchor="start")
        b += text(x + 10, 344, (f"{L['pt']}: {pt}" if k != 3 else pt), 12.5, 500, MUTED, anchor="start")
        if k < 4:
            b += line(f"M{x + w + 4},264 H{x + w + gap - 6}", i, MUTED, 3, marker="g")
    b += pill(x0 + 3 * (w + gap) - gap / 2, 214, L["blocks"], 12)
    # timeline ladder
    va = ["100 min", "600 min", "27 min", "12 h" if en else "12 t"]
    wt = ["20 min", "66 min", "30 min"]
    y_up, y_dn = 396, 430
    x = 40
    seg = 870 / 7
    path = f"M{x},{y_up}"
    for k in range(7):
        up = k % 2 == 0
        y = y_up if up else y_dn
        path += f" V{y} H{x + seg}"
        lab = va[k // 2] if up else wt[k // 2]
        b += text(x + seg / 2, (y - 14) if up else (y + 18), lab, 13.5, 700, TEAL if up else "#c2412d")
        x += seg
    b += f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    b += (f'<rect x="40" y="470" width="14" height="14" rx="3" fill="{TEAL}"/>' + text(62, 478, L["va"], 13, 600, MUTED, anchor="start")
          + f'<rect x="230" y="470" width="14" height="14" rx="3" fill="#c2412d"/>' + text(252, 478, L["wait"], 13, 600, MUTED, anchor="start"))
    return figure(950, 500, b, None, "Value stream map" if en else "Verdistrømskart")


# ---------- 5. Thinking maturity ----------
def thinking_maturity(lang):
    en = lang == "en"
    bands = [(1, 2, "#fbe3e1", "Pre-conventional" if en else "Prekonvensjonell"),
             (2, 6, "#fdf0dc", "Conventional" if en else "Konvensjonell"),
             (6, 8.3, "#dff1f1", "Post-conventional" if en else "Postkonvensjonell"),
             (8.3, 9.5, "#e9e5f5", "Post-post-conventional" if en else "Post-postkonvensjonell")]
    X0, X1, Y0, Y1 = 110, 860, 30, 400
    def px(age): return X0 + (age - 10) / 60 * (X1 - X0)
    def py(s): return Y1 - (s - 1) / 8.5 * (Y1 - Y0)
    i = _id()
    b = defs(i, AMBER)
    for lo, hi, c, lab in bands:
        b += f'<rect x="{X0}" y="{py(hi):.1f}" width="{X1 - X0}" height="{py(lo) - py(hi):.1f}" fill="{c}"/>'
        b += text(X1 - 14, (py(lo) + py(hi)) / 2, lab, 15, 700, DEEP, anchor="end")
    b += f'<line x1="{X0}" x2="{X1 - 190}" y1="{py(6.7):.1f}" y2="{py(6.7):.1f}" stroke="{TEAL}" stroke-dasharray="5 5" stroke-width="1.5"/>'
    b += text(X0 + 260, py(6.7) - 12, "Systems thinker" if en else "Systemtenker", 14, 700, TEAL, anchor="start")
    rnd = random.Random(7)
    for _ in range(150):
        age = 10 + rnd.random() ** 1.8 * 60
        s = min(7.2, max(1.4, rnd.gauss(4.3 + (age - 10) / 60 * 0.9, 0.9)))
        b += f'<circle cx="{px(age):.1f}" cy="{py(s):.1f}" r="3" fill="{MUTED}" fill-opacity=".45"/>'
    pts = [(12, 2.6), (15, 3.6), (18, 4.6), (21, 5.6), (24, 6.6), (27, 7.6), (30, 8.6)]
    b += line(f"M{px(11):.1f},{py(2.1):.1f} L{px(31.5):.1f},{py(9.3):.1f}", i, AMBER, 4)
    for a, s in pts:
        b += f'<circle cx="{px(a):.1f}" cy="{py(s):.1f}" r="7" fill="{AMBER}" stroke="#fff" stroke-width="2"/>'
    b += f'<path d="M{X0},{Y0} V{Y1} H{X1}" fill="none" stroke="{INK}" stroke-width="2"/>'
    for a in range(10, 71, 10):
        b += text(px(a), Y1 + 18, str(a), 13, 500, MUTED)
    b += text((X0 + X1) / 2, Y1 + 44, "Age" if en else "Alder", 14, 700, INK)
    b += (f'<g transform="translate(40,{(Y0 + Y1) / 2}) rotate(-90)">'
          + text(0, 0, "Degree of thinking awareness" if en else "Grad av tenkebevissthet", 14, 700, INK) + "</g>")
    cap = ("Thinking maturity: most adults stay in the conventional range; training can move people towards systems thinking"
           if en else "Tenkemodenhet: de fleste voksne blir værende i det konvensjonelle; trening kan flytte oss mot systemtenkning")
    return figure(900, 460, b, cap, cap)


# ---------- 6. VMCL and the three jigs ----------
def vmcl_jigs(lang):
    en = lang == "en"
    keys = [("V", "Vision" if en else "Visjon"), ("M", "Mission" if en else "Oppdrag"),
            ("C" if en else "K", "Capacity" if en else "Kapasitet"), ("L", "Learning" if en else "Læring")]
    cards = [("Line of sight" if en else "Siktelinje", DEEP), ("Systems" if en else "Systemer", TEAL), ("Learning" if en else "Læring", AMBER)]
    i = _id()
    b = defs(i)
    for k, (l, w) in enumerate(keys):
        x = 255 + k * 110
        b += card(x, 16, 90, 64, "#fff", "#cfe2e3", sw=1.5, r=10) + text(x + 45, 38, l, 22, 800, DEEP, family=HEAD) + text(x + 45, 64, w, 12.5, 600, MUTED)
    xs = [90, 360, 630]
    for k, ((name, c), x) in enumerate(zip(cards, xs)):
        b += card(x, 150, 200, 170, c, shadow=f"{i}s") + badge(x, 150, k + 1, c)
        b += text(x + 100, 180, name, 20, 700, "#fff", family=HEAD)
        if k == 0:
            for j, w in enumerate(keys[:2]):
                b += f'<rect x="{x + 40}" y="{210 + j * 46}" width="120" height="34" rx="17" fill="#fff" fill-opacity=".15" stroke="#fff" stroke-opacity=".6"/>' + text(x + 100, 228 + j * 46, w[1], 14, 600, "#fff")
        elif k == 1:
            for gx, gy, r in ((x + 70, 245, 22), (x + 128, 270, 16), (x + 118, 222, 12)):
                b += (f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="#fff" stroke-width="7" stroke-dasharray="5 4"/>'
                      f'<circle cx="{gx}" cy="{gy}" r="{r * .45:.1f}" fill="none" stroke="#fff" stroke-width="3"/>')
        else:
            for q, (lab, ang) in enumerate((("P", -45), ("D", 45), ("S", 135), ("A", 225))):
                import math
                qx, qy = x + 100 + 40 * math.cos(math.radians(ang)), 250 + 40 * math.sin(math.radians(ang))
                b += text(qx, qy, lab, 15, 800, "#fff")
            b += f'<circle cx="{x + 100}" cy="250" r="40" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-dasharray="6 5"/>'
    b += line("M290,190 C310,150 340,150 356,180", i, TEAL, 3) + pill(323, 130, "Select" if en else "Velge", 13)
    b += line("M560,190 C580,150 610,150 626,180", i, TEAL, 3) + pill(593, 130, "Focus" if en else "Fokus", 13)
    b += line("M380,324 C360,370 220,370 200,328", i, LINE, 3) + line("M650,324 C630,370 490,370 470,328", i, LINE, 3)
    cap = "The relation between VMCL and the three “jigs” in Obeya" if en else "Sammenhengen mellom VMCL og de tre «jiggene» i Obeya"
    return figure(920, 380, b, cap, cap)


# ---------- 7. Line of sight: present state to future state ----------
def line_of_sight(lang):
    en = lang == "en"
    left = [("Future state" if en else "Framtidig tilstand", AMBER), ("Obeya mission" if en else "Obeya-oppdrag", TEAL),
            ("Present state" if en else "Nåsituasjon", "#5b6b76")]
    right = [(3, ["A picture of the future state that is", "motivating · simple · measurable"] if en else ["Et bilde av framtidig tilstand som er", "motiverende · enkelt · målbart"]),
             (2, ["What we have to do together", "to reach our goal"] if en else ["Hva vi må gjøre sammen", "for å nå målet"]),
             (1, ["What is the situation we have to change?", "What do our problems look like?"] if en else ["Hvilken situasjon må vi endre?", "Hvordan ser problemene våre ut?"])]
    i = _id()
    b = defs(i)
    b += line("M160,312 V70", i, TEAL, 4)
    for k, ((name, c), (n, lines)) in enumerate(zip(left, right)):
        y = 30 + k * 120
        b += card(60, y, 200, 70, c, shadow=f"{i}s") + text(160, y + 35, name, 17, 700, "#fff", family=HEAD)
        b += line(f"M266,{y + 35} H336", i, LINE, 2, dash="3 5", end=False)
        b += card(340, y - 4, 520, 78, "#fff", "#cfe2e3", sw=1.5) + badge(340, y - 4, n, c, 15)
        b += text(370, y + 35, lines, 15.5, 600, INK, anchor="start")
    cap = "Jig 1, line of sight: from today's situation to a clear picture of the future" if en else "Jigg 1, siktelinje: fra dagens situasjon til et tydelig bilde av framtiden"
    return figure(900, 370, b, cap, cap)


# ---------- 8. System map ----------
def system_map(lang):
    en = lang == "en"
    i = _id()
    b = defs(i, MUTED)
    b += card(30, 20, 120, 84, TEAL, shadow=f"{i}s") + text(90, 62, ["See", "Think", "Act"] if en else ["Se", "Tenke", "Prøve"], 15, 700, "#fff")
    b += card(210, 26, 330, 72, DEEP, shadow=f"{i}s") + text(375, 62, "The main system" if en else "Hovedsystemet", 20, 700, "#fff", family=HEAD)
    b += line("M154,62 H204", i, MUTED, 3, marker="g")
    cols = [(40, ["#5b6b76", TEAL, "#cfd8dd", TEAL2]), (300, [TEAL2, "#cfd8dd", DEEP]), (560, ["#cfd8dd", TEAL, "#5b6b76"])]
    pos = {}
    for c, (x, fills) in enumerate(cols):
        for r, f in enumerate(fills):
            y = 150 + r * 66
            hot = (c, r) in ((1, 1), (2, 2))
            b += card(x, y, 150, 46, f, AMBER if hot else None, sw=3.5, r=10)
            pos[(c, r)] = (x, y)
    for (a, bb) in (((0, 0), (1, 0)), ((0, 2), (1, 1)), ((1, 1), (2, 0)), ((1, 2), (2, 2)), ((0, 3), (1, 2))):
        (x1, y1), (x2, y2) = pos[a], pos[bb]
        b += line(f"M{x1 + 154},{y1 + 23} C{x1 + 200},{y1 + 23} {x2 - 50},{y2 + 23} {x2 - 6},{y2 + 23}", i, MUTED, 2.5, start=True, marker="g")
    b += line("M375,102 V144", i, MUTED, 3, marker="g")
    b += (f'<rect x="760" y="160" width="22" height="16" rx="4" fill="#fff" stroke="{AMBER}" stroke-width="3.5"/>'
          + text(792, 168, ["Where the", "system gets", "stuck"] if en else ["Der systemet", "låser seg"], 13.5, 600, MUTED, anchor="start", lh=1.3)
          + f'<rect x="760" y="250" width="22" height="16" rx="4" fill="{TEAL}"/>'
          + text(792, 258, ["Parts and", "relationships"] if en else ["Deler og", "relasjoner"], 13.5, 600, MUTED, anchor="start", lh=1.3))
    cap = "A system map: the parts of the system and how they affect each other" if en else "Et systemkart: delene i systemet og hvordan de påvirker hverandre"
    return figure(900, 400, b, cap, cap)


# ---------- 9. DSRP ----------
def dsrp(lang):
    en = lang == "en"
    cols = [("D", "Distinctions" if en else "Skiller", ["What is it?", "What is it not?"] if en else ["Hva er det?", "Hva er det ikke?"], DEEP),
            ("S", "Systems" if en else "Systemer", ["What is it part of?", "Part and whole"] if en else ["Hva er det en del av?", "Del og helhet"], TEAL),
            ("R", "Relationships" if en else "Relasjoner", ["How does it relate?", "Action and reaction"] if en else ["Hvordan henger det sammen?", "Aksjon og reaksjon"], TEAL2),
            ("P", "Perspectives" if en else "Perspektiver", ["Seen from what", "point of view?"] if en else ["Sett fra hvilket", "ståsted?"], AMBER)]
    i = _id()
    b = defs(i)
    for k, (l, name, q, c) in enumerate(cols):
        x = 20 + k * 222
        b += card(x, 20, 200, 300, "#fff", "#d7e6e7", sw=1.5, shadow=f"{i}s")
        b += f'<circle cx="{x + 100}" cy="82" r="40" fill="{c}"/>' + text(x + 100, 84, l, 36, 800, "#fff", family=HEAD)
        b += text(x + 100, 150, name, 19, 700, INK, family=HEAD) + text(x + 100, 192, q, 14, 500, MUTED)
        cx, cy = x + 100, 268
        if l == "D":
            b += f'<rect x="{cx - 46}" y="{cy - 26}" width="46" height="46" rx="8" fill="{c}"/><rect x="{cx + 4}" y="{cy - 20}" width="40" height="40" rx="8" fill="none" stroke="{c}" stroke-width="3" stroke-dasharray="5 4"/>'
        elif l == "S":
            b += f'<rect x="{cx - 50}" y="{cy - 28}" width="100" height="56" rx="10" fill="none" stroke="{c}" stroke-width="3"/>' + "".join(
                f'<rect x="{cx - 40 + j * 28}" y="{cy - 10}" width="20" height="20" rx="4" fill="{c}"/>' for j in range(3))
        elif l == "R":
            b += (f'<rect x="{cx - 52}" y="{cy - 16}" width="32" height="32" rx="6" fill="{c}"/><rect x="{cx + 20}" y="{cy - 16}" width="32" height="32" rx="6" fill="{c}"/>'
                  + line(f"M{cx - 14},{cy} H{cx + 14}", i, c, 3, start=True))
        else:
            b += (f'<circle cx="{cx}" cy="{cy}" r="14" fill="{c}"/>'
                  + f'<path d="M{cx - 54},{cy - 20} Q{cx - 34},{cy - 34} {cx - 18},{cy - 12}" fill="none" stroke="{MUTED}" stroke-width="2.5"/>'
                  + f'<path d="M{cx + 54},{cy + 20} Q{cx + 34},{cy + 34} {cx + 18},{cy + 12}" fill="none" stroke="{MUTED}" stroke-width="2.5"/>'
                  + f'<circle cx="{cx - 54}" cy="{cy - 20}" r="6" fill="{MUTED}"/><circle cx="{cx + 54}" cy="{cy + 20}" r="6" fill="{MUTED}"/>')
    cap = ("DSRP: the four simple rules of systems thinking (Dr. Derek Cabrera)" if en
           else "DSRP: systemtenkningens fire enkle regler (dr. Derek Cabrera)")
    return figure(900, 340, b, cap, cap)


# ---------- 10. See together, then learn in small trials ----------
def learning_steps(lang):
    en = lang == "en"
    i = _id()
    b = defs(i)
    b += card(40, 20, 150, 56, TEAL, shadow=f"{i}s") + text(115, 48, "See together" if en else "Se sammen", 16, 700, "#fff")
    b += line("M115,82 V128", i, MUTED, 3, marker="g")
    # staircase of PDSA cycles
    b += f'<path d="M30,340 H110 V284 H190 V228 H270 V172 H330 V340 Z" fill="{SOFT}" stroke="#cfe2e3" stroke-width="2"/>'
    for k, c in enumerate(("#5b6b76", TEAL, AMBER)):
        x, y = 70 + k * 80, 300 - k * 56
        b += f'<circle cx="{x}" cy="{y}" r="24" fill="{c}"/>' + text(x, y - 6, "P   D", 11, 800, "#fff") + text(x, y + 8, "A   S", 11, 800, "#fff")
        b += f'<path d="M{x - 26},{y - 30} A30,30 0 0 1 {x + 26},{y - 30}" fill="none" stroke="{c}" stroke-width="3" marker-end="url(#{i}a)"/>'
    b += text(180, 368, "Step by step, one trial at a time" if en else "Steg for steg, ett forsøk om gangen", 13.5, 600, MUTED)
    # right: loop
    b += card(420, 20, 450, 56, SOFT, "#cfe2e3", sw=1.5) + badge(420, 20, 1, TEAL, 14)
    b += text(445, 48, "Break challenges down into learning cycles (experiments)" if en else "Bryt utfordringene ned i læringssykluser (eksperimenter)", 14.5, 600, DEEP, anchor="start")
    b += card(450, 165, 130, 70, "#5b6b76", shadow=f"{i}s") + text(515, 200, ["Real", "world"] if en else ["Virkelig", "verden"], 15, 700, "#fff")
    b += card(710, 165, 130, 70, TEAL, shadow=f"{i}s") + text(775, 200, ["Mental", "models"] if en else ["Mentale", "modeller"], 15, 700, "#fff")
    b += line("M515,158 C560,96 730,96 775,158", i, LINE, 3) + line("M775,242 C730,304 560,304 515,242", i, LINE, 3)
    b += card(420, 324, 450, 56, SOFT, "#cfe2e3", sw=1.5) + badge(420, 324, 2, AMBER, 14)
    b += text(445, 352, "Run trials to learn fast" if en else "Gjør forsøk for å lære raskt", 14.5, 600, DEEP, anchor="start")
    cap = "Jig 3, learning: break challenges into small trials and learn from each one" if en else "Jigg 3, læring: bryt utfordringene ned i små forsøk og lær av hvert av dem"
    return figure(900, 400, b, cap, cap)


# ---------- 11. Learning Culture Mirror ----------
def lc_mirror(lang):
    en = lang == "en"
    items = (["Shared vision", "Safe learning environment", "Building on best knowledge", "Strong performance teams", "Continual improvement", "Describing and sharing learning"]
             if en else ["Felles visjon", "Trygt læringsmiljø", "Bygge på beste kunnskap", "Sterke prestasjonsteam", "Kontinuerlig forbedring", "Beskrive og dele læring"])
    import math
    i = _id()
    b = defs(i)
    cx, cy, R = 450, 260, 175
    pts = [(cx + R * math.cos(math.radians(-90 + k * 60)), cy + R * math.sin(math.radians(-90 + k * 60))) for k in range(6)]
    b += '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{SOFT}" stroke="{LINE}" stroke-width="3"/>'
    for x, y in pts:
        b += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{LINE}" stroke-width="2"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="46" fill="{DEEP}"/>' + text(cx, cy, ["LC", "Mirror"] if en else ["LK-", "speilet"], 15, 700, "#fff")
    cols = [TEAL, TEAL2, DEEP, TEAL, TEAL2, DEEP]
    for k, ((x, y), lab, c) in enumerate(zip(pts, items, cols)):
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="60" fill="{c}" stroke="#fff" stroke-width="4" filter="url(#{i}s)"/>'
        b += text(x, y - 30, str(k + 1), 18, 800, "#ffd38a", family=HEAD)
        lines, cur = [], ""
        for w in lab.split(" "):
            if cur and len(cur) + 1 + len(w) > 11:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        b += text(x, y + 8, lines, 12, 700, "#fff", lh=1.2)
    # magnifier on item 1
    x, y = pts[0]
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="70" fill="none" stroke="{AMBER_L}" stroke-width="8"/>'
    b += f'<path d="M{x - 50:.1f},{y + 50:.1f} L{x - 86:.1f},{y + 86:.1f}" stroke="{AMBER_L}" stroke-width="12" stroke-linecap="round"/>'
    cap = ("The Learning Culture Mirror: six criteria for an adaptive learning culture" if en
           else "Læringskulturspeilet: seks kriterier for en tilpasningsdyktig læringskultur")
    return figure(900, 520, b, cap, cap)


# ---------- 12. Deming's learning cycle (PDSA) ----------
def deming_pdsa(lang):
    en = lang == "en"
    steps = ([("Plan", ["Plan a change or a test", "aimed at improvement."]), ("Do", ["Carry it out, preferably", "on a small scale."]),
              ("Study", ["Study the results.", "What did we learn?"]), ("Act", ["Adopt the change, abandon it,", "or run through the cycle again."])]
             if en else
             [("Planlegg", ["Planlegg en endring eller et", "forsøk som skal gi forbedring."]), ("Utfør", ["Gjennomfør det, helst", "i liten skala."]),
              ("Studer", ["Studer resultatene.", "Hva lærte vi?"]), ("Handle", ["Ta i bruk endringen, forkast den,", "eller gå gjennom syklusen igjen."])])
    import math
    i = _id()
    b = defs(i)
    cx, cy, R = 450, 210, 120
    cols = [DEEP, TEAL, TEAL2, AMBER]
    for k in range(4):
        a1, a2 = -90 + k * 90 + 8, -90 + (k + 1) * 90 - 8
        x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
        x2, y2 = cx + R * math.cos(math.radians(a2)), cy + R * math.sin(math.radians(a2))
        b += f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{cols[k]}" stroke-width="22"/>'
        ah = a2 + 2
        tx, ty = cx + R * math.cos(math.radians(ah + 7)), cy + R * math.sin(math.radians(ah + 7))
        bx1, by1 = cx + (R - 20) * math.cos(math.radians(ah)), cy + (R - 20) * math.sin(math.radians(ah))
        bx2, by2 = cx + (R + 20) * math.cos(math.radians(ah)), cy + (R + 20) * math.sin(math.radians(ah))
        b += f'<path d="M{bx1:.1f},{by1:.1f} L{tx:.1f},{ty:.1f} L{bx2:.1f},{by2:.1f} Z" fill="{cols[k]}"/>'
    b += text(cx, cy - 10, "PDSA", 30, 800, DEEP, family=HEAD) + text(cx, cy + 22, "W. E. Deming", 13, 600, MUTED)
    places = [(cx + 150, 70, "start"), (cx + 150, 350, "start"), (cx - 150, 350, "end"), (cx - 150, 70, "end")]
    for k, ((name, lines), (x, y, anc)) in enumerate(zip(steps, places)):
        b += badge(x + (16 if anc == "start" else -16), y - 26, k + 1, cols[k], 15)
        b += text(x + (40 if anc == "start" else -40), y - 26, name, 19, 700, cols[k], anchor=anc, family=HEAD)
        b += text(x, y + 10, lines, 14, 500, INK, anchor=anc)
    cap = "Deming's learning cycle: note that he wrote Study, not Check" if en else "Demings læringssyklus: legg merke til at han skrev Studer, ikke Kontroller"
    return figure(900, 420, b, cap, cap)


# ---------- 13. Strategy path (performance over time) ----------
def strategy_path(lang):
    en = lang == "en"
    i = _id()
    b = defs(i, INK)
    b += f'<path d="M80,40 V380 H860" fill="none" stroke="{INK}" stroke-width="2.5" marker-start="url(#{i}a)" marker-end="url(#{i}a)"/>'
    b += text(90, 26, "Performance" if en else "Ytelse", 15, 700, INK, anchor="start") + text(850, 404, "Time" if en else "Tid", 15, 700, INK, anchor="end")
    b += line("M230,300 C250,250 290,240 350,232", i, TEAL, 4)
    b += line("M480,205 C540,180 560,120 640,96", i, AMBER, 4, dash="10 8")
    b += text(580, 190, "Development" if en else "Utvikling", 15, 600, MUTED, anchor="start", italic=True)
    for (x, y, w, h, c, lab, n) in ((120, 300, 170, 66, "#5b6b76", ["Present", "state"] if en else ["Nå-", "situasjonen"], 1),
                                    (350, 196, 190, 66, TEAL, ["Where to", "be next"] if en else ["Hvor vi skal", "være neste"], 3),
                                    (640, 56, 200, 70, AMBER, ["Vision", "future state"] if en else ["Visjon", "framtidig tilstand"], 2)):
        b += card(x, y, w, h, c, shadow=f"{i}s") + badge(x, y, n, c, 15) + text(x + w / 2, y + h / 2, lab, 16, 700, "#fff")
    b += badge(270, 246, 4, TEAL, 14)
    cap = "Hoshin kanri: from present state to the next step on the way to the vision" if en else "Hoshin kanri: fra nåsituasjonen til neste steg på vei mot visjonen"
    return figure(900, 420, b, cap, cap)


# ---------- 14. Keys to Hoshin kanri (list, not a picture) ----------
def hoshin_keys(lang):
    en = lang == "en"
    items = (["An involving planning and execution process that is improved continuously through the year (L, learning; PDSA).",
              "Focus on the most important of the important: customers, users and the good life first; bad news is “good news”.",
              "Action learning at all levels and in all units to reach the vision (V), everyone taking part in the mission (M).",
              "Action learning based on knowledge: systems thinking.",
              "Balance between doing the right things and the day-to-day work of doing things right."]
             if en else
             ["En involverende planleggings- og gjennomføringsprosess som forbedres kontinuerlig gjennom året (L, læring; PDSA).",
              "Fokus på det viktigste av det viktige: kunder, brukere og det gode liv først; dårlige nyheter er «gode nyheter».",
              "Handlingslæring på alle nivåer og i alle enheter for å nå visjonen (V), der alle er med på oppdraget (O).",
              "Handlingslæring basert på kunnskap: systemtenkning.",
              "Balanse mellom å gjøre de riktige tingene og den daglige driften: å gjøre tingene riktig."])
    key = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="7" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M11.5 12H21M17 12v4M20 12v3" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
    lis = "".join(f'<li><span class="key">{key}</span><span>{t}</span></li>' for t in items)
    title = "Keys to successful Hoshin kanri" if en else "Nøkler til vellykket Hoshin kanri"
    return f'<figure class="diagram keys-list"><b>{title}</b><ul>{lis}</ul></figure>'


# ---------- 15. Hoshin kanri: the words ----------
def hoshin_words(lang):
    en = lang == "en"
    i = _id()
    b = defs(i)
    for k, (zh, word, mean, c) in enumerate((("方针", "Hoshin", "Direction" if en else "Retning", TEAL),
                                             ("管理", "Kanri", "Execution" if en else "Gjennomføring", AMBER))):
        x = 60 + k * 420
        b += card(x, 20, 360, 200, "#fff", "#d7e6e7", sw=1.5, shadow=f"{i}s")
        b += text(x + 180, 92, zh, 72, 500, INK, family="'Noto Serif CJK SC', 'Songti SC', 'SimSun', serif")
        b += f'<rect x="{x + 40}" y="146" width="280" height="50" rx="25" fill="{c}"/>' + text(x + 180, 172, f"{word} = {mean}", 20, 700, "#fff")
    b += text(450, 120, "+", 46, 300, MUTED)
    return figure(900, 240, b, None, "Hoshin kanri: direction and execution" if en else "Hoshin kanri: retning og gjennomføring")


DIAGRAMS = {
    "184a40a55ddf.png": vmcl_steps, "8b49d4fd07ca.png": mental_loop, "918e2b7334aa.png": three_rules,
    "d2c240cb895e.png": value_stream, "0d719f30b41a.png": thinking_maturity, "eab4518bfc15.png": vmcl_jigs,
    "d8faa8242ffc.png": line_of_sight, "731ba7b77457.png": system_map, "92fe93e3b6e5.jpg": dsrp,
    "c4b83cda92b1.png": learning_steps, "89cabc9e1e31.png": lc_mirror, "d6cb8eec4ff2.jpg": deming_pdsa,
    "7f531e0d142e.png": strategy_path, "ea83a3cfdb03.png": hoshin_keys, "e5a6a9f0e2d4.png": hoshin_words,
}


def pdsa_ring():
    """Small PDSA ring in the same style, for cards (no text labels apart from the letters)."""
    import math
    i = _id()
    cx, cy, R = 160, 160, 105
    cols = [DEEP, TEAL, TEAL2, AMBER]
    b = ""
    for k, lab in enumerate("PDSA"):
        a1, a2 = -90 + k * 90 + 8, -90 + (k + 1) * 90 - 8
        x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
        x2, y2 = cx + R * math.cos(math.radians(a2)), cy + R * math.sin(math.radians(a2))
        b += f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{cols[k]}" stroke-width="26"/>'
        ah = a2 + 2
        tx, ty = cx + R * math.cos(math.radians(ah + 8)), cy + R * math.sin(math.radians(ah + 8))
        bx1, by1 = cx + (R - 22) * math.cos(math.radians(ah)), cy + (R - 22) * math.sin(math.radians(ah))
        bx2, by2 = cx + (R + 22) * math.cos(math.radians(ah)), cy + (R + 22) * math.sin(math.radians(ah))
        b += f'<path d="M{bx1:.1f},{by1:.1f} L{tx:.1f},{ty:.1f} L{bx2:.1f},{by2:.1f} Z" fill="{cols[k]}"/>'
        am = math.radians((a1 + a2) / 2)
        b += text(cx + R * math.cos(am), cy + R * math.sin(am) + 1, lab, 17, 800, "#fff", family=HEAD)
    b += text(cx, cy, "PDSA", 30, 800, DEEP, family=HEAD)
    return f'<svg class="pdsa pdsa-ring" viewBox="0 0 320 320" role="img" aria-label="Plan, Do, Study, Act">{b}</svg>'
