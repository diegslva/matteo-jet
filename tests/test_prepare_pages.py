"""Testes do empacotamento; não representam teste do jogo em celular."""
import hashlib
import importlib.util
import json
import stat
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("prepare_pages", ROOT / "scripts/prepare_pages.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.payloads = {name: b"conteudo de teste" for name in module.PUBLIC_FILES}
        self.payloads["build-info.json"] = json.dumps({
            "version": "0.3.1", "build": "teste", "bytes": len(self.payloads["index.html"]),
        }).encode()
        self.config = {"schema": 1, "package": "release.zip", "version": "0.3.1",
                       "build": "teste", "files": {name: {
                           "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                       } for name, data in self.payloads.items()}}
        self.write_package()

    def sync_config(self):
        self.config["sha256"] = hashlib.sha256((self.root / "release.zip").read_bytes()).hexdigest()
        (self.root / "deployment.json").write_text(json.dumps(self.config))

    def write_package(self, extra=None):
        with zipfile.ZipFile(self.root / "release.zip", "w") as archive:
            for name, data in self.payloads.items():
                archive.writestr(name, data)
            if extra:
                archive.writestr(*extra)
        self.sync_config()

    def test_exact_output_and_idempotence(self):
        self.assertEqual(module.prepare(self.root), module.prepare(self.root))
        self.assertEqual({p.name: p.read_bytes() for p in (self.root / "_site").iterdir()}, self.payloads)

    def test_missing_package(self):
        (self.root / "release.zip").unlink()
        with self.assertRaisesRegex(ValueError, "Pacote ausente"):
            module.prepare(self.root)

    def test_wrong_archive_digest(self):
        with (self.root / "release.zip").open("ab") as stream:
            stream.write(b"modificado")
        with self.assertRaisesRegex(ValueError, "SHA-256 do ZIP"):
            module.prepare(self.root)

    def test_unsafe_path(self):
        self.write_package(("../arquivo.html", b"invalido"))
        with self.assertRaisesRegex(ValueError, "nomes inesperados"):
            module.prepare(self.root)

    def test_duplicate_entry(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.write_package(("index.html", b"duplicado"))
        with self.assertRaisesRegex(ValueError, "duplicados"):
            module.prepare(self.root)

    def test_wrong_payload_digest(self):
        self.config["files"]["index.html"]["sha256"] = "0" * 64
        self.sync_config()
        with self.assertRaisesRegex(ValueError, "SHA-256 divergente"):
            module.prepare(self.root)

    def test_mismatched_build(self):
        self.config["build"] = "outro"
        self.sync_config()
        with self.assertRaisesRegex(ValueError, "Versão ou build"):
            module.prepare(self.root)

    def test_symlink_output(self):
        (self.root / "_site").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "link simbólico"):
            module.prepare(self.root)

    def test_unexpected_output(self):
        (self.root / "_site").mkdir()
        (self.root / "_site/privado.txt").write_text("nao publicar")
        with self.assertRaisesRegex(ValueError, "entradas estranhas"):
            module.prepare(self.root)

    def test_symlink_entry(self):
        with zipfile.ZipFile(self.root / "release.zip", "w") as archive:
            for name, data in self.payloads.items():
                info = zipfile.ZipInfo(name)
                if name == "index.html":
                    info.create_system = 3
                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, data)
        self.sync_config()
        with self.assertRaisesRegex(ValueError, "Entrada não permitida"):
            module.prepare(self.root)


if __name__ == "__main__":
    unittest.main()
