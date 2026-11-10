from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


vri = load_module("vri_source", "scripts/vri_source.py")

REPO_ROOT = Path(__file__).resolve().parent.parent


def book(*blocks: str) -> bytes:
    body = "\n".join(blocks)
    xml = f'<?xml version="1.0" encoding="UTF-16"?>\n<TEI.2><text><body>{body}</body></text></TEI.2>'
    return xml.encode("utf-16")


def para(n: str | None, text: str, rend: str = "bodytext") -> str:
    number = f' n="{n}"' if n else ""
    lead = f'<hi rend="paranum">{n}</hi><hi rend="dot">.</hi> ' if n else ""
    return f'<p rend="{rend}"{number}>{lead}{text}</p>'


class FixtureRepo:
    """A throwaway VRI clone with just the books a test needs."""

    def __init__(self, books: dict[str, bytes]) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name, data in books.items():
            (self.root / f"{name}.mul.xml").write_bytes(data)

    def __enter__(self) -> Path:
        vri._book_blocks.cache_clear()
        return self.root

    def __exit__(self, *exc) -> None:
        vri._book_blocks.cache_clear()
        self.tmp.cleanup()


MN_BOOK = book(
    '<head rend="book">Mūlapaṇṇāsapāḷi</head>',
    '<head rend="chapter">1. Mūlapariyāyavaggo</head>',
    '<p rend="subhead">1. Mūlapariyāyasuttaṃ</p>',
    para("1", "Evaṃ me sutaṃ – first discourse."),
    '<p rend="subhead">2. Sabbāsavasuttaṃ</p>',
    para("14", "Sabbāsavasaṃvarapariyāyaṃ vo desessāmi."),
    '<p rend="subhead">Dassanā pahātabbāsavā</p>',
    para(None, "an unnumbered section heading does not start a discourse"),
    '<head rend="chapter">2. Sīhanādavaggo</head>',
    '<p rend="subhead">1. Cūḷasīhanādasuttaṃ</p>',
    para("139", "Idheva, bhikkhave, samaṇo."),
)


class OrdinalTests(unittest.TestCase):
    def test_mn_numbers_count_discourses_across_vaggas(self) -> None:
        with FixtureRepo({"s0201m": MN_BOOK}) as root:
            third = vri.locate("MN 3", local_dir=root)
            second = vri.locate("MN 2", local_dir=root)
        self.assertEqual(third.heading, "1. Cūḷasīhanādasuttaṃ")
        self.assertIn("samaṇo", third.text)
        # An unnumbered section heading belongs to the discourse it sits in.
        self.assertIn("does not start a discourse", second.text)
        self.assertNotIn("Sabbāsavasuttaṃ", second.text, "headings are not passage text")

    def test_a_number_past_the_end_is_not_placed(self) -> None:
        with FixtureRepo({"s0201m": MN_BOOK, "s0202m": book(), "s0203m": book()}) as root:
            self.assertIsNone(vri.locate("MN 9", local_dir=root))


SN_BOOK = book(
    '<head rend="book">Nidānavaggo</head>',
    '<head rend="chapter">1. Nidānasaṃyuttaṃ</head>',
    '<p rend="subhead">1. Paṭiccasamuppādasuttaṃ</p>', para("1", "one"),
    '<p rend="subhead">2. Vibhaṅgasuttaṃ</p>', para("2", "two"),
    '<p rend="subhead">3-5. Tatiyādisuttāni</p>', para("3-5", "three to five"),
    '<p rend="subhead">6. Chaṭṭhasuttaṃ</p>', para("6", "six"),
    '<head rend="chapter">2. Abhisamayasaṃyuttaṃ</head>',
    '<p rend="subhead">1. Nakhasikhāsuttaṃ</p>', para("74", "nail"),
)


class SamyuttaTests(unittest.TestCase):
    def test_samyuttas_count_across_books_and_ranges_count_their_width(self) -> None:
        first = book('<head rend="chapter">1. Devatāsaṃyuttaṃ</head>',
                     '<p rend="subhead">1. Oghataraṇasuttaṃ</p>', para("1", "flood"))
        books = {"s0301m": first, "s0302m": SN_BOOK, "s0303m": book(), "s0304m": book(), "s0305m": book()}
        with FixtureRepo(books) as root:
            self.assertIn("flood", vri.locate("SN 1.1", local_dir=root).text)
            self.assertIn("two", vri.locate("SN 2.2", local_dir=root).text)
            self.assertIn("three to five", vri.locate("SN 2.4", local_dir=root).text)
            self.assertIn("six", vri.locate("SN 2.6", local_dir=root).text)
            self.assertIn("nail", vri.locate("SN 3.1", local_dir=root).text)


class AnguttaraTests(unittest.TestCase):
    def tika(self) -> bytes:
        return book(
            '<head rend="book">Tikanipātapāḷi</head>',
            '<p rend="subhead">1. Titthāyatanādisuttaṃ</p>', para("61", "first half"),
            para("62", "second half, numbered separately by VRI"),
            '<p rend="subhead">3. Venāgapurasuttaṃ</p>', para("63", "venaga"),
            '<p rend="subhead">5. Kesamuttisuttaṃ</p>', para("66", "kalama"),
        )

    def test_paragraph_number_locates_the_discourse(self) -> None:
        books = {name: book() for name in vri.BOOKS["AN"]}
        books["s0402m2"] = self.tika()
        with FixtureRepo(books) as root:
            found = vri.locate("AN 3.61", local_dir=root)
        self.assertEqual(found.heading, "1. Titthāyatanādisuttaṃ")
        self.assertIn("first half", found.text)

    def test_the_tika_offset_shifts_later_citations(self) -> None:
        books = {name: book() for name in vri.BOOKS["AN"]}
        books["s0402m2"] = self.tika()
        with FixtureRepo(books) as root:
            found = vri.locate("AN 3.65", local_dir=root)
        self.assertEqual(found.heading, "5. Kesamuttisuttaṃ")

    def test_the_ten_recollections_share_one_paragraph(self) -> None:
        ekaka = book(para("296", "Buddhānussati."), para("297", "Dhammānussati…pe… upasamānussati."), para("298", "next"))
        books = {name: book() for name in vri.BOOKS["AN"]}
        books["s0401m"] = ekaka
        with FixtureRepo(books) as root:
            self.assertIn("Buddhānussati", vri.locate("AN 1.296", local_dir=root).text)
            self.assertIn("upasamānussati", vri.locate("AN 1.305", local_dir=root).text)
            self.assertIn("upasamānussati", vri.locate("AN 1.300", local_dir=root).text)


class VerseTests(unittest.TestCase):
    def test_a_verse_runs_from_its_number_to_the_next(self) -> None:
        dhp = book(
            '<head rend="chapter">2. Appamādavaggo</head>',
            '<p rend="hangnum" n="21"><hi rend="paranum">21</hi><hi rend="dot">.</hi></p>',
            '<p rend="gatha1">Appamādo amatapadaṃ, pamādo maccuno padaṃ;</p>',
            '<p rend="gathalast">Appamattā na mīyanti, ye pamattā yathā matā.</p>',
            '<p rend="hangnum" n="22"><hi rend="paranum">22</hi><hi rend="dot">.</hi></p>',
            '<p rend="gatha1">Etaṃ visesato ñatvā,</p>',
        )
        with FixtureRepo({"s0502m": dhp}) as root:
            verse = vri.locate("Dhp 21", local_dir=root)
        self.assertIn("Appamādo amatapadaṃ", verse.text)
        self.assertIn("yathā matā", verse.text)
        self.assertNotIn("Etaṃ", verse.text)

    def test_notes_and_page_breaks_are_not_text(self) -> None:
        text = vri.plain('Appamādo <pb ed="V" n="0.0016" /> amatapadaṃ <note>amataṃ padaṃ (ka.)</note>, pamādo')
        self.assertEqual(text, "Appamādo amatapadaṃ , pamādo")


class OfflineTests(unittest.TestCase):
    def test_offline_mode_never_downloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vri._book_blocks.cache_clear()
            previous = os.environ.pop("VRI_TIPITAKA_DIR", None)
            try:
                with self.assertRaises(vri.SourceUnavailable):
                    vri.read_book("s0201m", cache_dir=Path(tmp), allow_fetch=False)
            finally:
                if previous is not None:
                    os.environ["VRI_TIPITAKA_DIR"] = previous
                vri._book_blocks.cache_clear()


class RealEditionTests(unittest.TestCase):
    """Run only where the VRI books are on disk; they are never committed."""

    def setUp(self) -> None:
        cache = REPO_ROOT / ".vri-cache"
        if not (cache / "s0201m.mul.xml").is_file() and not os.environ.get("VRI_TIPITAKA_DIR"):
            self.skipTest("VRI books are not on disk")
        vri._book_blocks.cache_clear()

    def test_known_titles_land_where_they_are_cited(self) -> None:
        expected = {
            "MN 10": "Satipaṭṭhāna", "SN 12.61": "Assutavā", "SN 36.6": "Salla",
            "SN 56.11": "Dhammacakkappavattana", "AN 2.9": "Cariya", "AN 3.65": "Kesamutti",
            "AN 3.136": "Uppādā", "AN 11.12": "Dutiyamahānāma", "Snp 1.8": "Metta",
            "Ud 8.3": "Tatiyanibbānapaṭisaṃyutta", "Iti 44": "Nibbānadhātu", "DN 15": "Mahānidāna",
        }
        for citation, title in expected.items():
            with self.subTest(citation=citation):
                found = vri.locate(citation, allow_fetch=False)
                self.assertIsNotNone(found)
                self.assertIn(title.casefold(), found.heading.casefold())


if __name__ == "__main__":
    unittest.main()
