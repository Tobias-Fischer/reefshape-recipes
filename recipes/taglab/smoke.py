# Starts TagLab through the installed launcher (offscreen, from another cwd), quits after the main window is up.
import os, sys, tempfile, faulthandler
faulthandler.dump_traceback_later(900, exit=True)
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TAGLAB_MODELS"] = tempfile.mkdtemp()
os.chdir(tempfile.mkdtemp())
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
orig = QApplication.exec
def ex(*a):
    def up():
        print("MAIN WINDOW UP")
        QApplication.quit()
    QTimer.singleShot(3000, up)
    return orig(*a)
QApplication.exec = staticmethod(ex)
import taglab_launcher
sys.argv = ["taglab"]
try:
    taglab_launcher.main()
except SystemExit as e:
    assert e.code in (0, None), e.code
from source.genutils import modelsDir
assert modelsDir() == os.environ["TAGLAB_MODELS"]
print("OK")
# the optional tools' dependencies: Refine border (libcoraline) and Train your network (qhoptim, albumentations)
from coraline.Coraline import lib
assert lib is not None, "libcoraline not found"
import numpy as np
from coraline import Coraline
yy, xx = np.mgrid[:120, :120]
img = np.where(np.hypot(yy - 60, xx - 60) < 30, 200, 60).astype(np.uint8)
img = np.stack([img] * 3, axis=2)
mask = (np.hypot(yy - 60, xx - 60) < 40).astype(np.ubyte)
Coraline.segment(img, None, mask, None, 0.0, conservative=0.1, grow=0, radius=30, depth_weight=0.0)
assert abs(int(mask.sum()) - 2827) < 300, mask.sum()   # a disc of radius 30
import albumentations
import qhoptim.pyt
print("OK tools")
