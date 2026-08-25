#!/usr/bin/env python3
# Build profile-card-redesign.html — a 3-slide "Before -> After" UI redesign
# showcase (light theme, serif italic headline, curved arrow), inspired by
# a reference Jeff shared (examples/Example5/, by @ui.abraham). Reuses the
# standard ig-frame/carousel shell (avatar/handle/dots/actions/caption) but
# each slide is a light "case study" card instead of the usual dark/green
# code-block format. The in-artwork attribution photo is Jeff's real photo
# (reference/assets/jeff-photo.jpg); the IG header avatar stays the usual
# stylized brand portrait for consistency with every other carousel.

import base64
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(BASE, "..", "..", "reference", "assets")
OUT = os.path.join(BASE, "profile-card-redesign.html")


def b64(path):
    with io.open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


avatar_b64 = b64(os.path.join(SHARED, "portrait.jpg"))
jeff_photo_b64 = b64(os.path.join(SHARED, "jeff-photo.jpg"))

TOTAL = 4

STYLE = """
  *{margin:0;padding:0;box-sizing:border-box;}
  :root{
    --green:#22C55E;--green-light:#4ADE80;--green-dark:#15803D;
    --dark-bg:#0A0F0C;--font:'Space Grotesk',sans-serif;--serif:'Playfair Display',serif;
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
  .ig-dots{display:flex;justify-content:center;gap:5px;padding:10px;}
  .dot{width:6px;height:6px;border-radius:50%;background:#444;transition:background 0.3s,transform 0.3s;}
  .dot.active{background:var(--green);transform:scale(1.2);}
  .ig-actions{display:flex;align-items:center;padding:8px 16px;gap:14px;}
  .ig-actions svg{color:#aaa;cursor:pointer;}
  .ig-actions svg:hover{color:#fff;}
  .ig-bookmark{margin-left:auto;}
  .ig-caption{padding:0 16px 16px;font-size:13px;color:#aaa;line-height:1.5;}
  .ig-caption strong{color:#fff;}

  .ba-slide{width:420px;height:525px;flex-shrink:0;background:linear-gradient(160deg,#efefef 0%,#d7d7d7 100%);position:relative;overflow:hidden;display:flex;flex-direction:column;}
  .ba-topbar{display:flex;justify-content:space-between;align-items:center;padding:22px 26px 0;font-family:var(--font);font-size:11px;color:#8d8d8d;letter-spacing:0.3px;}
  .ba-headline{font-family:var(--serif);font-style:italic;font-weight:700;color:#141414;line-height:1;}
  .ba-card-area{flex:1;display:flex;align-items:center;justify-content:center;position:relative;}
  .ba-footer{display:flex;align-items:center;justify-content:space-between;padding:0 26px 24px;}
  .ba-avatar{width:30px;height:30px;border-radius:50%;overflow:hidden;flex-shrink:0;}
  .ba-avatar img{width:100%;height:100%;object-fit:cover;object-position:top center;}
  .ba-handle{font-family:var(--font);font-size:12.5px;font-weight:700;color:#141414;}
  .ba-handle-sub{font-family:var(--font);font-size:9.5px;color:#9a9a9a;}
  .ba-tag{display:flex;align-items:center;gap:5px;font-family:var(--font);font-size:10.5px;color:#7a7a7a;}

  .pc{width:230px;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 20px 44px rgba(0,0,0,0.2);}
  .pc .photo{width:100%;height:190px;overflow:hidden;background:#ddd;}
  .pc .photo img{width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;}
  .pc .body{padding:9px 15px 11px;}
  .pc .name{font-family:var(--font);font-size:13.5px;font-weight:700;color:#141414;margin-bottom:1px;}
  .pc .role{font-family:var(--font);font-size:9px;color:#8a8a8a;margin-bottom:4px;}
  .pc .bio{font-family:var(--font);font-size:8.5px;line-height:1.35;color:#8a8a8a;margin-bottom:5px;}
  .pc .stat-line{display:flex;justify-content:space-between;font-family:var(--font);font-size:10px;padding:2.5px 0;border-top:1px solid #f0f0f0;}
  .pc .stat-line .lbl{color:#8a8a8a;}
  .pc .stat-line .val{color:#141414;font-weight:700;}
  .pc .btn{width:100%;text-align:center;padding:6px;border-radius:8px;font-family:var(--font);font-size:10px;font-weight:700;margin-top:3px;}
  .pc .btn-dark{background:#141414;color:#fff;}

  .pc2{width:310px;background:#fff;border-radius:20px;padding:18px;box-shadow:0 20px 44px rgba(0,0,0,0.2);}
  .pc2 .head-row{display:flex;align-items:center;gap:10px;margin-bottom:12px;}
  .pc2 .avatar{width:44px;height:44px;border-radius:12px;overflow:hidden;flex-shrink:0;background:#ddd;}
  .pc2 .avatar img{width:100%;height:100%;object-fit:cover;object-position:top center;}
  .pc2 .name{font-family:var(--font);font-size:14.5px;font-weight:700;color:#141414;}
  .pc2 .role{font-family:var(--font);font-size:10.5px;color:#8a8a8a;margin-top:2px;}
  .pc2 .bio{font-family:var(--font);font-size:10.5px;line-height:1.5;color:#6b6b6b;margin-bottom:14px;}
  .pc2 .stat-row{display:flex;margin-bottom:16px;}
  .pc2 .stat{flex:1;border-left:1px solid #ececec;padding-left:12px;}
  .pc2 .stat:first-child{border-left:none;padding-left:0;}
  .pc2 .stat .lbl{font-family:var(--font);font-size:10px;color:#9a9a9a;margin-bottom:3px;}
  .pc2 .stat .val{font-family:var(--font);font-size:13px;font-weight:700;color:#141414;}
  .pc2 .btn-row{display:flex;gap:8px;}
  .pc2 .btn{flex:1;text-align:center;padding:10px;border-radius:9px;font-family:var(--font);font-size:11.5px;font-weight:700;}
  .pc2 .btn-dark{background:#141414;color:#fff;}
  .pc2 .btn-light{background:#f2f2f2;color:#141414;}

  .fw-photo{width:130px;height:130px;border-radius:22px;overflow:hidden;box-shadow:0 20px 44px rgba(0,0,0,0.25);margin:0 auto 16px;}
  .fw-photo img{width:100%;height:100%;object-fit:cover;object-position:center 20%;display:block;}
  .fw-name{font-family:var(--font);font-size:17px;font-weight:700;color:#141414;text-align:center;margin-bottom:2px;}
  .fw-handle{font-family:var(--font);font-size:12px;color:#9a9a9a;text-align:center;margin-bottom:18px;}
  .fw-btn{display:inline-flex;align-items:center;gap:7px;padding:13px 28px;background:#141414;color:#fff;font-family:var(--font);font-weight:700;font-size:14px;border-radius:28px;}
"""


def topbar(idx):
    return f"""<div class="ba-topbar"><span>Profile Card Redesign</span><span>0{idx}</span></div>"""


def footer():
    return f"""
      <div class="ba-footer">
        <div style="display:flex;align-items:center;gap:9px;">
          <div class="ba-avatar"><img src="data:image/jpeg;base64,{jeff_photo_b64}" alt=""></div>
          <div>
            <div class="ba-handle">Jeffthedev__</div>
            <div class="ba-handle-sub">@jeffthedev__</div>
          </div>
        </div>
        <div class="ba-tag">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 16V4M7 4l-3 3M7 4l3 3M17 8v12M17 20l3-3M17 20l-3-3"/></svg>
          Profile Card Redesign
        </div>
      </div>
"""


def profile_card(scale=1.0):
    card = f"""
      <div class="pc">
        <div class="photo"><img src="data:image/jpeg;base64,{jeff_photo_b64}" alt=""></div>
        <div class="body">
          <div class="name">Jeffthedev</div>
          <div class="role">Fullstack Developer &middot; Remote</div>
          <p class="bio">I'm a fullstack developer who blends clean code with practical, ship-ready solutions.</p>
          <div class="stat-line"><span class="lbl">Projects</span><span class="val">50</span></div>
          <div class="stat-line"><span class="lbl">Followers</span><span class="val">78.4K</span></div>
          <div class="stat-line"><span class="lbl">Rating</span><span class="val">4.9</span></div>
          <div class="btn btn-dark">Hire now</div>
          <div class="btn btn-dark" style="background:#f2f2f2;color:#141414;">Message</div>
        </div>
      </div>
"""
    if scale == 1.0:
        return card
    w = int(230 * scale)
    h_box = int(438 * scale)
    return f'<div style="width:{w}px;height:{h_box}px;overflow:visible;"><div style="transform:scale({scale});transform-origin:top left;">{card}</div></div>'


def profile_card2(scale=1.0):
    card = f"""
      <div class="pc2">
        <div class="head-row">
          <div class="avatar"><img src="data:image/jpeg;base64,{jeff_photo_b64}" alt=""></div>
          <div>
            <div class="name">Jeffthedev</div>
            <div class="role">Fullstack Developer &middot; Remote</div>
          </div>
        </div>
        <p class="bio">I'm a fullstack developer who builds products that actually ship &mdash; clean code, practical solutions.</p>
        <div class="stat-row">
          <div class="stat"><div class="lbl">Projects</div><div class="val">50</div></div>
          <div class="stat"><div class="lbl">Followers</div><div class="val">78.4K</div></div>
          <div class="stat"><div class="lbl">Rating</div><div class="val">4.9</div></div>
        </div>
        <div class="btn-row">
          <div class="btn btn-dark">Hire now</div>
          <div class="btn btn-light">Message</div>
        </div>
      </div>
"""
    if scale == 1.0:
        return card
    w = int(310 * scale)
    h_box = int(210 * scale)
    return f'<div style="width:{w}px;height:{h_box}px;overflow:visible;"><div style="transform:scale({scale});transform-origin:top left;">{card}</div></div>'


def arrow_svg(flip=False):
    path = "M4 40 C 60 -6, 160 -6, 216 40" if not flip else "M216 40 C 160 -6, 60 -6, 4 40"
    return f"""<svg width="220" height="46" viewBox="0 0 220 46" fill="none" style="position:absolute;">
      <path d="{path}" stroke="#141414" stroke-width="2" stroke-linecap="round"/>
      <path d="M204 30 L 216 40 L 202 44" stroke="#141414" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>"""


def slide_overview():
    return f"""
      <div class="ba-slide">
        {topbar(0)}
        <div style="padding:44px 26px 0;position:relative;">
          <div style="display:flex;align-items:center;gap:0;position:relative;">
            <div class="ba-headline" style="font-size:38px;">Before</div>
            <div style="width:90px;height:36px;position:relative;margin:0 4px;">
              <svg width="90" height="40" viewBox="0 0 90 40" fill="none"><path d="M4 30 C 30 2, 60 2, 84 14" stroke="#141414" stroke-width="2" stroke-linecap="round"/><path d="M72 8 L 84 14 L 76 24" stroke="#141414" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
            </div>
            <div class="ba-headline" style="font-size:38px;">After</div>
          </div>
        </div>
        <div class="ba-card-area" style="gap:22px;padding-top:6px;">
          {profile_card(scale=0.62)}
          {profile_card2(scale=0.56)}
        </div>
        {footer()}
      </div>
"""


def slide_before():
    return f"""
      <div class="ba-slide">
        {topbar(1)}
        <div style="padding:24px 26px 0;">
          <div class="ba-headline" style="font-size:42px;">Before</div>
        </div>
        <div class="ba-card-area">
          {profile_card(scale=1.0)}
        </div>
        {footer()}
      </div>
"""


def slide_after():
    return f"""
      <div class="ba-slide">
        {topbar(2)}
        <div style="padding:24px 26px 0;">
          <div class="ba-headline" style="font-size:42px;">After</div>
        </div>
        <div class="ba-card-area">
          {profile_card2(scale=1.0)}
        </div>
        {footer()}
      </div>
"""


def slide_follow():
    return f"""
      <div class="ba-slide">
        {topbar(3)}
        <div style="padding:24px 26px 0;">
          <div class="ba-headline" style="font-size:38px;">Like this<br>redesign?</div>
        </div>
        <div class="ba-card-area">
          <div>
            <div class="fw-photo"><img src="data:image/jpeg;base64,{jeff_photo_b64}" alt=""></div>
            <div class="fw-name">Jeffthedev</div>
            <div class="fw-handle">@jeffthedev__</div>
            <div style="text-align:center;">
              <div class="fw-btn">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
                Follow for more
              </div>
            </div>
          </div>
        </div>
        {footer()}
      </div>
"""


def foot(total):
    dots = "\n".join(
        f'    <div class="dot{" active" if i == 0 else ""}" data-idx="{i}"></div>'
        for i in range(total)
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
    <strong>Jeffthedev__</strong> Redesigned my profile card &mdash; before vs after. Small changes, way less clutter. Which one would YOU trust more? #uidesign #webdev #productdesign
  </div>

</div><!-- /ig-frame -->

<script>
  const track=document.getElementById('track'),viewport=document.getElementById('viewport'),allDots=document.querySelectorAll('.dot');
  const TOTAL={total},SLIDE_W=420;
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


head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jeffthedev — Profile Card Redesign</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,700&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
<div class="ig-frame">

  <div class="ig-header">
    <div class="ig-avatar"><img src="data:image/jpeg;base64,{avatar_b64}" alt=""></div>
    <div class="ig-info">
      <div class="ig-handle">Jeffthedev__</div>
      <div class="ig-sub">Developer Education</div>
    </div>
    <div class="ig-more">&middot;&middot;&middot;</div>
  </div>

  <div class="carousel-viewport" id="viewport">
    <div class="carousel-track" id="track">
"""

html = head + slide_overview() + slide_before() + slide_after() + slide_follow() + foot(TOTAL)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
