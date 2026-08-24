import re, os

FILES = '/Users/mac/Downloads/files'
ASSETS = f'{FILES}/vscode-extensions-assets'

base = open(f'{FILES}/git-commands.html').read()
guide = open(f'{FILES}/correct.html').read()
STYLE = re.search(r'<style>.*?</style>', base, re.S).group(0)
SCRIPT = re.search(r'<script>.*?</script>', base, re.S).group(0)

uris = list(dict.fromkeys(re.findall(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', guide)))
PORTRAIT = min(uris, key=len)
WORDMARK = max(uris, key=len)

def svg(name, size):
    s = open(f'{ASSETS}/{name}.svg').read()
    s = re.sub(r'<\?xml.*?\?>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r'\1', s, count=1)
    s = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r'\1', s, count=1)
    s = re.sub(r'<svg\b', f'<svg style="width:{size}px;height:{size}px;display:block;" ', s, count=1)
    return s.strip()

N = 8  # cover + 6 extensions + cta

# ---- extra CSS for the recommendation layout ----
EXTRA = '''
<style>
  .app-tile{width:54px;height:54px;border-radius:14px;background:#141414;border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 6px 18px rgba(0,0,0,0.28);}
  .cat-badge{display:inline-flex;align-items:center;padding:5px 11px;border-radius:999px;font-family:var(--font);font-size:9.5px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;white-space:nowrap;flex-shrink:0;}
  .cat-badge-light{background:rgba(34,197,94,0.12);color:var(--green-dark);border:1px solid rgba(34,197,94,0.28);}
  .cat-badge-dark{background:rgba(255,255,255,0.08);color:var(--green-light);border:1px solid rgba(255,255,255,0.16);}
  .blurb{font-family:var(--font);font-size:14px;line-height:1.45;font-weight:500;margin-bottom:13px;}
  .blurb-light{color:#3A4A40;}
  .blurb-dark{color:rgba(255,255,255,0.74);}
  .feat-card{border-radius:14px;padding:2px 16px;}
  .feat-card-light{background:#fff;border:1px solid var(--light-border);box-shadow:0 6px 22px rgba(0,0,0,0.05);}
  .feat-card-dark{background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.08);}
  .feat-row{display:flex;gap:12px;padding:11px 0;align-items:baseline;}
  .feat-row-light + .feat-row-light{border-top:1px solid #EEF2EF;}
  .feat-row-dark + .feat-row-dark{border-top:1px solid rgba(255,255,255,0.06);}
  .feat-label{width:78px;flex-shrink:0;font-family:var(--font);font-size:9px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;}
  .feat-label-light{color:#9AA8A0;}
  .feat-label-dark{color:rgba(255,255,255,0.4);}
  .feat-val{flex:1;font-family:var(--font);font-size:12.5px;line-height:1.42;font-weight:500;}
  .feat-val-light{color:#2A352E;}
  .feat-val-dark{color:rgba(255,255,255,0.85);}
  .feat-val strong{font-weight:700;}
  .feat-val-light strong{color:var(--green-dark);}
  .feat-val-dark strong{color:var(--green-light);}
  .fact{border-left:3px solid var(--green);border-radius:0 9px 9px 0;padding:11px 14px;margin-top:13px;font-family:var(--font);font-size:12.5px;line-height:1.5;}
  .fact-light{background:rgba(34,197,94,0.08);color:#3A4A40;}
  .fact-dark{background:rgba(34,197,94,0.07);color:rgba(255,255,255,0.72);}
  .fact-light strong{color:var(--green-dark);}
  .fact-dark strong{color:var(--green-light);}
  .dotgrid{position:absolute;top:34px;right:30px;width:96px;height:70px;z-index:1;
    background-image:radial-gradient(currentColor 1px,transparent 1px);background-size:13px 13px;opacity:0.18;}
</style>'''

ARROW_D = ('<div class="arrow-dark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
           '<path d="M9 6l6 6-6 6" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
ARROW_L = ('<div class="arrow-light"><svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
           '<path d="M9 6l6 6-6 6" stroke="rgba(0,0,0,0.22)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

def pbar(idx, light=False):
    w = idx/N*100
    cls = 'light' if light else 'dark'
    return (f'<div class="progress-bar"><div class="progress-track progress-track-{cls}">'
            f'<div class="progress-fill progress-fill-{cls}" style="width:{w:.2f}%;"></div></div>'
            f'<span class="slide-num-{cls}">{idx}/{N}</span></div>')

# ---------------- EXTENSION DATA ----------------
APPS = [
    dict(name='GitHub Copilot', desc='The AI pair programmer', cat='AI Autocomplete', logo='app_githubcopilot', light=True,
         blurb='Ghost-text suggestions that finish your line, your function, your whole boilerplate file.',
         killer='Inline completions plus a chat that knows your open files.',
         best='Staying in flow instead of stopping to think about syntax.',
         tip='Hit <strong>Tab</strong> to accept, <strong>Esc</strong> to dismiss — and learn to write a clear comment first; it reads it as the prompt.'),
    dict(name='GitLens', desc='Git, supercharged', cat='Git Superpowers', logo='app_gitlens', light=False,
         blurb='Turns the editor into a time machine — every line tells you <strong>who</strong> changed it and <strong>why</strong>.',
         killer='Inline blame on the current line, plus a full file history view.',
         best='Understanding code you did not write.',
         tip='Hover any line to see the commit, author and message — no more <strong>git blame</strong> in a separate terminal.'),
    dict(name='Prettier', desc='Opinionated code formatter', cat='Code Formatter', logo='app_prettier', light=True,
         blurb='Stops every formatting argument your team will ever have — one style, applied on save.',
         killer='Reformats the whole file the instant you hit save.',
         best='Consistent code without thinking about spaces or quotes.',
         tip='Turn on <strong>format on save</strong> in settings and commit a config — the diff noise just disappears.'),
    dict(name='ESLint', desc='Find problems before you run', cat='Linter', logo='app_eslint', light=False,
         blurb='Catches bugs, bad patterns and unused code <strong>as you type</strong> — red squiggles, not runtime crashes.',
         killer='Live linting with one-click auto-fixes in the editor.',
         best='Killing whole classes of bugs before they ship.',
         tip='Pair it with Prettier — let ESLint catch logic, let Prettier handle style. They are a team, not rivals.'),
    dict(name='Tailwind IntelliSense', desc='by Tailwind Labs', cat='CSS Tooling', logo='app_tailwindcss', light=True,
         blurb='Autocomplete, linting and color previews for every Tailwind class you type.',
         killer='Suggests classes and shows the exact color or spacing inline.',
         best='Building UIs fast without memorizing the class names.',
         tip='Hover a class to see the raw CSS it expands to — a painless way to actually learn the framework.'),
    dict(name='Docker', desc='by Microsoft', cat='Containers', logo='app_docker', light=False,
         blurb='Manage images, containers and registries from a panel — never memorize <strong>docker</strong> flags again.',
         killer='Build, run and attach to containers from the sidebar.',
         best='Working with containers without living in the terminal.',
         tip='Right-click a running container to view logs or open a shell inside it — instantly.'),
]

def app_slide(idx, a):
    light = a['light']
    ld = 'light' if light else 'dark'
    slide_cls = 'slide-light' if light else 'slide-dark'
    name_color = '#0A0F0C' if light else '#fff'
    sub_color = '#5C6B62' if light else 'rgba(255,255,255,0.5)'
    arrow = ARROW_L if light else ARROW_D

    deco = ('<div class="noise"></div>' if not light else
            '<div style="position:absolute;top:-50px;left:-50px;width:230px;height:230px;background:radial-gradient(circle,rgba(34,197,94,0.16) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>')
    dotgrid = f'<div class="dotgrid" style="color:{"#9AA8A0" if light else "#22C55E"};"></div>'

    return f'''      <!-- SLIDE {idx} — {a['name']} -->
      <div class="slide {slide_cls}">
        {deco}
        {dotgrid}
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 28px 50px;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:17px;">
            <div class="app-tile">{svg(a['logo'],30)}</div>
            <div style="flex:1;min-width:0;">
              <div style="font-family:var(--font);font-size:23px;font-weight:700;color:{name_color};line-height:1.12;">{a['name']}</div>
              <div style="font-family:var(--font);font-size:12.5px;color:{sub_color};">{a['desc']}</div>
            </div>
            <span class="cat-badge cat-badge-{ld}">{a['cat']}</span>
          </div>
          <p class="blurb blurb-{ld}">{a['blurb']}</p>
          <div class="feat-card feat-card-{ld}">
            <div class="feat-row feat-row-{ld}">
              <span class="feat-label feat-label-{ld}">Killer feature</span>
              <span class="feat-val feat-val-{ld}">{a['killer']}</span>
            </div>
            <div class="feat-row feat-row-{ld}">
              <span class="feat-label feat-label-{ld}">Best for</span>
              <span class="feat-val feat-val-{ld}">{a['best']}</span>
            </div>
          </div>
          <div class="fact fact-{ld}">{a['tip']}</div>
        </div>
        {arrow}
        {pbar(idx, light)}
      </div>
'''

# ---------------- COVER ----------------
def cover_icon(asset, top, right, size=44, rot=0):
    return (f'<div style="position:absolute;top:{top}px;right:{right}px;width:{size}px;height:{size}px;border-radius:12px;'
            f'background:#141414;border:1px solid rgba(255,255,255,0.14);display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 8px 22px rgba(0,0,0,0.4);transform:rotate({rot}deg);z-index:2;">{svg(asset, int(size*0.54))}</div>')

icons = (cover_icon('app_githubcopilot', 40, 150, 46, -8) + cover_icon('app_gitlens', 32, 64, 50, 6) +
         cover_icon('app_prettier', 96, 28, 42, -4) + cover_icon('app_eslint', 120, 132, 44, 7) +
         cover_icon('app_docker', 176, 70, 46, -6) + cover_icon('app_tailwindcss', 92, 214, 40, 5))

cover = f'''      <!-- SLIDE 1 — COVER -->
      <div class="slide slide-dark">
        <div style="position:absolute;inset:0;z-index:0;">
          <img src="{PORTRAIT}" style="position:absolute;right:-10px;bottom:0;height:100%;width:auto;object-fit:cover;object-position:top center;filter:grayscale(20%);" alt="">
          <div style="position:absolute;inset:0;background:linear-gradient(to right,rgba(10,15,12,1) 0%,rgba(10,15,12,0.9) 40%,rgba(10,15,12,0.35) 75%,transparent 100%);"></div>
          <div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(10,15,12,0.97) 0%,rgba(10,15,12,0.5) 40%,transparent 68%);"></div>
          <div style="position:absolute;inset:0;background:linear-gradient(to left,rgba(21,128,61,0.16) 0%,transparent 55%);"></div>
        </div>
        {icons}
        <div style="position:relative;z-index:3;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 50px;">
          <div style="margin-bottom:18px;"><img src="{WORDMARK}" style="height:27px;width:auto;display:block;" alt="Jeffthedev"></div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:11px;">
            <span class="pill pill-green" style="font-weight:700;letter-spacing:0.5px;">2026</span>
            <span class="tag tag-dark">VS Code</span>
          </div>
          <div class="heading" style="color:#fff;font-size:32px;margin-bottom:13px;">VS Code Extensions<br>Every Developer<br><span style="color:var(--green-light);">Should Have</span></div>
          <p class="body-text body-dark" style="max-width:262px;font-size:13px;">6 add-ons that make the editor work harder than you do. Swipe.</p>
        </div>
        {ARROW_D}
        {pbar(1)}
      </div>
'''

# ---------------- CTA ----------------
def stat(big, small):
    return (f'<div style="flex:1;text-align:center;"><div style="font-family:var(--font);font-size:21px;font-weight:700;color:#fff;line-height:1;">{big}</div>'
            f'<div style="font-family:var(--font);font-size:11px;color:rgba(255,255,255,0.5);margin-top:3px;">{small}</div></div>')
vdiv = '<div style="width:1px;background:rgba(255,255,255,0.18);align-self:stretch;margin:2px 0;"></div>'

cta = f'''      <!-- SLIDE {N} — CTA -->
      <div class="slide" style="background:var(--dark-bg);">
        <div style="position:absolute;inset:0;z-index:0;">
          <img src="{PORTRAIT}" style="position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:105%;width:auto;object-fit:cover;object-position:top center;filter:grayscale(60%) brightness(0.5);" alt="">
          <div style="position:absolute;inset:0;background:linear-gradient(165deg,rgba(10,15,12,0.94) 0%,rgba(21,128,61,0.72) 50%,rgba(34,197,94,0.58) 100%);"></div>
          <div style="position:absolute;top:0;left:0;right:0;height:50%;background:linear-gradient(to bottom,rgba(10,15,12,0.65) 0%,transparent 100%);"></div>
          <div style="position:absolute;bottom:0;left:0;right:0;height:42%;background:linear-gradient(to top,rgba(10,15,12,0.88) 0%,transparent 100%);"></div>
        </div>
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:space-between;height:100%;padding:30px 32px 50px;">
          <div><img src="{WORDMARK}" style="height:27px;width:auto;display:block;" alt="Jeffthedev"></div>
          <div>
            <span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Takeaway</span>
            <div class="heading" style="color:#fff;font-size:27px;margin-bottom:13px;line-height:1.15;">A sharper<br><span style="color:var(--green-light);">setup, today.</span></div>
            <p class="body-text" style="font-size:13px;color:rgba(255,255,255,0.72);max-width:290px;margin-bottom:20px;">The right extensions don't just save keystrokes — they catch bugs and teach you as you work. Install two tonight.</p>
            <div style="display:flex;gap:16px;margin-bottom:22px;">{stat('6','extensions')}{vdiv}{stat('Free','all of them')}{vdiv}{stat('Daily','dev content')}</div>
            <div style="display:inline-flex;align-items:center;padding:12px 26px;background:var(--green);color:#0A0F0C;font-family:var(--font);font-weight:700;font-size:14px;border-radius:28px;letter-spacing:0.2px;">Follow @Jeffthedev__</div>
          </div>
        </div>
        {pbar(N)}
      </div>
'''

slides = cover + ''.join(app_slide(i+2, a) for i, a in enumerate(APPS)) + cta
dots = '\n'.join(f'    <div class="dot{" active" if i==0 else ""}" data-idx="{i}"></div>' for i in range(N))
actions = '''  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
    <div class="ig-bookmark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></div>
  </div>'''

doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jeffthedev — VS Code Extensions Every Developer Should Have</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{STYLE}
{EXTRA}
</head>
<body>
<div class="ig-frame">

  <div class="ig-header">
    <div class="ig-avatar"><img src="{PORTRAIT}"></div>
    <div class="ig-info">
      <div class="ig-handle">Jeffthedev__</div>
      <div class="ig-sub">Developer Education</div>
    </div>
    <div class="ig-more">···</div>
  </div>

  <div class="carousel-viewport" id="viewport">
    <div class="carousel-track" id="track">

{slides}
    </div><!-- /carousel-track -->
  </div><!-- /carousel-viewport -->

  <div class="ig-dots" id="dots">
{dots}
  </div>

{actions}

  <div class="ig-caption">
    <strong>Jeffthedev__</strong> 6 VS Code extensions every developer should have in 2026 — GitHub Copilot, GitLens, Prettier, ESLint, Tailwind CSS IntelliSense and Docker. All free. Save it, then install two tonight. Follow for daily developer content. #vscode #webdev #developer #coding #programming #softwaredevelopment #jeffthedev
  </div>

</div><!-- /ig-frame -->

{SCRIPT}
</body>
</html>
'''

open(f'{FILES}/vscode-extensions.html', 'w').write(doc)
emoji = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍✅]')
print("emoji:", len(emoji.findall(doc)),
      "| blue:", len(re.findall(r'#3B82F6|#60A5FA|#1D4ED8|59,130,246', doc)),
      "| orange:", len(re.findall(r'#FB923C|251,146,60', doc)),
      "| lines:", doc.count(chr(10))+1)
