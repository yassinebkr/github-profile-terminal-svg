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
<div align="center">

<img src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/terminal.svg"
     width="100%" alt="Animated Debian XFCE terminal profile" />

<a href="PORTFOLIO_URL">
  <img src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/pages-cta.svg"
       width="100%" alt="Explore my interactive portfolio" />
</a>

<a href="https://github.com/GITHUB_USERNAME/GENERATOR_REPO">
  <img src="https://raw.githubusercontent.com/GITHUB_USERNAME/GENERATOR_REPO/main/assets/how-made-it.svg"
       width="100%" alt="How this terminal was made" />
</a>

</div>
```

The terminal SVG is an image, not an interactive shell. The first linked
graphic opens your portfolio; the second opens the generator source.

## 4. Check the profile

- Visit `https://github.com/GITHUB_USERNAME`, using your actual username.
- Confirm that the terminal SVG and both linked graphics appear.
- Open the two links to verify their destinations.
- Check the mobile layout and ensure the animation ends without erasing text.

To change the terminal content, edit `scripts/make_terminal.py`, regenerate
`assets/terminal.svg`, and commit **both the source and the output** in the
generator repository. GitHub may cache the rendered image briefly.
