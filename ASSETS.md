## Per-Person Assets

Each person has their own folder with separate content:

- `Shalini/`
- `Mom/`

In each folder:

- `profile.json` -> name + letter message
- `stickers/` -> any `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`
- `audio/cat.mp3` -> optional override cat sound
- `audio/dog.mp3` -> optional override dog sound
- `pets/cat.png` -> optional custom cat image
- `pets/dog.png` -> optional custom dog image

If a profile does not provide audio files, the build uses default sounds in `audio/`.

Then rebuild:

`python build.py`

Outputs:

- `Shalini/index.html`
- `Mom/index.html`
