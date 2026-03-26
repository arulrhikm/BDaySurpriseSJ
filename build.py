"""V6 Build: Support a folder of stickers, inject dynamically into the template."""
import base64, os, glob, json

DIR = os.path.dirname(os.path.abspath(__file__))
brain = r'C:\Users\arulr\.gemini\antigravity\brain\a23a06a0-9b85-4282-9760-a238b9b54b3f'

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Read pet images from brain (since they are constant and not in stickers/)
dog_b64 = b64(os.path.join(brain, 'media__1774477141059.png'))
cat_b64 = b64(os.path.join(brain, 'media__1774477141102.png'))

# Read all stickers from the stickers folder
stickers_dir = os.path.join(DIR, 'stickers')
sticker_files = glob.glob(os.path.join(stickers_dir, '*.png')) + \
                glob.glob(os.path.join(stickers_dir, '*.jpg')) + \
                glob.glob(os.path.join(stickers_dir, '*.jpeg'))

# Convert all stickers to data URIs
sticker_uris = []
for sticker_path in sticker_files:
    ext = os.path.splitext(sticker_path)[1].lower()
    mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
    uri = f"data:{mime};base64,{b64(sticker_path)}"
    sticker_uris.append(uri)

# Create the JS array
stickers_js = json.dumps(sticker_uris)

with open(os.path.join(DIR, 'template.html'), 'r', encoding='utf-8') as f:
    template = f.read()

dog_audio_b64 = "data:audio/mp3;base64," + b64(os.path.join(DIR, 'audio', 'freesound_community-single-dog-bark-king-charles-spaniel-41366.mp3'))
cat_audio_b64 = "data:audio/mp3;base64," + b64(os.path.join(DIR, 'audio', 'dragon-studio-cute-cat-meow-472372.mp3'))

html = (template
    .replace('__CAT_B64__', cat_b64)
    .replace('__DOG_B64__', dog_b64)
    .replace('__STICKERS_ARRAY__', stickers_js)
    .replace('__CAT_AUDIO_B64__', cat_audio_b64)
    .replace('__DOG_AUDIO_B64__', dog_audio_b64)
)

with open(os.path.join(DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Built V7 index.html ({len(html)} chars, {len(sticker_uris)} stickers)')
