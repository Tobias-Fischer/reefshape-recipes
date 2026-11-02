import numpy as np, simsimd
a = np.arange(8, dtype=np.float32); b = np.ones(8, np.float32)
assert abs(simsimd.sqeuclidean(a, b) - ((a - b) ** 2).sum()) < 1e-4
# albucore (albumentations 2.0.8) uses this
w = np.frombuffer(simsimd.wsum(a, b, alpha=2, beta=1), dtype=np.float32)
assert np.allclose(w, 2 * a + b)
print("OK")
