import re, os

FILES = '/Users/mac/Downloads/files'
ASSETS = f'{FILES}/everyday-apps-2-assets'

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

# ---- extra CSS for the app-stack layout ----
EXTRA = '''
<style>
  .app-tile{width:54px;height:54px;border-radius:14px;background:#141414;border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 6px 18px rgba(0,0,0,0.28);}
  .stack-card{border-radius:14px;padding:4px 16px;}
  .stack-card-light{background:#fff;border:1px solid var(--light-border);box-shadow:0 6px 22px rgba(0,0,0,0.05);}
  .stack-card-dark{background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.08);}
  .stack-row{display:flex;align-items:center;gap:12px;padding:8px 0;}
  .stack-row-light + .stack-row-light{border-top:1px solid #EEF2EF;}
  .stack-row-dark + .stack-row-dark{border-top:1px solid rgba(255,255,255,0.06);}
  .stack-label{width:74px;flex-shrink:0;font-family:var(--font);font-size:9.5px;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
  .stack-label-light{color:#9AA8A0;}
  .stack-label-dark{color:rgba(255,255,255,0.38);}
  .chips{display:flex;flex-wrap:wrap;gap:6px;flex:1;}
  .chip{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border-radius:8px;font-family:var(--font);font-size:11.5px;font-weight:600;}
  .chip-light{background:#F3F6F4;border:1px solid #E6ECE8;color:#1F2A24;}
  .chip-dark{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.88);}
  .chip-ico{width:16px;height:16px;display:inline-flex;align-items:center;justify-content:center;}
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
    w = idx/8*100
    cls = 'light' if light else 'dark'
    return (f'<div class="progress-bar"><div class="progress-track progress-track-{cls}">'
            f'<div class="progress-fill progress-fill-{cls}" style="width:{w:.2f}%;"></div></div>'
            f'<span class="slide-num-{cls}">{idx}/8</span></div>')

# ---------------- APP DATA ----------------
APPS = [
    dict(name='TikTok', desc='Short-form video at scale', users='~1.5B', logo='app_tiktok', light=True,
         fact='Its recommendation engine serves <strong>1B+ users</strong> on a Go and Python core.',
         rows=[('Backend',[('Go','tech_go'),('Python','tech_python'),('C++','tech_cplusplus')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('MySQL','tech_mysql'),('TiDB','tech_tidb')]),
               ('Cache',[('Redis','tech_redis')]),
               ('Infra',[('Kubernetes','tech_kubernetes')])]),
    dict(name='X', desc='Real-time global conversation', users='~600M', logo='app_x', light=False,
         fact='X rebuilt its timeline in <strong>Scala</strong> and processes ~500M posts a day.',
         rows=[('Backend',[('Scala','tech_scala'),('Java','tech_java')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('MySQL','tech_mysql'),('Manhattan','tech_genericdb')]),
               ('Cache',[('Redis','tech_redis')]),
               ('Streaming',[('Kafka','tech_apachekafka')])]),
    dict(name='Pinterest', desc='Visual discovery engine', users='~550M', logo='app_pinterest', light=True,
         fact='Pinterest runs a heavily-sharded <strong>Python + MySQL</strong> core for 550M+ users.',
         rows=[('Backend',[('Python','tech_python'),('Java','tech_java')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('MySQL','tech_mysql'),('HBase','tech_genericdb')]),
               ('Cache',[('Memcached','tech_memcached')]),
               ('Infra',[('AWS','tech_aws')])]),
    dict(name='LinkedIn', desc='The professional network', users='~1B', logo='app_linkedin', light=False,
         fact='<strong>Kafka was born at LinkedIn</strong> — it now moves 7T+ messages a day.',
         rows=[('Backend',[('Java','tech_java'),('Scala','tech_scala')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('MySQL','tech_mysql'),('Espresso','tech_genericdb')]),
               ('Streaming',[('Kafka','tech_apachekafka')]),
               ('Infra',[('Azure','tech_azure')])]),
    dict(name='Snapchat', desc='Ephemeral messaging', users='~800M', logo='app_snapchat', light=True,
         fact="Snap runs almost entirely on <strong>Google Cloud + AWS</strong> — one of GCP's largest customers.",
         rows=[('Backend',[('Java','tech_java'),('Python','tech_python')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('MySQL','tech_mysql'),('Bigtable','tech_genericdb')]),
               ('Infra',[('Google Cloud','tech_googlecloud'),('AWS','tech_aws')])]),
    dict(name='Discord', desc='Chat for communities', users='~200M', logo='app_discord', light=False,
         fact='Discord moved <strong>trillions of messages</strong> from Cassandra to ScyllaDB for speed.',
         rows=[('Backend',[('Elixir','tech_elixir'),('Rust','tech_rust'),('Python','tech_python')]),
               ('Frontend',[('React','tech_react')]),
               ('Database',[('ScyllaDB','tech_scylladb'),('Cassandra','tech_cassandra')]),
               ('Cache',[('Redis','tech_redis')]),
               ('Infra',[('Google Cloud','tech_googlecloud')])]),
]

def app_slide(idx, a):
    light = a['light']
    ld = 'light' if light else 'dark'
    slide_cls = 'slide-light' if light else 'slide-dark'
    name_color = '#0A0F0C' if light else '#fff'
    sub_color = '#5C6B62' if light else 'rgba(255,255,255,0.5)'
    badge = 'badge-green' if light else 'badge-red'
    arrow = ARROW_L if light else ARROW_D

    rows_html = ''
    for label, techs in a['rows']:
        chips = ''.join(
            f'<span class="chip chip-{ld}"><span class="chip-ico">{svg(asset,16)}</span>{tech}</span>'
            for tech, asset in techs)
        rows_html += (f'<div class="stack-row stack-row-{ld}">'
                      f'<span class="stack-label stack-label-{ld}">{label}</span>'
                      f'<div class="chips">{chips}</div></div>\n            ')

    deco = ('<div class="noise"></div>' if not light else
            '<div style="position:absolute;top:-50px;left:-50px;width:230px;height:230px;background:radial-gradient(circle,rgba(34,197,94,0.16) 0%,transparent 70%);pointer-events:none;z-index:1;"></div>')
    dotgrid = f'<div class="dotgrid" style="color:{"#9AA8A0" if light else "#22C55E"};"></div>'

    return f'''      <!-- SLIDE {idx} — {a['name']} -->
      <div class="slide {slide_cls}">
        {deco}
        {dotgrid}
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 28px 50px;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
            <div class="app-tile">{svg(a['logo'],32)}</div>
            <div style="flex:1;min-width:0;">
              <div style="font-family:var(--font);font-size:23px;font-weight:700;color:{name_color};line-height:1.12;">{a['name']}</div>
              <div style="font-family:var(--font);font-size:12.5px;color:{sub_color};">{a['desc']}</div>
            </div>
            <span class="badge {badge}">{a['users']} users</span>
          </div>
          <div class="stack-card stack-card-{ld}">
            {rows_html.rstrip()}
          </div>
          <div class="fact fact-{ld}">{a['fact']}</div>
        </div>
        {arrow}
        {pbar(idx, light)}
      </div>
'''

# ---------------- COVER ----------------
def cover_icon(asset, top, right, size=44, rot=0):
    return (f'<div style="position:absolute;top:{top}px;right:{right}px;width:{size}px;height:{size}px;border-radius:12px;'
            f'background:#141414;border:1px solid rgba(255,255,255,0.14);display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 8px 22px rgba(0,0,0,0.4);transform:rotate({rot}deg);z-index:2;">{svg(asset, int(size*0.58))}</div>')

icons = (cover_icon('app_discord', 40, 150, 46, -8) + cover_icon('app_tiktok', 32, 64, 50, 6) +
         cover_icon('app_x', 96, 28, 42, -4) + cover_icon('app_pinterest', 120, 132, 44, 7) +
         cover_icon('app_snapchat', 176, 70, 46, -6) + cover_icon('app_linkedin', 92, 214, 40, 5))

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
            <span class="pill pill-green" style="font-weight:700;letter-spacing:0.5px;">PART 2</span>
            <span class="tag tag-dark">Developer Knowledge</span>
          </div>
          <div class="heading" style="color:#fff;font-size:33px;margin-bottom:13px;">Tech Stacks<br>Behind Apps<br><span style="color:var(--green-light);">You Use Daily</span></div>
          <p class="body-text body-dark" style="max-width:255px;font-size:13px;">6 more giant apps — and what really runs them under the hood. Swipe.</p>
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

cta = f'''      <!-- SLIDE 8 — CTA -->
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
            <div class="heading" style="color:#fff;font-size:27px;margin-bottom:13px;line-height:1.15;">Same tools you're<br><span style="color:var(--green-light);">learning right now.</span></div>
            <p class="body-text" style="font-size:13px;color:rgba(255,255,255,0.72);max-width:290px;margin-bottom:20px;">React, Python, Redis, Kafka — the giants run on the exact stack you can pick up today. Keep building.</p>
            <div style="display:flex;gap:16px;margin-bottom:22px;">{stat('6 apps','this post')}{vdiv}{stat('100%','public info')}{vdiv}{stat('Daily','dev content')}</div>
            <div style="display:inline-flex;align-items:center;padding:12px 26px;background:var(--green);color:#0A0F0C;font-family:var(--font);font-weight:700;font-size:14px;border-radius:28px;letter-spacing:0.2px;">Follow @Jeffthedev__</div>
          </div>
        </div>
        {pbar(8)}
      </div>
'''

slides = cover + ''.join(app_slide(i+2, a) for i, a in enumerate(APPS)) + cta
dots = '\n'.join(f'    <div class="dot{" active" if i==0 else ""}" data-idx="{i}"></div>' for i in range(8))
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
<title>Jeffthedev — Tech Stacks Behind Apps You Use Daily (Part 2)</title>
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
    <strong>Jeffthedev__</strong> Part 2 — the tech stacks behind 6 more apps you use every day. Save it and follow for daily developer content. #techstack #webdev #javascript #react #coding #developer #softwaredevelopment #jeffthedev
  </div>

</div><!-- /ig-frame -->

{SCRIPT}
</body>
</html>
'''

open(f'{FILES}/everyday-apps-2.html', 'w').write(doc)
emoji = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍✅]')
print("emoji:", len(emoji.findall(doc)),
      "| blue:", len(re.findall(r'#3B82F6|#60A5FA|#1D4ED8|59,130,246', doc)),
      "| orange:", len(re.findall(r'#FB923C|251,146,60', doc)),
      "| lines:", doc.count(chr(10))+1)
