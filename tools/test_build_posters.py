import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from build_posters import build, SLOT_DIR


class PosterBuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'images/posters/main'
        self.source.mkdir(parents=True)
        (self.root / 'poster-recruitment.html').write_text('募集', encoding='utf-8')
        (self.root / 'index.html').write_text('{{POSTER_COUNT}} {{POSTER_CARDS}}', encoding='utf-8')

    def image(self, name, size=(20, 30)):
        Image.new('RGB', size, '#254438').save(self.source / name)

    def test_add_remove_resize_and_escape(self):
        self.image('poster.png', (2500, 3500))
        self.image('recruitment.png')
        first = build(self.root, self.root / 'first')
        self.assertEqual(len(first), 2)
        self.image('イベント&案内.PNG')
        self.image('new.jpg')
        (self.source / 'ignored.txt').write_text('ignore')
        old = self.root / 'images/posters/old'
        old.mkdir()
        Image.new('RGB', (20, 30)).save(old / 'slot0.png')
        second = build(self.root, self.root / 'second')
        self.assertEqual([r['sourceFile'] for r in second], ['poster.png', 'recruitment.png', 'new.jpg', 'イベント&案内.PNG'])
        self.assertTrue(all(max(r['width'], r['height']) <= 2048 for r in second))
        self.assertEqual(second[0]['height'], 2048)
        manifest = json.loads((self.root / 'second/data/slide_poster_manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['boards'][0]['order'], [2048, 2049, 2050, 2051])
        self.assertTrue((self.root / 'second/images/posters/main/slot0.png').exists())
        self.assertIn('イベント&amp;案内', (self.root / 'second/index.html').read_text(encoding='utf-8'))
        for slot in range(4):
            self.assertTrue((self.root / f'second/{SLOT_DIR}/slot{slot}.png').exists())
        (self.source / 'new.jpg').unlink()
        third = build(self.root, self.root / 'third')
        self.assertEqual(len(third), 3)
        self.assertNotIn('new.jpg', [r['sourceFile'] for r in third])

    def test_invalid_inputs_do_not_create_site(self):
        with self.assertRaises(ValueError):
            build(self.root, self.root / 'empty')
        self.assertFalse((self.root / 'empty').exists())
        for i in range(65):
            self.image(f'{i:02}.png')
        with self.assertRaises(ValueError):
            build(self.root, self.root / 'overflow')
        self.assertFalse((self.root / 'overflow').exists())
        (self.source / '64.png').unlink()
        self.assertEqual(len(build(self.root, self.root / 'maximum')), 64)
        (self.source / '00.png').write_bytes(b'broken png')
        with self.assertRaises(OSError):
            build(self.root, self.root / 'broken')
        self.assertFalse((self.root / 'broken').exists())


if __name__ == '__main__':
    unittest.main()
