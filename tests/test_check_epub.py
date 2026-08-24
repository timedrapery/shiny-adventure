from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts import check_epub


class EpubValidationTests(unittest.TestCase):
    def _write_epub(self, path: Path) -> None:
        container = b'''<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>'''
        package = b'''<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/></manifest>
<spine><itemref idref="nav"/></spine></package>'''
        nav = b'''<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Reader</title></head>
<body><nav><a href="nav.xhtml">Home</a></nav></body></html>'''
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("mimetype", b"application/epub+zip", compress_type=zipfile.ZIP_STORED)
            archive.writestr("META-INF/container.xml", container)
            archive.writestr("EPUB/package.opf", package)
            archive.writestr("EPUB/nav.xhtml", nav)

    def test_valid_minimal_epub_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "book.epub"
            self._write_epub(path)
            self.assertEqual(check_epub.validate_epub(path), [])

    def test_broken_internal_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "book.epub"
            self._write_epub(path)
            with zipfile.ZipFile(path, "a") as archive:
                archive.writestr(
                    "EPUB/broken.xhtml",
                    '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>x</title></head><body><a href="missing.xhtml">x</a></body></html>',
                )
            self.assertTrue(any("broken internal link" in item for item in check_epub.validate_epub(path)))


if __name__ == "__main__":
    unittest.main()
