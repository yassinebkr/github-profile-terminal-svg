# Publish the animation on your GitHub profile

A GitHub profile README and the SVG generator are **separate repositories**.
You can update the image here without copying this generator's code into
your personal profile.

## 1. Prepare this generator repository

Rename the repository to a descriptive name, for example
`github-profile-terminal-svg`, using **Settings → General → Repository name**.

Suggested repository description:

> Python generator for an animated Debian/XFCE terminal SVG in GitHub profile READMEs.

Make the generator repository public when you are ready, using
**Settings → General → Danger Zone → Change repository visibility**.

## 2. Create the profile repository

Create a **public** repository named exactly `yassinebkr` under the
`yassinebkr` account. Check **Add a README file** when creating it.

GitHub recognizes `yassinebkr/yassinebkr` as the profile README source.

## 3. Add the image and links

Paste the following into the **profile** repository's `README.md`. Replace
`GENERATOR_REPO` with the new name of this repository after renaming it.

```html
<div align="center">

<img src="https://raw.githubusercontent.com/yassinebkr/GENERATOR_REPO/main/assets/terminal.svg"
     width="100%" alt="Animated Debian XFCE terminal profile" />

<a href="https://yassinebkr.github.io/ShellFolio/?run=launch">
  <img src="https://raw.githubusercontent.com/yassinebkr/GENERATOR_REPO/main/assets/pages-cta.svg"
       width="100%" alt="Explore my interactive portfolio" />
</a>

<a href="https://github.com/yassinebkr/GENERATOR_REPO">
  <img src="https://raw.githubusercontent.com/yassinebkr/GENERATOR_REPO/main/assets/how-made-it.svg"
       width="100%" alt="How this terminal was made" />
</a>

</div>
```

The first image is a preview. The **Open ShellFolio** graphic links to the
interactive portfolio, while **How I made it** links to the generator.

## 4. Verify

- Open `https://github.com/yassinebkr` and confirm the images appear.
- Follow both graphic links and verify they point to the intended repositories.
- Check mobile layout, text legibility and that animation completes once.
- Change a value in `scripts/make_terminal.py`, regenerate and push.
  Confirm the profile image updates (GitHub's image cache may take time).

## Maintenance

After edits to profile data or the template, run:

```bash
python3 scripts/make_terminal.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Commit **both source and generated SVG** in this generator repository.
The profile README can keep linking to the same raw SVG path.
