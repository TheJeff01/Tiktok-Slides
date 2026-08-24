import re, os

FILES = '/Users/mac/Downloads/files'
ASSETS = f'{FILES}/free-apis-assets'

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

N = 8  # cover + 6 APIs + cta

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

# ---------------- API DATA ----------------
APPS = [
    dict(name='GitHub API', desc='REST + GraphQL', cat='Developer Data', logo='app_github', light=True,
         blurb='Every public repo, user and commit on GitHub — <strong>queryable with a single GET request</strong>.',
         killer='Pull your own repos, languages and commit activity.',
         best='A live portfolio page that updates itself when you ship.',
         tip='No key needed for 60 requests/hour. A free personal token bumps that to <strong>5,000</strong> — enough for anything you will build.'),
    dict(name='Unsplash API', desc='Photos in production quality', cat='Images', logo='app_unsplash', light=False,
         blurb='Search <strong>millions of high-res photos</strong> and drop them straight into your app — legally.',
         killer='A search endpoint that returns magazine-grade imagery.',
         best='Making any project instantly look designed, not default.',
         tip='The free demo tier gives you 50 requests/hour — plenty for a portfolio project. Just keep the photographer credit; it is required.'),
    dict(name='TMDB API', desc='The Movie Database', cat='Movies & TV', logo='app_themoviedatabase', light=True,
         blurb='Posters, ratings, cast and trailers for <strong>nearly every movie and show ever made</strong>.',
         killer='Full metadata plus poster art from one search call.',
         best='Netflix-style browsers, watchlists and rating apps.',
         tip='Free for non-commercial use with an API key. The poster images alone make this the <strong>best-looking demo data</strong> you can get.'),
    dict(name='Spotify Web API', desc='by Spotify', cat='Music Data', logo='app_spotify', light=False,
         blurb='Tracks, artists, albums and playlists — plus <strong>each user’s own listening data</strong> via OAuth.',
         killer='Build a personal “your top artists this month” dashboard.',
         best='Music apps people actually want to share.',
         tip='The OAuth flow is the real prize: implementing it properly is <strong>exactly what interviewers ask about</strong>.'),
    dict(name='NASA APIs', desc='api.nasa.gov', cat='Space Data', logo='app_nasa', light=True,
         blurb='Astronomy Picture of the Day, <strong>real Mars rover photos</strong> and near-Earth asteroid data.',
         killer='APOD: one GET returns a stunning image plus its story.',
         best='An eye-catching project that stands out in a feed of to-do apps.',
         tip='Works instantly with the shared <strong>DEMO_KEY</strong>. A free personal key takes 30 seconds and gives you 1,000 requests/hour.'),
    dict(name='Stripe', desc='Test mode', cat='Payments', logo='app_stripe', light=False,
         blurb='The full payment platform, free in test mode — <strong>real checkout flows, fake money</strong>.',
         killer='A working checkout using test card 4242 4242 4242 4242.',
         best='E-commerce projects that prove you can handle money.',
         tip='A portfolio store with a <strong>real Stripe checkout</strong> says more to employers than five CRUD apps. Test mode is free forever.'),
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

icons = (cover_icon('app_github', 40, 150, 46, -8) + cover_icon('app_spotify', 32, 64, 50, 6) +
         cover_icon('app_stripe', 96, 28, 42, -4) + cover_icon('app_unsplash', 120, 132, 44, 7) +
         cover_icon('app_nasa', 176, 70, 46, -6) + cover_icon('app_themoviedatabase', 92, 214, 40, 5))

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
            <span class="pill pill-green" style="font-weight:700;letter-spacing:0.5px;">$0</span>
            <span class="tag tag-dark">APIs</span>
          </div>
          <div class="heading" style="color:#fff;font-size:32px;margin-bottom:13px;">Free APIs to Build<br>Your Next<br><span style="color:var(--green-light);">Portfolio Project</span></div>
          <p class="body-text body-dark" style="max-width:262px;font-size:13px;">6 APIs with free tiers generous enough to ship something real. Swipe.</p>
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
            <div class="heading" style="color:#fff;font-size:27px;margin-bottom:13px;line-height:1.15;">Stop building<br><span style="color:var(--green-light);">another to-do app.</span></div>
            <p class="body-text" style="font-size:13px;color:rgba(255,255,255,0.72);max-width:290px;margin-bottom:20px;">Pick one API, ship one project, put the live link in your portfolio. Real data beats fake data every time.</p>
            <div style="display:flex;gap:16px;margin-bottom:22px;">{stat('6','APIs')}{vdiv}{stat('$0','to start')}{vdiv}{stat('Daily','dev content')}</div>
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
<title>Jeffthedev — Free APIs to Build Your Next Portfolio Project</title>
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
    <strong>Jeffthedev__</strong> 6 free APIs to build your next portfolio project — GitHub, Unsplash, TMDB, Spotify, NASA and Stripe test mode. All free to start, all impressive in a demo. Save this, pick one API and ship one project this month. Follow for daily developer content. #webdev #api #developer #coding #portfolio #javascript #softwaredevelopment #jeffthedev
  </div>

</div><!-- /ig-frame -->

{SCRIPT}
</body>
</html>
'''

open(f'{FILES}/free-apis.html', 'w').write(doc)
emoji = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍✅]')
print("emoji:", len(emoji.findall(doc)),
      "| blue:", len(re.findall(r'#3B82F6|#60A5FA|#1D4ED8|59,130,246', doc)),
      "| orange:", len(re.findall(r'#FB923C|251,146,60', doc)),
      "| lines:", doc.count(chr(10))+1)
