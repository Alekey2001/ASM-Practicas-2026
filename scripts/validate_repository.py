"""Validaciones locales sin red, secretos en salida ni cambios en el repositorio."""
import ast
import csv
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate():
    errors = []
    counts = {}
    files = [p for p in ROOT.rglob('*') if p.is_file() and not any(
        part in {'.git', '.revision-temp', '__pycache__', '.venv'}
        for part in p.relative_to(ROOT).parts
    ) and p.relative_to(ROOT).parts[:2] != ('docs', 'revision') and not p.name.startswith('~$')]
    markdown = [p for p in files if p.suffix == '.md']
    link_count = 0
    for path in markdown:
        body = path.read_text(encoding='utf-8-sig')
        visible = []
        fence = None
        for line in body.splitlines():
            marker = re.match(r'^\s*(`{3,}|~{3,})', line)
            if marker:
                token = marker.group(1)
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence):
                    fence = None
            elif fence is None:
                visible.append(line)
        if fence:
            errors.append(f'Bloque sin cierre: {path.relative_to(ROOT)}')
        content = '\n'.join(visible)
        targets = re.findall(r'!?\[[^\]]*\]\(\s*(<[^>]+>|[^)]+)\)', content)
        targets += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', content, flags=re.M)
        targets += re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', content)
        for target in targets:
            target = target.strip().strip('<>')
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            local = path if not parts.path else (path.parent / unquote(parts.path)).resolve()
            link_count += 1
            if not local.is_relative_to(ROOT) or not local.exists():
                errors.append(f'Enlace local inválido: {path.relative_to(ROOT)} -> {target}')
            elif parts.fragment:
                # No se usan anchors locales actualmente; fallar explícitamente si aparecen.
                errors.append(f'Anchor requiere validación: {path.relative_to(ROOT)} -> {target}')
        if path.as_posix().endswith('docs/public/FE_DE_ERRATAS.md'):
            continue
        if any(marker in body for marker in ('docs/revision/', 'RESULTADOS.md', 'PRIVACIDAD.md',
                                              'clasificacion-imagenes.csv', 'inventario-previo.csv')):
            errors.append(f'Referencia pública a material privado: {path.relative_to(ROOT)}')
    counts['markdown'] = len(markdown)
    counts['enlaces_locales'] = link_count

    python_files = [p for p in files if p.suffix == '.py']
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except SyntaxError:
            errors.append(f'Sintaxis Python: {path.relative_to(ROOT)}')
    counts['python_sintaxis'] = len(python_files)

    classification = ROOT / 'docs/revision/clasificacion-imagenes.csv'
    if classification.exists():
        with classification.open(encoding='utf-8', newline='') as handle:
            mappings = list(csv.DictReader(handle))
        image_paths = {p.relative_to(ROOT).as_posix() for p in files if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.jfif'}}
        if image_paths != {row['destino'] for row in mappings} or len(mappings) != 57:
            errors.append('La clasificación no cubre exactamente las 57 imágenes.')
        for row in mappings:
            target = ROOT / row['destino']
            if not target.exists() or sha256(target) != row['sha256_publico']:
                errors.append('Imagen ausente o modificada después del plan: ' + row['destino'])
        counts['imagenes'] = len(mappings)
        counts['imagenes_bytes_originales'] = sum(row['sha256_original'] == row['sha256_publico'] for row in mappings)
    else:
        counts['imagenes_clasificacion'] = 'omitida: CSV histórico privado no disponible'

    png_path = ROOT / 'images/mobile-appsec/mobsf/arranque-anonimizado.png'
    if png_path.exists():
        png = png_path.read_bytes()
        offset, chunks = 8, []
        while offset + 12 <= len(png):
            length = struct.unpack('>I', png[offset:offset + 4])[0]
            chunks.append(png[offset + 4:offset + 8].decode('ascii', errors='replace'))
            offset += length + 12
        forbidden = {'tEXt', 'iTXt', 'zTXt', 'eXIf'}
        if forbidden.intersection(chunks):
            errors.append('Metadatos adicionales en PNG anonimizado; revisar.')
        counts['png_anonimizado_sin_texto_exif'] = not forbidden.intersection(chunks)
    else:
        counts['png_anonimizado'] = 'omitido: artefacto público no disponible en esta base'

    inventory = ROOT / 'docs/revision/inventario-previo.csv'
    if inventory.exists() and classification.exists():
        with inventory.open(encoding='utf-8-sig', newline='') as handle:
            original = list(csv.DictReader(handle))
        moves = {row['origen']: row['destino'] for row in mappings}
        moves['redes/publicaciones_simuladas.txt'] = 'redes/README_osint.md'
        for row in original:
            path = ROOT / moves.get(row['path'], row['path'])
            if not path.exists():
                errors.append('Original sin destino: ' + row['path'])
            if path.suffix.lower() in {'.pdf', '.pptx'} and sha256(path).lower() != row['sha256'].lower():
                errors.append('Documento binario original alterado: ' + row['path'])
            if row['path'] in {'emailscorp/aiaco_corporate_emails.csv', 'scripts/fault.json'} and sha256(path).lower() != row['sha256'].lower():
                errors.append('Datos originales alterados: ' + row['path'])
        counts['archivos_originales_localizados'] = len(original)
    else:
        counts['inventario_historico'] = 'omitido: insumos privados no disponibles'

    with (ROOT / 'emailscorp/aiaco_corporate_emails.csv').open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if reader.fieldnames != ['Nombre', 'Apellido', 'Email']:
            errors.append('Cabecera CSV incorrecta.')
    if len(rows) != 50 or len({r['Email'] for r in rows}) != 50 or any(not re.fullmatch(r'[a-z]+\.[a-z]+@aiaco\.local', r['Email']) for r in rows):
        errors.append('Formato, cantidad o unicidad del CSV original incorrectos.')
    counts['csv_registros'] = len(rows)

    fixture = json.loads((ROOT / 'scripts/fault.json').read_text(encoding='utf-8-sig'))
    for name in ('emailscorp/mysql/init.sql', 'scripts/database.sql'):
        content = (ROOT / name).read_text(encoding='utf-8-sig')
        values = content.split('VALUES', 1)[1].strip().rstrip(';')
        parsed = ast.literal_eval('[' + re.sub(r'\bNULL\b', 'None', values) + ']')
        expected = [(r['email'], r['password_md5'], r['password_plain']) for r in fixture]
        if parsed != expected:
            errors.append('Fixture SQL/JSON divergente: ' + name)
    counts['fixture_filas'] = len(fixture)
    counts['fixture_texto_plano'] = sum(r['password_plain'] is not None for r in fixture)
    counts['fixture_md5'] = sum(r['password_md5'] is not None for r in fixture)
    counts['fixture_pares_inconsistentes'] = sum(hashlib.md5(r['password_plain'].encode()).hexdigest() != r['password_md5'] for r in fixture if r['password_plain'] is not None)

    sql = (ROOT / 'emailscorp/mysql/sanitize_copy.sql').read_text(encoding='utf-8')
    sql = re.sub(r'--[^\n]*', '', sql)
    if re.search(r'\b(?:DROP|TRUNCATE|DELETE|ALTER|REPLACE)\b', sql, re.I):
        errors.append('Operación destructiva inesperada en saneamiento.')
    if re.search(r'\bUPDATE\s+leaked_credentials\b', sql, re.I):
        errors.append('UPDATE sobre original en saneamiento.')
    if 'SELECT id, email, password_md5, NULL FROM leaked_credentials' not in sql:
        errors.append('La proyección de saneamiento no excluye texto plano.')
    counts['sql'] = 'Fixtures cotejados; revisión textual no destructiva. No es validación del motor MySQL.'

    tracked = subprocess.run(
        ['git', 'ls-files', '-z'], cwd=ROOT, check=True, capture_output=True, text=False
    ).stdout.decode('utf-8', errors='replace').split('\0')
    temporary = [path for path in tracked if Path(path).name.startswith('~$')]
    if temporary:
        errors.append('Archivo temporal de Office rastreado: ' + ', '.join(temporary))
    counts['archivos_temporales_rastreados'] = len(temporary)

    patterns = [rb'(?:AKIA|ASIA)[A-Z0-9]{16}', rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'\bsk-[A-Za-z0-9]{30,}']
    text_suffixes = {'.md', '.txt', '.sql', '.json', '.yml', '.yaml', '.py', '.ps1', '.csv'}
    candidates = []
    for path in files:
        if path.suffix.lower() in text_suffixes and any(re.search(pattern, path.read_bytes()) for pattern in patterns):
            candidates.append(path.relative_to(ROOT).as_posix())
    counts['candidatos_secretos_texto'] = candidates
    if candidates:
        errors.append('Revisar candidatos de secretos (solo rutas registradas).')
    return {'comprobaciones': counts, 'errores': errors}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errores']))
