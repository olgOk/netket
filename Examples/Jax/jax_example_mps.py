import netket as nk
import numpy as np
import jax
from jax.experimental.optimizers import sgd as JaxSgd
import cProfile

# 1D Lattice
L = 16
g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)

# Hilbert space of spins on the graph
hi = nk.hilbert.Spin(graph=g, s=0.5)

ha = nk.operator.Ising(h=1.0, hilbert=hi)

ma = nk.machine.MPSPeriodic(hi, bond_dim=4, diag=False, symperiod=None, dtype=complex)
ma.jax_init_parameters(seed=1232)

# Jax Sampler
sa = nk.sampler.jax.MetropolisLocal(machine=ma, n_chains=8)

# Using a Jax Optimizer
j_op = JaxSgd(0.01)
op = nk.optimizer.Jax(ma, j_op)


# Stochastic Reconfiguration
sr = nk.optimizer.SR(diag_shift=0.1)

# Create the optimization driver
gs = nk.Vmc(
    hamiltonian=ha, sampler=sa, optimizer=op, n_samples=1000, sr=None, n_discard=0
)

# The first iteration is slower because of start-up jit times
gs.run(out="test", n_iter=1)

gs.run(out="test", n_iter=10000)
