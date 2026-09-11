"""Valida a entrega aprovada e prepara somente os arquivos públicos do Pages."""
from __future__ import annotations

import hashlib
import json
import platform
import stat
import sys
import traceback
import zipfile
from pathlib import Path

TOOL_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parent.parent
PUBLIC_FILES = frozenset({
    "index.html", "manifest.webmanifest", "service-worker.js", "icon-192.png",
    "icon-512.png", "favicon.svg", "build-info.json", ".nojekyll",
})
MAX_PACKAGE_BYTES = 25 * 1024 * 1024
MAX_EXTRACTED_BYTES = 64 * 1024 * 1024


def prepare(root: Path) -> dict[str, object]:
    config = json.loads((root / "deployment.json").read_text(encoding="utf-8"))
    if config.get("schema") != 1 or set(config["files"]) != PUBLIC_FILES:
        raise ValueError("Manifesto de publicação incompatível ou incompleto.")
    package_name = config["package"]
    if not isinstance(package_name, str) or Path(package_name).name != package_name:
        raise ValueError("O pacote precisa estar na raiz do repositório.")
    package = root / package_name
    if not package.is_file() or package.is_symlink():
        raise ValueError(f"Pacote ausente: envie {package_name} para a raiz da branch main.")
    if package.stat().st_size > MAX_PACKAGE_BYTES:
        raise ValueError("O pacote excede o limite configurado.")
    if hashlib.sha256(package.read_bytes()).hexdigest() != config["sha256"]:
        raise ValueError("SHA-256 do ZIP diverge da entrega aprovada; publicação interrompida.")
    payloads: dict[str, bytes] = {}
    with zipfile.ZipFile(package) as archive:
        entries = archive.infolist()
        if len(entries) != len(PUBLIC_FILES) or {e.filename for e in entries} != PUBLIC_FILES:
            raise ValueError("O ZIP contém nomes inesperados, ausentes ou duplicados.")
        if sum(e.file_size for e in entries) > MAX_EXTRACTED_BYTES:
            raise ValueError("Conteúdo descompactado excede o limite configurado.")
        for entry in entries:
            if entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16) or entry.flag_bits & 1:
                raise ValueError(f"Entrada não permitida no pacote: {entry.filename}.")
            expected = config["files"][entry.filename]
            if entry.file_size != expected["bytes"]:
                raise ValueError(f"Tamanho divergente em {entry.filename}.")
            payload = archive.read(entry)
            if hashlib.sha256(payload).hexdigest() != expected["sha256"]:
                raise ValueError(f"SHA-256 divergente em {entry.filename}.")
            payloads[entry.filename] = payload
    metadata = json.loads(payloads["build-info.json"])
    if metadata.get("version") != config["version"] or metadata.get("build") != config["build"]:
        raise ValueError("Versão ou build do jogo diverge do manifesto de publicação.")
    if metadata.get("bytes") != len(payloads["index.html"]):
        raise ValueError("Metadados não correspondem ao tamanho do HTML.")
    site = root / "_site"
    if site.is_symlink():
        raise ValueError("A pasta de publicação não pode ser um link simbólico.")
    site.mkdir(exist_ok=True)
    if any(p.name not in PUBLIC_FILES or p.is_symlink() or not p.is_file() for p in site.iterdir()):
        raise ValueError("A pasta _site contém entradas estranhas à publicação.")
    for name, payload in payloads.items():
        (site / name).write_bytes(payload)
    return {"version": config["version"], "build": config["build"],
            "files": len(payloads), "bytes": sum(map(len, payloads.values())), "output": "_site"}


def main() -> int:
    print(json.dumps({"level": "info", "event": "pages_preparation_start",
                      "tool_version": TOOL_VERSION, "runtime": platform.python_version(),
                      "config": {"max_package_bytes": MAX_PACKAGE_BYTES}}), flush=True)
    try:
        result = prepare(ROOT)
    except Exception as error:
        print(json.dumps({"level": "error", "event": "pages_preparation_failed",
                          "message": str(error), "stack": traceback.format_exc()},
                         ensure_ascii=False), file=sys.stderr, flush=True)
        return 1
    print(json.dumps({"level": "info", "event": "pages_preparation_complete", **result}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
