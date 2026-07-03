# Initial velocities

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![NumPy](https://img.shields.io/badge/NumPy-Latest-green)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

Generate initial atomic velocities from the Maxwell-Boltzmann distribution.

For a system at temperature T, each Cartesian component of the velocity
(vx, vy, vz) follows a normal distribution with variance related to the
particle mass and temperature. Consequently, the magnitude of the velocity
is consistent with the Maxwell-Boltzmann distribution.

The velocities are generated from uniformly distributed pseudo-random
numbers using the Box-Muller transform, which converts uniform random
variables into normally distributed variables.

This project was developed as part of a Master's research project.

---

## Features

* Generate initial atomic velocities from the Maxwell-Boltzmann distribution.
* Read **XYZ** structure files.
* Write new file with velocities in the same input format.
* Simple command-line interface.

---

## Supported Formats

### Input

* XYZ (`.xyz`)

### Output

* XYZ (`.xyz`)

---

## Requirements

* Python 3.12+

Install the required dependency with:

```bash
pip install numpy
```

---

## Usage

```bash
python initial_velocities.py --file <input_file>.xyz
```

or

```bash
python initial_velocities.py --file <input_file>.xyz --temperature <value>
```

or

```bash
python initial_velocities.py --file <input_file>.xyz --temperature <value> --output <output>.xyz
```

If no output filename is provided, the program creates:

```text
<input_file>_velocities_<temperature>.pdb
```

---

## Example Output

```text
+ Reading XYZ file.
  - Reading lines...
  - Adjust velocities.

+ The total momentum of the system is zero.

+ Saving new file:
  - Path........: ...\initial_velocities\examples
  - Output file.: adenine_velocities_320.xyz
```

---

## Project Structure

```text
initial_velocities/
│
├── README.md
└── LICENSE
└── docs/
    ├── doc_pt-br_initial_velocities.pdf
    └── doc_eng_initial_velocities.pdf
├── examples/
└── src/
    └── initial_velocities.py
```

---

## Limitations

* Only XYZ format are currently supported.
* Atomic masses are obtained from an internal lookup table.

---

## Author

**Rogério Ribeiro Macêdo**

GitHub: <https://github.com/rogerioribeiromacedo>

LinkedIn: <https://linkedin.com/in/rogerioribeiromacedo>

---

## License

This project is distributed under the GPLv3 License.
