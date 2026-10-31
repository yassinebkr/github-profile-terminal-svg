# Add the animated terminal to your GitHub profile

GitHub displays the `README.md` of a **public repository named after your
GitHub username** on your profile page. The SVG generator can live in a
separate repository.

## 1. Prepare the generator

Fork this repository, or use your own copy. If necessary, rename it in
**Settings → General → Repository name** and set its visibility to **Public**
in **Settings → General → Danger Zone**.

Generate and validate the SVG before embedding it:

```bash
python3 scripts/make_terminal.py
python3 scripts/make_cta.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

## 2. Create your profile repository

Create a public repository named exactly `GITHUB_USERNAME` under the account
`GITHUB_USERNAME`. Enable **Add a README file**.

For example, an account called `example-user` needs a public repository
called `example-user/example-user`.

## 3. Embed the animated SVG

Replace these placeholders **everywhere** in the snippet:

| Placeholder | Replace with |
| --- | --- |
| `GITHUB_USERNAME` | Your GitHub account username |
| `GENERATOR_REPO` | The name of your public SVG generator repository |
| `PORTFOLIO_URL` | The full URL of your portfolio or other destination, including `https://` |

Paste the updated snippet into the profile repository's `README.md`:

```html
<p align="center">
  <a href="PORTFOLIO_URL"><img
    src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/terminal.svg"
    width="100%" alt="Open the interactive portfolio from this animated terminal" /></a>
</p>

<p align="center">
  <a href="PORTFOLIO_URL"><img
    src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/shellfolio-cta-arrows-v3.svg"
    width="296" height="62" alt="Click the terminal above or this button to open the interactive portfolio" /></a>
  <a href="https://github.com/GITHUB_USERNAME/GENERATOR_REPO"><img
    src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/source-button.svg"
    width="296" height="62" alt="View SVG generator source and build notes" /></a>
</p>

<p align="center">
  ↓ Explore the pinned repositories below, or
  <a href="https://github.com/GITHUB_USERNAME?tab=repositories">browse all projects</a>.
</p>
```

For a short personal introduction, use **GitHub → Edit profile → Bio**.
The profile README template deliberately starts with the animated terminal.

The SVG is an animated image and **clicking it opens your portfolio**. The
first compact button has a green upward arrow matching the large pink arrow
on the second button, and a smaller white right arrow following "OR CLICK HERE
TO OPEN". Clicking the first button also opens the portfolio. Its distinct
asset filename avoids GitHub caching the older arrow arrangement. The second
button opens the generator's source.
Both buttons have a 296 × 62 px viewport and explicit HTML dimensions.
The profile also invites visitors to explore other repositories.

## 4. Check the profile

- Visit `https://github.com/GITHUB_USERNAME`, using your actual username.
- Confirm that the terminal SVG and both linked graphics appear.
- Open the two links to verify their destinations.
- Check the mobile layout and ensure the animation ends without erasing text.

To change terminal content, edit `scripts/make_terminal.py` and regenerate
`assets/terminal.svg`. To customize either CTA arrow, edit `MAIN_ARROW` or
`INLINE_ARROW` in `scripts/make_cta.py`, then run that script. Configure only
direction (`up`, `right`, `down`, `left`), length in pixels, stroke width
and six-digit hex color. Commit the generated SVG with its source. GitHub may
cache a previously rendered image; publish under a fresh filename when a
visible profile change needs to bypass that cache.
