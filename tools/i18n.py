"""Make the site bilingual after tools/build.py has written the English site.

English pages stay where they are; Norwegian copies go under /no/.
Text is translated with two dictionaries of HTML fragments:
  tools/i18n/nb.json  English -> Norwegian (Bokmål)
  tools/i18n/en.json  Norwegian -> English (for pages written in Norwegian)

Usage:
  python3 tools/i18n.py .            build the /no/ site and the language switch
  python3 tools/i18n.py . --missing  list text that still needs translating
"""
import html as htmllib
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
MISSING = "--missing" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://bigtex79.github.io/learnorg.global/"

# Pages written in English that get a Norwegian copy under /no/
EN_SRC = ["", "services/", "sensei-mentorship/", "training/", "off-site-training/",
          "e-learning-services/", "learning-culture/", "obeya/", "e-resources/",
          "past-events/", "contact/", "book-resources/", "about-us/"]
# Pages written in Norwegian: the root copy becomes English, the /no/ copy keeps the Norwegian text
NO_SRC = ["trippel-l/", "obeya-dagseminar/", "det-er-ledelse/"]
# Norwegian book companion pages: one copy, Norwegian menu, EN switch goes to the English counterpart
NO_ONLY = {"book-resources/lean-ledelse/": "book-resources/",
           "book-resources/laerende-organisasjoner/": "book-resources/",
           "book-resources/systemtenkning-med-obeya/": "book-resources/systems-thinking-with-obeya/"}
for i in range(1, 13):
    NO_ONLY[f"book-resources/laerende-organisasjoner/kapittel-{i}/"] = "book-resources/"
# English-only page with a Norwegian counterpart
EN_PAIR = {"book-resources/systems-thinking-with-obeya/": "book-resources/systemtenkning-med-obeya/"}

BILINGUAL = set(EN_SRC) | set(NO_SRC)


def load(name):
    p = os.path.join(HERE, "i18n", name)
    return json.load(open(p, encoding="utf8")) if os.path.exists(p) else {}


NB = load("nb.json")
EN = load("en.json")

BLOCK = r"(?:p|h[1-6]|li|div|section|ul|ol|article|nav|header|footer|main|figure|blockquote|table|tr|form)"
SEG_TAGS = r"(p|div|h[1-6]|li|figcaption|blockquote|td|th|dt|dd|a|button|span|b|strong|small|i|em|label|title|text)"
SEG_RE = re.compile(rf"<{SEG_TAGS}(\s[^>]*)?>((?:(?!<{BLOCK}[\s>/]).)*?)</\1>", re.S)
ATTR_RE = re.compile(r'(\s(?:alt|title|aria-label|content)=")([^"]*)(")')
SKIP = re.compile(r"^(PDF|Word|Excel|PowerPoint) · |^[\s\d+().,:;·/–—-]*$|@|^https?:|^[A-Z]{2,4}$|^EN$|^NO$")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def segments(text):
    """Text fragments to translate, longest first."""
    found = set()
    for m in SEG_RE.finditer(text):
        inner = norm(m.group(3))
        if inner and not SKIP.search(re.sub(r"<[^>]+>", "", inner)) and re.search(r"[A-Za-zÆØÅæøå]", re.sub(r"<[^>]+>", "", inner)):
            found.add(inner)
    for m in ATTR_RE.finditer(text):
        v = norm(m.group(2))
        if v and re.search(r"[A-Za-z]{3}", v) and not v.startswith(("http", "width=", "summary", "website")) and "/" not in v:
            found.add(v)
    return sorted(found, key=len, reverse=True)


def lookup(k, table):
    if k in table:
        return table[k]
    m = re.match(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})$", k)
    if m and m.group(1) in table:
        return table[m.group(1)] + " " + m.group(2)
    if " | " in k:
        left, right = k.rsplit(" | ", 1)
        if left in table:
            return table[left] + " | " + right
    return None


def translate(text, table, missing=None):
    def key_of(raw):
        blobs = re.findall(r"<svg\b.*?</svg>|<img\b[^>]*>", raw, re.S)
        k = re.sub(r"<svg\b.*?</svg>|<img\b[^>]*>", "¤", raw, flags=re.S)
        urls = re.findall(r'(?:href|src)="([^"]*)"', k)
        k = re.sub(r'((?:href|src)=")[^"]*(")', r"\1§\2", k)
        return k, urls, blobs

    def fill(out, urls, blobs):
        for u in urls:
            out = out.replace("§", u, 1)
        for b in blobs:
            out = out.replace("¤", b, 1)
        return out

    def seg(m):
        raw = norm(m.group(3))
        k, urls, blobs = key_of(raw)
        open_tag = f"<{m.group(1)}{m.group(2) or ''}>"
        found = lookup(k, table)
        if found is not None:
            return open_tag + fill(found, urls, blobs) + f"</{m.group(1)}>"
        plain = re.sub(r"<[^>]+>", "", raw)
        outside = re.sub(r"<(\w+)\b[^>]*>.*?</\1>|<svg\b.*?</svg>|<[^>]+>", "", raw, flags=re.S)
        has_children = bool(re.search(r"<(a|span|button|svg|img|b|i|small|label)\b", raw))
        if missing is not None and (not has_children or re.search(r"[A-Za-zÆØÅæøå]{2}", outside)):
            if not SKIP.search(plain) and re.search(r"[A-Za-zÆØÅæøå]", plain):
                missing.add(k)
        if has_children:
            return open_tag + SEG_RE.sub(seg, m.group(3)) + f"</{m.group(1)}>"
        return m.group(0)

    text = SEG_RE.sub(seg, text)

    def attr(m):
        v = norm(m.group(2))
        found = lookup(v, table)
        if found is not None:
            return m.group(1) + htmllib.escape(htmllib.unescape(found), quote=True) + m.group(3)
        if missing is not None and re.search(r"[A-Za-z]{3} [A-Za-z]", v) and not v.startswith("http"):
            missing.add(v)
        return m.group(0)
    return ATTR_RE.sub(attr, text)


def depth_prefix(path):
    return "../" * path.count("/")


def rewrite_links(text, src_path, dst_path, to_no):
    """Re-point relative links for a page that moves from src_path to dst_path."""
    src_dir = src_path
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|tel:|#|data:|javascript:)", url):
            return m.group(0)
        path, sep, frag = url.partition("#")
        path, qs, query = path.partition("?")
        target = os.path.normpath(os.path.join(src_dir, path or "."))
        target = "" if target == "." else target
        is_dir = (path == "" or path.endswith("/") or path in (".", ".."))
        if is_dir and target:
            target += "/"
        if to_no and target in BILINGUAL:
            target = "no/" + target
        new = depth_prefix(dst_path) + target
        if new == "":
            new = "./"
        return f'{attr}="{new}{qs}{query}{sep}{frag}"'
    return re.sub(r'(href|src)="([^"]*)"', fix, text)


def switch(cur, en_href, no_href):
    def item(code, href, label):
        if code == cur:
            return f'<a aria-current="true" lang="{"nb" if code == "NO" else "en"}">{code}</a>'
        return f'<a href="{href}" hreflang="{"nb" if code == "NO" else "en"}" lang="{"nb" if code == "NO" else "en"}" title="{label}">{code}</a>'
    return ('<div class="lang-switch" role="navigation" aria-label="Language / Språk">'
            + item("EN", en_href, "English") + item("NO", no_href, "Norsk") + "</div>")


def finish(text, dst_path, lang, en_path, no_path):
    r = depth_prefix(dst_path)
    rel = lambda p: (r + p) if (r + p) else "./"
    text = re.sub(r'<html lang="[a-z]+">', f'<html lang="{lang}">', text, count=1)
    if lang == "nb":
        text = text.replace("All rights reserved.", "Alle rettigheter forbeholdt.")
    text = text.replace("<!--LANGSWITCH-->", switch("NO" if lang == "nb" else "EN", rel(en_path), rel(no_path)))
    text = re.sub(r'(<meta property="og:locale" content=")[^"]*', r"\1" + ("nb_NO" if lang == "nb" else "en_GB"), text)
    text = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + SITE_URL + dst_path, text)
    text = re.sub(r'(<link rel="canonical" href=")[^"]*', r"\g<1>" + SITE_URL + dst_path, text)
    alt = (f'<link rel="alternate" hreflang="en" href="{SITE_URL}{en_path}">\n'
           f'<link rel="alternate" hreflang="nb" href="{SITE_URL}{no_path}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{en_path}">\n')
    text = re.sub(r'<link rel="alternate" hreflang[^>]*>\n', "", text)
    text = text.replace('<link rel="canonical"', alt + '<link rel="canonical"', 1)
    return text


def read(path):
    return open(os.path.join(ROOT, path, "index.html"), encoding="utf8").read()


def write(path, text):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf8").write(text)


def main_part(text):
    a, b = text.find("<main>"), text.find("</main>")
    return a, b


def run():
    miss_nb, miss_en = set(), set()
    out = {}
    for p in EN_SRC:
        src = read(p)
        out[p] = finish(src, p, "en", p, "no/" + p)
        no = rewrite_links(translate(src, NB, miss_nb), p, "no/" + p, True)
        out["no/" + p] = finish(no, "no/" + p, "nb", p, "no/" + p)
    for p in NO_SRC:
        src = read(p)
        a, b = main_part(src)
        en = src[:a] + translate(src[a:b], EN, miss_en) + src[b:]
        # English chrome, translated <title>/description from the English dictionary as well
        en = translate(en, EN)
        out[p] = finish(en, p, "en", p, "no/" + p)
        no = rewrite_links(translate(src, NB, miss_nb), p, "no/" + p, True)
        out["no/" + p] = finish(no, "no/" + p, "nb", p, "no/" + p)
    for p, en_target in NO_ONLY.items():
        src = read(p)
        no = rewrite_links(translate(src, NB, miss_nb), p, p, True)
        out[p] = finish(no, p, "nb", en_target, p)
    for p, no_target in EN_PAIR.items():
        out[p] = finish(read(p), p, "en", p, no_target)
    if MISSING:
        json.dump({"nb": sorted(miss_nb, key=len), "en": sorted(miss_en, key=len)},
                  sys.stdout, ensure_ascii=False, indent=1)
        print(f"\nmissing nb={len(miss_nb)} en={len(miss_en)}", file=sys.stderr)
        return
    for p, t in out.items():
        write(p, t)
    print(f"bilingual: {len(out)} pages written; untranslated nb={len(miss_nb)} en={len(miss_en)}")


run()
