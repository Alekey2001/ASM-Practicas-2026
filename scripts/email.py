"""Genera identidades sintéticas del laboratorio sin sobrescribir por defecto."""
import argparse
import csv
import random
import unicodedata
from pathlib import Path

DOMAIN = "aiaco.local"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "emailscorp" / "aiaco_corporate_emails.csv"
HEADER = ["Nombre", "Apellido", "Email"]

nombres = [
    "Alejandro","Carlos","Luis","Miguel","Juan","Pedro","Javier","Diego",
    "Fernando","Ricardo","Andrés","José","Eduardo","Daniel","Roberto",
    "Hugo","Ángel","Raúl","Víctor","Francisco","Sofía","María","Laura",
    "Ana","Fernanda","Gabriela","Patricia","Paola","Valeria","Andrea",
    "Lucía","Diana","Carmen","Verónica","Elena","Karla","Mónica","Sandra"
]

apellidos = [
    "Rodríguez","García","Martínez","López","González","Hernández",
    "Pérez","Sánchez","Ramírez","Torres","Flores","Rivera",
    "Jiménez","Morales","Castillo","Vargas","Ortega","Medina",
    "Navarro","Ruiz","Silva","Rojas","Mendoza","Delgado","Campos"
]

def normalize(value):
    return "".join(char for char in unicodedata.normalize("NFKD", value.lower())
                   if not unicodedata.combining(char))


def generate_records(count=50, seed=None):
    candidates = {
        f"{normalize(first)}.{normalize(last)}@{DOMAIN}": (first, last)
        for first in nombres for last in apellidos
    }
    if not 1 <= count <= len(candidates):
        raise ValueError(f"La cantidad debe estar entre 1 y {len(candidates)}.")
    selected = random.Random(seed).sample(sorted(candidates), count)
    return sorted((*candidates[address], address) for address in selected)


def write_csv(path, records, replace=False):
    # El modo x rechaza de forma atómica un destino ya existente.
    with path.open("w" if replace else "x", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        writer.writerows(records)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, help="Semilla opcional para reproducir los registros.")
    parser.add_argument("--count", type=int, default=50, help="Cantidad de registros (50 por defecto).")
    parser.add_argument("--replace", action="store_true", help="Permite reemplazar explícitamente el CSV existente.")
    args = parser.parse_args(argv)
    try:
        records = generate_records(args.count, args.seed)
        write_csv(OUTPUT_PATH, records, replace=args.replace)
    except FileExistsError:
        parser.exit(1, "El CSV ya existe; usa --replace solo si deseas sustituirlo.\n")
    except (ValueError, OSError) as error:
        parser.exit(1, f"No se generó el CSV: {error}\n")
    print(f"Generados {len(records)} correos sintéticos en {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
