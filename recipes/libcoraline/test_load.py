# The library is where TagLab's loader looks, and has the C entry points it calls through ctypes.
import ctypes, os, sys
p = sys.prefix
if sys.platform == "win32":
    f = os.path.join(p, "Library", "bin", "coraline.dll")
elif sys.platform == "darwin":
    f = os.path.join(p, "lib", "libcoraline.dylib")
else:
    f = os.path.join(p, "lib", "libcoraline.so")
lib = ctypes.CDLL(f)
lib.Coraline_segment
lib.Coraline_mutual
print("OK", f)
