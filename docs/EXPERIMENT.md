# Engineering OS — XFCE visual revision

The terminal uses a single standalone SVG image. Its XFCE-style title bar, GTK menu and near-black shell colors are based on the user's reference screenshot.

The Debian vector geometry is embedded directly from the local vector source. The generator draws the long-format Unix listing with realistic permissions, owners, sizes and sample timestamps.

## Rebuild

    python3 scripts/make_terminal.py
    python3 scripts/validate.py

The template lives at assets/terminal-template.svg, the Debian artwork at assets/debian-open-use.svg, and the resulting file at assets/terminal.svg.

## Review

Review the generated asset in the GitHub README; compare its window controls, monochrome shell text, Debian vector, spacing and alignment to XFCE Terminal. The final image can later link to a full GitHub Pages interactive terminal.
