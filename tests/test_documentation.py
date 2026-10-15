"""Keep the GitHub landing page multilingual without scripts or file navigation."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_all_languages_expand_inline_and_only_english_starts_open(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        sections = re.findall(r'(<details(?: open)?>)\s*<summary><strong>([^<]+)</strong></summary>(.*?)</details>', readme, re.S)
        self.assertEqual({label for _, label, _ in sections}, {'English', 'Português', '简体中文', 'Español'})
        self.assertEqual([label for tag, label, _ in sections if 'open' in tag], ['English'])
        for _, _, body in sections:
            self.assertIn('repair --apply', body)
            self.assertIn('watch --lang', body)
        self.assertNotIn('<script', readme.lower())

    def test_portuguese_has_no_default_badge(self):
        for path in [ROOT / 'README.md', *list((ROOT / 'docs').glob('README.*.md'))]:
            text = path.read_text(encoding='utf-8')
            for badge in ('Português (padrão)', 'Português (default)', 'Português (predeterminado)', 'Português（默认）'):
                self.assertNotIn(badge, text, str(path))

    def test_local_markdown_file_links_exist(self):
        for path in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                target = target.split('#')[0]
                if not target or target.startswith(('https:', 'http:')):
                    continue
                self.assertTrue((path.parent / target).is_file(), f'{path.relative_to(ROOT)}: {target}')


if __name__ == '__main__':
    unittest.main()
