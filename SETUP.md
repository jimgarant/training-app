# Road to 1:35 — Getting it on your iPhone

Everything in this folder goes to GitHub Pages. One-time setup, about ten minutes,
all in the browser, no coding tools needed.

## Part 1 — Put the app online (on your computer)

1. Go to https://github.com and sign in (or create a free account).
2. Click the "+" in the top-right → **New repository**.
   - Name: `training-app` (or anything you like)
   - Visibility: **Public** (required for free GitHub Pages)
   - Click **Create repository**.
3. On the new repository page, click **uploading an existing file**
   (or Add file → Upload files).
4. Drag in ALL the contents of this folder:
   `index.html`, `manifest.webmanifest`, `sw.js`, `LICENSE`, and the whole
   `icons` folder (drag the folder itself; GitHub keeps the structure).
5. Click **Commit changes**.
6. Go to **Settings → Pages** (left sidebar, under "Code and automation").
   - Under "Build and deployment", Source: **Deploy from a branch**.
   - Branch: **main**, folder: **/ (root)** → **Save**.
7. Wait a minute or two, then refresh the Pages screen. It shows your URL:
   `https://<your-username>.github.io/training-app/`

Note on privacy: the repository is public, but the app contains no personal
data. Your training entries are stored only on the device you use the app on
(localStorage), never in the repository.

## Part 2 — Install on the iPhone

1. Open the URL from step 7 in **Safari** (must be Safari, not Chrome).
2. Check the app loads and looks right.
3. Tap the **Share** button (square with arrow) → **Add to Home Screen** → **Add**.
4. Open it from the home screen icon. Full screen, no browser chrome,
   works offline from now on.

## Updating the app later

Edit or re-upload `index.html` in the GitHub repository (Add file → Upload
files again overwrites it). The phone picks up the new version the next time
you open the app with a connection. Your data is untouched by updates.

## Important: where your data lives

Entries are saved on the device where you type them. The phone and the
desktop copies each keep their own log; they do not sync with each other.
Use the app's export/backup from Settings if you want to move data across.
