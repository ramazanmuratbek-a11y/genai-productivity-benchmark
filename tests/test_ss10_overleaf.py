import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'overleaf'

class TestSS10Overleaf(unittest.TestCase):
    def test_manuscript_structure(self):
        main = (PAPER/'main.tex').read_text(encoding='utf-8')
        self.assertIn(r'\documentclass[conference]{IEEEtran}', main)
        for pkg in ('amsmath','booktabs','graphicx','hyperref'):
            self.assertIn(pkg, main)
        for section in ('01_introduction','02_methodology','03_demonstration_results','04_discussion'):
            self.assertIn(r'\input{sections/'+section+'}', main)
            self.assertTrue((PAPER/'sections'/(section+'.tex')).is_file())

    def test_citation_keys_match_bibliography(self):
        bib=(PAPER/'references.bib').read_text(encoding='utf-8')
        cited='\n'.join(p.read_text(encoding='utf-8') for p in (PAPER/'sections').glob('*.tex'))
        keys=set(re.findall(r'@\w+\s*\{([^,\s]+),', bib))
        refs=[x.strip() for group in re.findall(r'\\cite\{([^}]+)\}',cited) for x in group.split(',')]
        self.assertGreaterEqual(len(refs),3)
        self.assertTrue(all(r in keys for r in refs))
        self.assertNotIn('C:' + chr(92) + 'Users' + chr(92),bib)
        self.assertNotIn('file =',bib)
        self.assertNotIn('abstract =',bib)

    def test_methods_labels_and_honest_units(self):
        s=(PAPER/'sections'/'02_methodology.tex').read_text(encoding='utf-8')
        for lbl in ('fig:pipeline','tab:design','eq:pairedtime','eq:factmetrics'):
            self.assertIn(r'\label{'+lbl+'}',s)
        for ref in (r'\ref{fig:pipeline}',r'\ref{tab:design}',r'\eqref{eq:pairedtime}'):
            self.assertIn(ref,s)
        self.assertIn('minutes',s)
        self.assertIn('milliseconds',s)

    def test_synthetic_status_never_confused_with_results(self):
        a=(PAPER/'main.tex').read_text(encoding='utf-8')
        b=(PAPER/'sections'/'03_demonstration_results.tex').read_text(encoding='utf-8')
        self.assertIn('No participants have yet been recruited',a)
        self.assertIn('four fictional participants',b)
        self.assertIn('100 timed Python executions',b)
        self.assertIn('No AI',b)
        self.assertIn('With AI',b)

if __name__ == '__main__': unittest.main()
