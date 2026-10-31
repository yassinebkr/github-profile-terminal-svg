# Engineering OS / GitHub README experiment

## GitHub interaction

The terminal is composed from adjacent SVG assets. Each `entry-*.svg` is
wrapped in a native HTML `<a href="#section">` element, creating a full-row
click target. Internal heading anchors keep navigation within the README.

The interface uses a simulated `ls -l ~/workspace` listing with representative
Unix permission, ownership, size, and timestamp fields. The repository's
engineering domains are the actual destinations of each directory link.

## Design

- Debian 13 / XFCE terminal aesthetics
- CSS cursor and SMIL typewriter effects
- Long-format directory entries, visually continuous with the terminal
- Native GitHub Markdown anchor navigation
- Dedicated project and competency sections

## Manual GitHub verification

1. Open this branch's rendered README.
2. Check the prompt `ls -l ~/workspace` and its directory entries.
3. Click an entire directory line such as `hardware/`.
4. Confirm navigation to the matching section on the same page.
5. Use `Return to workspace` to navigate to the top of the terminal.
6. Review image seam spacing, responsiveness and keyboard navigation.

## Known behavior

SVG illustrations can open their source assets when GitHub automatically wraps
them in links. Directory images carry explicit internal links to select the
matching section. The separate sections present predefined engineering
information. Each section may be navigated through native Markdown anchors.
