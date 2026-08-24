#!/usr/bin/env python3
# Build nextjs-vs-tanstack.html from the git-commands.html code-block shell,
# swapping only the text content (cover, 7 content slides, CTA, caption, title).
# Base64 images (avatar / cover portrait / wordmark / CTA) are reused verbatim.

import io

SRC = "git-commands.html"
OUT = "nextjs-vs-tanstack.html"

with io.open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ---- title ----
html = html.replace(
    "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
    "<title>Jeffthedev — Next.js vs TanStack Start</title>",
)

# ---- cover slide text ----
html = html.replace(
    '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
    '<span class="tag tag-dark" style="margin-bottom:11px;">React · Head to Head</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
    '<div class="heading" style="color:#fff;font-size:30px;margin-bottom:14px;">Next.js vs TanStack<br><span style="color:var(--green-light);">which one in 2026?</span></div>',
)
html = html.replace(
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
    '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">Two ways to build full-stack React that disagree on almost everything. The honest comparison — swipe.</p>',
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

# code line helpers — comparison blocks: faint framework label comment,
# then a green approach line; red is reserved for genuine pain points.
# Lines returned WITHOUT trailing <br>; joined later (never rstrip "<br>\n").
def cmt_d(text):
    return '<span class="code-cmt">%s</span>' % text

def cmt_l(text):
    return '<span class="code-cmt-l">%s</span>' % text

def green_d(text):
    return '<span class="code-green">%s</span>' % text

def green_l(text):
    return '<span class="code-key-l">%s</span>' % text

def red_line(text):
    return '<span class="code-red">%s</span>' % text

def block(lines):
    return '            ' + '<br>\n            '.join(lines) + '\n'

slides = []

# SLIDE 2 — #1 Philosophy (dark)
code2 = block([
    cmt_d("// next.js"),
    green_d("server components · client islands"),
    cmt_d("// tanstack start"),
    green_d("client app first · SSR when it helps"),
])
slides.append(slide_dark(
    "#1 · Philosophy", "badge-green", "Big picture",
    "Server-first", "meets client-first",
    "Next.js starts on the server and sprinkles in the client. TanStack starts from the client and reaches back.",
    code2,
    callout_dark("Real talk →", "Neither is wrong. They optimize for different kinds of apps.")
))

# SLIDE 3 — #2 Routing (light)
code3 = block([
    cmt_l("// next.js — app router"),
    green_l("app/blog/[slug]/page.tsx"),
    cmt_l("// tanstack router"),
    green_l("routes/blog.$slug.tsx → params typed"),
])
slides.append(slide_light(
    "#2 · Routing", "badge-green", "Type-safe",
    "Same idea,", "different guarantees",
    "Both route from files. Only one can prove your links and params are real at compile time.",
    code3,
    callout_light("Tip:", "In TanStack, a broken Link is a type error before it’s ever a 404.")
))

# SLIDE 4 — #3 Data fetching (dark)
code4 = block([
    cmt_d("// next.js — in a server component"),
    green_d("const posts = await getPosts()"),
    cmt_d("// tanstack — route loader"),
    green_d("loader: () => ensureQueryData(posts)"),
])
slides.append(slide_dark(
    "#3 · Data", "badge-green", "RSC vs loaders",
    "Fetch in render,", "or load before it",
    "Next fetches while the server renders. TanStack loads before render and hands it to Query.",
    code4,
    callout_dark("Real talk →", "Next hides the wire, TanStack shows you the cache. Pick the magic you can debug.")
))

# SLIDE 5 — #4 Caching (light, the pain point)
code5 = block([
    cmt_l("// next.js"),
    red_line("4 layers: memo · data · route · router"),
    cmt_l("// tanstack"),
    green_l("one cache: TanStack Query — you own it"),
])
slides.append(slide_light(
    "#4 · Caching", "badge-red", "Pain point",
    "Four caches,", "or just one",
    "The loudest Next.js complaint isn’t RSC — it’s guessing which cache served you stale data.",
    code5,
    callout_light_red("Warning:", "If you can’t explain why a page is stale, the cache owns you — not the other way round.")
))

# SLIDE 6 — #5 Server calls (dark)
code6 = block([
    cmt_d("// next.js — server action"),
    green_d("'use server' → form actions"),
    cmt_d("// tanstack"),
    green_d("createServerFn() → typed RPC"),
])
slides.append(slide_dark(
    "#5 · Server calls", "badge-green", "Typed RPC",
    "Both are a POST —", "one types the trip",
    "Server actions and server functions compile to the same thing. The difference is what TypeScript knows.",
    code6,
    callout_dark("Rule:", "If the client calls the server, the types should make the round trip too.")
))

# SLIDE 7 — #6 Choosing (light)
code7 = block([
    cmt_l("// next.js"),
    green_l("huge ecosystem · hiring pool · Vercel DX"),
    cmt_l("// tanstack"),
    green_l("Vite under the hood → deploy anywhere"),
])
slides.append(slide_light(
    "#6 · Choosing", "badge-green", "Tradeoffs",
    "The résumé pick,", "or the control pick",
    "Next.js has a decade of answers on Stack Overflow. TanStack gives you the whole machine, visible.",
    code7,
    callout_light("Tip:", "Boring reasons — team, hiring, docs — beat benchmark charts every time.")
))

# SLIDE 8 — takeaway (dark, custom layout matching git-commands)
takeaway = (
'      <div class="slide slide-dark">\n'
'        <div class="noise"></div>\n'
'        <div style="position:absolute;top:-40px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>\n'
'        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
'          <span class="tag tag-dark" style="margin-bottom:11px;">The takeaway</span>\n'
'          <div class="heading" style="color:#fff;margin-bottom:14px;font-size:27px;">It’s not a war —<br><span style="color:var(--green-light);">it’s a fit question.</span></div>\n'
'          <div style="display:flex;flex-direction:column;gap:9px;">\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Pick Next.js when…</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">Content and SEO carry the app, pages mix marketing with product, and you want the ecosystem to carry you.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:#fff;font-family:var(--font);margin-bottom:5px;">Pick TanStack when…</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">It’s an app-like dashboard, the client does the heavy lifting, and you want types end to end with Query at the core.</p>\n'
'            </div>\n'
'            <div style="padding:12px 14px;background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:10px;">\n'
'              <div style="font-size:13px;font-weight:700;color:var(--green-light);font-family:var(--font);margin-bottom:5px;">Real talk &rarr;</div>\n'
'              <p style="font-size:12px;color:rgba(255,255,255,0.55);font-family:var(--font);line-height:1.5;">You’re not marrying a framework — you’re hiring one for this app. Rehire per project.</p>\n'
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
    '<span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Verdict</span>',
)
html = html.replace(
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
    '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">Save this for the next<br>framework debate.</div>',
)

cta_items = [
    "Next = server-first · TanStack = client-first",
    "TanStack routes are typed end to end",
    "Four Next.js caches vs one Query cache",
    "‘use server’ vs createServerFn()",
    "Choose per app, not per hype cycle",
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
    '<strong>Jeffthedev__</strong> Next.js vs TanStack Start — the honest comparison, no fanboying. Which side are you on? #react #nextjs #tanstack #webdev',
)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
