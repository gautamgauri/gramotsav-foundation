# Gramotsav Foundation — website

Static site for [Gramotsav Foundation](https://www.instagram.com/gramotsavfoundation/), a Section 8 non-profit in Patna, Bihar. Built to be hosted on GitHub Pages — no build step, no dependencies, no server.

Structure and stylesheet are adapted from the `apna-foundation` site; content, palette and imagery are Gramotsav's own.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — who we are, the method, both projects, gallery, registration |
| `our-story.html` | Why we exist, registered objects, five commitments, where we work |
| `programmes.html` | The learning arc, both projects, folk culture work |
| `learning-through-music.html` | Public version of the completed project's impact & closure report |
| `blind-school-project.html` | Full concept note — components, phases, M&E, budget heads, risk, ToC |
| `support.html` | Partnership routes: CSR, programme sponsorship, in-kind, volunteering |
| `transparency.html` | Registration, tax status, adopted policies, how funds are handled |
| `contact.html` | Contact details + a mailto-based enquiry form |

## Editing

Page content lives in `build.py`, not in the `.html` files — the HTML is **generated**, so edits made directly to `.html` will be overwritten.

```bash
python3 build.py      # regenerates all 8 pages
```

Shared header, nav, footer and organisation facts are in the `HEAD`, `FOOT` and `ORG` blocks at the top of `build.py`. Change a fact once there and every page picks it up.

Styling is in `styles.css` (CSS custom properties at the top control the whole palette). Behaviour — mobile nav and the mailto contact form — is in `main.js`.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying to GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → `main` / root. `.nojekyll` is present so files are served as-is.

## Communication materials

`materials/` holds the launch comms kit — organisation profile, funder one-pager, boilerplate and key messages, social media kit, and email templates. See `materials/03-boilerplate-and-key-messages.md` first; it contains the numbers and language discipline everything else depends on.

## Content sourcing

All factual content is drawn from Gramotsav Foundation's own documents (shared 31 Aug 2026): the Learning Through Music closure report, the Blind School Project concept note, the certificate of incorporation, Section 8 licence, MOA/AOA, the s.332 and s.354 tax orders, and the Finance / Procurement / Travel / PoSH policies. Photographs are from the foundation's session and event archive.

**Deliberately not published:** PAN, TAN, bank account details, and the registered office's `C/o` line. These are supplied directly during due diligence.

## Before this goes live — needs confirmation from Gramotsav

- [ ] **Logo.** `logo.svg` / `logo.png` are a placeholder mark (marigold rosette over a stage, on indigo). Replace with the real logo if one exists.
- [ ] **Photo consent.** Confirm parent/guardian and school consent for every image in `img/` before the site is public.
- [ ] **Contact details.** Is `gramotsavfoundation@gmail.com` the right public address? Should a phone number be listed?
- [ ] **Named people.** No directors, founders or staff are currently named anywhere on the site. Decide whether to add a team section.
- [ ] **Tax registration numbers.** `transparency.html` publishes the s.332 and s.354 URNs. Standard practice, but confirm Gramotsav is comfortable.
- [ ] **Learning Through Music.** Confirm the project ran with a named partner school, and whether that school and any collaborating organisation should be credited.
- [ ] **Participant numbers.** The site deliberately claims none. Add verified figures when they exist.
- [ ] **Custom domain**, if wanted — add a `CNAME` file.
