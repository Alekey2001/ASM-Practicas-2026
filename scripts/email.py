import csv
import random
from pathlib import Path

DOMAIN = "aiaco.local"

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

emails = set()

while len(emails) < 50:
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)

    usuario = (
        nombre.lower()
        .replace("á","a")
        .replace("é","e")
        .replace("í","i")
        .replace("ó","o")
        .replace("ú","u")
        + "."
        + apellido.lower()
        .replace("á","a")
        .replace("é","e")
        .replace("í","i")
        .replace("ó","o")
        .replace("ú","u")
    )

    emails.add((nombre, apellido, f"{usuario}@{DOMAIN}"))

emails = sorted(list(emails))
output_path = Path(__file__).resolve().parent.parent / "aiaco_corporate_emails.csv"

with open(output_path,"w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Nombre",
        "Apellido",
        "Email"
    ])

    writer.writerows(emails)

print(f"Generados {len(emails)} correos.")