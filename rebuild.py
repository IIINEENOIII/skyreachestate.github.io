#!/usr/bin/env python3
"""De-concatenate the skyreachestate.github.io pages: one valid document per page,
newest design generation wins, internal duplications removed, fragments completed."""
import re, sys

D = "/home/hatch/workspace/skyreach-site"

def lines(path):
    with open(path) as f:
        return f.read().split("\n")  # keep 1-indexed logic via L[i-1]

def rng(L, a, b):
    return L[a-1:b]

def check(cond, msg):
    if not cond:
        print("ASSERT FAILED:", msg); sys.exit(1)

FOOTER_COLS = """  <footer class="footer">
    <div class="container cols">
      <div>
        <div class="brand" style="margin-bottom:8px"><div class="logo">SR</div><div>SkyReach Estate</div></div>
        <div class="small">Email: <a href="mailto:BRANDON@SKYREACHESTATE.COM">BRANDON@SKYREACHESTATE.COM</a> • Phone: <a href="tel:+18327054042">+1 (832) 705-4042</a></div>
        <div class="small" style="margin-top:10px">© <span id="year"></span> SkyReach Estate.</div>
      </div>
      <div class="small"><b>Disclosure:</b> Informational only. Not legal/tax advice. Time-sensitive situations (foreclosure/bankruptcy) should involve qualified counsel.</div>
    </div>
  </footer>

  <script src="assets/site.js"></script>
</body>
</html>"""

# ---------------- index.html ----------------
L = lines(f"{D}/index.html")
check(L[130] == '<body class="home-luxe">', "index 131 body")
check("luxe-hero fade-in" in L[286], "index 287 luxe-hero")
check("</header>" in L[303], "index 304 /header")
check("luxe-stat-strip" in L[306], "index 307 stat strip")
check("</section>" in L[312], "index 313 /section")
check("How it works" in L[340], "index 341 how it works")
check("01 · Share your property" in L[352], "index 353 tile 01")
check("Why sellers choose SkyReach" in L[370], "index 371 why sellers")
check(L[382].strip().startswith("<form class="), "index 383 stray form")
check('id="get-started"' in L[383], "index 384 real form")
check("Situations we handle every week" in L[411], "index 412 situations")
check("pro-gallery" in L[415], "index 416 gallery")
check("Why sellers choose SkyReach" in L[432], "index 433 why sellers dup")
check('<footer class="footer">' in L[470], "index 471 footer")
check("SkyReach Estate.</div>" in L[474], "index 475 copy line")
check("mailto:BRANDON" in L[475], "index 476 contact")
check("</html>" in L[484], "index 485 /html")

head_index = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>SkyReach Estate | Modern Home Selling in Texas</title>
  <meta name="description" content="SkyReach Estate helps Texas homeowners sell with a modern, clear process and flexible timelines." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body class="home-luxe">
  <div class="nav">
    <div class="container nav-inner">
      <a class="brand" href="#top">
        <div class="logo">SR</div>
        <div>SkyReach Estate</div>
      </a>
      <div class="nav-links">
        <a class="pill" href="solutions.html">Solutions</a>
        <a class="pill" href="timelines.html">Timelines</a>
        <a class="pill" href="about.html">About</a>
        <a class="btn primary" href="contact.html">Contact</a>
      </div>
    </div>
  </div>
"""
parts = [head_index]
parts += rng(L, 287, 304)    # luxe hero
parts += rng(L, 307, 313)    # stat strip (one copy)
parts += rng(L, 337, 344)    # how-it-works header
parts += rng(L, 351, 366)    # 01/02/03 tiles (skip dup 01-only block 345-350)
parts += rng(L, 368, 382)    # why-sellers card
parts += rng(L, 384, 406)    # form (skip stray nested <form> at 383)
parts += rng(L, 408, 423)    # situations gallery (skip stray closers 424-429, skip dup why-sellers 430-470)
parts += rng(L, 471, 476)    # footer open through contact line (skip dupe © at 477)
parts += rng(L, 478, 485)    # rest of footer + script + close
with open(f"{D}/index.html", "w") as f:
    f.write("\n".join(parts))
print("index.html rebuilt:", len("\n".join(parts).split("\n")), "lines")

# ---------------- solutions.html ----------------
L = lines(f"{D}/solutions.html")
check(L[9] == "<body>", "solutions 10 body")
check('<div class="nav">' in L[22], "solutions 23 nav")
check("We evaluate: fast cash close" in L[61], "solutions 62 li2")
check(L[62].strip().startswith("@@"), "solutions 63 diff marker")
check("</ul>" in L[63], "solutions 64 /ul")
check("</html>" in L[109], "solutions 110 /html")

restored_bullet = '          <li>If a purchase isn\'t the right fit, we\'ll tell you — and point you to <a href="creative-finance.html">other structures</a> or local resources.</li>'
parts = []
parts += rng(L, 1, 10)       # head + body
parts += rng(L, 23, 62)      # nav..foreclosure bullets
parts.append(restored_bullet)  # replaces the leaked diff hunk
parts += rng(L, 64, 110)     # rest of page
with open(f"{D}/solutions.html", "w") as f:
    f.write("\n".join(parts))
print("solutions.html rebuilt")

# ---------------- contact.html ----------------
L = lines(f"{D}/contact.html")
check(L[9] == "<body>", "contact 10 body")
check("<!-- NAV -->" in L[27], "contact 28 nav comment")
check("</html>" in L[262], "contact 263 /html")
parts = rng(L, 1, 10) + rng(L, 28, 263)
with open(f"{D}/contact.html", "w") as f:
    f.write("\n".join(parts))
print("contact.html rebuilt")

# ---------------- about.html ----------------
L = lines(f"{D}/about.html")
check(L[9] == "<body>", "about 10 body")
check('<div class="nav">' in L[19], "about 20 nav")
check("Offer alternative structures" in L[58], "about 59 last li")
parts = rng(L, 1, 10) + rng(L, 20, 59)
completion_about = """</li>
          <li>Coordinate clean closings with reputable title and escrow partners.</li>
        </ul>
      </div>

      <div class="callout fade-in">
        <h3 style="margin:0">Talk to us first.</h3>
        <div class="small">Facing a deadline or a tough property situation? A short call is the fastest way to get clear options.</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn primary" href="contact.html">Contact us</a>
          <a class="btn ghost" href="solutions.html">See solutions</a>
        </div>
        <div class="small"><b>Fast contact:</b> <a href="mailto:BRANDON@SKYREACHESTATE.COM">BRANDON@SKYREACHESTATE.COM</a> • <a href="tel:+18327054042">+1 (832) 705-4042</a></div>
      </div>
    </div>
  </section>

""" + FOOTER_COLS
parts.append(completion_about)
with open(f"{D}/about.html", "w") as f:
    f.write("\n".join(parts))
print("about.html rebuilt")

# ---------------- timelines.html ----------------
L = lines(f"{D}/timelines.html")
check(L[9] == "<body>", "timelines 10 body")
check('<div class="nav">' in L[21], "timelines 22 nav")
check("Ideal when speed is more important" in L[60], "timelines 61 meta")
parts = rng(L, 1, 10) + rng(L, 22, 61)
completion_timelines = """      </div>

      <div class="tile fade-in">
        <h3>2–6 weeks (Balanced)</h3>
        <ul class="list">
          <li>Time to compare a cash offer against other paths.</li>
          <li>Room for title work, payoff coordination, and move planning.</li>
          <li>A good fit when there's pressure but no auction date yet.</li>
        </ul>
        <div class="meta">Speed plus breathing room to make the right call.</div>
      </div>

      <div class="tile fade-in">
        <h3>1–3 months (Flexible)</h3>
        <ul class="list">
          <li>Best when you want options, not just speed.</li>
          <li>Time to explore creative structures when they make sense.</li>
          <li>Move-out and transition planning on your schedule.</li>
        </ul>
        <div class="meta">For life transitions that need coordination, not rushing.</div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container split">
      <div class="card fade-in">
        <h2>What affects your timeline</h2>
        <ul class="list">
          <li>Title or lien complexity</li>
          <li>Probate or estate coordination</li>
          <li>Payoff and reinstatement processing</li>
          <li>Access and move-out timing</li>
        </ul>
      </div>

      <div class="callout fade-in">
        <h3 style="margin:0">Up against a deadline?</h3>
        <div class="small">Tell us the date you're working against and we'll map the fastest realistic path.</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn primary" href="contact.html">Talk to SkyReach</a>
          <a class="btn ghost" href="solutions.html">See solutions</a>
        </div>
      </div>
    </div>
  </section>

""" + FOOTER_COLS
parts.append(completion_timelines)
with open(f"{D}/timelines.html", "w") as f:
    f.write("\n".join(parts))
print("timelines.html rebuilt")

# ---------------- creative-finance.html ----------------
L = lines(f"{D}/creative-finance.html")
check('<div class="nav">' in L[13], "cf 14 nav")
check("What sellers usually care about" in L[119], "cf 120 sellers care")
check('<div class="container cards">' in L[143], "cf 144 dangling open")
head_cf = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Creative Finance | SkyReach Estate</title>
  <meta name="description" content="Creative finance options explained in plain English: seller financing, subject-to, wraps, lease options, and when cash is best." />
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body>
"""
parts = [head_cf] + rng(L, 14, 142) + ["", FOOTER_COLS]
with open(f"{D}/creative-finance.html", "w") as f:
    f.write("\n".join(parts))
print("creative-finance.html rebuilt")

# ---------------- thanks.html ----------------
L = lines(f"{D}/thanks.html")
check(L[9] == "<body>", "thanks 10 body")
check('<div class="nav">' in L[15], "thanks 16 nav")
check("Back to home" in L[40], "thanks 41 back home")
footer_simple = """  <footer class="footer">
    <div class="container">
      <p>© <span id="year"></span> SkyReach Estate</p>
    </div>
  </footer>

  <script src="assets/site.js"></script>
</body>
</html>"""
parts = rng(L, 1, 10) + rng(L, 16, 45) + ["", footer_simple]
with open(f"{D}/thanks.html", "w") as f:
    f.write("\n".join(parts))
print("thanks.html rebuilt")
print("ALL PAGES REBUILT OK")
