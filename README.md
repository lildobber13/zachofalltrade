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

## The /apps/... URLs
Your apps live on Lovable, so `/apps/neverendingbacklog` on zachofalltrade.com has to forward to each app's Lovable address. Two options:

1. Point `url` straight at the Lovable address (simplest, always works).
2. Keep the pretty path and add a redirect at your host. Netlify and Cloudflare Pages read the `_redirects` file included here. Use a 302 redirect rather than a rewrite, because proxying a single page app under a sub path usually breaks its asset links.

## Easter eggs
Spoilers: Konami code, `idkfa`, `xyzzy`, hidden commands in the DOS prompt (`help`, `coffee`, `sudo`), a Recycle Bin worth browsing, Minesweeper, and a starfield screen saver after two idle minutes (or right-click the desktop). Add `?noboot` to the URL to skip the boot sequence.
