"""Pruebas locales aisladas: no reemplazan el CSV versionado."""
import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('email.py')


class EmailGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        (self.root / 'emailscorp').mkdir()
        (self.root / 'otro-directorio').mkdir()
        self.script = self.root / 'scripts/email.py'
        shutil.copyfile(SCRIPT, self.script)
        self.output = self.root / 'emailscorp/aiaco_corporate_emails.csv'

    def run_generator(self, *args):
        return subprocess.run([sys.executable, str(self.script), *args],
                              cwd=self.root / 'otro-directorio', capture_output=True)

    def test_destination_header_format_count_unique_and_seed(self):
        result = self.run_generator('--seed', '42')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'aiaco_corporate_emails.csv').exists())
        self.assertFalse((self.root / 'otro-directorio/aiaco_corporate_emails.csv').exists())
        with self.output.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.reader(handle))
        self.assertEqual(rows[0], ['Nombre', 'Apellido', 'Email'])
        self.assertEqual(len(rows) - 1, 50)
        self.assertEqual(len({row[2] for row in rows[1:]}), 50)
        for row in rows[1:]:
            self.assertEqual(len(row), 3)
            self.assertRegex(row[2], r'^[a-z]+\.[a-z]+@aiaco\.local$')
        first = hashlib.sha256(self.output.read_bytes()).digest()
        self.assertEqual(self.run_generator('--seed', '42', '--replace').returncode, 0)
        self.assertEqual(hashlib.sha256(self.output.read_bytes()).digest(), first)

    def test_existing_file_requires_replace(self):
        sentinel = b'contenido que no debe sobrescribirse\n'
        self.output.write_bytes(sentinel)
        self.assertNotEqual(self.run_generator('--seed', '1').returncode, 0)
        self.assertEqual(self.output.read_bytes(), sentinel)
        self.assertEqual(self.run_generator('--seed', '1', '--replace', '--count', '7').returncode, 0)
        with self.output.open(encoding='utf-8', newline='') as handle:
            self.assertEqual(len(list(csv.reader(handle))), 8)

    def test_invalid_counts_do_not_create_output(self):
        for count in ('0', '-1', '951'):
            with self.subTest(count=count):
                self.assertNotEqual(self.run_generator('--count', count).returncode, 0)
                self.assertFalse(self.output.exists())

    def test_all_combinations_terminate_without_duplicates(self):
        self.assertEqual(self.run_generator('--seed', '4', '--count', '950').returncode, 0)
        with self.output.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 950)
        self.assertEqual(len({row['Email'] for row in rows}), 950)


if __name__ == '__main__':
    unittest.main()
