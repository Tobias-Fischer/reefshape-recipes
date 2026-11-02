# QHAdam and QHM minimise a convex quadratic.
import torch
from qhoptim.pyt import QHAdam, QHM

for make in (lambda p: QHAdam(p, lr=0.1, nus=(0.7, 1.0), betas=(0.95, 0.999)),
             lambda p: QHM(p, lr=0.1, momentum=0.9, nu=0.7)):
    x = torch.nn.Parameter(torch.tensor([3.0, -2.0]))
    opt = make([x])
    for _ in range(300):
        opt.zero_grad()
        (x ** 2).sum().backward()
        opt.step()
    assert x.abs().max() < 0.05, x
print("OK")
