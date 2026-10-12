# zachofalltrade.com: ZachOS 95

A single-file retro desktop portfolio. No build step, no dependencies. Open `index.html` in a browser, or host the folder anywhere that serves static files.

## Adding an app
Edit the `CONFIG.apps` array near the top of the script in `index.html`:

```js
{ id: 'onlyline', name: 'Onlyline', url: '/apps/onlyline', description: 'What it does.' }
```

Each app appears as a folder in Applications (and in Start > Programs > Applications). Opening the folder shows `Launch <name>.exe`; double-clicking it opens `url` in a new tab. You can type the `id` in the DOS prompt or Start > Run too.

## Documents
`CONFIG.documents` holds the text files in My Documents. Set `CONFIG.resumePdfUrl` (for example `/resume.pdf`) to add a real Resume.pdf, and use `CONFIG.links` for LinkedIn, GitHub and similar shortcuts. The About Me and Resume text shipped here is placeholder copy built from a few basics. Edit it.

## The /apps/... URLs (GitHub Pages)
Each app has a small redirect page at `apps/<id>/index.html` that forwards to its Lovable address, so `zachofalltrade.com/apps/<id>` works on GitHub Pages. To add an app, add an entry to `CONFIG.apps` and create a matching redirect page (copy any existing one and change the target). To point an app at a custom domain later, change the target in its redirect page.

## Screen size
The whole interface scales up on large screens (125% from 1000px wide, 150% from 1600px wide) so it feels like an older, lower resolution display. Visitors can change it from right-click on the desktop, then Display Settings. You can also force a size with `?scale=1.5` in the URL.

## Easter eggs
Spoilers: Konami code, `idkfa`, `xyzzy`, hidden commands in the DOS prompt (`help`, `coffee`, `sudo`), a Recycle Bin worth browsing, Minesweeper, and a starfield screen saver after two idle minutes (or right-click the desktop). Add `?noboot` to the URL to skip the boot sequence.
