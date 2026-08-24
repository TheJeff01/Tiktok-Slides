#!/usr/bin/env python3
# Build TWO versions of the "Color Palettes for Your Next UI" carousel from the
# git-commands.html shell — same cover/CTA/photo assets (reused verbatim) but
# two different chrome styles for the 7 content slides, for Jeff to compare:
#   color-palettes-a.html — standard slide chrome (tag/badge/callout/progress+arrow)
#   color-palettes-b.html — frameless/minimal (grid bg, card, handle pill, no chrome)

import io

SRC = "git-commands.html"

with io.open(SRC, "r", encoding="utf-8") as f:
    base_html = f.read()

# ---- shared text swaps (title / cover / CTA / caption) ----
def apply_shared_text(html):
    html = html.replace(
        "<title>Jeffthedev — 5 Git Commands That Saved My Ass</title>",
        "<title>Jeffthedev — Color Palettes for Your Next UI</title>",
    )
    html = html.replace(
        '<span class="tag tag-dark" style="margin-bottom:11px;">Git · Survival Kit</span>',
        '<span class="tag tag-dark" style="margin-bottom:11px;">UI · Color Theory</span>',
    )
    html = html.replace(
        '<div class="heading" style="color:#fff;font-size:33px;margin-bottom:14px;">5 git commands<br><span style="color:var(--green-light);">that saved my ass</span></div>',
        '<div class="heading" style="color:#fff;font-size:31px;margin-bottom:14px;">Color palettes for<br><span style="color:var(--green-light);">your next UI</span></div>',
    )
    html = html.replace(
        '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">The exact commands I reach for when a repo goes sideways. Steal them — swipe.</p>',
        '<p class="body-text body-dark" style="max-width:265px;font-size:13px;">Real hex pairs and where each one actually works. No more guessing — swipe.</p>',
    )
    html = html.replace(
        '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">5 commands. Save them<br>before you need them.</div>',
        '<div class="heading" style="color:#fff;font-size:24px;margin-bottom:18px;line-height:1.15;">7 palettes. Steal them<br>for your next build.</div>',
    )
    cta_items = [
        "Slate &amp; Amber — dashboards &amp; admin panels",
        "Midnight &amp; Mint — dark-mode interfaces",
        "Ink &amp; Coral — error &amp; warning states",
        "Deep Violet &amp; Lilac — SaaS branding",
        "Charcoal &amp; Cyan — developer tools",
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
    insertion = anchor + checklist_item("Forest &amp; Cream — eco &amp; wellness apps") + checklist_item("Navy &amp; Gold — fintech &amp; premium products")
    assert anchor in html, "5th CTA checklist item anchor not found"
    html = html.replace(anchor, insertion)

    html = html.replace(
        '<strong>Jeffthedev__</strong> 5 git commands that have saved me more times than I can count. Save this before your next "oh no" moment. #git #webdev #programming',
        '<strong>Jeffthedev__</strong> Color palettes for your next UI — real hex pairs and where each one actually works. Save this for your next project. #webdev #uidesign #colorpalette',
    )
    return html

# ---- palette content (shared copy across both versions) ----
PALETTES = [
    dict(tag="#1 · Dashboards", badge="Neutral + Accent", head1="Slate &amp; Amber", head2="for clean dashboards",
         body="A calm neutral paired with one warm accent — reserve amber for actions only.",
         name1="Slate", hex1="#2B3038", bg1="#2B3038", fg1="#FFFFFF",
         name2="Amber", hex2="#FFB020", bg2="#FFB020", fg2="#231A00",
         callout_label="Use for:", callout_text="dashboards, admin panels, data-heavy UIs.", dark=True),
    dict(tag="#2 · Dark Mode UI", badge="Deep + Fresh", head1="Midnight &amp; Mint", head2="for dark-mode screens",
         body="A near-black base keeps dark mode easy on the eyes; mint signals success without shouting.",
         name1="Midnight", hex1="#0B1220", bg1="#0B1220", fg1="#FFFFFF",
         name2="Mint", hex2="#34D399", bg2="#34D399", fg2="#062B1D",
         callout_label="Use for:", callout_text="dark-mode dashboards, code editors, night-shift apps.", dark=False),
    dict(tag="#3 · Error &amp; Warning", badge="High Contrast", head1="Ink &amp; Coral", head2="for states that matter",
         body="Reserve coral for errors and warnings only — it loses power if it's everywhere.",
         name1="Ink", hex1="#14141A", bg1="#14141A", fg1="#FFFFFF",
         name2="Coral", hex2="#FF6B6B", bg2="#FF6B6B", fg2="#3A0A0A",
         callout_label="Rule:", callout_text="if more than 10% of the screen is coral, check your hierarchy.", dark=True),
    dict(tag="#4 · SaaS Branding", badge="Premium Feel", head1="Deep Violet &amp; Lilac", head2="for SaaS branding",
         body="Violet reads premium and confident; lilac softens it just enough for everyday UI.",
         name1="Deep Violet", hex1="#4C1D95", bg1="#4C1D95", fg1="#FFFFFF",
         name2="Lilac", hex2="#C4B5FD", bg2="#C4B5FD", fg2="#2E1065",
         callout_label="Use for:", callout_text="pricing pages, onboarding flows, marketing sites.", dark=False),
    dict(tag="#5 · Dev Tools", badge="Terminal Vibes", head1="Charcoal &amp; Cyan", head2="for developer tools",
         body="The classic terminal pairing — charcoal disappears, cyan highlights exactly what matters.",
         name1="Charcoal", hex1="#1E1E1E", bg1="#1E1E1E", fg1="#FFFFFF",
         name2="Cyan", hex2="#22D3EE", bg2="#22D3EE", fg2="#003544",
         callout_label="Tip:", callout_text="pair with a monospace font and the terminal feel writes itself.", dark=True),
    dict(tag="#6 · Eco / Wellness", badge="Calm + Organic", head1="Forest &amp; Cream", head2="for wellness apps",
         body="Deep green feels grounded and natural; cream keeps the layout light and breathable.",
         name1="Forest", hex1="#1B4332", bg1="#1B4332", fg1="#FFFFFF",
         name2="Cream", hex2="#FDF6EC", bg2="#FDF6EC", fg2="#3A2E1F",
         callout_label="Use for:", callout_text="health apps, sustainability brands, journaling tools.", dark=False),
    dict(tag="#7 · Fintech", badge="Trust + Value", head1="Navy &amp; Gold", head2="for premium products",
         body="Navy signals trust and stability; gold is the accent that says this app handles money well.",
         name1="Navy", hex1="#0A2540", bg1="#0A2540", fg1="#FFFFFF",
         name2="Gold", hex2="#D4AF37", bg2="#D4AF37", fg2="#3B2E05",
         callout_label="Rule:", callout_text="gold works as an accent, not a background — under 15% of the UI.", dark=True),
]

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

PCTS = ["22.22", "33.33", "44.44", "55.56", "66.67", "77.78", "88.89"]
NUMS = ["2/9", "3/9", "4/9", "5/9", "6/9", "7/9", "8/9"]

# ================= VERSION A — standard slide chrome =================
def swatch_pair(p):
    return (
        '          <div style="display:flex;flex-direction:column;gap:8px;margin:14px 0 4px;">\n'
        '            <div style="border-radius:12px;height:78px;display:flex;flex-direction:column;justify-content:center;padding:0 16px;background:%s;">\n'
        '              <div style="font-family:var(--font);font-weight:700;font-size:16px;color:%s;">%s</div>\n'
        '              <div style="font-family:\'Courier New\',monospace;font-size:11px;margin-top:3px;color:%s;opacity:0.75;">HEX %s</div>\n'
        '            </div>\n'
        '            <div style="border-radius:12px;height:78px;display:flex;flex-direction:column;justify-content:center;padding:0 16px;background:%s;">\n'
        '              <div style="font-family:var(--font);font-weight:700;font-size:16px;color:%s;">%s</div>\n'
        '              <div style="font-family:\'Courier New\',monospace;font-size:11px;margin-top:3px;color:%s;opacity:0.75;">HEX %s</div>\n'
        '            </div>\n'
        '          </div>\n'
    ) % (p["bg1"], p["fg1"], p["name1"], p["fg1"], p["hex1"], p["bg2"], p["fg2"], p["name2"], p["fg2"], p["hex2"])

def callout_dark(p):
    return ('          <div style="margin-top:4px;padding:10px 13px;background:rgba(34,197,94,0.06);'
            'border:1px solid rgba(34,197,94,0.18);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;">'
            '<strong style="color:var(--green-light);">%s</strong> %s</span></div>\n' % (p["callout_label"], p["callout_text"]))

def callout_light(p):
    return ('          <div style="margin-top:4px;padding:10px 13px;background:rgba(34,197,94,0.07);'
            'border:1px solid rgba(34,197,94,0.18);border-radius:9px;">'
            '<span style="font-family:var(--font);font-size:12px;color:#3A4A40;line-height:1.5;">'
            '<strong style="color:var(--green-dark);">%s</strong> %s</span></div>\n' % (p["callout_label"], p["callout_text"]))

def slide_a_dark(p):
    s = '      <div class="slide slide-dark">\n'
    s += '        <div class="noise"></div>\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:11px;">\n'
    s += '            <span class="tag tag-dark">%s</span>\n' % p["tag"]
    s += '            <span class="badge badge-green">%s</span>\n' % p["badge"]
    s += '          </div>\n'
    s += '          <div class="heading" style="color:#fff;margin-bottom:13px;font-size:26px;">%s<br><span style="color:var(--green-light);">%s</span></div>\n' % (p["head1"], p["head2"])
    s += '          <p class="body-text body-dark" style="margin-bottom:6px;font-size:13px;">%s</p>\n' % p["body"]
    s += swatch_pair(p)
    s += callout_dark(p)
    s += '        </div>\n'
    return s

def slide_a_light(p):
    s = '      <div class="slide slide-light">\n'
    s += '        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">\n'
    s += '          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:11px;">\n'
    s += '            <span class="tag tag-light">%s</span>\n' % p["tag"]
    s += '            <span class="badge badge-green">%s</span>\n' % p["badge"]
    s += '          </div>\n'
    s += '          <div class="heading" style="color:#0A0F0C;font-size:26px;margin-bottom:12px;">%s<br><span style="color:var(--green-dark);">%s</span></div>\n' % (p["head1"], p["head2"])
    s += '          <p class="body-text body-light" style="margin-bottom:6px;font-size:13px;">%s</p>\n' % p["body"]
    s += swatch_pair(p)
    s += callout_light(p)
    s += '        </div>\n'
    return s

# ================= VERSION B — frameless / minimal =================
def slide_b(p):
    s = '      <div class="slide" style="background:#fff;background-image:linear-gradient(rgba(0,0,0,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,0.04) 1px,transparent 1px);background-size:20px 20px;display:flex;flex-direction:column;align-items:center;padding:24px 20px;">\n'
    s += '        <div style="display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid rgba(0,0,0,0.1);border-radius:20px;padding:6px 14px 6px 6px;box-shadow:0 2px 6px rgba(0,0,0,0.06);margin-bottom:22px;">\n'
    s += '          <div style="width:20px;height:20px;border-radius:50%;background:var(--green);display:flex;align-items:center;justify-content:center;font-size:10px;color:#0A0F0C;font-weight:700;font-family:var(--font);">J</div>\n'
    s += '          <span style="font-family:var(--font);font-weight:700;font-size:13px;color:#0A0F0C;">@Jeffthedev__</span>\n'
    s += '        </div>\n'
    s += '        <div style="width:100%;border-radius:22px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.12);">\n'
    s += '          <div style="height:170px;display:flex;flex-direction:column;justify-content:center;padding:0 26px;background:%s;">\n' % p["bg1"]
    s += '            <div style="font-family:var(--font);font-weight:800;font-size:24px;color:%s;">%s</div>\n' % (p["fg1"], p["name1"])
    s += '            <div style="display:inline-block;margin-top:10px;border:1px solid %s;border-radius:20px;padding:6px 14px;font-family:var(--font);font-weight:600;font-size:13px;letter-spacing:0.5px;color:%s;width:fit-content;">HEX CODE: %s</div>\n' % (
        ("rgba(255,255,255,0.4)" if p["dark"] else "rgba(0,0,0,0.4)"), p["fg1"], p["hex1"])
    s += '          </div>\n'
    s += '          <div style="height:170px;display:flex;flex-direction:column;justify-content:center;padding:0 26px;background:%s;">\n' % p["bg2"]
    s += '            <div style="font-family:var(--font);font-weight:800;font-size:24px;color:%s;">%s</div>\n' % (p["fg2"], p["name2"])
    s += '            <div style="display:inline-block;margin-top:10px;border:1px solid rgba(0,0,0,0.35);border-radius:20px;padding:6px 14px;font-family:var(--font);font-weight:600;font-size:13px;letter-spacing:0.5px;color:%s;width:fit-content;">HEX CODE: %s</div>\n' % (p["fg2"], p["hex2"])
    s += '          </div>\n'
    s += '        </div>\n'
    s += '        <div style="margin-top:16px;font-family:var(--font);font-size:11px;color:rgba(0,0,0,0.35);">%s — %s</div>\n' % (p["tag"], p["callout_text"])
    s += '      </div>\n'
    return s

markerA = '<span class="slide-num-dark">1/9</span></div>\n      </div>\n'
markerB = '      <!-- SLIDE 9 — CTA -->'

def build(version):
    html = apply_shared_text(base_html)
    a = html.index(markerA) + len(markerA)
    b = html.index(markerB)
    mid = ""
    for i, p in enumerate(PALETTES):
        if version == "a":
            slide = slide_a_dark(p) if p["dark"] else slide_a_light(p)
            arrow = arrow_dark() if p["dark"] else arrow_light()
            prog = prog_dark(PCTS[i], NUMS[i]) if p["dark"] else prog_light(PCTS[i], NUMS[i])
            mid += slide + arrow + prog + "      </div>\n"
        else:
            mid += slide_b(p)
    html = html[:a] + mid + html[b:]
    return html

for version, out in [("a", "color-palettes-a.html"), ("b", "color-palettes-b.html")]:
    html = build(version)
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out, "len", len(html))
