"""Task 4 / SS11 source integrity checks. Structural checks, not PDF layout validation."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'overleaf'
SECTIONS = PAPER / 'sections'


def source_text():
    names = ['main.tex'] + [f'sections/{n:02d}_{name}.tex' for n,name in [
        (1,'introduction'), (2,'methodology'), (3,'demonstration_results'),
        (4,'discussion'), (5,'conclusion')]]
    return '\n'.join((PAPER / name).read_text(encoding='utf-8') for name in names)


class TestTask4SS11Paper(unittest.TestCase):
    def test_main_document_and_five_sections(self):
        main = (PAPER / 'main.tex').read_text(encoding='utf-8')
        self.assertEqual(main.count(r'\begin{document}'), 1)
        self.assertEqual(main.count(r'\end{document}'), 1)
        self.assertIn(r'\documentclass[conference]{IEEEtran}', main)
        for section in ['01_introduction', '02_methodology', '03_demonstration_results',
                        '04_discussion', '05_conclusion']:
            self.assertTrue((SECTIONS / (section + '.tex')).is_file())
            self.assertIn(r'\input{sections/' + section + '}', main)
        self.assertIn(r'\bibliography{references}', main)

    def test_abstract_word_limit(self):
        main = (PAPER / 'main.tex').read_text(encoding='utf-8')
        match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', main, flags=re.S)
        self.assertIsNotNone(match)
        cleaned = re.sub(r'\\[a-zA-Z]+', '', match.group(1))
        count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", cleaned))
        self.assertGreaterEqual(count, 150, f'Abstract too short: {count} words')
        self.assertLessEqual(count, 250, f'Abstract too long: {count} words')

    def test_twelve_distinct_sources_all_cited(self):
        bibliography = (PAPER / 'references.bib').read_text(encoding='utf-8')
        keys = re.findall(r'@\w+\s*\{([^,\s]+),', bibliography)
        self.assertEqual(len(keys), 12)
        self.assertEqual(len(set(keys)), 12)
        citations = {key.strip() for group in re.findall(r'\\cite\s*\{([^}]+)\}', source_text())
                     for key in group.split(',')}
        self.assertEqual(citations, set(keys), 'Missing or unused bibliography citation key')
        for forbidden in ('file =', 'abstract =', 'C:\\Users\\', 'file:///'):
            self.assertNotIn(forbidden, bibliography)

    def test_no_undefined_or_duplicated_references(self):
        paper = source_text()
        labels = re.findall(r'\\label\s*\{([^}]+)\}', paper)
        refs = re.findall(r'\\(?:ref|eqref)\s*\{([^}]+)\}', paper)
        self.assertEqual(len(labels), len(set(labels)), 'Duplicate LaTeX label')
        self.assertTrue(set(refs).issubset(set(labels)), f'Undefined references: {set(refs)-set(labels)}')
        self.assertIn('fig:writing_time', labels)
        self.assertIn('fig:writing_time', refs)
        self.assertIn('sec:conclusion', refs)

    def test_figure_present_and_used(self):
        path = PAPER / 'fig1_latency_vs_load.pdf'
        self.assertTrue(path.is_file())
        self.assertTrue(path.read_bytes().startswith(b'%PDF-'))
        results = (SECTIONS / '03_demonstration_results.tex').read_text(encoding='utf-8')
        self.assertIn(r'\includegraphics', results)
        self.assertIn('fig1_latency_vs_load.pdf', results)
        self.assertIn('condition-wise', results)
        self.assertIn('fictional', results)

    def test_synthetic_disclosure_and_units(self):
        paper = source_text()
        self.assertIn('No real participants have been recruited', paper)
        self.assertIn('four fictional participant pairs', paper)
        self.assertIn('100 measured Python software executions', paper)
        self.assertIn('3.875 minutes', paper)
        self.assertIn('milliseconds', paper)


if __name__ == '__main__':
    unittest.main()
