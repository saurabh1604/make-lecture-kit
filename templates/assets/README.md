# templates/assets — brand assets

Drop the BITS Pilani logo here to turn on the logo. The text wordmark
**"WILP, BITS Pilani"** always shows even without it, so nothing breaks if this
folder is empty.

```
templates/assets/bits-logo.png
```

## Companion PDF (`companion.tex`)
The logo appears in a small **white chip** at the top-right of the navy title
banner, so a logo of any colour stays legible. If the file is absent, only the
white wordmark shows. The template looks for the logo at `assets/bits-logo.png`
(next to the `.tex`) and at `../../templates/assets/bits-logo.png` (the shared
copy, when building from `output/<slug>/`). A PNG ~400 px wide is plenty.

## Interactive lecture (`lecture.html`)
The sidebar shows the logo on a white chip beside the wordmark. Because the
lecture is a single portable file, either:

- copy `bits-logo.png` next to the `.html` (keep the `assets/` folder name), **or**
- embed it: replace the `src="assets/bits-logo.png"` on the `<img class="bits-logo">`
  with a base64 `data:` URI so the logo travels inside the one file.

If the image is missing, the wordmark shows and the broken `<img>` hides itself.

---

`bits-logo.png` — the official **BITS Pilani** logo (transparent PNG, extracted
from the course slides) — is bundled here, so the logo shows out of the box. To
change it, just replace that one file (a transparent or white-background PNG
works best on both the navy banner and the dark sidebar). If the file is removed,
both templates fall back to the text wordmark automatically.
