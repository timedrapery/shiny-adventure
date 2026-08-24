#!/usr/bin/env python3
"""Validate the generated EPUB's container, package, navigation, and links."""

from __future__ import annotations

import argparse
import posixpath
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EPUB = REPO_ROOT / "site" / "downloads" / "osf-pali-readings.epub"
CONTAINER_NS = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
OPF_NS = {"opf": "http://www.idpf.org/2007/opf"}
XHTML_NS = {"x": "http://www.w3.org/1999/xhtml"}


def _archive_target(base: str, href: str) -> str | None:
    split = urlsplit(href)
    if split.scheme or split.netloc or not split.path:
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), unquote(split.path)))


def validate_epub(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.is_file():
        return [f"missing EPUB: {path}"]
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as error:
        return [f"invalid ZIP container: {error}"]
    with archive:
        names = set(archive.namelist())
        infos = archive.infolist()
        if not infos or infos[0].filename != "mimetype":
            failures.append("mimetype must be the first archive entry")
        elif infos[0].compress_type != zipfile.ZIP_STORED:
            failures.append("mimetype must be stored without compression")
        if "mimetype" not in names or archive.read("mimetype") != b"application/epub+zip":
            failures.append("mimetype must contain application/epub+zip exactly")
        container_name = "META-INF/container.xml"
        if container_name not in names:
            return failures + ["missing META-INF/container.xml"]
        try:
            container = ET.fromstring(archive.read(container_name))
        except ET.ParseError as error:
            return failures + [f"container.xml is not valid XML: {error}"]
        rootfile = container.find(".//c:rootfile", CONTAINER_NS)
        package_name = rootfile.get("full-path") if rootfile is not None else None
        if not package_name or package_name not in names:
            return failures + ["container.xml does not point to an existing package document"]
        try:
            package = ET.fromstring(archive.read(package_name))
        except ET.ParseError as error:
            return failures + [f"package document is not valid XML: {error}"]

        manifest: dict[str, str] = {}
        nav_items = 0
        for item in package.findall(".//opf:manifest/opf:item", OPF_NS):
            item_id = item.get("id")
            href = item.get("href")
            if not item_id or not href:
                failures.append("every manifest item needs id and href")
                continue
            target = _archive_target(package_name, href)
            if target is None or target not in names:
                failures.append(f"manifest target is missing: {href}")
            manifest[item_id] = target or ""
            if "nav" in (item.get("properties") or "").split():
                nav_items += 1
        if nav_items != 1:
            failures.append(f"EPUB needs exactly one navigation document; found {nav_items}")
        for itemref in package.findall(".//opf:spine/opf:itemref", OPF_NS):
            idref = itemref.get("idref")
            if not idref or idref not in manifest:
                failures.append(f"spine references missing manifest id: {idref}")

        for name in sorted(names):
            if not name.casefold().endswith((".xhtml", ".html")):
                continue
            try:
                document = ET.fromstring(archive.read(name))
            except ET.ParseError as error:
                failures.append(f"{name}: invalid XHTML ({error})")
                continue
            if document.find(".//x:title", XHTML_NS) is None:
                failures.append(f"{name}: missing title")
            for anchor in document.findall(".//x:a", XHTML_NS):
                href = anchor.get("href")
                if not href:
                    continue
                target = _archive_target(name, href)
                if target is not None and target not in names:
                    failures.append(f"{name}: broken internal link {href}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_EPUB)
    args = parser.parse_args()
    failures = validate_epub(args.path)
    if failures:
        print("EPUB validation failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"EPUB validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
