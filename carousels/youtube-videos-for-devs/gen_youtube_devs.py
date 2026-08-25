#!/usr/bin/env python3
# Build youtube-videos-for-devs.html — a NEW layout variant (not the code-block
# shell): numbered "01. Master X" category slides, each showing a realistic
# YouTube video card (real thumbnail / title / channel / views / upload age,
# pulled from live YouTube search results). Cover + CTA reuse Jeff's standard
# portrait + wordmark photo slides (shared assets in reference/assets/).

import base64
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(BASE, "..", "..")
ASSETS = os.path.join(BASE, "assets")
SHARED = os.path.join(REPO, "reference", "assets")
OUT = os.path.join(BASE, "youtube-videos-for-devs.html")


def b64(path):
    with io.open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


portrait_b64 = b64(os.path.join(SHARED, "portrait.jpg"))
wordmark_b64 = b64(os.path.join(SHARED, "wordmark.png"))

VIDEOS = [
    dict(
        num="01", dark=True,
        cat1="Master", cat2="CSS Grid",
        channel="Kevin Powell",
        title="The EASIEST way to get started with CSS GRID",
        views="220K views", age="5 years ago", dur="6:51",
        thumb="css-grid.jpg",
    ),
    dict(
        num="02", dark=False,
        cat1="Master", cat2="JavaScript",
        channel="Programming with Mosh",
        title="JavaScript Course for Beginners – Your First Step to Web Development",
        views="15M views", age="8 years ago", dur="48:17",
        thumb="javascript.jpg",
    ),
    dict(
        num="03", dark=True,
        cat1="Master", cat2="Flexbox",
        channel="Bro Code",
        title="Learn CSS flexbox in 10 minutes!",
        views="331K views", age="2 years ago", dur="10:01",
        thumb="flexbox.jpg",
    ),
    dict(
        num="04", dark=False,
        cat1="Master", cat2="Git & GitHub",
        channel="freeCodeCamp.org",
        title="Git and GitHub for Beginners - Crash Course",
        views="5.1M views", age="6 years ago", dur="1:08:30",
        thumb="git-github.jpg",
    ),
    dict(
        num="05", dark=True,
        cat1="Master", cat2="VS Code",
        channel="Fireship",
        title="VS Code in 100 Seconds",
        views="1.3M views", age="4 years ago", dur="2:34",
        thumb="vscode.jpg",
    ),
    dict(
        num="06", dark=False,
        cat1="Master", cat2="DevTools",
        channel="Fireship",
        title="21+ Browser Dev Tools & Tips You Need To Know",
        views="375K views", age="5 years ago", dur="9:26",
        thumb="devtools.jpg",
    ),
    dict(
        num="07", dark=True,
        cat1="Master", cat2="AI Coding Tools",
        channel="Fireship",
        title="The Truth about GitHub Copilot // AI Programming First Look",
        views="903K views", age="5 years ago", dur="8:30",
        thumb="ai-copilot.jpg",
    ),
]

TOTAL = 9


def pct(n):
    return f"{n / TOTAL * 100:.2f}"


STYLE = """
  *{margin:0;padding:0;box-sizing:border-box;}
  :root{
    --green:#22C55E;--green-light:#4ADE80;--green-dark:#15803D;
    --light-bg:#F0FAF4;--light-border:#D1EAD8;--dark-bg:#0A0F0C;
    --font:'Space Grotesk',sans-serif;
  }
  body{background:#111;display:flex;justify-content:center;align-items:flex-start;min-height:100vh;padding:40px 20px;font-family:var(--font);}
  .ig-frame{width:420px;max-width:100%;background:#1a1a1a;border-radius:16px;box-shadow:0 32px 80px rgba(0,0,0,0.8);overflow:hidden;}
  .ig-header{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid #222;}
  .ig-avatar{width:36px;height:36px;border-radius:50%;border:2px solid var(--green);overflow:hidden;flex-shrink:0;}
  .ig-avatar img{width:100%;height:100%;object-fit:cover;}
  .ig-info{flex:1;}
  .ig-handle{font-size:13px;font-weight:600;color:#fff;}
  .ig-sub{font-size:11px;color:#666;}
  .ig-more{color:#555;font-size:20px;cursor:pointer;}
  .carousel-viewport{width:420px;aspect-ratio:4/5;overflow:hidden;position:relative;cursor:grab;user-select:none;}
  .carousel-viewport:active{cursor:grabbing;}
  .carousel-track{display:flex;height:100%;transition:transform 0.35s cubic-bezier(0.25,0.46,0.45,0.94);will-change:transform;}
  .slide{width:420px;height:525px;flex-shrink:0;position:relative;display:flex;flex-direction:column;overflow:hidden;}
  .slide-light{background:var(--light-bg);}
  .slide-dark{background:var(--dark-bg);}
  .tag{font-family:var(--font);font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;}
  .tag-light{color:var(--green);}
  .tag-dark{color:var(--green-light);}
  .heading{font-family:var(--font);font-size:30px;font-weight:700;letter-spacing:-0.4px;line-height:1.1;}
  .body-text{font-family:var(--font);font-size:14px;font-weight:400;line-height:1.55;}
  .body-light{color:#3A4A40;}
  .body-dark{color:rgba(255,255,255,0.65);}
  .noise{position:absolute;inset:0;opacity:0.025;pointer-events:none;z-index:1;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:150px 150px;}
  .ig-dots{display:flex;justify-content:center;gap:5px;padding:10px;}
  .dot{width:6px;height:6px;border-radius:50%;background:#444;transition:background 0.3s,transform 0.3s;}
  .dot.active{background:var(--green);transform:scale(1.2);}
  .ig-actions{display:flex;align-items:center;padding:8px 16px;gap:14px;}
  .ig-actions svg{color:#aaa;cursor:pointer;}
  .ig-actions svg:hover{color:#fff;}
  .ig-bookmark{margin-left:auto;}
  .ig-caption{padding:0 16px 16px;font-size:13px;color:#aaa;line-height:1.5;}
  .ig-caption strong{color:#fff;}
  .progress-bar{position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;}
  .progress-track{flex:1;height:3px;border-radius:2px;overflow:hidden;}
  .progress-track-dark{background:rgba(255,255,255,0.12);}
  .progress-track-light{background:rgba(0,0,0,0.08);}
  .progress-fill{height:100%;border-radius:2px;}
  .progress-fill-dark{background:#fff;}
  .progress-fill-light{background:var(--green);}
  .slide-num-dark{font-size:11px;color:rgba(255,255,255,0.4);font-weight:500;}
  .slide-num-light{font-size:11px;color:rgba(0,0,0,0.3);font-weight:500;}
  .arrow-dark{position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,rgba(255,255,255,0.07));}
  .arrow-light{position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,rgba(0,0,0,0.05));}
  .num-big-dark{font-family:var(--font);font-size:50px;font-weight:700;color:rgba(255,255,255,0.9);line-height:1;}
  .num-big-light{font-family:var(--font);font-size:50px;font-weight:700;color:#0A0F0C;line-height:1;}
  .cat-heading{font-family:var(--font);font-weight:700;font-size:29px;line-height:1.15;position:relative;display:inline-block;padding-bottom:12px;}
  .cat-heading::after{content:'';position:absolute;left:0;bottom:0;width:56px;height:2px;background:var(--green);}
  .video-card{background:#fff;border:2px solid var(--green);border-radius:14px;overflow:hidden;box-shadow:0 10px 28px rgba(0,0,0,0.3);flex-shrink:0;}
  .video-thumb{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;background:#000;}
  .video-thumb img{width:100%;height:100%;object-fit:cover;display:block;}
  .video-duration{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,0.82);color:#fff;font-size:11px;font-weight:600;padding:2px 6px;border-radius:4px;font-family:var(--font);}
  .video-info{display:flex;align-items:flex-start;justify-content:space-between;padding:12px 14px 14px;gap:10px;}
  .video-title{font-family:var(--font);font-size:14px;font-weight:600;color:#0A0F0C;line-height:1.35;}
  .video-meta{font-family:var(--font);font-size:11.5px;color:#767676;margin-top:5px;}
"""


def head():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jeffthedev — Must-Watch YouTube Videos For Web Developers</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
<div class="ig-frame">

  <div class="ig-header">
    <div class="ig-avatar"><img src="data:image/jpeg;base64,{portrait_b64}" alt=""></div>
    <div class="ig-info">
      <div class="ig-handle">Jeffthedev__</div>
      <div class="ig-sub">Developer Education</div>
    </div>
    <div class="ig-more">···</div>
  </div>

  <div class="carousel-viewport" id="viewport">
    <div class="carousel-track" id="track">
"""


def cover_slide():
    return f"""
      <!-- SLIDE 1 — COVER -->
      <div class="slide slide-dark">
        <div style="position:absolute;inset:0;z-index:0;">
          <img src="data:image/jpeg;base64,{portrait_b64}" style="position:absolute;right:-10px;bottom:0;height:100%;width:auto;object-fit:cover;object-position:top center;filter:grayscale(15%);" alt="">
          <div style="position:absolute;inset:0;background:linear-gradient(to right,rgba(10,15,12,1) 0%,rgba(10,15,12,0.88) 38%,rgba(10,15,12,0.25) 75%,transparent 100%);"></div>
          <div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(10,15,12,0.97) 0%,rgba(10,15,12,0.45) 38%,transparent 65%);"></div>
          <div style="position:absolute;inset:0;background:linear-gradient(to left,rgba(21,128,61,0.15) 0%,transparent 55%);"></div>
        </div>
        <svg style="position:absolute;inset:0;opacity:0.05;pointer-events:none;z-index:1;" width="420" height="525" viewBox="0 0 420 525">
          <line x1="0" y1="175" x2="420" y2="175" stroke="#22C55E" stroke-width="1"/>
          <line x1="0" y1="350" x2="420" y2="350" stroke="#22C55E" stroke-width="1"/>
          <line x1="140" y1="0" x2="140" y2="525" stroke="#22C55E" stroke-width="1"/>
          <line x1="280" y1="0" x2="280" y2="525" stroke="#22C55E" stroke-width="1"/>
        </svg>
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;height:100%;padding:0 32px 52px;">
          <div style="margin-bottom:20px;"><img src="data:image/png;base64,{wordmark_b64}" style="height:28px;width:auto;display:block;" alt="Jeffthedev"></div>
          <span class="tag tag-dark" style="margin-bottom:11px;">YouTube · Watchlist</span>
          <div class="heading" style="color:#fff;font-size:32px;margin-bottom:14px;">Must-Watch Videos<br><span style="color:var(--green-light);">For Web Developers</span></div>
          <p class="body-text body-dark" style="max-width:270px;font-size:13px;">7 videos that'll actually make you better at this job. Bookmark before you lose them.</p>
        </div>
        <div class="arrow-dark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="progress-bar"><div class="progress-track progress-track-dark"><div class="progress-fill progress-fill-dark" style="width:{pct(1)}%;"></div></div><span class="slide-num-dark">1/9</span></div>
      </div>
"""


def video_slide(v, idx):
    dark = v["dark"]
    slide_cls = "slide-dark" if dark else "slide-light"
    num_cls = "num-big-dark" if dark else "num-big-light"
    tag_cls = "tag-dark" if dark else "tag-light"
    body_cls = "body-dark" if dark else "body-light"
    heading_color = "#fff" if dark else "#0A0F0C"
    arrow = "arrow-dark" if dark else "arrow-light"
    arrow_stroke = "rgba(255,255,255,0.35)" if dark else "rgba(0,0,0,0.22)"
    ptrack = "progress-track-dark" if dark else "progress-track-light"
    pfill = "progress-fill-dark" if dark else "progress-fill-light"
    pnum = "slide-num-dark" if dark else "slide-num-light"
    noise = '<div class="noise"></div>' if dark else ""
    menu_color = "#555" if True else "#555"

    return f"""
      <!-- SLIDE {idx} — {v['num']} {v['cat2']} -->
      <div class="slide {slide_cls}">
        {noise}
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-start;height:100%;padding:30px 30px 52px;">
          <span class="tag {tag_cls}" style="margin-bottom:8px;">{v['channel']}</span>
          <div class="{num_cls}" style="margin-bottom:8px;">{v['num']}.</div>
          <div class="cat-heading" style="color:{heading_color};margin-bottom:20px;">{v['cat1']} <span style="color:var(--green);">{v['cat2']}</span></div>
          <div class="video-card">
            <div class="video-thumb">
              <img src="data:image/jpeg;base64,{{thumb_b64}}" alt="">
              <div class="video-duration">{v['dur']}</div>
            </div>
            <div class="video-info">
              <div>
                <div class="video-title">{v['title']}</div>
                <div class="video-meta">{v['views']} · {v['age']}</div>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="{menu_color}" style="flex-shrink:0;margin-top:2px;"><circle cx="12" cy="5" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="12" cy="19" r="1.8"/></svg>
            </div>
          </div>
        </div>
        <div class="{arrow}"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="{arrow_stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="progress-bar"><div class="progress-track {ptrack}"><div class="progress-fill {pfill}" style="width:{pct(idx)}%;"></div></div><span class="{pnum}">{idx}/9</span></div>
      </div>
"""


def cta_slide():
    items = " / ".join(f"{v['cat2']}" for v in VIDEOS)
    checklist = ""
    for v in VIDEOS:
        checklist += f"""
              <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:16px;height:16px;border-radius:4px;background:rgba(34,197,94,0.3);border:1px solid rgba(34,197,94,0.5);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="9" height="9" viewBox="0 0 9 9" fill="none"><path d="M1.5 4.5l2 2 4-4" stroke="#4ADE80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <span style="font-family:var(--font);font-size:12px;color:rgba(255,255,255,0.85);font-weight:400;line-height:1.5;">{v['num']}. {v['cat2']} — {v['channel']}</span>
              </div>"""

    return f"""
      <!-- SLIDE 9 — CTA -->
      <div class="slide" style="background:var(--dark-bg);">
        <div style="position:absolute;inset:0;z-index:0;">
          <img src="data:image/jpeg;base64,{portrait_b64}" style="position:absolute;left:50%;transform:translateX(-50%);bottom:0;height:105%;width:auto;object-fit:cover;object-position:top center;filter:grayscale(60%) brightness(0.5);" alt="">
          <div style="position:absolute;inset:0;background:linear-gradient(165deg,rgba(10,15,12,0.94) 0%,rgba(21,128,61,0.72) 50%,rgba(34,197,94,0.58) 100%);"></div>
          <div style="position:absolute;top:0;left:0;right:0;height:50%;background:linear-gradient(to bottom,rgba(10,15,12,0.65) 0%,transparent 100%);"></div>
          <div style="position:absolute;bottom:0;left:0;right:0;height:40%;background:linear-gradient(to top,rgba(10,15,12,0.88) 0%,transparent 100%);"></div>
        </div>
        <div style="position:relative;z-index:2;display:flex;flex-direction:column;justify-content:space-between;height:100%;padding:28px 32px 52px;">
          <div><img src="data:image/png;base64,{wordmark_b64}" style="height:28px;width:auto;display:block;" alt="Jeffthedev"></div>
          <div>
            <span class="tag" style="color:rgba(255,255,255,0.5);letter-spacing:2px;font-size:10px;font-weight:600;text-transform:uppercase;display:block;margin-bottom:10px;">The Watchlist</span>
            <div class="heading" style="color:#fff;font-size:22px;margin-bottom:16px;line-height:1.15;">7 videos. Save them<br>before you lose them.</div>
            <div style="display:flex;flex-direction:column;gap:7px;margin-bottom:20px;">{checklist}
            </div>
            <div style="display:inline-flex;align-items:center;padding:12px 26px;background:var(--green);color:#0A0F0C;font-family:var(--font);font-weight:700;font-size:14px;border-radius:28px;letter-spacing:0.2px;">Follow @Jeffthedev__</div>
          </div>
        </div>
        <div class="progress-bar"><div class="progress-track progress-track-dark"><div class="progress-fill progress-fill-dark" style="width:100.00%;"></div></div><span class="slide-num-dark">9/9</span></div>
      </div>
"""


def foot():
    dots = "\n".join(
        f'    <div class="dot{" active" if i == 0 else ""}" data-idx="{i}"></div>'
        for i in range(TOTAL)
    )
    return f"""
    </div><!-- /carousel-track -->
  </div><!-- /carousel-viewport -->

  <div class="ig-dots" id="dots">
{dots}
  </div>

  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
    <div class="ig-bookmark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></div>
  </div>

  <div class="ig-caption">
    <strong>Jeffthedev__</strong> 7 YouTube videos every web developer should watch — CSS Grid, Flexbox, JavaScript, Git, VS Code, DevTools, and AI coding tools. Save this list. #webdev #css #javascript #programming
  </div>

</div><!-- /ig-frame -->

<script>
  const track=document.getElementById('track'),viewport=document.getElementById('viewport'),allDots=document.querySelectorAll('.dot');
  const TOTAL=9,SLIDE_W=420;
  let current=0,startX=0,isDragging=false,dragOffset=0;
  function goTo(idx){{
    current=Math.max(0,Math.min(TOTAL-1,idx));
    track.style.transition='transform 0.35s cubic-bezier(0.25,0.46,0.45,0.94)';
    track.style.transform=`translateX(${{-current*SLIDE_W}}px)`;
    allDots.forEach((d,i)=>d.classList.toggle('active',i===current));
  }}
  viewport.addEventListener('pointerdown',e=>{{isDragging=true;startX=e.clientX;dragOffset=0;track.style.transition='none';viewport.setPointerCapture(e.pointerId);}});
  viewport.addEventListener('pointermove',e=>{{if(!isDragging)return;dragOffset=e.clientX-startX;track.style.transform=`translateX(${{-current*SLIDE_W+dragOffset}}px)`;}});
  viewport.addEventListener('pointerup',()=>{{if(!isDragging)return;isDragging=false;if(dragOffset<-SLIDE_W*0.2)goTo(current+1);else if(dragOffset>SLIDE_W*0.2)goTo(current-1);else goTo(current);}});
  allDots.forEach(d=>d.addEventListener('click',()=>goTo(+d.dataset.idx)));
  document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight')goTo(current+1);if(e.key==='ArrowLeft')goTo(current-1);}});
</script>
</body>
</html>
"""


parts = [head(), cover_slide()]
for i, v in enumerate(VIDEOS, start=2):
    thumb_path = os.path.join(ASSETS, v["thumb"])
    slide_html = video_slide(v, i).replace("{thumb_b64}", b64(thumb_path))
    parts.append(slide_html)
parts.append(cta_slide())
parts.append(foot())

html = "".join(parts)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
