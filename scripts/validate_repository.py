"""Validaciones locales de artefactos públicos; no requiere red ni revisión privada."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".revision-temp", "__pycache__", ".venv"}
PRIVATE_MARKERS = (
    "docs/revision/", "RESULTADOS.md", "PRIVACIDAD.md",
    "clasificacion-imagenes.csv", "inventario-previo.csv",
)


def files_in_clone() -> list[Path]:
    return [path for path in ROOT.rglob("*") if path.is_file() and not any(
        part in EXCLUDED_DIRS or path.relative_to(ROOT).parts[:2] == ("docs", "revision")
        or path.name.startswith("~$") for part in path.relative_to(ROOT).parts)]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def local_markdown_links(path: Path, body: str) -> list[str]:
    links = []
    for line in body.splitlines():
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            continue
        links.extend(match.group(1).strip("< >") for match in re.finditer(
            r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)]+)\)", line))
    return links


def validate() -> dict[str, object]:
    errors: list[str] = []
    skipped: list[str] = []
    counts: dict[str, object] = {}
    files = files_in_clone()
    markdown = [path for path in files if path.suffix.lower() == ".md"]
    for path in markdown:
        body = path.read_text(encoding="utf-8-sig")
        is_errata = relative(path) == "docs/public/FE_DE_ERRATAS.md"
        if not is_errata and any(marker in body for marker in PRIVATE_MARKERS):
            errors.append(f"Referencia a material privado: {relative(path)}")
        for target in local_markdown_links(path, body):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                errors.append(f"Enlace local inválido: {relative(path)} -> {target}")
    counts["markdown"] = len(markdown)

    python_files = [path for path in files if path.suffix.lower() == ".py"]
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Sintaxis Python: {relative(path)} ({exc.msg})")
    counts["python_sintaxis"] = len(python_files)

    png = ROOT / "images/mobile-appsec/mobsf/arranque-anonimizado.png"
    if png.exists():
        data, offset, chunks = png.read_bytes(), 8, []
        while offset + 12 <= len(data):
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            chunks.append(data[offset + 4:offset + 8].decode("ascii", errors="replace"))
            offset += length + 12
        forbidden = {"tEXt", "iTXt", "zTXt", "eXIf"}
        if forbidden.intersection(chunks):
            errors.append("La captura MobSF pública conserva metadatos de texto/EXIF.")
        counts["png_anonimizado_sin_metadatos"] = not forbidden.intersection(chunks)
    else:
        skipped.append("No existe la captura MobSF anonimizada en esta base; control omitido.")

    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True, text=False
    ).stdout.decode("utf-8", errors="replace").split("\0")
    temporary = [path for path in tracked if Path(path).name.startswith("~$")]
    if temporary:
        errors.append("Archivo temporal de Office rastreado: " + ", ".join(temporary))
    counts["archivos_temporales_rastreados"] = len(temporary)

    patterns = (
        rb"(?:AKIA|ASIA)[A-Z0-9]{16}",
        rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        rb"gh[pousr]_[A-Za-z0-9]{30,}",
        rb"\bsk-[A-Za-z0-9]{30,}",
    )
    text_suffixes = {".md", ".txt", ".sql", ".json", ".yml", ".yaml", ".py", ".ps1", ".csv"}
    candidates = [relative(path) for path in files if path.suffix.lower() in text_suffixes
                  and any(re.search(pattern, path.read_bytes()) for pattern in patterns)]
    if candidates:
        errors.append("Candidatos de secretos en texto: " + ", ".join(candidates))
    counts["candidatos_secretos_texto"] = candidates
    counts["sha256_script"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return {"comprobaciones": counts, "omitidas": skipped, "errores": errors}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result["errores"]))
