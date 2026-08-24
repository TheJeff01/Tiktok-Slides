#!/usr/bin/env python3
# Build TWO variants of the deploy-platforms carousel from the git-commands.html
# shell — same cover/CTA/photo assets (reused verbatim), same 7-platform copy,
# but two different treatments for the empty dead space on content slides:
#   deploy-platforms-hero.html — big hero screenshot, tightened bullets
#   deploy-platforms-glow.html — original small screenshot card + a subtle
#                                 radial glow + ghost numeral behind the heading

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "git-commands", "git-commands.html")

with io.open(SRC, "r", encoding="utf-8") as f:
    base_html = f.read()

def apply_shared_text(html):
    html = html.replace(
        "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
        "<title>Jeffthedev — Free Platforms to Deploy Your App</title>",
    )
    html = html.replace(
        '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
        '<span class="tag tag-dark" style="margin-bottom:11px;">Hosting · Free Tier</span>',
    )
    html = html.replace(
        '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
        '<div class="heading" style="color:#fff;font-size:31px;margin-bottom:14px;">Free platforms to<br><span style="color:var(--green-light);">deploy your app</span></div>',
    )
    html = html.replace(
        '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
        '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">No credit card, no excuses — pick one of these and ship your project today.</p>',
    )
    html = html.replace(
        '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
        '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">7 ways to ship it<br>without spending a cent.</div>',
    )
    cta_items = [
        "Vercel — one-click React/Next.js deploys",
        "Netlify — the original git-to-deploy",
        "GitHub Pages — free static hosting",
        "Render — full-stack apps + databases",
        "Railway — backend + DB, fast setup",
    ]
    old_items = [
        "reflog — recover seemingly lost commits",
        "stash — shelve work, switch branches fast",
        "commit --amend — fix the last commit",
        "cherry-pick — grab one commit by hash",
        "reset --soft — uncommit but keep your work",
    ]
    for old, new in zip(old_items, cta_items):
        html = html.replace(
            '<span style="font-family:var(--font);font-size:12.5px;color:rgba(255,255,255,0.85);font-weight:400;line-height:1.5;">%s</span>' % old,
            '<span style="font-family:var(--font);font-size:12.5px;color:rgba(255,255,255,0.85);font-weight:400;line-height:1.5;">%s</span>' % new,
        )

    def checklist_item(text):
        return (
            '              <div style="display:flex;align-items:center;gap:10px;">\n'
            '                <div style="width:16px;height:16px;border-radius:4px;background:rgba(34,197,94,0.3);border:1px solid rgba(34,197,94,0.5);display:flex;align-items:center;justify-content:center;flex-shrink:0;">\n'
            '                  <svg width="9" height="9" viewBox="0 0 9 9" fill="none"><path d="M1.5 4.5l2 2 4-4" stroke="#4ADE80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'
            '                </div>\n'
            '                <span style="font-family:var(--font);font-size:12.5px;color:rgba(255,255,255,0.85);font-weight:400;line-height:1.5;">%s</span>\n'
            '              </div>\n' % text
        )

    anchor = '<span style="font-family:var(--font);font-size:12.5px;color:rgba(255,255,255,0.85);font-weight:400;line-height:1.5;">%s</span>\n              </div>\n' % cta_items[4]
    insertion = anchor + checklist_item("Firebase — hosting + backend-as-a-service") + checklist_item("Cloudflare Pages — fastest edge CDN")
    assert anchor in html, "5th CTA checklist item anchor not found"
    html = html.replace(anchor, insertion)

    html = html.replace(
        '<strong>Jeffthedev__</strong> 5 git commands that have saved me more times than I can count. Save this before your next "oh no" moment. #git #webdev #programming',
        '<strong>Jeffthedev__</strong> Free platforms to deploy your website or app — no credit card required. Save this for your next project. #webdev #hosting #buildinpublic',
    )
    return html

# ---- platform content (shared across both variants) ----
# bullets: flat list of strings, OR sublists: list of (label, [items])
PLATFORMS = [
    dict(n=1, name="Vercel", tagline="Deploy in one click.", dark=True, domain="vercel.com/docs", img="vercel",
         bullets=["Very easy to deploy", "Connect GitHub and deploy automatically", "Great for React and Next.js projects"]),
    dict(n=2, name="Netlify", tagline="The original git-to-deploy.", dark=False, domain="netlify.com", img="netlify",
         bullets=["Just as easy to deploy as Vercel", "Connect GitHub and deploy automatically", "Adds built-in forms and simple functions"]),
    dict(n=3, name="GitHub Pages", tagline="Free forever, no card.", dark=True, domain="pages.github.com", img="github-pages",
         bullets=["Completely free", "Easy to connect with GitHub projects", "Perfect for portfolio websites"]),
    dict(n=4, name="Render", tagline="For the backend half.", dark=False, domain="render.com", img="render",
         sublists=[("Good for:", ["Node.js apps, Python apps &amp; APIs", "Full-stack apps with a database"])]),
    dict(n=5, name="Railway", tagline="Ship backend fast.", dark=True, domain="railway.com", img="railway",
         sublists=[("Best for:", ["Backend apps", "Databases"]), ("Features:", ["Easy deployment", "Free usage credits"])]),
    dict(n=6, name="Firebase", tagline="Hosting + backend in one.", dark=False, domain="firebase.google.com", img="firebase",
         sublists=[("Best for:", ["Web apps", "React / Angular / Vue apps"]), ("Features:", ["Global CDN", "Fast deployment"])]),
    dict(n=7, name="Cloudflare Pages", tagline="Speed as the default.", dark=True, domain="pages.cloudflare.com", img="cloudflare-pages",
         sublists=[("Best for:", ["Static websites", "JAMstack apps"]), ("Features:", ["Fast CDN", "GitHub integration"])]),
]

PCTS = ["22.22", "33.33", "44.44", "55.56", "66.67", "77.78", "88.89"]
NUMS = ["2/9", "3/9", "4/9", "5/9", "6/9", "7/9", "8/9"]

def arrow(dark):
    color = "rgba(255,255,255,0.35)" if dark else "rgba(0,0,0,0.22)"
    cls = "arrow-dark" if dark else "arrow-light"
    return '        <div class="%s"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="%s" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n' % (cls, color)

def prog(dark, pct, num):
    track = "progress-track-dark" if dark else "progress-track-light"
    fill = "progress-fill-dark" if dark else "progress-fill-light"
    numcls = "slide-num-dark" if dark else "slide-num-light"
    return ('        <div class="progress-bar"><div class="progress-track %s">'
            '<div class="progress-fill %s" style="width:%s%%;"></div></div>'
            '<span class="%s">%s</span></div>\n' % (track, fill, pct, numcls, num))

# =================================================================
# VARIANT 1 — "hero": big screenshot, compact tightened bullets
# =================================================================
def hero_mock(p):
    dark = p["dark"]
    dot_c = "rgba(255,255,255,0.25)" if dark else "rgba(0,0,0,0.15)"
    border = "rgba(255,255,255,0.1)" if dark else "var(--light-border)"
    bg = "rgba(255,255,255,0.03)" if dark else "rgba(0,0,0,0.02)"
    dom_c = "rgba(255,255,255,0.4)" if dark else "rgba(0,0,0,0.4)"
    return (
        '          <div style="border-radius:14px;overflow:hidden;border:1px solid ' + border + ';background:' + bg + ';margin-bottom:16px;">\n'
        '            <div style="display:flex;align-items:center;gap:6px;padding:9px 12px;border-bottom:1px solid ' + border + ';">\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="margin-left:8px;font-family:\'Courier New\',monospace;font-size:10.5px;color:' + dom_c + ';">' + p["domain"] + '</div>\n'
        '            </div>\n'
        '            <img src="deploy-platforms-assets/' + p["img"] + '.jpg" style="display:block;width:100%;height:222px;object-fit:cover;object-position:left top;">\n'
        '          </div>\n'
    )

def hero_bullets(p):
    dark = p["dark"]
    dot_c = "var(--green-light)" if dark else "var(--green-dark)"
    text_c = "rgba(255,255,255,0.85)" if dark else "#2A362F"
    label_c = "rgba(255,255,255,0.85)" if dark else "#2A362F"
    out = ""
    if "bullets" in p:
        for line in p["bullets"]:
            out += ('            <div style="display:flex;gap:8px;margin-bottom:5px;"><span style="color:' + dot_c + ';font-weight:700;flex-shrink:0;">&bull;</span>'
                    '<span style="font-family:var(--font);font-size:12.5px;color:' + text_c + ';line-height:1.35;">' + line + '</span></div>\n')
    else:
        for label, items in p["sublists"]:
            out += '            <div style="font-family:var(--font);font-size:12.5px;color:' + label_c + ';font-weight:600;margin:6px 0 4px;">' + label + '</div>\n'
            for line in items:
                out += ('            <div style="display:flex;gap:8px;margin-bottom:4px;"><span style="color:' + dot_c + ';font-weight:700;flex-shrink:0;">&bull;</span>'
                        '<span style="font-family:var(--font);font-size:12.5px;color:' + text_c + ';line-height:1.3;">' + line + '</span></div>\n')
    return '          <div>\n' + out + '          </div>\n'

def hero_slide(p):
    cls = "slide-dark" if p["dark"] else "slide-light"
    head_c = "var(--green-light)" if p["dark"] else "var(--green-dark)"
    tag_body_cls = "body-dark" if p["dark"] else "body-light"
    s = '      <div class="slide %s">\n' % cls
    if p["dark"]:
        s += '        <div class="noise"></div>\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;height:100%;padding:26px 32px 52px;">\n'
    s += hero_mock(p)
    s += '          <div class="heading" style="color:%s;font-size:24px;margin-bottom:4px;">%s. %s</div>\n' % (head_c, p["n"], p["name"])
    s += '          <p class="body-text %s" style="margin-bottom:10px;font-size:12.5px;">%s</p>\n' % (tag_body_cls, p["tagline"])
    s += hero_bullets(p)
    s += '        </div>\n'
    return s

# =================================================================
# VARIANT 2 — "glow": original compact card + radial glow + ghost numeral
# =================================================================
def glow_mock(p):
    dark = p["dark"]
    dot_c = "rgba(255,255,255,0.25)" if dark else "rgba(0,0,0,0.15)"
    border = "rgba(255,255,255,0.1)" if dark else "var(--light-border)"
    bg = "rgba(255,255,255,0.03)" if dark else "rgba(0,0,0,0.02)"
    dom_c = "rgba(255,255,255,0.4)" if dark else "rgba(0,0,0,0.4)"
    return (
        '          <div style="border-radius:12px;overflow:hidden;border:1px solid ' + border + ';background:' + bg + ';">\n'
        '            <div style="display:flex;align-items:center;gap:6px;padding:9px 12px;border-bottom:1px solid ' + border + ';">\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:' + dot_c + ';"></div>\n'
        '              <div style="margin-left:8px;font-family:\'Courier New\',monospace;font-size:10.5px;color:' + dom_c + ';">' + p["domain"] + '</div>\n'
        '            </div>\n'
        '            <img src="deploy-platforms-assets/' + p["img"] + '.jpg" style="display:block;width:100%;height:112px;object-fit:cover;object-position:top;">\n'
        '          </div>\n'
    )

def glow_bullets(p):
    dark = p["dark"]
    dot_c = "var(--green-light)" if dark else "var(--green-dark)"
    text_c = "rgba(255,255,255,0.85)" if dark else "#2A362F"
    out = ""
    if "bullets" in p:
        for line in p["bullets"]:
            out += ('            <div style="display:flex;gap:9px;margin-bottom:9px;"><span style="color:' + dot_c + ';font-weight:700;flex-shrink:0;">&bull;</span>'
                    '<span style="font-family:var(--font);font-size:14px;color:' + text_c + ';line-height:1.4;">' + line + '</span></div>\n')
    else:
        for label, items in p["sublists"]:
            out += '            <div style="font-family:var(--font);font-size:14px;color:' + text_c + ';font-weight:600;margin-bottom:7px;">' + label + '</div>\n'
            for line in items:
                out += ('            <div style="display:flex;gap:9px;margin-bottom:9px;"><span style="color:' + dot_c + ';font-weight:700;flex-shrink:0;">&bull;</span>'
                        '<span style="font-family:var(--font);font-size:14px;color:' + text_c + ';line-height:1.4;">' + line + '</span></div>\n')
    return '          <div style="margin-bottom:16px;">\n' + out + '          </div>\n'

def glow_slide(p):
    cls = "slide-dark" if p["dark"] else "slide-light"
    head_c = "var(--green-light)" if p["dark"] else "var(--green-dark)"
    tag_body_cls = "body-dark" if p["dark"] else "body-light"
    numeral_c = "rgba(255,255,255,0.045)" if p["dark"] else "rgba(0,0,0,0.045)"
    glow_c = "rgba(34,197,94,0.10)" if p["dark"] else "rgba(34,197,94,0.09)"
    s = '      <div class="slide %s">\n' % cls
    if p["dark"]:
        s += '        <div class="noise"></div>\n'
    s += '        <div style="position:absolute;top:-50px;right:-50px;width:260px;height:260px;background:radial-gradient(circle,%s 0%%,transparent 70%%);pointer-events:none;z-index:1;"></div>\n' % glow_c
    s += '        <div style="position:absolute;top:32px;left:26px;font-family:var(--font);font-weight:800;font-size:170px;line-height:1;color:%s;z-index:1;user-select:none;">%s</div>\n' % (numeral_c, p["n"])
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div class="heading" style="color:%s;font-size:28px;margin-bottom:6px;">%s. %s</div>\n' % (head_c, p["n"], p["name"])
    s += '          <p class="body-text %s" style="margin-bottom:14px;font-size:13px;">%s</p>\n' % (tag_body_cls, p["tagline"])
    s += glow_bullets(p)
    s += glow_mock(p)
    s += '        </div>\n'
    return s

markerA = '<span class="slide-num-dark">1/9</span></div>\n      </div>\n'
markerB = '      <!-- SLIDE 9 — CTA -->'

def build(variant):
    html = apply_shared_text(base_html)
    a = html.index(markerA) + len(markerA)
    b = html.index(markerB)
    mid = ""
    for i, p in enumerate(PLATFORMS):
        slide = hero_slide(p) if variant == "hero" else glow_slide(p)
        mid += slide + arrow(p["dark"]) + prog(p["dark"], PCTS[i], NUMS[i]) + "      </div>\n"
    return html[:a] + mid + html[b:]

for variant, out in [("hero", "deploy-platforms-hero.html"), ("glow", "deploy-platforms-glow.html")]:
    html = build(variant)
    with io.open(os.path.join(BASE, out), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out, "len", len(html))
