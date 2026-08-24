#!/usr/bin/env python3
# Build http-status-codes.html from the git-commands.html code-block shell,
# swapping only the text content (cover, 7 content slides, CTA, caption, title).
# Base64 images (avatar / cover portrait / wordmark / CTA) are reused verbatim.

import io

SRC = "git-commands.html"
OUT = "http-status-codes.html"

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — HTTP Status Codes Every Dev Should Know</title>",
)

# ---- cover slide text ----
html = html.replace(
    '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
    '<span class="tag tag-dark" style="margin-bottom:11px;">HTTP · Field Guide</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
    '<div class="heading" style="color:#fff;font-size:31px;margin-bottom:14px;">HTTP status codes<br><span style="color:var(--green-light);">every dev should know</span></div>',
)
html = html.replace(
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The response codes you’ll actually meet in real apps — what each one means and when it shows up. Swipe.</p>',
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

# code line helpers — colored code + visible label + faint comment.
# Return the line WITHOUT a trailing <br>; lines are joined later so the
# block never ends on a dangling <br> (and we avoid fragile rstrip tricks).
def cd(code, color, label, cmt):  # dark code-block line
    return ('<span class="code-%s">%s</span>%s<span style="color:rgba(255,255,255,0.82);">%s</span>%s<span class="code-cmt">%s</span>'
            % (color, code, NB * 2, label, NB * 2, cmt))

def cl(code, color, label, cmt):  # light code-block line
    return ('<span class="code-%s">%s</span>%s<span style="color:#3A4A40;">%s</span>%s<span class="code-cmt-l">%s</span>'
            % (color, code, NB * 2, label, NB * 2, cmt))

def block(lines):
    # join code lines with <br> separators + 12-space indent, trailing newline
    return '            ' + '<br>\n            '.join(lines) + '\n'

slides = []

# SLIDE 2 — #1 the map (dark)
code2 = block([
    cd("1xx", "cmt", "Informational", "hold on a sec"),
    cd("2xx", "green", "Success", "it worked"),
    cd("3xx", "green", "Redirection", "look elsewhere"),
    cd("4xx", "red", "Client error", "your fault"),
    cd("5xx", "red", "Server error", "their fault"),
])
slides.append(slide_dark(
    "#1 · The map", "badge-green", "Mental model",
    "Five classes,", "one digit each",
    "Every code’s first digit tells you the category. Learn the five buckets and you can guess the rest.",
    code2,
    callout_dark("var(--green-light)", "Rule:", "First digit = the category. The other two just narrow it down.")
))

# SLIDE 3 — #2 2xx success (light)
code3 = block([
    cl("200", "green", "OK", "standard success"),
    cl("201", "green", "Created", "POST made a resource"),
    cl("202", "green", "Accepted", "queued, not done yet"),
    cl("204", "green", "No Content", "success, empty body"),
])
slides.append(slide_light(
    "#2 · 2xx", "badge-green", "Success",
    "2xx success", "it actually worked",
    "The happy path. The request was received, understood, and accepted by the server.",
    code3,
    callout_light("Tip:", "After a successful POST, return 201 with a Location header — not a bare 200.")
))

# SLIDE 4 — #3 3xx redirects (dark)
code4 = block([
    cd("301", "green", "Moved Permanently", "update your links"),
    cd("302", "green", "Found", "temporary redirect"),
    cd("304", "green", "Not Modified", "use your cache"),
    cd("308", "green", "Permanent Redirect", "keeps the method"),
])
slides.append(slide_dark(
    "#3 · 3xx", "badge-green", "Redirects",
    "3xx redirects", "look over there",
    "The resource lives somewhere else — or it hasn’t changed since you last asked for it.",
    code4,
    callout_dark("var(--green-light)", "Rule:", "301 is permanent and cached hard. Reach for 302/307 when the move is temporary.")
))

# SLIDE 5 — #4 the big four 4xx (light)
code5 = block([
    cl("400", "red", "Bad Request", "malformed input"),
    cl("401", "red", "Unauthorized", "you’re not logged in"),
    cl("403", "red", "Forbidden", "logged in, not allowed"),
    cl("404", "red", "Not Found", "no such resource"),
])
slides.append(slide_light(
    "#4 · 4xx", "badge-red", "Client error",
    "4xx client errors", "your request, your bug",
    "The four you’ll hit most. The request reached the server, but something about it was wrong.",
    code5,
    callout_light_red("Warning:", "401 = who are you? 403 = I know you, you still can’t. Don’t swap them.")
))

# SLIDE 6 — #5 the useful 4xx (dark)
code6 = block([
    cd("405", "red", "Method Not Allowed", "wrong verb"),
    cd("409", "red", "Conflict", "state clash"),
    cd("422", "red", "Unprocessable", "validation failed"),
    cd("429", "red", "Too Many Requests", "slow down"),
])
slides.append(slide_dark(
    "#5 · 4xx", "badge-green", "Worth knowing",
    "Beyond 404", "the precise 4xx",
    "The codes that make an API feel deliberate instead of throwing 400 at absolutely everything.",
    code6,
    callout_dark("var(--green-light)", "Tip:", "422 is the clean way to say ‘valid JSON, invalid data’. 429 should send a Retry-After header.")
))

# SLIDE 7 — Bonus 5xx (light)
code7 = block([
    cl("500", "red", "Internal Server Error", "it crashed"),
    cl("502", "red", "Bad Gateway", "bad upstream reply"),
    cl("503", "red", "Service Unavailable", "down / overloaded"),
    cl("504", "red", "Gateway Timeout", "upstream too slow"),
])
slides.append(slide_light(
    "Bonus · 5xx", "badge-red", "Server error",
    "5xx server errors", "not your fault",
    "The request was fine — the server broke trying to handle it. Time to go read the logs.",
    code7,
    callout_light("Tip:", "502 vs 504: 502 = upstream sent garbage, 504 = upstream never answered in time.")
))

# SLIDE 8 — takeaway (dark, custom layout matching git-commands)
takeaway = (
'      <div class="slide slide-dark">\n'
'        <div class="noise"></div>\n'
'        <div style="position:absolute;top:-40px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>\n'
'        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
'          <span class="tag tag-dark" style="margin-bottom:11px;">The takeaway</span>\n'
'          <div class="heading" style="color:#fff;margin-bottom:14px;font-size:27px;">Status codes are a<br><span style="color:var(--green-light);">shared language.</span></div>\n'
'          <div style="display:flex;flex-direction:column;gap:9px;">\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">The first digit tells the story</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">2xx worked, 3xx moved, 4xx you, 5xx them. Everything else is just detail.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Be specific on purpose</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">403 over 401, 409 over 400, 422 over 500. The right code is free documentation.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:var(--green-light);font-family:var(--font);margin-bottom:5px;">Real talk &rarr;</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Returning 200 with {error:true} in the body breaks every client that trusts the status line.</p>\n'
'            </div>\n'
'          </div>\n'
'        </div>\n'
)

# assemble middle with arrows + progress bars
mid = ""
# slide 2 (dark)
mid += slides[0] + arrow_dark() + prog_dark("22.22", "2/9") + "      </div>\n"
# slide 3 (light)
mid += slides[1] + arrow_light() + prog_light("33.33", "3/9") + "      </div>\n"
# slide 4 (dark)
mid += slides[2] + arrow_dark() + prog_dark("44.44", "4/9") + "      </div>\n"
# slide 5 (light)
mid += slides[3] + arrow_light() + prog_light("55.56", "5/9") + "      </div>\n"
# slide 6 (dark)
mid += slides[4] + arrow_dark() + prog_dark("66.67", "6/9") + "      </div>\n"
# slide 7 (light)
mid += slides[5] + arrow_light() + prog_light("77.78", "7/9") + "      </div>\n"
# slide 8 (dark, takeaway)
mid += takeaway + arrow_dark() + prog_dark("88.89", "8/9") + "      </div>\n"

html = html[:a] + mid + html[b:]

# ---- CTA slide ----
html = html.replace(
    '<span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Cheat Sheet</span>',
    '<span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Cheat Sheet</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">Bookmark this before<br>your next 3am bug.</div>',
)

cta_items = [
    "2xx — success, the request worked",
    "3xx — redirect, look somewhere else",
    "4xx — client error, fix your request",
    "5xx — server error, go check the logs",
    "401 ≠ 403, 502 ≠ 504 — know the pairs",
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
    '<strong>Jeffthedev__</strong> The HTTP status codes you’ll actually meet in production — and what each one is really telling you. Save it for your next debugging session. #webdev #programming #backend',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
