#!/usr/bin/env python3
# Build profile-card-vote.html — a single-image "A or B?" design-poll post
# (not a swipeable carousel). Two mockup treatments of Jeff's own profile
# card side by side, inviting a comment vote. Portrait + wordmark reused
# from reference/assets/.

import base64
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(BASE, "..", "..", "reference", "assets")
OUT = os.path.join(BASE, "profile-card-vote.html")


def b64(path):
    with io.open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


portrait_b64 = b64(os.path.join(SHARED, "portrait.jpg"))
wordmark_b64 = b64(os.path.join(SHARED, "wordmark.png"))

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jeffthedev — A or B?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box;}}
  :root{{
    --green:#22C55E;--green-light:#4ADE80;--green-dark:#15803D;
    --dark-bg:#0A0F0C;--font:'Space Grotesk',sans-serif;
  }}
  html{{background:var(--dark-bg);}}
  body{{width:1080px;height:1350px;background:var(--dark-bg);font-family:var(--font);position:relative;overflow:hidden;}}
  .grid-bg{{position:absolute;inset:0;opacity:0.05;pointer-events:none;}}
  .wrap{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;height:100%;padding:64px 70px 56px;}}
  .brand-row{{display:flex;align-items:center;gap:12px;align-self:flex-start;}}
  .brand-row img{{height:26px;width:auto;display:block;}}
  .kicker{{font-family:var(--font);font-size:15px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--green-light);text-align:center;margin-top:54px;}}
  .headline{{font-family:var(--font);font-weight:700;font-size:52px;line-height:1.15;color:#fff;text-align:center;letter-spacing:-0.5px;margin-top:16px;max-width:820px;}}
  .cards-row{{display:flex;align-items:flex-start;gap:56px;margin-top:56px;}}
  .card-col{{display:flex;flex-direction:column;align-items:center;}}
  .opt-tag{{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--green);color:#0A0F0C;font-weight:700;font-size:19px;margin-bottom:16px;}}
  .card{{width:420px;height:660px;border-radius:26px;overflow:hidden;position:relative;box-shadow:0 24px 60px rgba(0,0,0,0.55);}}
  .card-a{{background:#161a17;}}
  .card-a .photo{{width:100%;height:436px;overflow:hidden;background:#161a17;}}
  .card-a .photo img{{width:100%;height:100%;object-fit:cover;object-position:top center;}}
  .card-a .info{{padding:22px 24px 26px;}}
  .card-b{{background:#0A0F0C;}}
  .card-b .photo{{position:absolute;inset:0;}}
  .card-b .photo img{{width:100%;height:100%;object-fit:cover;object-position:top center;}}
  .card-b .fade{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(to top,rgba(10,15,12,0.97) 0%,rgba(10,15,12,0.55) 55%,transparent 100%);}}
  .card-b .info{{position:absolute;left:0;right:0;bottom:0;padding:24px 24px 28px;}}
  .name-row{{display:flex;align-items:center;gap:8px;margin-bottom:10px;}}
  .name{{font-family:var(--font);font-weight:700;font-size:23px;color:#fff;}}
  .badge{{width:19px;height:19px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
  .badge-a{{background:var(--green);}}
  .badge-b{{background:transparent;border:2px solid #fff;}}
  .bio{{font-family:var(--font);font-size:14.5px;line-height:1.5;color:rgba(255,255,255,0.6);margin-bottom:20px;max-width:340px;}}
  .stat-row{{display:flex;align-items:center;gap:18px;}}
  .stat{{display:flex;align-items:center;gap:6px;font-family:var(--font);font-size:14px;font-weight:600;color:rgba(255,255,255,0.75);}}
  .stat svg{{opacity:0.6;}}
  .follow-btn{{margin-left:auto;display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:24px;font-family:var(--font);font-weight:700;font-size:14px;}}
  .follow-a{{background:#fff;color:#0A0F0C;}}
  .follow-b{{background:#fff;color:#0A0F0C;}}
  .foot{{margin-top:auto;text-align:center;}}
  .foot-cta{{font-family:var(--font);font-size:22px;font-weight:600;color:#fff;margin-bottom:10px;}}
  .foot-cta span{{color:var(--green-light);}}
  .foot-sub{{font-family:var(--font);font-size:14px;color:rgba(255,255,255,0.4);}}
</style>
</head>
<body>

  <svg class="grid-bg" width="1080" height="1350" viewBox="0 0 1080 1350">
    <line x1="0" y1="450" x2="1080" y2="450" stroke="#22C55E" stroke-width="1"/>
    <line x1="0" y1="900" x2="1080" y2="900" stroke="#22C55E" stroke-width="1"/>
    <line x1="360" y1="0" x2="360" y2="1350" stroke="#22C55E" stroke-width="1"/>
    <line x1="720" y1="0" x2="720" y2="1350" stroke="#22C55E" stroke-width="1"/>
  </svg>

  <div class="wrap">
    <div class="brand-row">
      <img src="data:image/png;base64,{wordmark_b64}" alt="Jeffthedev">
    </div>

    <div class="kicker">Design Poll</div>
    <div class="headline">Which profile card would<br>make <span style="color:var(--green-light);">you</span> hit follow?</div>

    <div class="cards-row">
      <div class="card-col">
        <div class="opt-tag">A</div>
        <div class="card card-a">
          <div class="photo"><img src="data:image/jpeg;base64,{portrait_b64}" alt=""></div>
          <div class="info">
            <div class="name-row">
              <div class="name">Jeffthedev</div>
              <div class="badge badge-a"><svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M1.5 5l2.2 2.2L8.5 2.5" stroke="#0A0F0C" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
            </div>
            <p class="bio">Fullstack Developer sharing what actually works.</p>
            <div class="stat-row">
              <div class="stat"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>78.4K</div>
              <div class="stat"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>112</div>
              <div class="follow-btn follow-a">Follow +</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card-col">
        <div class="opt-tag">B</div>
        <div class="card card-b">
          <div class="photo"><img src="data:image/jpeg;base64,{portrait_b64}" alt=""></div>
          <div class="fade"></div>
          <div class="info">
            <div class="name-row">
              <div class="name">Jeffthedev</div>
              <div class="badge badge-b"><svg width="9" height="9" viewBox="0 0 10 10" fill="none"><path d="M1.5 5l2.2 2.2L8.5 2.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
            </div>
            <p class="bio">A Fullstack Developer sharing what actually works.</p>
            <div class="stat-row">
              <div class="stat"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>78.4K</div>
              <div class="stat"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>112</div>
              <div class="follow-btn follow-b">Follow +</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="foot">
      <div class="foot-cta">Comment <span>A</span> or <span>B</span> — I'll actually use the winner.</div>
      <div class="foot-sub">Follow @Jeffthedev__ for more design breakdowns</div>
    </div>
  </div>

</body>
</html>
"""

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", OUT, "len", len(html))
