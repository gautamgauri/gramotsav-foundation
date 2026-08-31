#!/usr/bin/env python3
"""Generates the Gramotsav Foundation static site from shared shell + per-page content.

Run:  python3 build.py     (writes *.html into this directory)
Edit page content in PAGES below; the header, footer and nav come from the shell.
"""
import os, re

SITE = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("index.html", "Home"),
    ("our-story.html", "Our Story"),
    ("programmes.html", "Programmes"),
    ("impact.html", "Impact"),
    ("contact.html", "Contact"),
]

ORG = {
    "name": "Gramotsav Foundation",
    "tag": "Patna · Folk Culture & Inclusive Learning",
    "email": "gramotsavfoundation@gmail.com",
    "instagram": "https://www.instagram.com/gramotsavfoundation/",
    "instagram_handle": "@gramotsavfoundation",
    "address": "C/o Suraj Kumar, A. K. Road, Machuatoli, Patna Sadar, Patna – 800016, Bihar, India",
    "pan": "AAMCG9005G",
    "cin": "U88900BR2026NPL083562",
    "licence": "182161",
    "inc_date": "19 March 2026",
    "urn_reg": "AAMCG9005GE20261",
    "urn_appr": "AAMCG9005GF20261",
    "reg_date": "24 August 2026",
    "reg_valid": "TY 2026-27 to TY 2028-29",
}

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:type" content="website" />
<meta property="og:image" content="logo.png" />
<link rel="icon" href="logo.png" type="image/png" />
<link rel="apple-touch-icon" href="logo.png" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Mukta:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css" />
</head>
<body>

<header class="site-header">
  <nav class="nav">
    <a class="brand" href="index.html">
      <img class="brand-logo" src="logo.png" alt="Gramotsav Foundation logo" />
      <span class="brand-name">Gramotsav<span>Foundation · Patna</span></span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false">&#9776;</button>
    <ul class="nav-links">
{navitems}
      <li><a href="support.html" class="btn btn--primary nav-cta">Support Us</a></li>
    </ul>
  </nav>
</header>
"""

FOOT = """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:14px;">
          <img class="brand-logo" src="logo.png" alt="Gramotsav Foundation logo" />
          <span class="brand-name" style="color:#fff;">Gramotsav<span>Foundation · Patna</span></span>
        </a>
        <p style="max-width:36ch;">A Section 8 non-profit in Patna. Folk culture, inclusive learning, and a route from creative skill towards a living. <span class="devnagri">मिट्टी से मंच तक</span>.</p>
        <div class="socials">
          <a class="social-btn" href="{instagram}" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16ZM12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.3-1.46.72-2.13 1.38C1.35 2.68.93 3.35.63 4.14.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.3.79.72 1.46 1.38 2.13.67.66 1.34 1.08 2.13 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.9 5.9 0 0 0 2.13-1.38 5.9 5.9 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0 0-1.38-2.13A5.9 5.9 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0Zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32ZM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm6.41-10.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88Z"/></svg></a>
          <a class="social-btn" href="mailto:{email}" aria-label="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 4h20v16H2V4Zm2.4 2L12 11.6 19.6 6H4.4ZM20 8.3l-8 5.9-8-5.9V18h16V8.3Z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="our-story.html">Our Story</a>
        <a href="impact.html">Vision, Mission &amp; Impact</a>
        <a href="learning-through-music.html">Learning Through Music</a>
        <a href="blind-school-project.html">Blind School Project</a>
        <a href="music-beyond-vision.html">Music &amp; Art Beyond Vision</a>
      </div>
      <div>
        <h4>Get Involved</h4>
        <a href="support.html">Partner &amp; Support</a>
        <a href="support.html#volunteer">Volunteer</a>
        <a href="contact.html">Contact Us</a>
        <a href="transparency.html">Governance &amp; Compliance</a>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 Gramotsav Foundation &middot; A Section 8 non-profit company &middot; CIN {cin} &middot; Patna, Bihar
    </div>
  </div>
</footer>

<script src="main.js"></script>
</body>
</html>
"""


def shell(slug, title, desc, body):
    navitems = ""
    for href, label in NAV:
        cls = ' class="active"' if href == slug else ""
        navitems += f'      <li><a href="{href}"{cls}>{label}</a></li>\n'
    head = HEAD.format(title=title, desc=desc, navitems=navitems.rstrip("\n"))
    foot = FOOT.format(**ORG)
    return head + body + foot


# --------------------------------------------------------------------------
# Reusable fragments
# --------------------------------------------------------------------------

def banner(h1, p):
    return f"""
<section class="page-banner">
  <div class="container">
    <h1>{h1}</h1>
    <p>{p}</p>
  </div>
</section>
"""


CTA = """
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>Bring a stage to a child who has never had one</h2>
      <p>We are young, registered and ready to start. There is room for a partner on the Blind School Project, for someone to sponsor a cohort of learners, or for a saathi who can give us a morning a week.</p>
      <div class="btn-row center">
        <a href="support.html" class="btn btn--light">Partner With Us</a>
        <a href="contact.html" class="btn btn--ghost" style="border-color:#fff;color:#fff;">Talk to the Team</a>
      </div>
    </div>
  </div>
</section>
"""

JOURNEY = """
<div class="journey">
  <span>Listen</span><i>&rarr;</i><span>Learn</span><i>&rarr;</i><span>Practise</span><i>&rarr;</i>
  <span>Create</span><i>&rarr;</i><span>Collaborate</span><i>&rarr;</i><span>Perform</span><i>&rarr;</i><span>Impact</span>
</div>
"""

# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

PAGES = {}

# ---------------------------------------------------------------- HOME -----
PAGES["index.html"] = dict(
    title="Gramotsav Foundation — Folk Culture & Inclusive Learning, Patna",
    desc="Gramotsav Foundation is a Patna-based Section 8 non-profit using folk culture, music and the arts to build confidence, inclusion and creative livelihoods in Bihar. Mitti Se Manch Tak.",
    body="""
<section class="hero">
  <div class="container">
    <span class="tagline-hi">मिट्टी से मंच तक</span>
    <h1>From the soil to the stage.</h1>
    <p>Folk culture and inclusive learning, in Bihar. Children here learn a song, learn a taal, and then get a manch of their own. For most of them that stage is a first.</p>
    <div class="btn-row">
      <a href="programmes.html" class="btn btn--light">Our Programmes</a>
      <a href="support.html" class="btn btn--green">Partner With Us</a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><b>2,000+</b><span>Children reached</span></div>
      <div class="hero-stat"><b>12</b><span>Fellows, 10 of them women</span></div>
      <div class="hero-stat"><b>10+</b><span>Artists engaged</span></div>
    </div>
  </div>
</section>

<!-- MISSION -->
<section class="section">
  <div class="container section-head">
    <span class="eyebrow">Who We Are</span>
    <h2>Culture is not decoration here. It is what we teach with.</h2>
    <p class="lead mx-auto">Gramotsav Foundation is a Section 8 non-profit company in Patna, Bihar. We work to keep the folk traditions of rural and indigenous India in use, and we teach with them: the lok geet a grandmother still sings, the taal a dholak keeps. Mostly with children whom the ordinary classroom has already left behind.</p>
  </div>
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="card-media"><img src="img/harmonium-hands.jpg" alt="Children gathered closely around a harmonium and dholak, learning by touch and sound" /></div>
        <div class="card-body">
          <span class="card-tag">Inclusive Learning</span>
          <h3>Audio-first music</h3>
          <p>Instrument teaching that needs neither sight nor notation. A phrase is played, played again, then put under the student's hands. Riyaz does the rest.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/community-event.jpg" alt="A community cultural gathering with festive bunting and families watching a performance" /></div>
        <div class="card-body">
          <span class="card-tag">Folk &amp; Heritage</span>
          <h3>Bhojpuri, Maithili, Magahi</h3>
          <p>Lok geet from the Bhojpuri, Maithili and Magahi traditions, the stories that travel with them, and the instruments they were written for. Children meet their own culture as something worth knowing.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/guitar-community.jpg" alt="A facilitator playing guitar with young children in a community learning space" /></div>
        <div class="card-body">
          <span class="card-tag">Creative Livelihood</span>
          <h3>Skill to opportunity</h3>
          <p>Music can be work: performance, teaching, recording, ensemble jobs. We promise nobody a job. We do show what years of riyaz can open up, and we say it plainly.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PHILOSOPHY -->
<section class="section section--navy">
  <div class="container section-head">
    <span class="eyebrow">Our Philosophy</span>
    <h2><span class="devnagri">मिट्टी से मंच तक</span> &mdash; Mitti Se Manch Tak</h2>
    <p class="lead mx-auto">Mitti is the soil a child comes from. Manch is the stage. The whole method sits between those two words, and every programme we run follows the same arc.</p>
  </div>
  <div class="container">""" + JOURNEY + """</div>
</section>

<!-- PROGRAMMES -->
<section class="section">
  <div class="container section-head">
    <span class="eyebrow">What We Do</span>
    <h2>Three projects, one idea</h2>
  </div>
  <div class="container">
    <div class="grid grid-2">
      <div class="card">
        <div class="card-media"><img src="img/harmonium-dholak.jpg" alt="Students seated on the floor around a harmonium and dholak during a music session" /></div>
        <div class="card-body">
          <span class="pill pill--done">Completed &amp; closed</span>
          <h3>Learning Through Music</h3>
          <p>An audio-first music programme for children and young people with visual impairment. Listening, instrument practice, ensemble work, performance. The project period is complete and the full impact and closure report is published here.</p>
          <a href="learning-through-music.html" class="btn btn--ghost" style="margin-top:14px;">Read the closure report &rarr;</a>
        </div>
      </div>
      <div class="card">
        <div class="card-media"><img src="img/music-session-school.jpg" alt="A facilitator teaching a music session to a class of school students" /></div>
        <div class="card-body">
          <span class="pill pill--open">Seeking partners</span>
          <h3>Blind School Project</h3>
          <p>A full inclusive-education model for blind and visually impaired students: accessible learning materials, assistive technology, life skills, music and arts, sports, and career exposure. Built so that another school can run it.</p>
          <a href="blind-school-project.html" class="btn btn--ghost" style="margin-top:14px;">Read the concept note &rarr;</a>
        </div>
      </div>
    </div>
    <div class="grid" style="margin-top:28px;">
      <div class="card">
        <div class="card-body">
          <span class="pill pill--open">With government</span>
          <h3>Music Beyond Vision &amp; Art Beyond Vision</h3>
          <p>A Music and Creative Arts Club inside a government or school space, proposed to the Department of Social Welfare. The department gives a room and instructor support; we bring the curriculum, the facilitation and the artists.</p>
          <a href="music-beyond-vision.html" class="btn btn--ghost" style="margin-top:14px;">Read the proposal &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- GALLERY -->
<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">From Our Sessions</span>
    <h2>What the work actually looks like</h2>
  </div>
  <div class="container">
    <div class="gallery">
      <a href="img/harmonium-hands.jpg" target="_blank"><img src="img/harmonium-hands.jpg" alt="Children learning harmonium by touch" loading="lazy" /></a>
      <a href="img/music-class-board.jpg" target="_blank"><img src="img/music-class-board.jpg" alt="A music session at the blackboard with a keyboard" loading="lazy" /></a>
      <a href="img/community-session.jpg" target="_blank"><img src="img/community-session.jpg" alt="A community learning session with children seated on the floor" loading="lazy" /></a>
      <a href="img/blackboard-alankar.jpg" target="_blank"><img src="img/blackboard-alankar.jpg" alt="A student writing on the blackboard during a session" loading="lazy" /></a>
      <a href="img/keyboard-teaching.jpg" target="_blank"><img src="img/keyboard-teaching.jpg" alt="A facilitator teaching at the keyboard" loading="lazy" /></a>
      <a href="img/classroom-activity.jpg" target="_blank"><img src="img/classroom-activity.jpg" alt="Students working together during a classroom activity" loading="lazy" /></a>
      <a href="img/guitar-community.jpg" target="_blank"><img src="img/guitar-community.jpg" alt="A guitar session with young children in a community space" loading="lazy" /></a>
      <a href="img/fellowship-launch.jpg" target="_blank"><img src="img/fellowship-launch.jpg" alt="The Learning Through Music Fellowship launch event" loading="lazy" /></a>
    </div>
  </div>
</section>

<!-- IMPACT -->
<section class="section section--navy">
  <div class="container section-head">
    <span class="eyebrow">Our Impact</span>
    <h2>Talent is everywhere. Opportunity is not.</h2>
    <p class="lead mx-auto">Gramotsav has worked with nearly 2,000 children through its artistic, cultural, educational and community initiatives.</p>
  </div>
  <div class="container">
    <div class="impact">
      <div><div class="n">2,000+</div><div class="l">Children reached</div></div>
      <div><div class="n">100+</div><div class="l">Currently engaged</div></div>
      <div><div class="n">12</div><div class="l">Fellows, most recent project</div></div>
      <div><div class="n">10</div><div class="l">Women among those 12</div></div>
      <div><div class="n">10+</div><div class="l">Artists engaged</div></div>
      <div><div class="n">Patna</div><div class="l">Our base, in Bihar</div></div>
    </div>
    <div class="btn-row center" style="margin-top:30px;">
      <a href="impact.html" class="btn btn--light">Vision, mission and what the numbers mean &rarr;</a>
    </div>
  </div>
</section>

<!-- PARTNERS -->
<section class="section section--tight">
  <div class="container section-head" style="margin-bottom:28px;">
    <span class="eyebrow">We Work With</span>
    <h2>Partner organisations</h2>
  </div>
  <div class="container" style="max-width:1000px;">
    <div class="partners">
      <span><img src="img/partners/manzil-mystics.png" alt="Manzil Mystics Foundation" loading="lazy" /></span>
      <span><img src="img/partners/diksha.png" alt="Diksha Foundation" loading="lazy" /></span>
      <span><img src="img/partners/kilkari.png" alt="Kilkari Bihar Bal Bhavan" loading="lazy" /></span>
      <span><img src="img/partners/hhfc-trust.png" alt="HHFC Trust" loading="lazy" /></span>
      <span><img src="img/partners/kala-talks.png" alt="Kala Talks" loading="lazy" /></span>
    </div>
  </div>
</section>

<!-- REGISTRATION STRIP -->
<section class="section section--tight">
  <div class="container section-head" style="margin-bottom:26px;">
    <span class="eyebrow">Registered &amp; Compliant</span>
    <h2>Young organisation, complete paperwork</h2>
  </div>
  <div class="container" style="max-width:840px;">
    <dl class="facts">
      <div><dt>Legal form</dt><dd>Section 8 non-profit company, Companies Act 2013</dd></div>
      <div><dt>Incorporated</dt><dd>19 March 2026, Patna, Bihar</dd></div>
      <div><dt>Tax registration</dt><dd>Provisional registration granted 24 Aug 2026</dd></div>
      <div><dt>Donor deduction</dt><dd>Provisional approval granted 24 Aug 2026</dd></div>
    </dl>
    <div class="btn-row center" style="margin-top:26px;">
      <a href="transparency.html" class="btn btn--ghost">Full governance &amp; compliance detail &rarr;</a>
    </div>
  </div>
</section>
""" + CTA)

# ------------------------------------------------------------ OUR STORY ----
PAGES["our-story.html"] = dict(
    title="Our Story — Gramotsav Foundation",
    desc="Why Gramotsav Foundation exists: folk culture as a medium for inclusive learning in Bihar, our objects, values and the people behind the work.",
    body=banner("Our Story", "A five-month-old foundation in Patna, named after the day a village gathers to sing.") + """
<section class="section">
  <div class="container prose">
    <span class="eyebrow">The Idea</span>
    <h2>Gramotsav means the festival of the village</h2>
    <p>In rural Bihar the <em>gramotsav</em> is the day the whole gaon turns out. People sing, people perform, and the old stories get handed down one more time. It is also where a good many children first find out they have something worth saying out loud.</p>
    <p>We think that is roughly how children learn best too. Not sitting still while a syllabus is read at them, but inside something that is actually happening: a lok geet they can join, a taal they can hold on to.</p>
    <p>We were incorporated as a Section 8 non-profit company in Patna on 19 March 2026. We are small and we intend to stay specific. Folk culture, inclusive education, and a route from creative skill towards a living: that is the whole remit, and we write every programme up so another organisation could run it without us.</p>

    <h3>What we set out to do</h3>
    <p>Our founding objects, as registered in our Memorandum of Association, are:</p>
    <ul>
      <li>To preserve, promote and revitalise the folk traditions and cultural heritage of rural and indigenous Indian communities, and build awareness and appreciation for them across diverse communities.</li>
      <li>To design and implement programmes for holistic development through inclusive platforms that strengthen traditional cultural identity and practices.</li>
      <li>To collaborate with indigenous communities and relevant institutions to integrate arts and culture into educational programmes, fostering holistic wellbeing.</li>
      <li>To promote gender equality by establishing institutional resource centres and community spaces that host educational and cultural activities.</li>
    </ul>
  </div>
</section>

<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">How We Work</span>
    <h2>Five commitments we hold ourselves to</h2>
  </div>
  <div class="container" style="max-width:900px;">
    <div class="steps">
      <div class="step"><div class="step-num">1</div><div>
        <h3>Accessibility is designed in, not added later</h3>
        <p>If a method only works for a child who can see the page, it is not our method. Accessibility shapes the teaching from the first baithak onward.</p>
      </div></div>
      <div class="step"><div class="step-num">2</div><div>
        <h3>Children create, they do not only consume</h3>
        <p>A room is only a creative space if the young people in it are making something. Ours are built around riyaz, improvisation, and performances the students put together themselves.</p>
      </div></div>
      <div class="step"><div class="step-num">3</div><div>
        <h3>We teach the songs that are already here</h3>
        <p>Bhojpuri, Maithili and Magahi traditions, folk instruments, festival songs, oral storytelling. That is the material we teach with. A child who ends up proud of where they come from has learned something worth having.</p>
      </div></div>
      <div class="step"><div class="step-num">4</div><div>
        <h3>We say what music can and cannot get you</h3>
        <p>We promise nobody employment. We do lay out the actual routes: performance, teaching, ensemble work, recording, running something of your own. And we start that conversation while the riyaz is still going on, not once it is over.</p>
      </div></div>
      <div class="step"><div class="step-num">5</div><div>
        <h3>We document so others can copy us</h3>
        <p>Every project ends in a written record: what we did, how it went, what we got wrong. Our closure reports go up on this site where anyone can read them.</p>
      </div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items:center;">
      <div class="story-media"><img src="img/community-event.jpg" alt="Families and children gathered at a community cultural event" /></div>
      <div>
        <span class="eyebrow">Where We Work</span>
        <h2>Patna, and the districts around it</h2>
        <p>Our registered office is in Patna, and sessions run in schools, special schools and community learning spaces around the city. Bihar has a folk tradition that is still very much alive and a serious shortage of accessible education. We work in the space between those two facts.</p>
        <p style="margin-top:14px;">We start inside institutions that already exist. It gets material to students faster, it builds up the teachers who are already in the room, and nothing collapses the day a grant ends.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="container">
    <p class="pull" style="color:#fff;">Listening comes first. Wanting to try comes next. After that it is riyaz, and riyaz is mostly repetition, and repetition is where the confidence actually comes from.</p>
  </div>
</section>
""" + CTA)

# ----------------------------------------------------------- PROGRAMMES ----
PAGES["programmes.html"] = dict(
    title="Programmes — Gramotsav Foundation",
    desc="Gramotsav Foundation's programmes: Learning Through Music (completed), the Blind School Project (seeking partners), and our folk culture and community work in Bihar.",
    body=banner("Programmes", "Three projects and one method. Each of them runs from mitti to manch, along the same arc.") + """
<section class="section">
  <div class="container section-head">
    <span class="eyebrow">The Method</span>
    <h2>One learning arc, applied everywhere</h2>
    <p class="lead mx-auto">We do not run a scatter of activities. Each programme moves a learner along the same sequence, and how far along that sequence a young person gets is how we measure it.</p>
  </div>
  <div class="container">""" + JOURNEY + """</div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="story">
      <div class="story-media"><img src="img/harmonium-dholak.jpg" alt="Students seated around a harmonium and dholak in a music session" /></div>
      <div>
        <span class="pill pill--done">Completed &amp; closed</span>
        <h3>Learning Through Music</h3>
        <p class="kicker">Audio-first music education</p>
        <p style="margin-top:12px;">An inclusive creative learning programme for children and young people with visual impairment. Instrument instruction did not depend on Braille notation. Students learned through guided listening, audio demonstration, spoken instruction, repetition, rhythmic cues, musical memory and hands-on practice, moving from solo riyaz into ensemble and band work.</p>
        <p style="margin-top:12px;">The project period is complete. The full impact and closure report is on this site: approach, journey, outcomes, key learnings and legacy.</p>
        <a href="learning-through-music.html" class="btn btn--ghost" style="margin-top:16px;">Read the closure report &rarr;</a>
      </div>
    </div>

    <div class="story">
      <div class="story-media"><img src="img/classroom-activity.jpg" alt="Students working together during an inclusive classroom activity" /></div>
      <div>
        <span class="pill pill--open">Seeking partners</span>
        <h3>Blind School Project</h3>
        <p class="kicker">Inclusive education, end to end</p>
        <p style="margin-top:12px;">A model for blind and visually impaired students that reaches past classroom support: accessible academic material, assistive technology and digital literacy, mobility and independent-living skills, music and the arts, sports and wellbeing, career and vocational exposure, with parent, teacher and community engagement around all of it.</p>
        <p style="margin-top:12px;">Eight phases over a first year, with a defined monitoring framework and an explicit sustainability strategy, so a school, NGO or CSR partner can take the model on instead of depending on us to run it forever.</p>
        <a href="blind-school-project.html" class="btn btn--ghost" style="margin-top:16px;">Read the concept note &rarr;</a>
      </div>
    </div>

    <div class="story">
      <div class="story-media"><img src="img/keyboard-teaching.jpg" alt="A facilitator teaching a music session at the keyboard" /></div>
      <div>
        <span class="pill pill--open">With government</span>
        <h3>Music Beyond Vision &amp; Art Beyond Vision</h3>
        <p class="kicker">A club inside a government space</p>
        <p style="margin-top:12px;">A Music and Creative Arts Club for children and young people with visual impairment, proposed to the Department of Social Welfare. The department provides a room, whatever instruments exist, and instructor honorarium support. We bring the audio-first curriculum, the facilitation, the artists, the band work and the documentation.</p>
        <p style="margin-top:12px;">Twelve months, from setting up the room to mapping out where each student could go next. Built on infrastructure the institution already has, so it does not fall over when a grant ends.</p>
        <a href="music-beyond-vision.html" class="btn btn--ghost" style="margin-top:16px;">Read the proposal &rarr;</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container section-head">
    <span class="eyebrow">Running Through Both</span>
    <h2>Folk culture and community practice</h2>
    <p class="lead mx-auto">The cultural work runs through both projects. It is the material we teach with, and it also stands on its own in community settings.</p>
  </div>
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="card-media ph-4" style="height:170px;font-size:3rem;">&#9834;</div>
        <div class="card-body">
          <span class="card-tag">Repertoire</span>
          <h3>Regional song traditions</h3>
          <p>Bhojpuri, Maithili and Magahi lok geet, festival and community music, folk and traditional instruments, and Indian classical foundations where appropriate.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media ph-3" style="height:170px;font-size:3rem;">&#128172;</div>
        <div class="card-body">
          <span class="card-tag">Oral tradition</span>
          <h3>Storytelling &amp; expression</h3>
          <p>Spoken expression, oral storytelling and musical memory. This is how most of the material got here in the first place: mouth to ear, guru to shishya.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-media ph-6" style="height:170px;font-size:3rem;">&#127914;</div>
        <div class="card-body">
          <span class="card-tag">Performance</span>
          <h3>Community stages</h3>
          <p>Public performance is a step in the method rather than a showcase bolted on at the end. Standing on a manch in front of people is where the confidence gets built.</p>
        </div>
      </div>
    </div>
  </div>
</section>
""" + CTA)

# ------------------------------------------------- LEARNING THROUGH MUSIC --
PAGES["learning-through-music.html"] = dict(
    title="Learning Through Music — Impact & Closure Report | Gramotsav Foundation",
    desc="The full impact and closure report for Gramotsav Foundation's Learning Through Music project — an audio-first music programme for children with visual impairment in Bihar.",
    body=banner("Learning Through Music", "Final impact &amp; closure report. An audio-first music programme for children and young people with visual impairment.") + """
<section class="section">
  <div class="container prose">
    <span class="pill pill--done">Project completed and formally closed</span>
    <h2>Project closure statement</h2>
    <p>The Learning Through Music project has been completed and formally closed. This page is the public version of its final documentation: purpose, approach, implementation experience, learning journey and key outcomes.</p>
    <p>The project started from one idea: that music can be more than a subject on a timetable. It can carry learning, confidence, expression, collaboration, cultural connection, and a route towards a livelihood.</p>

    <h3>Vision</h3>
    <p>To create an inclusive creative learning environment where children and young people with visual impairment can discover music, learn through an audio-first approach, express themselves, collaborate with peers, connect with their cultural roots, and develop confidence and skill.</p>

    <h3>Objectives</h3>
    <ul>
      <li>Create an accessible and welcoming space for learning through music.</li>
      <li>Use an audio-first approach for music and instrument instruction.</li>
      <li>Encourage children to discover and develop their musical interests.</li>
      <li>Build confidence, communication, teamwork and creative expression.</li>
      <li>Create opportunities for group music-making and student bands.</li>
      <li>Connect learners with regional, folk and Indian musical traditions.</li>
      <li>Provide exposure to performance and professional creative environments.</li>
      <li>Introduce music as a possible pathway towards future livelihood.</li>
    </ul>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="container section-head" style="margin-bottom:28px;">
    <span class="eyebrow">The Philosophy</span>
    <h2><span class="devnagri">मिट्टी से मंच तक</span></h2>
    <p class="lead mx-auto">From a learner's own roots and first encounter with music, to the confidence of standing on a stage.</p>
  </div>
  <div class="container">""" + JOURNEY + """</div>
</section>

<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">The Approach</span>
    <h2 style="margin-bottom:22px;">Audio-first, not notation-dependent</h2>
    <p class="lead" style="margin-bottom:26px;">Instrument instruction was not dependent on Braille notation. Students learned through listening, spoken explanation, audio demonstration, repetition, verbal cues, rhythm patterns, musical memory and guided hands-on practice.</p>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Learning method</th><th>How it was used</th></tr></thead>
        <tbody>
          <tr><td><strong>Listening</strong></td><td>Students developed musical awareness through guided listening and audio examples.</td></tr>
          <tr><td><strong>Audio demonstration</strong></td><td>Musical and instrumental patterns were demonstrated through sound.</td></tr>
          <tr><td><strong>Verbal instruction</strong></td><td>Facilitators explained techniques and sequences through spoken instruction.</td></tr>
          <tr><td><strong>Repetition</strong></td><td>Patterns and exercises were repeated to support memory and confidence.</td></tr>
          <tr><td><strong>Rhythm &amp; cues</strong></td><td>Verbal and rhythmic cues supported timing and coordination.</td></tr>
          <tr><td><strong>Hands-on practice</strong></td><td>Students learned by practising instruments and musical exercises directly.</td></tr>
          <tr><td><strong>Group learning</strong></td><td>Students learned with peers through shared practice and musical interaction.</td></tr>
          <tr><td><strong>Performance</strong></td><td>Practical performance provided a natural way to demonstrate learning.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">The Journey</span>
    <h2 style="margin-bottom:22px;">Day one to impact</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Stage</th><th>What happened</th></tr></thead>
        <tbody>
          <tr><td><strong>Day one</strong></td><td>Welcome, listening, rhythm activities, discovery of musical interests and orientation.</td></tr>
          <tr><td><strong>Discovery</strong></td><td>Students explored music, voice, rhythm and the available instruments.</td></tr>
          <tr><td><strong>Learning</strong></td><td>Students began structured audio-based musical learning.</td></tr>
          <tr><td><strong>Practice</strong></td><td>Regular practice built familiarity, memory and confidence.</td></tr>
          <tr><td><strong>Collaboration</strong></td><td>Students participated in shared musical activities and ensemble learning.</td></tr>
          <tr><td><strong>Creation</strong></td><td>The programme created space for creative expression and musical ideas.</td></tr>
          <tr><td><strong>Band / ensemble</strong></td><td>Students worked together and developed group performance skills.</td></tr>
          <tr><td><strong>Performance</strong></td><td>Learning moved towards public expression and performance opportunities.</td></tr>
          <tr><td><strong>Impact</strong></td><td>Strengthened confidence, participation, creativity and future possibilities.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="story">
      <div class="story-media"><img src="img/harmonium-hands.jpg" alt="Children gathered around a harmonium, learning through touch and sound" /></div>
      <div>
        <span class="kicker">Connecting with our roots</span>
        <h3>The repertoire was local on purpose</h3>
        <p style="margin-top:12px;">Part of the point was to tie the learning to where the students actually come from. The sounds in the room were the sounds of their own communities, and the material carried India's oral and musical heritage with it: Bhojpuri, Maithili, Magahi and related traditions; traditional and folk instruments; festival and community songs; oral storytelling; Indian classical music; and folk material given contemporary interpretation.</p>
      </div>
    </div>
    <div class="story">
      <div class="story-media"><img src="img/harmonium-dholak.jpg" alt="A group music session with harmonium and dholak" /></div>
      <div>
        <span class="kicker">Bands &amp; collaboration</span>
        <h3>From individual skill to a group that needs you</h3>
        <p style="margin-top:12px;">The aim was to move students out of solo practice and into playing with other people. Playing together, whether that is two students trading phrases in a jugalbandi or a full band, gives you a reason to listen to somebody else, to hold your own part, and to turn up for rehearsal because others are waiting. Students identified shared musical interests, formed small groups, took on roles, developed a shared repertoire, and built confidence through collective performance.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Impact Framework</span>
    <h2 style="margin-bottom:22px;">What the project set out to move, and where</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Area</th><th>Impact intended / observed through the project</th></tr></thead>
        <tbody>
          <tr><td><strong>Access</strong></td><td>An audio-based approach made music learning more accessible.</td></tr>
          <tr><td><strong>Learning</strong></td><td>Students engaged with music through listening, demonstration and practice.</td></tr>
          <tr><td><strong>Confidence</strong></td><td>Performance and group participation created opportunities for self-expression.</td></tr>
          <tr><td><strong>Collaboration</strong></td><td>Ensemble and band activities promoted teamwork.</td></tr>
          <tr><td><strong>Creativity</strong></td><td>Students were encouraged to create, interpret and express.</td></tr>
          <tr><td><strong>Culture</strong></td><td>Music provided a connection to regional and Indian traditions.</td></tr>
          <tr><td><strong>Opportunity</strong></td><td>Performance and professional exposure introduced future possibilities.</td></tr>
          <tr><td><strong>Livelihood</strong></td><td>The project established a conceptual pathway from musical skill to creative opportunity.</td></tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:18px;font-size:.95rem;color:var(--muted);">Outcomes for this project are documented qualitatively. Quantitative enrolment, attendance and skills-progression indicators are built into the monitoring framework of the <a href="blind-school-project.html">Blind School Project</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <span class="eyebrow">What We Learned</span>
    <h2>Eight key learnings</h2>
    <ul>
      <li><strong>Accessibility should be built into the teaching method from the beginning</strong>, not retro-fitted once the method already exists.</li>
      <li><strong>Audio can be a powerful primary medium</strong> for music and instrument instruction, not merely a support for it.</li>
      <li><strong>Students benefit when learning is practical, participatory and experience-based.</strong></li>
      <li><strong>A creative space becomes more meaningful when students can create</strong>, not only consume, content.</li>
      <li><strong>Group music bridges individual skill and social participation.</strong></li>
      <li><strong>Cultural learning becomes stronger when local artists, traditions and lived experience are included.</strong></li>
      <li><strong>Performance is an important milestone</strong> in building confidence and ownership.</li>
      <li><strong>Livelihood thinking should begin during skill development</strong>, rather than only after training is complete.</li>
    </ul>

    <h3>Challenges</h3>
    <p>Implementation had to bend around individual learning needs, the resources on hand, how consistently students could keep up their riyaz, and what chances there were to carry on afterwards. What it confirmed: teaching has to stay flexible, mentoring has to be patient, resources have to be accessible, and students need real occasions to show what they can do.</p>

    <h3>Legacy</h3>
    <p>What lasts is the idea of a room where children with visual impairment are known for their talent and their creativity. The shift the project was after: from children as recipients of support, to children as musicians, creators, performers and potential professionals.</p>

    <div class="note" style="margin-top:32px;">
      <strong>On how we document students.</strong> Our preferred approach for future documentation is to capture a student's journey through audio, photographs or video where appropriate, facilitator observations, performance records and student reflections &mdash; keeping the focus on agency, achievement and growth, rather than presenting disability only through limitation.
    </div>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="container">
    <p class="pull" style="color:#fff;">From mitti to manch. That is the whole of it.</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h3>Acknowledgement</h3>
    <p>Gramotsav Foundation acknowledges the students, families, facilitators, mentors, partner institutions, artists and supporters whose participation made the Learning Through Music project possible.</p>
  </div>
</section>
""" + CTA)

# ------------------------------------------------- BLIND SCHOOL PROJECT ----
PAGES["blind-school-project.html"] = dict(
    title="Blind School Project — Concept Note | Gramotsav Foundation",
    desc="Gramotsav Foundation's Blind School Project: an inclusive education model for blind and visually impaired students in Bihar — accessible learning, assistive technology, life skills, music, sports and livelihood. Seeking CSR and institutional partners.",
    body=banner("Blind School Project", "An inclusive education, skills and assistive-technology model for children and young people who are blind or visually impaired.") + """
<section class="section">
  <div class="container prose">
    <span class="pill pill--open">Concept note &middot; seeking partners</span>
    <h2>Executive summary</h2>
    <p>The Blind School Project is an inclusive education and development initiative designed to create a safe, accessible and empowering learning environment for children and young people who are blind or visually impaired.</p>
    <p>It puts more around a student than classroom teaching on its own: accessible academic learning, life skills, digital literacy, assistive technology, music and the arts, vocational exposure, confidence building and community participation.</p>
    <p>The long-term aim is students who are more independent, more confident, and more active economically and socially, and a model of inclusive education that schools, NGOs, communities and institutional partners can pick up and run.</p>

    <h3>Why this project is needed</h3>
    <ul>
      <li>Blind and visually impaired students face barriers in accessing conventional textbooks, digital content and classroom resources.</li>
      <li>Accessible learning materials (Braille, audio resources, screen-reader compatible content) are often limited or expensive.</li>
      <li>Education alone is not sufficient: students also need mobility, communication, digital and independent-living skills.</li>
      <li>Exposure to music, theatre, arts, sports and cultural activity strengthens confidence, expression, social participation and belonging.</li>
      <li>Career guidance, vocational exposure and digital skills improve future livelihood opportunities.</li>
      <li>Families and communities need awareness and practical support to build an inclusive environment around the student.</li>
    </ul>
  </div>
</section>

<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">What the Project Provides</span>
    <h2>Six components, one student</h2>
  </div>
  <div class="container">
    <div class="grid grid-3">
      <div class="card"><div class="card-body">
        <span class="card-tag">A</span><h3>Accessible education</h3>
        <p>Braille and tactile learning materials, audio lessons and recorded resources, accessible worksheets and examinations, and individualised learning support.</p>
      </div></div>
      <div class="card"><div class="card-body">
        <span class="card-tag">B</span><h3>Digital &amp; assistive technology</h3>
        <p>Computer and smartphone literacy, screen readers and accessibility tools, Braille displays and keyboards where appropriate, online learning and safe internet use.</p>
      </div></div>
      <div class="card"><div class="card-body">
        <span class="card-tag">C</span><h3>Life skills &amp; independence</h3>
        <p>Personal organisation and daily living, communication and social skills, orientation and mobility awareness, and practical financial and digital skills.</p>
      </div></div>
      <div class="card"><div class="card-body">
        <span class="card-tag">D</span><h3>Music, arts &amp; culture</h3>
        <p>Singing and instrumental music, taal and voice training, theatre and storytelling, and creative expression at cultural events.</p>
      </div></div>
      <div class="card"><div class="card-body">
        <span class="card-tag">E</span><h3>Sports &amp; well-being</h3>
        <p>Accessible physical activity, yoga and movement, games adapted for visual impairment, and attention to mental well-being and peer interaction.</p>
      </div></div>
      <div class="card"><div class="card-body">
        <span class="card-tag">F</span><h3>Career &amp; livelihood</h3>
        <p>Career awareness, digital and vocational skills, mentorship by professionals, and exposure to employment and entrepreneurship opportunities.</p>
      </div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Implementation</span>
    <h2 style="margin-bottom:22px;">Eight phases</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Phase</th><th>Key activities</th></tr></thead>
        <tbody>
          <tr><td><strong>1 &middot; Need assessment</strong></td><td>Identify students, existing facilities, learning gaps, accessibility barriers and family needs.</td></tr>
          <tr><td><strong>2 &middot; Baseline assessment</strong></td><td>Document academic, digital, mobility, communication and life-skill levels of participating students.</td></tr>
          <tr><td><strong>3 &middot; Resource development</strong></td><td>Provide Braille and audio materials, devices, software, tactile resources and other learning aids.</td></tr>
          <tr><td><strong>4 &middot; Training</strong></td><td>Train teachers, facilitators, volunteers and students in accessible learning and assistive technology.</td></tr>
          <tr><td><strong>5 &middot; Regular programme</strong></td><td>Run academic support, digital literacy, life skills, music and arts, sports and career activities.</td></tr>
          <tr><td><strong>6 &middot; Mentoring &amp; exposure</strong></td><td>Connect students with professionals, artists, institutions and role models.</td></tr>
          <tr><td><strong>7 &middot; Monitoring</strong></td><td>Track attendance, participation, learning progress, skills and student feedback.</td></tr>
          <tr><td><strong>8 &middot; Scale &amp; sustainability</strong></td><td>Build institutional partnerships, CSR support and a replicable programme model.</td></tr>
        </tbody>
      </table>
    </div>

    <h2 style="margin:46px 0 22px;">Indicative first-year plan</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Period</th><th>Focus</th><th>Illustrative activities</th></tr></thead>
        <tbody>
          <tr><td>Months 1&ndash;2</td><td><strong>Assessment &amp; setup</strong></td><td>Baseline, student mapping, resource audit, procurement and orientation</td></tr>
          <tr><td>Months 3&ndash;4</td><td><strong>Accessible learning</strong></td><td>Braille and audio resources, digital basics, teacher support</td></tr>
          <tr><td>Months 5&ndash;6</td><td><strong>Life skills</strong></td><td>Communication, independence, mobility and practical skills</td></tr>
          <tr><td>Months 7&ndash;8</td><td><strong>Arts &amp; music</strong></td><td>Music classes, theatre, creative sessions and performances</td></tr>
          <tr><td>Months 9&ndash;10</td><td><strong>Technology &amp; career</strong></td><td>Advanced digital skills, career exposure and mentorship</td></tr>
          <tr><td>Months 11&ndash;12</td><td><strong>Showcase &amp; evaluation</strong></td><td>Student showcase, assessment, documentation and next-year planning</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Measurement</span>
    <h2 style="margin-bottom:18px;">How we will know it worked</h2>
    <div class="grid grid-2" style="gap:20px;">
      <div class="note">
        <strong>Participation &amp; retention</strong>
        <ul style="margin:10px 0 0 20px;">
          <li>Students enrolled and regularly participating</li>
          <li>Attendance and retention</li>
          <li>Participation in music, arts, sports and cultural activity</li>
        </ul>
      </div>
      <div class="note">
        <strong>Skills &amp; independence</strong>
        <ul style="margin:10px 0 0 20px;">
          <li>Improvement in academic and digital skills</li>
          <li>Students using assistive technology independently</li>
          <li>Life-skill and confidence assessments</li>
        </ul>
      </div>
      <div class="note">
        <strong>Evidence &amp; feedback</strong>
        <ul style="margin:10px 0 0 20px;">
          <li>Parent and teacher feedback</li>
          <li>Student portfolios and documented achievements</li>
        </ul>
      </div>
      <div class="note">
        <strong>Opportunity created</strong>
        <ul style="margin:10px 0 0 20px;">
          <li>External exposure, mentorship and career opportunities generated for students</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Budget Structure</span>
    <h2 style="margin-bottom:22px;">Where funding goes</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Budget head</th><th>Examples</th></tr></thead>
        <tbody>
          <tr><td><strong>Learning materials</strong></td><td>Braille books, tactile resources, audio content, stationery</td></tr>
          <tr><td><strong>Assistive technology</strong></td><td>Computers, screen-reader software, headphones, Braille devices</td></tr>
          <tr><td><strong>Human resources</strong></td><td>Special educators, facilitators, trainers, counsellors</td></tr>
          <tr><td><strong>Music &amp; arts</strong></td><td>Instruments, teaching materials, recording and performance support</td></tr>
          <tr><td><strong>Accessibility</strong></td><td>Signage, pathways, furniture and accessible infrastructure</td></tr>
          <tr><td><strong>Student activities</strong></td><td>Exposure visits, workshops and events</td></tr>
          <tr><td><strong>Monitoring &amp; documentation</strong></td><td>Assessments, reports, photography and video, impact documentation</td></tr>
          <tr><td><strong>Administration</strong></td><td>Communication, transport, utilities and programme coordination</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note" style="margin-top:22px;">
      <strong>Costed budget available on request.</strong> A line-item budget is prepared per site, because cost depends on student numbers, the host institution's existing facilities and the assistive-technology specification agreed with the partner. <a href="contact.html">Write to us</a> and we will send a costed proposal.
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Risk</span>
    <h2 style="margin-bottom:22px;">What could go wrong, and what we do about it</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Potential risk</th><th>Mitigation</th></tr></thead>
        <tbody>
          <tr><td>Limited resources</td><td>Phased implementation and diversified funding</td></tr>
          <tr><td>Low technology familiarity</td><td>Hands-on training and ongoing technical support</td></tr>
          <tr><td>Irregular participation</td><td>Family engagement, mentoring and student-centred activities</td></tr>
          <tr><td>Lack of trained staff</td><td>Capacity building and specialist partnerships</td></tr>
          <tr><td>Sustainability after funding</td><td>Institutional integration and multi-year partnerships</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <span class="eyebrow">Theory of Change</span>
    <h2>The logic, in one sentence</h2>
    <p class="lead">If blind and visually impaired students receive accessible education, appropriate technology, life skills, creative opportunities, mentorship and a supportive environment, then their confidence, independence, learning outcomes and participation can improve &mdash; contributing to greater educational, social and livelihood opportunity.</p>

    <h3>Sustainability</h3>
    <p>The project is designed so its impact continues beyond a single funding cycle: institutional ownership by the host school, trained teachers and facilitators, reusable accessible learning resources, long-term CSR partnerships, volunteer networks, student showcases and documented outcomes.</p>

    <h3>Who we want to work with</h3>
    <ul>
      <li>Corporate CSR partners</li>
      <li>Individual donors and philanthropic foundations</li>
      <li>Educational institutions and universities</li>
      <li>Assistive-technology companies</li>
      <li>Music, arts and cultural organisations</li>
      <li>Government and local institutional partners</li>
      <li>Volunteer networks and professional mentors</li>
    </ul>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="container">
    <p class="pull" style="color:#fff;max-width:30ch;">Every child deserves a chance to learn, grow and perform.</p>
  </div>
</section>
""" + CTA)

# --------------------------------------------------------------- SUPPORT ---
PAGES["support.html"] = dict(
    title="Partner & Support — Gramotsav Foundation",
    desc="Support Gramotsav Foundation: CSR partnership on the Blind School Project, programme sponsorship, in-kind giving of instruments and assistive technology, and volunteering in Patna.",
    body=banner("Partner &amp; Support", "Five months old, one project finished and documented, registration complete. Here is where support actually lands.") + """
<section class="section">
  <div class="container section-head">
    <span class="eyebrow">Ways to Help</span>
    <h2>Four ways to work with us</h2>
    <p class="lead mx-auto">We would rather have one partner who stays for three years than ten who stay for one. Each of these routes is designed around that.</p>
  </div>
  <div class="container">
    <div class="grid grid-2">
      <div class="tier featured">
        <div class="amt">CSR</div>
        <div class="per">Corporate social responsibility partnership</div>
        <ul>
          <li>Fund the Blind School Project at one site, end to end</li>
          <li>Named multi-year partnership with defined milestones</li>
          <li>Quarterly narrative and financial reporting</li>
          <li>Employee volunteering and mentorship opportunities</li>
          <li>Section 8 company, so the structure is CSR-eligible</li>
        </ul>
        <a href="contact.html" class="btn btn--primary">Request a costed proposal</a>
      </div>
      <div class="tier">
        <div class="amt">Programme</div>
        <div class="per">Sponsor a music or arts cohort</div>
        <ul>
          <li>Support one cohort of learners for a full session cycle</li>
          <li>Covers facilitator time, instruments and materials</li>
          <li>Ends in a student showcase you are invited to</li>
          <li>Documented outcomes and student portfolios</li>
        </ul>
        <a href="contact.html" class="btn btn--ghost">Talk to us</a>
      </div>
      <div class="tier">
        <div class="amt">In kind</div>
        <div class="per">Instruments, devices and expertise</div>
        <ul>
          <li>Musical instruments: harmonium, dholak, tabla, keyboard, guitar</li>
          <li>Screen-reader enabled computers and smartphones</li>
          <li>Braille displays, keyboards and tactile materials</li>
          <li>Audio recording and playback equipment</li>
          <li>Pro-bono accessibility or assistive-tech expertise</li>
        </ul>
        <a href="contact.html" class="btn btn--ghost">Offer support in kind</a>
      </div>
      <div class="tier" id="volunteer">
        <div class="amt">Time</div>
        <div class="per">Volunteer with us in Patna</div>
        <ul>
          <li>Music facilitators and practising artists</li>
          <li>Special educators and accessibility specialists</li>
          <li>Digital literacy and assistive-technology trainers</li>
          <li>Career mentors from any profession</li>
          <li>Documentation, photography and writing</li>
        </ul>
        <a href="contact.html" class="btn btn--ghost">Volunteer</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:820px;">
    <span class="eyebrow">Giving &amp; Tax</span>
    <h2 style="margin-bottom:18px;">What a donor should know</h2>
    <p class="lead" style="margin-bottom:22px;">Gramotsav Foundation is a Section 8 non-profit company. Our registration and our donor-deduction approval under the Income-tax Act are provisional, granted 24 August 2026 and valid to TY 2028-29. Eligible donations attract a tax deduction and we can issue you a receipt.</p>
    <div class="note">
      <strong>Before you transfer funds.</strong> Please write to us first at <a href="mailto:gramotsavfoundation@gmail.com">gramotsavfoundation@gmail.com</a>. We will send our banking details directly, along with our registration certificates and the receipt format. We do not publish account details on this website, and you should be wary of anyone who does.
    </div>
    <p style="margin-top:22px;font-size:.95rem;color:var(--muted);">Full registration numbers and governance detail are on our <a href="transparency.html">governance and compliance page</a>. We do not currently hold FCRA registration and therefore cannot accept foreign contributions.</p>
  </div>
</section>

<section class="section">
  <div class="container section-head">
    <span class="eyebrow">Our Commitment</span>
    <h2>What you get back from us</h2>
  </div>
  <div class="container" style="max-width:900px;">
    <div class="steps">
      <div class="step"><div class="step-num">&#10003;</div><div>
        <h3>Written policies, already adopted</h3>
        <p>Finance, procurement, travel and PoSH policies have been in force since 1 April 2026. They were written before anyone asked to see them.</p>
      </div></div>
      <div class="step"><div class="step-num">&#10003;</div><div>
        <h3>Reporting on your cycle, not ours</h3>
        <p>Narrative and financial reporting in your format and to your timetable, with photographs and student documentation.</p>
      </div></div>
      <div class="step"><div class="step-num">&#10003;</div><div>
        <h3>A public closure report</h3>
        <p>When a project ends we publish what worked, what did not, and what we learned. Our <a href="learning-through-music.html">first closure report</a> is already online.</p>
      </div></div>
      <div class="step"><div class="step-num">&#10003;</div><div>
        <h3>A model you can hand on</h3>
        <p>Everything is designed to be adopted by the host institution, so your funding builds capacity that outlasts the grant.</p>
      </div></div>
    </div>
  </div>
</section>
""" + CTA)

# ---------------------------------------------------------- TRANSPARENCY ---
PAGES["transparency.html"] = dict(
    title="Governance & Compliance — Gramotsav Foundation",
    desc="Gramotsav Foundation's registration, governance and compliance: Section 8 company details, CIN, tax registrations, and adopted finance, procurement, travel and PoSH policies.",
    body=banner("Governance &amp; Compliance", "Registration details, adopted policies and how we handle money. Published so that a funder does not have to ask.") + """
<section class="section">
  <div class="container" style="max-width:860px;">
    <span class="eyebrow">Legal Status</span>
    <h2 style="margin-bottom:22px;">Registration</h2>
    <dl class="facts">
      <div><dt>Registered name</dt><dd>Gramotsav Foundation</dd></div>
      <div><dt>Legal form</dt><dd>Company limited by shares, licensed under Section 8 of the Companies Act, 2013</dd></div>
      <div><dt>Date of incorporation</dt><dd>19 March 2026</dd></div>
      <div><dt>Corporate Identity Number</dt><dd>U88900BR2026NPL083562</dd></div>
      <div><dt>Section 8 licence number</dt><dd>182161</dd></div>
      <div><dt>Registering authority</dt><dd>Registrar of Companies, Central Registration Centre</dd></div>
      <div><dt>Registered office</dt><dd>C/o Suraj Kumar, A. K. Road, Machuatoli, Patna Sadar, Patna &ndash; 800016, Bihar</dd></div>
      <div><dt>Financial year</dt><dd>1 April to 31 March</dd></div>
    </dl>

    <h2 style="margin:44px 0 22px;">Tax registration</h2>
    <dl class="facts">
      <div><dt>Permanent Account Number (PAN)</dt><dd>AAMCG9005G</dd></div>
      <div><dt>Provisional registration (s.332)</dt><dd>URN AAMCG9005GE20261</dd></div>
      <div><dt>Provisional approval &mdash; donor deduction (s.354)</dt><dd>URN AAMCG9005GF20261</dd></div>
      <div><dt>Date granted</dt><dd>24 August 2026</dd></div>
      <div><dt>Valid for</dt><dd>TY 2026-27 to TY 2028-29</dd></div>
      <div><dt>Nature of activities</dt><dd>Charitable</dd></div>
      <div><dt>Foreign contribution (FCRA)</dt><dd>Not registered &mdash; we cannot accept foreign contributions</dd></div>
    </dl>
    <p style="margin-top:16px;font-size:.95rem;color:var(--muted);">Our PAN is published here because an Indian donor needs it to claim the deduction. Our TAN and our bank details are not published on this website; we send those directly. Certified copies of the certificate of incorporation, Section 8 licence, memorandum and articles of association, and tax registration orders go to prospective partners on request as part of due diligence.</p>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:860px;">
    <span class="eyebrow">Adopted Policies</span>
    <h2 style="margin-bottom:22px;">Four policies, in force since 1 April 2026</h2>
    <div class="grid grid-2" style="gap:20px;">
      <div class="note">
        <strong>Finance policy</strong>
        <p style="margin-top:8px;">Project and annual budgeting approved by the Board; monthly expenditure statements by the 5th; project-wise accounts and bank reconciliation; voucher management and advance control; salary and payment discipline.</p>
      </div>
      <div class="note">
        <strong>Procurement policy</strong>
        <p style="margin-top:8px;">Cash procurement prohibited at every level. Under &#8377;10,000: Director informed in advance. &#8377;10,000&ndash;&#8377;25,000: three quotations and Board approval in writing. Above &#8377;25,000: a Board-approved Purchase Committee, three quotations and full documentation.</p>
      </div>
      <div class="note">
        <strong>Travel policy</strong>
        <p style="margin-top:8px;">Prior approval for all official travel; published per-kilometre rates; original receipts and organisational expense formats; mandatory travel insurance; conduct and cultural-sensitivity standards.</p>
      </div>
      <div class="note">
        <strong>PoSH policy</strong>
        <p style="margin-top:8px;">Prevention, prohibition and redressal of sexual harassment at the workplace, under the 2013 Act and Rules. Zero tolerance, protection against retaliation, and coverage of all employees, members, volunteers and third parties on our premises.</p>
      </div>
    </div>
    <p style="margin-top:20px;font-size:.95rem;color:var(--muted);">Full policy documents are shared with partners, staff and volunteers, and provided on request during due diligence.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:820px;">
    <span class="eyebrow">Money</span>
    <h2 style="margin-bottom:18px;">How we handle funds</h2>
    <ul style="margin-left:20px;">
      <li style="margin-bottom:9px;">All expenditure runs against a budget approved by the Board of Directors.</li>
      <li style="margin-bottom:9px;">No cash procurement, at any level, for any amount.</li>
      <li style="margin-bottom:9px;">Monthly project-wise accounts, fund position and bank reconciliation to the Board by the 5th.</li>
      <li style="margin-bottom:9px;">Advances are settled before the next advance is released.</li>
      <li style="margin-bottom:9px;">Director and member reimbursements require Board approval, not a Director's own sign-off.</li>
      <li style="margin-bottom:9px;">Regular audit against the procurement policy, and annual statutory audit.</li>
    </ul>
    <div class="note" style="margin-top:24px;">
      <strong>A note on donations.</strong> We do not publish bank account details on this website. If you intend to give, please email us first and we will send our banking details, registration certificates and receipt format directly. Treat any account details for &ldquo;Gramotsav Foundation&rdquo; that reach you by any other route as suspect until you have confirmed them with us.
    </div>
  </div>
</section>

<section class="section section--soft section--tight">
  <div class="container" style="max-width:820px;">
    <div class="note">
      <strong>Reporting a concern.</strong> If you have a concern about our conduct, finances or safeguarding, whether you are a student, parent, staff member, volunteer or partner, write to <a href="mailto:gramotsavfoundation@gmail.com">gramotsavfoundation@gmail.com</a> marked <em>Confidential, for the Board</em>. Concerns raised in good faith will not be held against the person raising them.
    </div>
  </div>
</section>
""" + CTA)

# --------------------------------------------------------------- CONTACT ---
PAGES["contact.html"] = dict(
    title="Contact — Gramotsav Foundation, Patna",
    desc="Get in touch with Gramotsav Foundation, Patna — for CSR and institutional partnerships, volunteering, media enquiries or to request a costed project proposal.",
    body=banner("Contact", "Partnerships, volunteering, media or a costed proposal. Write to us and a person will reply.") + """
<section class="section">
  <div class="container">
    <div class="grid grid-2" style="gap:40px;align-items:start;">
      <div>
        <span class="eyebrow">Reach Us</span>
        <h2 style="margin-bottom:24px;">Gramotsav Foundation</h2>
        <ul class="info-list">
          <li><span class="info-ic">&#9993;</span><div>
            <strong>Email</strong><br>
            <a href="mailto:gramotsavfoundation@gmail.com">gramotsavfoundation@gmail.com</a><br>
            <span style="font-size:.9rem;color:var(--muted);">The fastest route for anything substantive.</span>
          </div></li>
          <li><span class="info-ic">&#127968;</span><div>
            <strong>Registered office</strong><br>
            C/o Suraj Kumar, A. K. Road, Machuatoli,<br>Patna Sadar, Patna &ndash; 800016, Bihar, India
          </div></li>
          <li><span class="info-ic">&#128241;</span><div>
            <strong>Instagram</strong><br>
            <a href="https://www.instagram.com/gramotsavfoundation/" target="_blank" rel="noopener">@gramotsavfoundation</a><br>
            <span style="font-size:.9rem;color:var(--muted);">Session photos and programme updates.</span>
          </div></li>
          <li><span class="info-ic">&#128196;</span><div>
            <strong>Due diligence</strong><br>
            Registration certificates, policies and a costed budget are sent on request. See <a href="transparency.html">governance &amp; compliance</a>.
          </div></li>
        </ul>
      </div>

      <div class="form-card">
        <h3 style="margin-bottom:6px;">Write to us</h3>
        <p style="font-size:.95rem;color:var(--muted);margin-bottom:20px;">This form opens your own email app with the message ready to send.</p>
        <form id="contact-form">
          <div class="field">
            <label for="cf-name">Your name</label>
            <input type="text" id="cf-name" name="name" required />
          </div>
          <div class="field">
            <label for="cf-org">Organisation <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
            <input type="text" id="cf-org" name="org" />
          </div>
          <div class="field">
            <label for="cf-topic">What is this about?</label>
            <select id="cf-topic" name="topic">
              <option>CSR or institutional partnership</option>
              <option>Request a costed project proposal</option>
              <option>Support in kind (instruments, devices, expertise)</option>
              <option>Volunteering</option>
              <option>Media or speaking</option>
              <option>Something else</option>
            </select>
          </div>
          <div class="field">
            <label for="cf-msg">Message</label>
            <textarea id="cf-msg" name="message" rows="5" required></textarea>
          </div>
          <button type="submit" class="btn btn--primary" style="width:100%;">Compose email &rarr;</button>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft section--tight">
  <div class="container section-head" style="margin-bottom:0;">
    <span class="eyebrow">A Small Note</span>
    <h2 style="font-size:1.6rem;">We are a young organisation and we answer our own email</h2>
    <p class="lead mx-auto">Gramotsav was registered in March 2026. There is no press office. Write with a real question and you will get a real answer, usually within a few working days.</p>
  </div>
</section>
""" + CTA)


# ---------------------------------------------------------------- IMPACT ---
PAGES["impact.html"] = dict(
    title="Vision, Mission & Impact — Gramotsav Foundation",
    desc="Gramotsav Foundation's vision and mission, our reach so far, our five focus areas and our partnership philosophy. Talent is everywhere; opportunity is not.",
    body=banner("Vision, Mission &amp; Impact", "What we are trying to build, how far we have got, and what a partner would be buying into.") + """
<section class="section">
  <div class="container">
    <div class="vm">
      <div>
        <span class="eyebrow">Vision</span>
        <h3>An inclusive, culturally confident society</h3>
        <p>Every person should get the chance to find their talent, build a skill, say something of their own, and then find somewhere to take it. We want art, music, culture and creative skill treated as real tools for education, confidence, inclusion, community and a living.</p>
        <p style="margin-top:12px;">Talent from the soil of a community, all the way to a stage worth standing on. <span class="devnagri">मिट्टी से मंच तक</span>.</p>
      </div>
      <div>
        <span class="eyebrow">Mission</span>
        <h3>Art, culture, education, inclusion, livelihood</h3>
        <ul>
          <li>Make creative and artistic learning reachable for children and communities that have had little of it.</li>
          <li>Use music, art and culture for learning, confidence, expression and inclusion.</li>
          <li>Find grassroots talent that stays unseen for social, economic, geographic or physical reasons.</li>
          <li>Build routes from learning to practice, performance, opportunity and livelihood.</li>
          <li>Make platforms where young people can express themselves properly.</li>
          <li>Give emerging artists, fellows and facilitators real creative work.</li>
          <li>Keep local culture in use, and connect it to what exists now.</li>
          <li>Build models other schools, institutions and communities can copy.</li>
          <li>Work with CSR partners, government, institutions, artists and communities.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">Reach So Far</span>
    <h2>Where we have got to</h2>
    <p class="lead mx-auto">Gramotsav Foundation has already worked with nearly 2,000 children through its various artistic, cultural, educational and community-based initiatives.</p>
  </div>
  <div class="container" style="max-width:900px;">
    <div class="impact">
      <div><div class="n">2,000+</div><div class="l">Children reached</div></div>
      <div><div class="n">100+</div><div class="l">Children currently engaged</div></div>
      <div><div class="n">12</div><div class="l">Fellows in most recent project</div></div>
      <div><div class="n">10</div><div class="l">Women fellows, of 12</div></div>
      <div><div class="n">10+</div><div class="l">Artists engaged</div></div>
      <div><div class="n">Patna</div><div class="l">Current base, Bihar</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container section-head">
    <span class="eyebrow">What the Numbers Represent</span>
    <h2>Attendance is not the point</h2>
    <p class="lead mx-auto">A head count only tells you who turned up. What we are actually trying to move a young person through is this.</p>
  </div>
  <div class="container">
    <div class="journey">
      <span>Discover</span><i>&rarr;</i><span>Learn</span><i>&rarr;</i><span>Create</span><i>&rarr;</i>
      <span>Perform</span><i>&rarr;</i><span>Connect</span><i>&rarr;</i><span>Grow</span><i>&rarr;</i><span>Opportunity</span>
    </div>
    <div class="table-wrap" style="margin-top:34px;max-width:820px;margin-left:auto;margin-right:auto;">
      <table class="tbl">
        <tbody>
          <tr><td class="k"><strong>Discover</strong></td><td>Finding talent and creative potential.</td></tr>
          <tr><td class="k"><strong>Learn</strong></td><td>Accessible chances to build a skill.</td></tr>
          <tr><td class="k"><strong>Create</strong></td><td>Imagination, experiment, saying your own thing.</td></tr>
          <tr><td class="k"><strong>Perform</strong></td><td>Showing that skill to a real audience.</td></tr>
          <tr><td class="k"><strong>Connect</strong></td><td>Relationships with artists, communities, institutions.</td></tr>
          <tr><td class="k"><strong>Grow</strong></td><td>Confidence, leadership, identity.</td></tr>
          <tr><td class="k"><strong>Opportunity</strong></td><td>Routes into further study, performance, work, enterprise.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">Focus Areas</span>
    <h2>Five things we work on</h2>
  </div>
  <div class="container" style="max-width:920px;">
    <div class="focus">
      <article><div class="num">01</div><div>
        <h3>Children &amp; creative learning</h3>
        <p>Every child deserves a way into creativity. Music, art and performance used to build learning, confidence, communication, teamwork and imagination.</p>
      </div></article>
      <article><div class="num">02</div><div>
        <h3>Inclusion through art</h3>
        <p>Art can make a room where difference becomes a strength. We build accessible creative work for children and communities that conventional learning does not reach.</p>
      </div></article>
      <article><div class="num">03</div><div>
        <h3>Grassroots talent</h3>
        <p>India has enormous artistic talent well outside the big cultural institutions and the metros. We look for it, and connect it to mentors, platforms and audiences.</p>
      </div></article>
      <article><div class="num">04</div><div>
        <h3>Youth &amp; fellowship</h3>
        <p>Our fellowships put young people to work with communities: learning, leading, contributing. Ten of the twelve fellows on our most recent project were women.</p>
      </div></article>
      <article><div class="num">05</div><div>
        <h3>Artists &amp; livelihood</h3>
        <p>An artist is also a teacher, a mentor, a facilitator, a community builder. We create work for artists in teaching, mentoring, performance and cultural programming.</p>
      </div></article>
    </div>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="container">
    <p class="pull" style="color:#fff;max-width:26ch;">Talent is everywhere. Opportunity is not.</p>
    <p class="lead mx-auto center" style="margin-top:18px;">Nobody has to be born comfortable to be extraordinary. Usually what is missing is not the talent. It is access, a mentor, a platform, a chance.</p>
  </div>
</section>

<section class="section">
  <div class="container section-head">
    <span class="eyebrow">We Work With</span>
    <h2>Partner organisations</h2>
  </div>
  <div class="container" style="max-width:1000px;">
    <div class="partners">
      <span><img src="img/partners/manzil-mystics.png" alt="Manzil Mystics Foundation" loading="lazy" /></span>
      <span><img src="img/partners/diksha.png" alt="Diksha Foundation" loading="lazy" /></span>
      <span><img src="img/partners/kilkari.png" alt="Kilkari Bihar Bal Bhavan" loading="lazy" /></span>
      <span><img src="img/partners/hhfc-trust.png" alt="HHFC Trust" loading="lazy" /></span>
      <span><img src="img/partners/kala-talks.png" alt="Kala Talks" loading="lazy" /></span>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container section-head">
    <span class="eyebrow">Partnership Philosophy</span>
    <h2>We are not only after money</h2>
    <p class="lead mx-auto">We want long partnerships with people who want the impact to be real and measurable. Six things a partner can bring, and money is one of them.</p>
  </div>
  <div class="container" style="max-width:920px;">
    <div class="grid grid-3">
      <div class="callout note"><strong>Space</strong><p style="margin-top:6px;">A safe, reachable place where children can learn and make things.</p></div>
      <div class="callout note"><strong>Resources</strong><p style="margin-top:6px;">Instruments, art materials, technology, learning material.</p></div>
      <div class="callout note"><strong>People</strong><p style="margin-top:6px;">Trainers, artists, facilitators, fellows and mentors.</p></div>
      <div class="callout note"><strong>Programmes</strong><p style="margin-top:6px;">Structured creative learning and community work.</p></div>
      <div class="callout note"><strong>Opportunities</strong><p style="margin-top:6px;">Performances, showcases, fellowships, livelihood routes.</p></div>
      <div class="callout note"><strong>Scale</strong><p style="margin-top:6px;">Taking what works to more communities and institutions.</p></div>
    </div>
  </div>
</section>
""" + CTA)

# ------------------------------------------------- MUSIC BEYOND VISION -----
PAGES["music-beyond-vision.html"] = dict(
    title="Music & Art Beyond Vision — Gramotsav Foundation",
    desc="Music Beyond Vision & Art Beyond Vision: Gramotsav Foundation's proposal for a Music and Creative Arts Club for children with visual impairment, in partnership with the Department of Social Welfare.",
    body=banner("Music &amp; Art Beyond Vision", "A Music and Creative Arts Club for children and young people with visual impairment, proposed in partnership with government.") + """
<section class="section">
  <div class="container prose">
    <span class="pill pill--open">Proposal &middot; seeking a government partner</span>
    <h2>What we are proposing</h2>
    <p>A dedicated Music and Creative Arts Club inside an existing school, government institution or suitable community space. A room where children and young people with visual impairment can learn, practise, make things together, explore where they come from, and perform.</p>
    <p>Students are pushed past learning on their own and towards making music together: ensembles, student bands, group performances, creative projects, cultural presentations.</p>
    <div class="journey" style="margin:26px 0;">
      <span>Discover</span><i>&rarr;</i><span>Learn</span><i>&rarr;</i><span>Practise</span><i>&rarr;</i><span>Create</span><i>&rarr;</i>
      <span>Collaborate</span><i>&rarr;</i><span>Perform</span><i>&rarr;</i><span>Build skills</span><i>&rarr;</i><span>Livelihood</span>
    </div>

    <h3>Why music and arts work here</h3>
    <p>These can be taught by listening, by voice, by touch, by demonstration, by repetition, by memory and by doing. None of that needs a printed page. So the programme is audio-first and practical rather than a conventional written classroom, and it does not depend on Braille-based music instruction.</p>

    <h3>Objectives</h3>
    <ul>
      <li>Create a safe, inclusive and accessible creative space for children with visual impairment.</li>
      <li>Provide audio-first and practical learning in music and the arts.</li>
      <li>Teach instruments through listening, spoken instruction and practice.</li>
      <li>Open up expression through music, tactile arts, storytelling and theatre.</li>
      <li>Build group learning, collaboration and student-led bands.</li>
      <li>Connect children with regional, folk and Indian traditions.</li>
      <li>Give them stage performance and public expression.</li>
      <li>Introduce digital and audio skills where it fits.</li>
      <li>Show music and the arts as possible livelihood routes.</li>
    </ul>
  </div>
</section>

<section class="section section--soft">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">Curriculum</span>
    <h2 style="margin-bottom:22px;">How the teaching runs</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Method</th><th>Application</th></tr></thead>
        <tbody>
          <tr><td><strong>Listening</strong></td><td>Guided listening to songs, instruments, rhythm and musical patterns.</td></tr>
          <tr><td><strong>Audio demonstration</strong></td><td>Demonstration of musical phrases, patterns and instrument techniques.</td></tr>
          <tr><td><strong>Spoken instruction</strong></td><td>Step-by-step verbal explanation of exercises and techniques.</td></tr>
          <tr><td><strong>Call &amp; response</strong></td><td>Students listen and reproduce musical phrases and rhythms.</td></tr>
          <tr><td><strong>Repetition</strong></td><td>Repeated riyaz to strengthen familiarity, memory and confidence.</td></tr>
          <tr><td><strong>Rhythm cues</strong></td><td>Auditory and verbal cues support timing and coordination.</td></tr>
          <tr><td><strong>Hands-on practice</strong></td><td>Students practise the instruments directly, with guidance.</td></tr>
          <tr><td><strong>Recorded practice</strong></td><td>Audio material supports practice outside the sessions.</td></tr>
          <tr><td><strong>Performance</strong></td><td>Performing is used as a learning milestone, not a display.</td></tr>
        </tbody>
      </table>
    </div>

    <h2 style="margin:46px 0 22px;">Twelve months</h2>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Phase</th><th>Period</th><th>Activities</th></tr></thead>
        <tbody>
          <tr><td class="k"><strong>Preparation</strong></td><td>Month 1</td><td>Space, student identification, resource planning, orientation</td></tr>
          <tr><td class="k"><strong>Discovery</strong></td><td>Months 1&ndash;2</td><td>Music and arts exploration; identifying interests and abilities</td></tr>
          <tr><td class="k"><strong>Foundation learning</strong></td><td>Months 2&ndash;4</td><td>Audio-first music and practical creative learning</td></tr>
          <tr><td class="k"><strong>Collaboration</strong></td><td>Months 4&ndash;6</td><td>Ensembles, group activities, band formation</td></tr>
          <tr><td class="k"><strong>Creation &amp; culture</strong></td><td>Months 7&ndash;9</td><td>Original work, folk and cultural learning, creative projects</td></tr>
          <tr><td class="k"><strong>Performance</strong></td><td>Months 10&ndash;11</td><td>Rehearsals, showcases, outside exposure</td></tr>
          <tr><td class="k"><strong>Evaluation &amp; pathways</strong></td><td>Month 12</td><td>Documentation, mentoring, mapping opportunities</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">The Partnership</span>
    <h2 style="margin-bottom:16px;">Who brings what</h2>
    <p class="lead" style="margin-bottom:24px;">The model is built to use what a government institution already has, rather than to duplicate it.</p>
    <div class="table-wrap">
      <table class="tbl">
        <thead><tr><th>Department of Social Welfare</th><th>Gramotsav Foundation</th></tr></thead>
        <tbody>
          <tr><td>One suitable room or shared space</td><td>Curriculum and programme design</td></tr>
          <tr><td>Musical instruments, where available</td><td>Music and arts facilitation</td></tr>
          <tr><td>Basic creative materials, where available</td><td>Student engagement and mentoring</td></tr>
          <tr><td>Instructor honorarium support, subject to norms</td><td>Band formation and creative activities</td></tr>
          <tr><td>Institutional coordination</td><td>Cultural learning, performance, documentation</td></tr>
          <tr><td>Convergence with relevant schemes</td><td>Linkages to artists, mentors and opportunities</td></tr>
        </tbody>
      </table>
    </div>

    <h3 style="margin-top:40px;">What the room needs</h3>
    <ul style="margin-left:20px;">
      <li style="margin-bottom:6px;">One dedicated room, or a suitable shared one</li>
      <li style="margin-bottom:6px;">Instruments chosen around what the students want to play</li>
      <li style="margin-bottom:6px;">A basic audio system, microphones and headphones</li>
      <li style="margin-bottom:6px;">Accessible digital and audio learning equipment where possible</li>
      <li style="margin-bottom:6px;">Basic art and creative materials</li>
      <li style="margin-bottom:6px;">Safe storage for instruments and materials</li>
      <li style="margin-bottom:6px;">Seating that can be moved around for practice</li>
    </ul>
  </div>
</section>

<section class="section section--soft">
  <div class="container prose">
    <span class="eyebrow">Measurement</span>
    <h2>What we will track</h2>
    <ul>
      <li>Student enrolment and attendance</li>
      <li>Individual learning and participation profiles</li>
      <li>Progress in musical and creative skills, and consistency of riyaz</li>
      <li>Participation in group activities, and the number of ensembles or bands formed</li>
      <li>Creative outputs and performances</li>
      <li>Confidence and communication indicators</li>
      <li>Cultural participation, and mentor and facilitator observations</li>
      <li>Exposure to professional opportunities</li>
    </ul>

    <h3>Sustainability</h3>
    <p>The programme is designed as a collaborative model on existing institutional infrastructure wherever possible. It holds up longer through government convergence, CSR partnerships, cultural collaborations, professional mentors, performance opportunities, and a student and alumni network.</p>

    <div class="note" style="margin-top:30px;">
      <strong>Interested departments and institutions.</strong> The full proposal, with the curriculum detail and the departmental support request, is available on letterhead. <a href="contact.html">Write to us</a> and we will send it and come and present it.
    </div>
  </div>
</section>
""" + CTA)


def build():
    written = []
    for slug, page in PAGES.items():
        html = shell(slug, page["title"], page["desc"], page["body"])
        with open(os.path.join(SITE, slug), "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append((slug, len(html)))
    return written


if __name__ == "__main__":
    for slug, size in build():
        print(f"  {slug:34s} {size:>7,} bytes")
