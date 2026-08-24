#!/usr/bin/env python3
# Build worth-your-money.html from the git-commands.html code-block shell,
# swapping only the text content (cover, 7 content slides, CTA, caption, title).
# Base64 images (avatar / cover portrait / wordmark / CTA) are reused verbatim.

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "git-commands", "git-commands.html")
OUT = os.path.join(BASE, "worth-your-money.html")

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — 5 Things Worth Your Money in Tech</title>",
)

# ---- cover slide text ----
html = html.replace(
    '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
    '<span class="tag tag-dark" style="margin-bottom:11px;">Money · Dev Life</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
    '<div class="heading" style="color:#fff;font-size:31px;margin-bottom:14px;">5 things worth<br><span style="color:var(--green-light);">your money in tech</span></div>',
)
html = html.replace(
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">Stop cutting corners on the wrong things. Spend here, save everywhere else. Swipe.</p>',
)

# ---- slides 2-8 (replace the whole middle block) ----
markerA = '<span class="slide-num-dark">1/9</span></div>\n      </div>\n'
markerB = '      <!-- SLIDE 9 — CTA -->'
a = html.index(markerA) + len(markerA)
b = html.index(markerB)

NB = "&nbsp;"

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

def callout_dark(strong_color, label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(34,197,94,0.06);'
            'border:1px solid rgba(34,197,94,0.18);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;">'
            '<strong style="color:%s;">%s</strong> %s</span></div>\n' % (strong_color, label, text))

def callout_dark_red(label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(255,107,107,0.07);'
            'border:1px solid rgba(255,107,107,0.22);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;">'
            '<strong style="color:#FF6B6B;">%s</strong> %s</span></div>\n' % (label, text))

def callout_light(label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(34,197,94,0.07);'
            'border:1px solid rgba(34,197,94,0.18);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:#3A4A40;line-height:1.5;">'
            '<strong style="color:var(--green-dark);">%s</strong> %s</span></div>\n' % (label, text))

def callout_light_red(label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(255,107,107,0.07);'
            'border:1px solid rgba(255,107,107,0.22);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:#3A4A40;line-height:1.5;">'
            '<strong style="color:#FF6B6B;">%s</strong> %s</span></div>\n' % (label, text))

def slide_dark(tag, badge_cls, badge_txt, head1, head2, body, code_inner, callout):
    s = '      <div class="slide slide-dark">\n'
    s += '        <div class="noise"></div>\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:11px;">\n'
    s += '            <span class="tag tag-dark">%s</span>\n' % tag
    s += '            <span class="badge %s">%s</span>\n' % (badge_cls, badge_txt)
    s += '          </div>\n'
    s += '          <div class="heading" style="color:#fff;margin-bottom:13px;font-size:26px;">%s<br><span style="color:var(--green-light);">%s</span></div>\n' % (head1, head2)
    s += '          <p class="body-text body-dark" style="margin-bottom:14px;font-size:13px;">%s</p>\n' % body
    s += '          <div class="code-block">\n%s          </div>\n' % code_inner
    s += callout
    s += '        </div>\n'
    return s

def slide_light(tag, badge_cls, badge_txt, head1, head2, body, code_inner, callout):
    s = '      <div class="slide slide-light">\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:11px;">\n'
    s += '            <span class="tag tag-light">%s</span>\n' % tag
    s += '            <span class="badge %s">%s</span>\n' % (badge_cls, badge_txt)
    s += '          </div>\n'
    s += '          <div class="heading" style="color:#0A0F0C;font-size:26px;margin-bottom:12px;">%s<br><span style="color:var(--green-dark);">%s</span></div>\n' % (head1, head2)
    s += '          <p class="body-text body-light" style="margin-bottom:13px;font-size:13px;">%s</p>\n' % body
    s += '          <div class="code-block-light">\n%s          </div>\n' % code_inner
    s += callout
    s += '        </div>\n'
    return s

# code line helpers — colored spec + visible label + faint comment.
def cd(code, color, label, cmt):  # dark code-block line
    return ('<span class="code-%s">%s</span>%s<span style="color:rgba(255,255,255,0.82);">%s</span>%s<span class="code-cmt">%s</span>'
            % (color, code, NB * 2, label, NB * 2, cmt))

def cl(code, color, label, cmt):  # light code-block line
    return ('<span class="code-%s">%s</span>%s<span style="color:#3A4A40;">%s</span>%s<span class="code-cmt-l">%s</span>'
            % (color, code, NB * 2, label, NB * 2, cmt))

def block(lines):
    return '            ' + '<br>\n            '.join(lines) + '\n'

slides = []

# SLIDE 2 — #1 Hardware — laptop (dark)
code2 = block([
    cd("16GB+ RAM", "green", "the floor, not the ceiling", "for a dev machine"),
    cd("SSD only", "green", "non-negotiable", "in 2026"),
    cd("the $200 discount", "red", "isn't worth it", "3 years of lag"),
])
slides.append(slide_dark(
    "#1 · Hardware", "badge-green", "Daily driver",
    "Your laptop", "isn't where you save",
    "It's the one tool between you and every line of code you'll ever ship. Buy once, cry once.",
    code2,
    callout_dark("var(--green-light)", "Rule:", "It should outlast the excuses you make for it lagging.")
))

# SLIDE 3 — #2 Environment — monitor (light)
code3 = block([
    cl("27in, 1440p", "green", "the sweet spot", "for code + docs side by side"),
    cl("one extra screen", "green", "measurable", "focus boost"),
    cl("alt-tab archaeology", "red", "the tax", "you pay without one"),
])
slides.append(slide_light(
    "#2 · Setup", "badge-green", "Focus",
    "A second screen", "pays for itself in a week",
    "Docs on one side, code on the other. No more digging through fifteen buried tabs.",
    code3,
    callout_light("Tip:", "Even a $150 used monitor beats zero extra screen real estate.")
))

# SLIDE 4 — #3 Infrastructure — internet (dark)
code4 = block([
    cd("wired &gt; wifi", "green", "for anything", "that actually matters"),
    cd("a backup hotspot", "green", "for the day", "it goes down"),
    cd("'good enough' wifi", "red", "isn't", "when you're mid-deploy"),
])
slides.append(slide_dark(
    "#3 · Infra", "badge-red", "Non-negotiable",
    "Bad wifi is a", "productivity tax",
    "Dropped calls, failed pushes, stalled deploys — the invisible cost adds up faster than you think.",
    code4,
    callout_dark_red("Warning:", "The outage always hits during a live demo or a deploy.")
))

# SLIDE 5 — #4 AI — Claude Pro (light)
code5 = block([
    cl("free tier", "red", "rate-limited", "thin context, waits"),
    cl("Pro", "green", "higher limits", "+ Claude Code access"),
    cl("Claude Code", "green", "agentic coding", "straight from your terminal"),
])
slides.append(slide_light(
    "#4 · AI", "badge-green", "Leverage",
    "Claude Pro is", "leverage, not a luxury",
    "Chat for planning, Claude Code for shipping — inside your own repo, from your own terminal.",
    code5,
    callout_light("Tip:", "It pays for itself the first time it saves you an hour.")
))

# SLIDE 6 — #5 Comfort — workspace (dark)
code6 = block([
    cd("a chair that fits you", "green", "your back", "will thank you at 40"),
    cd("sit/stand desk", "green", "cuts stiffness", "boosts focus"),
    cd("a $30 chair", "red", "false economy", "8 hours a day, every day"),
])
slides.append(slide_dark(
    "#5 · Comfort", "badge-green", "Longevity",
    "Your desk and chair", "run 8 hours a day too",
    "You wouldn't code on a machine with 4GB of RAM. Don't code on furniture that fights you either.",
    code6,
    callout_dark("var(--green-light)", "Rule:", "Hardware upgrades help nothing if your body clocks out first.")
))

# SLIDE 7 — Bonus — domain + hosting (light)
code7 = block([
    cl("$12/yr domain", "green", "the cheapest", "branding you'll ever buy"),
    cl("a paid hosting tier", "green", "no cold starts", "no surprise downtime"),
    cl("yourproject.vercel.app", "red", "not a brand", "it's a default"),
])
slides.append(slide_light(
    "Bonus · Ownership", "badge-green", "Own your name",
    "Your own domain", "is your name on the internet",
    "yourname.com beats a free subdomain the moment you actually want to be found.",
    code7,
    callout_light("Tip:", "Buy the domain the day you start the project, not the day you need it.")
))

# SLIDE 8 — takeaway (dark, custom layout matching git-commands)
takeaway = (
'      <div class="slide slide-dark">\n'
'        <div class="noise"></div>\n'
'        <div style="position:absolute;top:-40px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>\n'
'        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
'          <span class="tag tag-dark" style="margin-bottom:11px;">The takeaway</span>\n'
'          <div class="heading" style="color:#fff;margin-bottom:14px;font-size:27px;">Spend on what<br><span style="color:var(--green-light);">compounds daily.</span></div>\n'
'          <div style="display:flex;flex-direction:column;gap:9px;">\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">The theme is compounding</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Everything on this list gets used every single day — that\'s where the ROI hides.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Cut elsewhere, not here</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Skip the subscription you forgot about, not the tools you touch every day.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:var(--green-light);font-family:var(--font);margin-bottom:5px;">Real talk &rarr;</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">The best investment isn\'t the flashiest one — it\'s the one you stop thinking about.</p>\n'
'            </div>\n'
'          </div>\n'
'        </div>\n'
)

# assemble middle with arrows + progress bars
mid = ""
mid += slides[0] + arrow_dark() + prog_dark("22.22", "2/9") + "      </div>\n"
mid += slides[1] + arrow_light() + prog_light("33.33", "3/9") + "      </div>\n"
mid += slides[2] + arrow_dark() + prog_dark("44.44", "4/9") + "      </div>\n"
mid += slides[3] + arrow_light() + prog_light("55.56", "5/9") + "      </div>\n"
mid += slides[4] + arrow_dark() + prog_dark("66.67", "6/9") + "      </div>\n"
mid += slides[5] + arrow_light() + prog_light("77.78", "7/9") + "      </div>\n"
mid += takeaway + arrow_dark() + prog_dark("88.89", "8/9") + "      </div>\n"

html = html[:a] + mid + html[b:]

# ---- CTA slide ----
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 things worth<br>spending on this year.</div>',
)

cta_items = [
    "A good laptop — the tool you can't work around",
    "Reliable internet — the invisible dependency",
    "Claude Pro — AI leverage in your terminal",
    "Your workspace — desk + chair, 8 hrs a day",
    "A domain + real hosting — own your name",
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

# ---- caption ----
html = html.replace(
    '<strong>Jeffthedev__</strong> 5 git commands that have saved me more times than I can count. Save this before your next "oh no" moment. #git #webdev #programming',
    '<strong>Jeffthedev__</strong> 5 things actually worth paying for as a developer — the rest is optional. Save this before your next Amazon cart regret. #webdev #programming #devlife',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
