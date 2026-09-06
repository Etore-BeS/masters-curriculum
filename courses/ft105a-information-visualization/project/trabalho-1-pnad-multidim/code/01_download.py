#!/usr/bin/env python3
"""Download PNAD Continua microdata + dictionary from IBGE FTP (HTTPS)."""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

COURSE_DATA = Path(__file__).resolve().parents[3] / "data"
RAW = COURSE_DATA / "raw"
RAW.mkdir(parents=True, exist_ok=True)

MICRO_URL = (
    "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
    "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/"
    "Trimestral/Microdados/2026/PNADC_022026.zip"
)
DICT_URL = (
    "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
    "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/"
    "Trimestral/Microdados/Documentacao/Dicionario_e_input_20221031.zip"
)
DOWNLOADS = {
    "PNADC_022026.zip": MICRO_URL,
    "Dicionario_e_input_20221031.zip": DICT_URL,
}


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"SKIP (exists): {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    print(f"GET {url}")
    urllib.request.urlretrieve(url, dest)
    print(f"OK  {dest.name} ({dest.stat().st_size:,} bytes)")


def main() -> int:
    for name, url in DOWNLOADS.items():
        try:
            download(url, RAW / name)
        except Exception as exc:  # noqa: BLE001
            print(f"FAILED {name}: {exc}", file=sys.stderr)
            return 1
    print("Done. Next: 02_import_pnadc.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
