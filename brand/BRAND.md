# Fasil Teshome / FasHub

A restrained personal identity built around walnut, espresso and stone. The color direction follows Fasil's preference for brown and a strong, understated professional appearance. The FT monogram identifies Fasil; a future company can use its own name and symbol with the same palette.

## Palette

| Color | Hex | Role |
| --- | --- | --- |
| Walnut | `#6B4F3A` | Signature brown; headings and links on light backgrounds |
| Espresso | `#241D19` | Banner, statistics cards and main dark surface |
| Graphite | `#33312F` | Quiet secondary dark surface |
| Stone | `#BFA58A` | Headings, numbers and accents on dark backgrounds |
| Linen | `#D8C9BA` | Display text on espresso |
| Paper | `#FAF8F5` | Light surface and inverse body text |

Walnut is the primary brand color. Espresso gives the banner visual weight, while graphite moderates the warm palette. Use stone for selected text on dark surfaces. Keep normal body copy neutral and apply color to names, headings and statistical values. This palette replaces the earlier cobalt proposal.

## Contrast

- Walnut on white: 7.49:1
- Walnut on paper: 7.06:1
- Stone on GitHub dark (`#0D1117`): 8.08:1
- Stone on espresso: 7.09:1
- Paper on espresso: 15.66:1
- Linen on espresso: 10.27:1

These combinations exceed the 4.5:1 minimum for normal text in WCAG AA. Do not place walnut text directly on espresso. Recheck contrast before introducing new combinations.

## Typography and layout

Use a clear sans-serif family. Hubot Sans and Mona Sans remain suitable for a future site; the SVG assets use Arial/Helvetica for portability. The GitHub profile uses a compact banner, a direct professional introduction, an engineering section, one small statistics section and contact links.

GitHub removes inline styles, so colored section headings use small SVG images inside semantic headings. Each includes meaningful alternative text. Light and dark variants use GitHub-supported picture markup. Normal paragraphs retain GitHub's native colors and selectable text.

## Voice and scope

Lead with the current roles: Software Development Manager at Koket Inc and co-founder of YOME PLC. Mention INSA as previous employment. Describe AI engineering and full-stack web and mobile experience, including NestJS. State that Fasil is a Software Engineering graduate of Mekelle University. Keep the statement that most professional work is private; omit tutorial repositories as portfolio projects.

Fasil also offers freelance consulting for founders starting their own software companies. Include this in the introduction and contact invitation without promising specific services or outcomes beyond his stated experience.

He teaches programming languages and helps aspiring developers build strong software engineering skills. Mention programming education in the contact invitation.

Fasil currently works with the Ethiopian Civil Service Commission as a freelance software engineer, contributing to software product development. Describe it as a current freelance engagement without implying direct employment or publishing private project details. Include Electron.js under desktop development in the engineering stack.

Telegram: https://t.me/fashub21

LinkedIn: https://www.linkedin.com/in/fasil-teshome/

No portfolio website is listed until a current one is available. Keep the existing GitHub photograph; the FT monogram is an optional reusable asset.

## Automatically refreshed statistics

`.github/workflows/profile-stats.yml` refreshes the cards, README values and `brand/public-stats.json` daily at 03:17 UTC, on relevant code pushes, and on manual workflow dispatch. The Python updater uses only the standard library and GitHub's GraphQL API. It runs with the profile repository's built-in GITHUB_TOKEN; no personal token or external stats service is required for the visible data.

The contribution cards show the current calendar year and the sum of contribution years returned by GitHub. Contributions can include anonymous private activity the user already shares. Commit counts remain separate: they include only contribution-eligible commits visible to the updater. Restricted contribution totals are never added to commit counts.

Keep GitHub's existing native contribution calendar and activity timeline below the profile README. They retain GitHub's square cells, colors, year selector and automatic updates. The README does not duplicate the calendar or include a separate bar chart. Public repository count includes forks; stars earned excludes forks. The last-refresh time is recorded in `brand/public-stats.json`, with no timestamp or refresh notice displayed in the README. A failed API fetch leaves the previous successful output intact and fails the workflow rather than replacing missing data with zero.

The workflow needs permission to commit generated assets to this profile repository. It does not query repository contents or expose private repository names. Changes to GitHub visibility or token access can affect totals. Scheduled runs can be delayed or disabled by GitHub; the native profile contribution graph updates independently.

Local verification: `python3 -m unittest discover -s tests -v`. Local refresh with the existing GitHub CLI login: `python3 scripts/update_profile_stats.py --username FasHub`.

## Research informing the design

- [GitHub: Personalize your profile](https://docs.github.com/en/account-and-profile/tutorials/personalize-your-profile) — clear bio, identity and social links.
- [Anthony Fu](https://github.com/antfu) and [Sindre Sorhus](https://github.com/sindresorhus) — examples of concise, navigable profiles. Their open-source portfolios are not comparable to private commercial work; the design borrows clarity, not their project selection.
- [GitHub Markup](https://github.com/github/markup) — inline styles are sanitized, which constrains README text color.
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats#deploy-on-your-own-recommended) — maintainers recommend repository-generated SVGs or self-hosting because the shared public endpoint can be unreliable.
- [Adobe: Color meaning](https://www.adobe.com/creativecloud/design/discover/color-meaning.html) — brown and neutral combinations informed the direction; the exact palette is an original design choice, not a universal association.
- [W3C: Contrast minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum) — text contrast targets.
