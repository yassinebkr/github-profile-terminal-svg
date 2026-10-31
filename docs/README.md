# Engineering OS — interactive GitHub Pages terminal

A static Debian/XFCE-style portfolio environment for exploring engineering skills and verified project results. This site runs entirely in the browser using accessible HTML, CSS and JavaScript modules. The shell is a **curated read-only simulation**; its virtual filesystem contains portfolio information.

## Development

Run the tests with a supported version of Node.js:

```bash
node --test tests/*.test.mjs
```

Preview the site locally with a static file server:

```bash
python3 -m http.server --directory docs 8000
```

Then open `http://localhost:8000/`. On GitHub Pages, `/docs` on the `main` branch is the proposed publishing source.

## Exploring

Start with `help`, `ls -l workspace`, `skills`, `projects`, or `inspect lora`. You can use `cd`, `pwd`, `tree`, and `cat README.md` to navigate the modeled directories. Tab completes known commands and paths; Up/Down browses the command history; Ctrl+L clears the history view. Command buttons offer a convenient alternative to typing.

## Design and safety

- `index.html`, `style.css`, and `app.js` define the responsive interface.
- `engine.js` implements deterministic virtual filesystem commands with structured outputs.
- `tests/engine.test.mjs` exercises the interpreter, project claims, path handling and commands.
- All visible command output uses `textContent`; link destinations come from a known allowlist.
- The site uses a self-hosted Debian vector asset and a restrictive Content Security Policy.
- `assets/debian.svg` contains the Debian swirl, sourced from the repo's documented Debian artwork.

## Publishing from GitHub

1. Open the repository **Settings → Pages**.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select **main** and the **/docs** folder, then save.
4. Check the **Visit site** link once a successful Pages deployment appears.

GitHub Pages site eligibility depends on the repository visibility and GitHub account plan. Pages sites are publicly viewable, including those sourced from eligible private repositories. The GitHub repository's visibility should remain unchanged during preparation. Refer to https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site.
