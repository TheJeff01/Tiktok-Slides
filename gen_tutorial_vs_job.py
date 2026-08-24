#!/usr/bin/env python3
# Build tutorial-vs-job.html from the git-commands.html code-block shell,
# swapping only the text content (cover, 7 content slides, CTA, caption, title).
# Base64 images (avatar / cover portrait / wordmark / CTA) are reused verbatim.

import io

SRC = "git-commands.html"
OUT = "tutorial-vs-job.html"

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — What Tutorials Teach You vs. What the Job Is</title>",
)

# ---- cover slide text ----
html = html.replace(
    '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
    '<span class="tag tag-dark" style="margin-bottom:11px;">Career · Real Talk</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
    '<div class="heading" style="color:#fff;font-size:30px;margin-bottom:14px;">What tutorials teach<br><span style="color:var(--green-light);">vs. what the job is</span></div>',
)
html = html.replace(
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">Six gaps between the course and the actual job — the parts nobody puts in the tutorial. Swipe.</p>',
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

def callout_dark(label, text):
    return ('          <div style="margin-top:12px;padding:10px 13px;background:rgba(34,197,94,0.06);'
            'border:1px solid rgba(34,197,94,0.18);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;">'
            '<strong style="color:var(--green-light);">%s</strong> %s</span></div>\n' % (label, text))

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

# code line helpers for the "tutorial vs job" contrast blocks.
# Return lines WITHOUT trailing <br>; joined later (never rstrip "<br>\n").
def cmt_d(text):     # faint comment line, dark slide
    return '<span class="code-cmt">%s</span>' % text

def cmt_l(text):     # faint comment line, light slide
    return '<span class="code-cmt-l">%s</span>' % text

def green_d(text):   # "the tutorial" line, dark slide
    return '<span class="code-green">%s</span>' % text

def green_l(text):   # "the tutorial" line, light slide (green-dark for contrast)
    return '<span class="code-key-l">%s</span>' % text

def red_line(text):  # "the job" line, both slide types
    return '<span class="code-red">%s</span>' % text

def block(lines):
    return '            ' + '<br>\n            '.join(lines) + '\n'

slides = []

# SLIDE 2 — #1 Git (dark)
code2 = block([
    cmt_d("// the tutorial"),
    green_d("git add . → commit → push"),
    cmt_d("// the job — friday, 4:47pm"),
    red_line("CONFLICT: merge conflict in 14 files"),
])
slides.append(slide_dark(
    "#1 · Git", "badge-red", "Reality check",
    "The git you learn,", "the git you survive",
    "Tutorials end at push. The job starts where the history gets weird.",
    code2,
    callout_dark("Real talk →", "git stash and git reflog will save you more times than any course ever did.")
))

# SLIDE 3 — #2 Writing code (light)
code3 = block([
    cmt_l("// the tutorial — blank canvas"),
    green_l("npx create-react-app my-app"),
    cmt_l("// the job — 3 hours of reading later"),
    red_line("1 file changed, +1 −1"),
])
slides.append(slide_light(
    "#2 · The code", "badge-green", "The real skill",
    "Less writing code,", "more reading it",
    "You dream of greenfield. You inherit eight years of someone else’s decisions.",
    code3,
    callout_light("Tip:", "Reading code is the real skill — you’ll do ten times more of it than writing.")
))

# SLIDE 4 — #3 Requirements (dark)
code4 = block([
    cmt_d("// the tutorial"),
    green_d("spec.md — clear, complete, final"),
    cmt_d("// the job, mid-sprint"),
    red_line("“small change” → half the feature rewritten"),
])
slides.append(slide_dark(
    "#3 · Requirements", "badge-red", "Moving target",
    "A written spec,", "a moving target",
    "The course hands you requirements. The job hands you a vibe and a deadline.",
    code4,
    callout_dark("Rule:", "Ask the clarifying questions before you code — not after the demo.")
))

# SLIDE 5 — #4 Debugging (light)
code5 = block([
    cmt_l("// the tutorial"),
    green_l("Error at line 42 → fix line 42"),
    cmt_l("// the job"),
    red_line("passes locally · crashes in prod"),
    red_line("status: cannot reproduce"),
])
slides.append(slide_light(
    "#4 · Debugging", "badge-red", "Prod only",
    "Errors with answers,", "bugs with alibis",
    "Tutorial bugs point at a line. Real bugs only show up when a real user is watching.",
    code5,
    callout_light_red("Warning:", "“Works on my machine” are the four most expensive words in software.")
))

# SLIDE 6 — #5 The calendar (dark)
code6 = block([
    cmt_d("// the tutorial"),
    green_d("09:00 – 17:00 → deep work"),
    cmt_d("// the job"),
    red_line("09:30 standup · 11:00 sync"),
    red_line("14:00 “quick call?” · 16:00 finally code"),
])
slides.append(slide_dark(
    "#5 · The calendar", "badge-red", "Meetings",
    "Eight hours of flow,", "meet your calendar",
    "You pictured all-day deep work. Your calendar had other plans.",
    code6,
    callout_dark("Rule:", "Block your focus time like it’s production — because your output is.")
))

# SLIDE 7 — #6 Shipping (light)
code7 = block([
    cmt_l("// the tutorial"),
    green_l("npm run dev → it works → done"),
    cmt_l("// the job"),
    red_line("deploy → 500 → missing env var → rollback"),
])
slides.append(slide_light(
    "#6 · Shipping", "badge-green", "Done ≠ done",
    "“It works” is easy,", "“it’s live” is the job",
    "The tutorial ends when the code runs. The job starts when real users touch it.",
    code7,
    callout_light("Remember:", "Done means deployed, monitored, and still standing on Monday.")
))

# SLIDE 8 — takeaway (dark, custom layout matching git-commands)
takeaway = (
'      <div class="slide slide-dark">\n'
'        <div class="noise"></div>\n'
'        <div style="position:absolute;top:-40px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>\n'
'        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
'          <span class="tag tag-dark" style="margin-bottom:11px;">The takeaway</span>\n'
'          <div class="heading" style="color:#fff;margin-bottom:14px;font-size:27px;">The gap isn’t a scam —<br><span style="color:var(--green-light);">it’s the actual job.</span></div>\n'
'          <div style="display:flex;flex-direction:column;gap:9px;">\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Tutorials teach syntax</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">The job teaches judgment — tradeoffs, legacy code, and working with people.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Keep doing the courses</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">They get you in the door. Reading code, asking questions, and shipping keep you there.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:var(--green-light);font-family:var(--font);margin-bottom:5px;">Real talk &rarr;</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Every senior you admire was once shocked by this exact list. You’ll be fine.</p>\n'
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
    '<span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Cheat Sheet</span>',
    '<span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Reality Check</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">Screenshot this before<br>your first dev job.</div>',
)

cta_items = [
    "Less writing code, more reading it",
    "Requirements move — ask questions first",
    "“Works on my machine” isn’t done",
    "Guard your focus time from meetings",
    "Done = deployed and surviving real users",
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
    '<strong>Jeffthedev__</strong> What the tutorials teach you vs. what the job actually is — the parts no course covers. Which one hit you hardest? #webdev #programming #softwareengineer',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
