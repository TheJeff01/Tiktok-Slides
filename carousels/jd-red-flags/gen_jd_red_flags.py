#!/usr/bin/env python3
# Build jd-red-flags.html from the git-commands.html code-block shell,
# swapping only the text content (cover, 7 content slides, CTA, caption, title).
# Base64 images (avatar / cover portrait / wordmark / CTA) are reused verbatim.

import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "git-commands", "git-commands.html")
OUT = os.path.join(BASE, "jd-red-flags.html")

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — 5 Red Flags in a Job Description</title>",
)

# ---- cover slide text ----
html = html.replace(
    '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
    '<span class="tag tag-dark" style="margin-bottom:11px;">Career · Job Hunt</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
    '<div class="heading" style="color:#fff;font-size:31px;margin-bottom:14px;">5 red flags in a<br><span style="color:var(--green-light);">job description</span></div>',
)
html = html.replace(
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">Some postings tell on themselves before the interview even starts. Swipe.</p>',
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

def callout_dark_red(label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(255,107,107,0.07);'
            'border:1px solid rgba(255,107,107,0.22);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;">'
            '<strong style="color:#FF6B6B;">%s</strong> %s</span></div>\n' % (label, text))

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

def block(lines):
    return '            ' + '<br>\n            '.join(lines) + '\n'

def quote_dark(quote, note):
    return block([
        '<span class="code-red">%s</span>' % quote,
        '<span class="code-cmt">// %s</span>' % note,
    ])

def quote_light(quote, note):
    return block([
        '<span class="code-red">%s</span>' % quote,
        '<span class="code-cmt-l">// %s</span>' % note,
    ])

slides = []

# SLIDE 2 — #1 Scope (dark)
slides.append(slide_dark(
    "#1 · Scope", "badge-red", "Red flag",
    "Fast-paced", "environment",
    "Translation: no defined role, and you're about to become everyone's overflow valve.",
    quote_dark('"fast-paced, wears many hats"', "we're understaffed and haven't hired a plan"),
    callout_dark_red("Translation:", "If the role can't be described in one sentence, it hasn't been thought through.")
))

# SLIDE 3 — #2 The number (light)
slides.append(slide_light(
    "#2 · The number", "badge-red", "Red flag",
    "Competitive", "salary",
    "Competitive compared to what? It's a number they won't say to your face.",
    quote_light('"competitive salary" (no range)', "we hope you don't compare offers"),
    callout_light_red("Translation:", "Pay transparency exists. No range in 2026 is a choice, not an oversight.")
))

# SLIDE 4 — #3 The buzzword (dark)
slides.append(slide_dark(
    "#3 · The buzzword", "badge-red", "Red flag",
    "Looking for a", "rockstar ninja",
    "The vocabulary is a decade old. So, often, is the codebase and the culture.",
    quote_dark('"rockstar / ninja / 10x engineer"', "we want overperformance at underpay"),
    callout_dark_red("Translation:", "Job titles from 2013 usually come with management styles from 2013.")
))

# SLIDE 5 — #4 The fine print (light)
slides.append(slide_light(
    "#4 · The fine print", "badge-red", "Red flag",
    "Occasional weekend", "work required",
    "Overtime isn't occasional when it's already written into the posting before you've started.",
    quote_light('"must be willing to work weekends"', "unpaid overtime, pre-negotiated for you"),
    callout_light_red("Translation:", "If it's in the JD, it's not the exception — it's the actual schedule.")
))

# SLIDE 6 — #5 The math doesn't work (dark)
slides.append(slide_dark(
    "#5 · The math", "badge-red", "Red flag",
    "5+ years in a", "2-year-old framework",
    "Nobody proofread this. If they can't manage a job post, notice the pattern.",
    quote_dark('"5+ years required" (framework shipped 2 years ago)', "they don't know what they're asking for"),
    callout_dark_red("Translation:", "Written by someone who's never opened the docs for the thing they're hiring for.")
))

# SLIDE 7 — Bonus, the vibe (light)
slides.append(slide_light(
    "Bonus · The vibe", "badge-red", "Watch for it",
    "We're like a", "family here",
    "Families don't performance-review you. Watch what this phrase gets used to excuse.",
    quote_light('"we\'re like a family here"', "guilt is the retention strategy"),
    callout_light_red("Translation:", "A healthy team doesn't need a metaphor to stop you from asking for boundaries.")
))

# SLIDE 8 — takeaway (dark, custom layout matching git-commands)
takeaway = (
'      <div class="slide slide-dark">\n'
'        <div class="noise"></div>\n'
'        <div style="position:absolute;top:-40px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>\n'
'        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
'          <span class="tag tag-dark" style="margin-bottom:11px;">The takeaway</span>\n'
'          <div class="heading" style="color:#fff;margin-bottom:14px;font-size:27px;">Red flags are<br><span style="color:var(--green-light);">just bad writing.</span></div>\n'
'          <div style="display:flex;flex-direction:column;gap:9px;">\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Vague means unplanned</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">If they can\'t describe the role clearly, they haven\'t figured out what they need.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Silence is a number they know is low</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Missing salary range, missing team size — they\'re all the same tell.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:var(--green-light);font-family:var(--font);margin-bottom:5px;">Real talk &rarr;</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Reading the JD closely isn\'t being picky — it\'s doing the interview before the interview.</p>\n'
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
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 phrases to read twice<br>before you apply.</div>',
)

cta_items = [
    "“fast-paced” — undefined role, you're the overflow",
    "no salary range — they hope you won't compare",
    "“rockstar / ninja” — decade-old culture, still around",
    "“occasional weekends” — the real schedule, not the exception",
    "“like a family” — guilt dressed up as culture",
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
    '<strong>Jeffthedev__</strong> 5 phrases in a job description that are quietly telling on the company. Save this before your next application round. #careertips #webdev #techjobs',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
