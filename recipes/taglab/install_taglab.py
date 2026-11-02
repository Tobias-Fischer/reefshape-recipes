"""Install the TagLab tree into $PREFIX/share/taglab and the launcher into site-packages
(Python, so the same script works on Windows and Unix)."""
import os
import shutil
from pathlib import Path

prefix, sp_dir = Path(os.environ["PREFIX"]), Path(os.environ["SP_DIR"])
dest = prefix / "share" / "taglab"
dest.mkdir(parents=True, exist_ok=True)
skip = shutil.ignore_patterns("__pycache__", "*.pth", "*.dll")
for d in ("source", "models", "icons", "fonts", "dictionaries"):
    shutil.copytree(d, dest / d, ignore=skip, dirs_exist_ok=True)
# Coraline: the Python wrapper only; the library is the libcoraline package
shutil.copytree("coraline", dest / "coraline", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("src", "__pycache__", "*.dll", "*.so", "*.dylib", "CMakeLists.txt", "*.pro", "*.sh"))
for f in ("TagLab.py", "config.json", "TAGLAB_VERSION", "LICENSE", "taglab_launcher.py"):
    shutil.copy2(f, dest / f)
sp_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2("taglab_launcher.py", sp_dir / "taglab_launcher.py")
