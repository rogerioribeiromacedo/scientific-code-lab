"""
constants.py
------------
Physical constants and atomic data used in the Maxwell-Boltzmann
velocity generator.

Units are chosen to produce velocities in Angstroms per picosecond (Å/ps),
the standard unit in molecular dynamics simulations.

Unit system
-----------
    Mass        : atomic mass units (amu)
    Length      : Angstroms (Å)
    Time        : picoseconds (ps)
    Temperature : Kelvin (K)
    Velocity    : Å/ps
"""

# ──────────────────────────────────────────────────────────────────────────────
# Physical constants
# ──────────────────────────────────────────────────────────────────────────────

# Boltzmann constant in kJ/(mol * K)
# Consistent with mass in amu and velocity in Å/ps
KB: float = 8.31446e-3  # kJ / mol * K

# ──────────────────────────────────────────────────────────────────────────────
# Atomic masses (amu)
# Source: IUPAC 2021 atomic weights
# https://iupac.org/what-we-do/periodic-table-of-elements/
# ──────────────────────────────────────────────────────────────────────────────
ATOMIC_MASSES: dict[str, float] = {
     "H":   1.008,  "He":   4.003,  "Li":   6.941,  "Be":   9.012,  "B":  10.811,
     "C":  12.011,   "N":  14.007,  "O":   15.999,  "F":   18.998,  "Ne": 20.180,
    "Na":  22.990,  "Mg":  24.305,  "Al":  26.982,  "Si":  28.086,  "P":  30.974,
     "S":  32.060,  "Cl":  35.450,  "Ar":  39.948,  "K":   39.098,  "Ca": 40.078,
    "Fe":  55.845,  "Cu":  63.546,  "Zn":  65.380,  "Br":  79.904,  "Ag": 107.868,
     "I": 126.904,  "Au": 196.967,  "Hg": 200.592,  "Pb": 207.200
}