#!/usr/bin/env python3
# Build deploy-platforms.html from the git-commands.html shell, swapping the
# text content (cover, 7 content slides, CTA, caption, title). Content slides
# use a numbered-heading + plain-bullet-list + browser-mockup layout (closer
# to the reference "Platforms to deploy" screenshots) instead of the
# code-block layout used elsewhere. Base64 images (avatar / cover portrait /
# wordmark / CTA) are reused verbatim.

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "git-commands", "git-commands.html")
OUT = os.path.join(BASE, "deploy-platforms.html")

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — Free Platforms to Deploy Your App</title>",
)

# ---- cover slide text ----
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

# ---- slides 2-8 (replace the whole middle block) ----
markerA = '<span class="slide-num-dark">1/9</span></div>\n      </div>\n'
markerB = '      <!-- SLIDE 9 — CTA -->'
a = html.index(markerA) + len(markerA)
b = html.index(markerB)

def arrow_dark():
    return '        <div class="arrow-dark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n'

def arrow_light():
    return '        <div class="arrow-light"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="rgba(0,0,0,0.22)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n'

def prog_dark(pct, num):
    return ('        <div class="progress-bar"><div class="progress-track progress-track-dark">'
            '<div class="progress-fill progress-fill-dark" style="width:%s%%;"></div></div>'
            '<span class="slide-num-dark">%s</span></div>\n' % (pct, num))

def prog_light(pct, num):
    return ('        <div class="progress-bar"><div class="progress-track progress-track-light">'
            '<div class="progress-fill progress-fill-light" style="width:%s%%;"></div></div>'
            '<span class="slide-num-light">%s</span></div>\n' % (pct, num))

# ---- bullet list (plain, no code formatting — like the reference screenshots) ----
def bullets_dark(lines):
    items = "".join(
        '            <div style="display:flex;gap:9px;margin-bottom:9px;"><span style="color:var(--green-light);font-weight:700;flex-shrink:0;">&bull;</span>'
        '<span style="font-family:var(--font);font-size:14px;color:rgba(255,255,255,0.85);line-height:1.4;">%s</span></div>\n' % line
        for line in lines
    )
    return '          <div style="margin-bottom:16px;">\n%s          </div>\n' % items

def bullets_light(lines):
    items = "".join(
        '            <div style="display:flex;gap:9px;margin-bottom:9px;"><span style="color:var(--green-dark);font-weight:700;flex-shrink:0;">&bull;</span>'
        '<span style="font-family:var(--font);font-size:14px;color:#2A362F;line-height:1.4;">%s</span></div>\n' % line
        for line in lines
    )
    return '          <div style="margin-bottom:16px;">\n%s          </div>\n' % items

def sublist_dark(label, lines):
    s = '          <div style="font-family:var(--font);font-size:14px;color:rgba(255,255,255,0.85);font-weight:600;margin-bottom:7px;">%s</div>\n' % label
    s += bullets_dark(lines)
    return s

def sublist_light(label, lines):
    s = '          <div style="font-family:var(--font);font-size:14px;color:#2A362F;font-weight:600;margin-bottom:7px;">%s</div>\n' % label
    s += bullets_light(lines)
    return s

# ---- simple abstract browser-chrome mockup (no real screenshots — neutral dots + skeleton bars) ----
def browser_mock_dark(domain, img):
    return (
        '          <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.03);">\n'
        '            <div style="display:flex;align-items:center;gap:6px;padding:9px 12px;border-bottom:1px solid rgba(255,255,255,0.08);">\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.25);"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.25);"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.25);"></div>\n'
        '              <div style="margin-left:8px;font-family:\'Courier New\',monospace;font-size:10.5px;color:rgba(255,255,255,0.4);">' + domain + '</div>\n'
        '            </div>\n'
        '            <img src="deploy-platforms-assets/' + img + '.jpg" style="display:block;width:100%;height:112px;object-fit:cover;object-position:top;">\n'
        '          </div>\n'
    )

def browser_mock_light(domain, img):
    return (
        '          <div style="border-radius:12px;overflow:hidden;border:1px solid var(--light-border);background:rgba(0,0,0,0.02);">\n'
        '            <div style="display:flex;align-items:center;gap:6px;padding:9px 12px;border-bottom:1px solid var(--light-border);">\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(0,0,0,0.15);"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(0,0,0,0.15);"></div>\n'
        '              <div style="width:7px;height:7px;border-radius:50%;background:rgba(0,0,0,0.15);"></div>\n'
        '              <div style="margin-left:8px;font-family:\'Courier New\',monospace;font-size:10.5px;color:rgba(0,0,0,0.4);">' + domain + '</div>\n'
        '            </div>\n'
        '            <img src="deploy-platforms-assets/' + img + '.jpg" style="display:block;width:100%;height:112px;object-fit:cover;object-position:top;">\n'
        '          </div>\n'
    )

def slide_dark(number, name, tagline, body_html, domain, img):
    s = '      <div class="slide slide-dark">\n'
    s += '        <div class="noise"></div>\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div class="heading" style="color:var(--green-light);font-size:28px;margin-bottom:6px;">%s. %s</div>\n' % (number, name)
    s += '          <p class="body-text body-dark" style="margin-bottom:14px;font-size:13px;">%s</p>\n' % tagline
    s += body_html
    s += browser_mock_dark(domain, img)
    s += '        </div>\n'
    return s

def slide_light(number, name, tagline, body_html, domain, img):
    s = '      <div class="slide slide-light">\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div class="heading" style="color:var(--green-dark);font-size:28px;margin-bottom:6px;">%s. %s</div>\n' % (number, name)
    s += '          <p class="body-text body-light" style="margin-bottom:14px;font-size:13px;">%s</p>\n' % tagline
    s += body_html
    s += browser_mock_light(domain, img)
    s += '        </div>\n'
    return s

slides = []

# SLIDE 2 — #1 Vercel (dark)
slides.append(slide_dark(
    1, "Vercel", "Deploy in one click.",
    bullets_dark([
        "Very easy to deploy",
        "Connect GitHub and deploy automatically",
        "Great for React and Next.js projects",
    ]),
    "vercel.com/docs", "vercel"
))

# SLIDE 3 — #2 Netlify (light)
slides.append(slide_light(
    2, "Netlify", "The original git-to-deploy.",
    bullets_light([
        "Just as easy to deploy as Vercel",
        "Connect GitHub and deploy automatically",
        "Adds built-in forms and simple functions",
    ]),
    "netlify.com", "netlify"
))

# SLIDE 4 — #3 GitHub Pages (dark)
slides.append(slide_dark(
    3, "GitHub Pages", "Free forever, no card.",
    bullets_dark([
        "Completely free",
        "Easy to connect with GitHub projects",
        "Perfect for portfolio websites",
    ]),
    "pages.github.com", "github-pages"
))

# SLIDE 5 — #4 Render (light)
slides.append(slide_light(
    4, "Render", "For the backend half.",
    sublist_light("Good for:", [
        "Node.js apps, Python apps &amp; APIs",
        "Full-stack apps with a database",
    ]),
    "render.com", "render"
))

# SLIDE 6 — #5 Railway (dark)
slides.append(slide_dark(
    5, "Railway", "Ship backend fast.",
    sublist_dark("Best for:", ["Backend apps", "Databases"]) +
    sublist_dark("Features:", ["Easy deployment", "Free usage credits for beginners"]),
    "railway.com", "railway"
))

# SLIDE 7 — #6 Firebase (light)
slides.append(slide_light(
    6, "Firebase", "Hosting + backend in one.",
    sublist_light("Best for:", ["Web apps", "React / Angular / Vue apps"]) +
    sublist_light("Features:", ["Global CDN", "Fast deployment", "Easy CLI commands"]),
    "firebase.google.com", "firebase"
))

# SLIDE 8 — #7 Cloudflare Pages (dark)
slides.append(slide_dark(
    7, "Cloudflare Pages", "Speed as the default.",
    sublist_dark("Best for:", ["Static websites", "JAMstack apps"]) +
    sublist_dark("Features:", ["Fast CDN", "GitHub integration"]),
    "pages.cloudflare.com", "cloudflare-pages"
))

# assemble middle with arrows + progress bars
PCTS = ["22.22", "33.33", "44.44", "55.56", "66.67", "77.78", "88.89"]
NUMS = ["2/9", "3/9", "4/9", "5/9", "6/9", "7/9", "8/9"]
DARK_FLAGS = [True, False, True, False, True, False, True]

mid = ""
for i, slide in enumerate(slides):
    arrow = arrow_dark() if DARK_FLAGS[i] else arrow_light()
    prog = prog_dark(PCTS[i], NUMS[i]) if DARK_FLAGS[i] else prog_light(PCTS[i], NUMS[i])
    mid += slide + arrow + prog + "      </div>\n"

html = html[:a] + mid + html[b:]

# ---- CTA slide ----
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
    "Firebase — hosting + backend-as-a-service",
    "Cloudflare Pages — fastest edge CDN",
]
old_items = [
    "reflog — recover seemingly lost commits",
    "stash — shelve work, switch branches fast",
    "commit --amend — fix the last commit",
    "cherry-pick — grab one commit by hash",
    "reset --soft — uncommit but keep your work",
]
for old, new in zip(old_items, cta_items[:5]):
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
insertion = anchor + checklist_item(cta_items[5]) + checklist_item(cta_items[6])
assert anchor in html, "5th CTA checklist item anchor not found"
html = html.replace(anchor, insertion)

# ---- caption ----
html = html.replace(
    '<strong>Jeffthedev__</strong> 5 git commands that have saved me more times than I can count. Save this before your next "oh no" moment. #git #webdev #programming',
    '<strong>Jeffthedev__</strong> Free platforms to deploy your website or app — no credit card required. Save this for your next project. #webdev #hosting #buildinpublic',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
