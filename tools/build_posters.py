"""Build EBK's fixed URL slots and manifest from the upload folder."""
import hashlib
import html
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

BOARD_ID = 'world-poster-gallery'
SLOT_DIR = 'images/slide-posters/' + hashlib.sha256(BOARD_ID.encode()).hexdigest()
SUPPORTED = {'.png', '.jpg', '.jpeg', '.webp'}
MAX_POSTERS = 64  # EBK's additional-image capacity; changing it requires a world update.


def build(root, output):
    source = root / 'images/posters/main'
    priority = {'poster.png': 0, 'recruitment.png': 1}
    files = sorted((p for p in source.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED),
                   key=lambda p: (priority.get(p.name, 2), p.name.casefold(), p.name))
    if not 1 <= len(files) <= MAX_POSTERS:
        raise ValueError(f'Upload folder must contain 1–{MAX_POSTERS} images; found {len(files)}')
    # Decode every input before producing a deployable site. A bad upload keeps the previous deployment.
    for path in files:
        if path.is_symlink():
            raise ValueError(f'Symlinks are not supported: {path.name}')
        with Image.open(path) as image:
            image.verify()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(root / 'images', output / 'images')
    shutil.copy2(root / 'poster-recruitment.html', output / 'poster-recruitment.html')
    # Keep the old fixed URLs working for worlds that have not been uploaded again yet.
    for path in (root / 'images/posters/old').glob('slot*.png'):
        target = output / 'images/posters/main' / path.name
        if not target.exists():
            shutil.copy2(path, target)
    (output / SLOT_DIR).mkdir(parents=True)
    rows, cards = [], []
    for slot, path in enumerate(files):
        relative = f'{SLOT_DIR}/slot{slot}.png'
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image).convert('RGBA')
            image.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
            image.save(output / relative, format='PNG')
            width, height = image.size
        title = {'poster.png': 'Cafe & Bar Deltaria', 'recruitment.png': '掲載ポスター募集中'}.get(path.name, path.stem)
        rows.append({'index': 2048 + slot, 'title': title, 'imagePath': relative,
                     'sourceFile': path.name, 'enabled': True, 'link': '', 'width': width, 'height': height})
        cards.append(f'<article><a href="{relative}"><img src="{relative}" alt="{html.escape(title, quote=True)}" loading="lazy"></a>'
                     f'<h2>{slot + 1:02} · {html.escape(title)}</h2>'
                     f'<a href="images/posters/main/{quote(path.name)}">原本画像</a></article>')
    board = {'boardId': BOARD_ID, 'enabled': True, 'title': 'イベントポスター',
             'autoPlay': True, 'transition': 'fade', 'displaySeconds': 6, 'transitionSeconds': 1.2,
             'showControls': True, 'presentationOnly': False,
             'order': [r['index'] for r in rows], 'additionalImages': rows}
    manifest = {'protocol': 'EventBasicKit.SlidePosterManifest', 'schemaVersion': 1, 'boards': [board]}
    (output / 'data').mkdir(exist_ok=True)
    (output / 'data/slide_poster_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    template = (root / 'index.html').read_text(encoding='utf-8')
    assert '{{POSTER_CARDS}}' in template and '{{POSTER_COUNT}}' in template
    (output / 'index.html').write_text(template.replace('{{POSTER_CARDS}}', '\n'.join(cards)).replace('{{POSTER_COUNT}}', str(len(rows))), encoding='utf-8')
    (output / '.nojekyll').touch()
    return rows


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    root = Path(__file__).resolve().parents[1]
    rows = build(root, Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / '_site')
    print(json.dumps({'count': len(rows), 'posters': rows}, ensure_ascii=False, indent=2))
