"""Build per-person birthday cards using one shared template.

Expected structure:
  ./Shalini/
    profile.json
    stickers/
    audio/cat.mp3
    audio/dog.mp3
  ./Mom/
    profile.json
    stickers/
    audio/cat.mp3
    audio/dog.mp3
"""
import base64
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = DIR / "template.html"
BRAIN_DIR = Path(r"C:\Users\arulr\.gemini\antigravity\brain\a23a06a0-9b85-4282-9760-a238b9b54b3f")
PROFILE_NAMES = ["Shalini", "Mom"]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
DEFAULT_CAT_AUDIO = DIR / "audio" / "dragon-studio-cute-cat-meow-472372.mp3"
DEFAULT_DOG_AUDIO = DIR / "audio" / "freesound_community-single-dog-bark-king-charles-spaniel-41366.mp3"


def b64(path: Path) -> str:
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode()


def image_to_data_uri(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif ext == ".webp":
        mime = "image/webp"
    elif ext == ".gif":
        mime = "image/gif"
    elif ext == ".svg":
        mime = "image/svg+xml"
    else:
        mime = "image/png"
    return f"data:{mime};base64,{b64(path)}"


def audio_to_data_uri(path: Path) -> str:
    ext = path.suffix.lower()
    mime = "audio/mp3" if ext == ".mp3" else "audio/wav"
    return f"data:{mime};base64,{b64(path)}"


def load_profile(profile_dir: Path) -> dict:
    profile_path = profile_dir / "profile.json"
    if profile_path.exists():
        with profile_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def pick_first_existing(paths) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def sticker_uris(profile_dir: Path) -> list:
    stickers_dir = profile_dir / "stickers"
    if not stickers_dir.exists():
        return []
    files = sorted(
        [p for p in stickers_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda p: p.name.lower(),
    )
    return [image_to_data_uri(path) for path in files]


def build_one(profile_name: str, template: str, default_cat_b64: str, default_dog_b64: str) -> None:
    profile_dir = DIR / profile_name
    profile_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_profile(profile_dir)

    recipient = (cfg.get("recipient_name") or profile_name).strip()
    message = cfg.get(
        "message",
        f"Happy Birthday {recipient}!\nWishing you a cozy, joyful, and peaceful year ahead.",
    )
    cat_name = (cfg.get("cat_name") or "Rue").strip()
    dog_name = (cfg.get("dog_name") or "Wanda").strip()
    bg_top = cfg.get("background", {}).get("top", "#0e3d5e")
    bg_mid_1 = cfg.get("background", {}).get("mid_1", "#0e4a6a")
    bg_mid_2 = cfg.get("background", {}).get("mid_2", "#0b3a55")
    bg_bottom = cfg.get("background", {}).get("bottom", "#071f33")
    scene_mode = cfg.get("scene_mode", "pond")
    yt_night_id = cfg.get("yt_ambience", {}).get("night_video_id", "97G5esCpJsY")
    yt_day_id = cfg.get("yt_ambience", {}).get("day_video_id", "97G5esCpJsY")

    cat_audio_path = pick_first_existing([profile_dir / "audio" / "cat.mp3", DEFAULT_CAT_AUDIO])
    dog_audio_path = pick_first_existing([profile_dir / "audio" / "dog.mp3", DEFAULT_DOG_AUDIO])
    cat_audio_b64 = audio_to_data_uri(cat_audio_path) if cat_audio_path else ""
    dog_audio_b64 = audio_to_data_uri(dog_audio_path) if dog_audio_path else ""
    stickers_js = json.dumps(sticker_uris(profile_dir))

    profile_cat_image = cfg.get("cat_image")
    profile_dog_image = cfg.get("dog_image")
    cat_image_candidates = []
    dog_image_candidates = []
    if profile_cat_image:
        cat_image_candidates.append(profile_dir / profile_cat_image)
    if profile_dog_image:
        dog_image_candidates.append(profile_dir / profile_dog_image)
    cat_image_candidates.extend([profile_dir / "cat.png", profile_dir / "pets" / "cat.png"])
    dog_image_candidates.extend([profile_dir / "dog.png", profile_dir / "pets" / "dog.png"])
    cat_image_path = pick_first_existing(cat_image_candidates)
    dog_image_path = pick_first_existing(dog_image_candidates)
    cat_b64 = b64(cat_image_path) if cat_image_path else default_cat_b64
    dog_b64 = b64(dog_image_path) if dog_image_path else default_dog_b64

    html = (
        template.replace("__RECIPIENT_NAME__", recipient)
        .replace("__CAT_NAME__", cat_name)
        .replace("__DOG_NAME__", dog_name)
        .replace("__MESSAGE_TEXT__", json.dumps(message))
        .replace("__CAT_B64__", cat_b64)
        .replace("__DOG_B64__", dog_b64)
        .replace("__BG_TOP__", bg_top)
        .replace("__BG_MID_1__", bg_mid_1)
        .replace("__BG_MID_2__", bg_mid_2)
        .replace("__BG_BOTTOM__", bg_bottom)
        .replace("__SCENE_MODE__", scene_mode)
        .replace("__YT_NIGHT_ID__", yt_night_id)
        .replace("__YT_DAY_ID__", yt_day_id)
        .replace("__STICKERS_ARRAY__", stickers_js)
        .replace("__CAT_AUDIO_B64__", cat_audio_b64)
        .replace("__DOG_AUDIO_B64__", dog_audio_b64)
    )

    out_path = profile_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(
        f"Built {profile_name}/index.html "
        f"({len(html)} chars, {len(json.loads(stickers_js))} stickers, "
        f"cat_audio={'yes' if cat_audio_b64 else 'no'}, dog_audio={'yes' if dog_audio_b64 else 'no'}, "
        f"custom_cat={'yes' if cat_image_path else 'no'}, custom_dog={'yes' if dog_image_path else 'no'})"
    )


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    dog_b64 = b64(BRAIN_DIR / "media__1774477141059.png")
    cat_b64 = b64(BRAIN_DIR / "media__1774477141102.png")
    for name in PROFILE_NAMES:
        build_one(name, template, cat_b64, dog_b64)


if __name__ == "__main__":
    main()
