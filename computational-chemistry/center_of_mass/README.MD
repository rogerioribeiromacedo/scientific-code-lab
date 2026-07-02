# Center of Mass

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![NumPy](https://img.shields.io/badge/NumPy-Latest-green)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)


A Python program to compute the **center of mass (COM)** of a molecular structure and, optionally, translate the atomic coordinates so that the center of mass is located at the origin.

This project was developed as part of a Master's research project and is intended as a lightweight command-line utility for molecular structure analysis.

---

## Features

* Compute the center of mass of a molecular structure.
* Translate atomic coordinates to place the center of mass at the origin.
* Read **PDB** and **XYZ** structure files.
* Write translated structures in the same input format.
* Simple command-line interface.

---

## Supported Formats

### Input

* PDB (`.pdb`)
* XYZ (`.xyz`)

### Output

* PDB (`.pdb`)
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

### Compute the center of mass

```bash
python center_of_mass.py --file structure.pdb
```

or

```bash
python center_of_mass.py --file structure.xyz
```

---

### Translate the structure

```bash
python center_of_mass.py --file structure.pdb --translate
```

If no output filename is provided, the program creates:

```text
structure_translated.pdb
```

---

### Specify an output filename

```bash
python center_of_mass.py \
    --file structure.pdb \
    --translate \
    --output translated_structure.pdb
```

---

## Example Output

```text
+ Center of mass.
  - x = -0.125374
  - y =  3.245671
  - z =  1.542913
```

---

## Project Structure

```text
center_of_mass/
│
├── center_of_mass.py
├── README.md
└── LICENSE
```

---

## Method

The center of mass is computed according to

[
\mathbf{R}_{CM}
===============

\frac{\sum_i m_i \mathbf{r}_i}
{\sum_i m_i}
]

where:

* (m_i) is the mass of atom *i*;
* (\mathbf{r}_i) is its Cartesian coordinate.

Atomic masses are taken from the IUPAC standard atomic weights.

---

## Limitations

* Only PDB and XYZ formats are currently supported.
* The program assumes that the element symbol is correctly defined in the input file.
* Atomic masses are obtained from an internal lookup table.

---

## Future Improvements

Possible future extensions include:

* Support for additional molecular formats.

---

## Author

**Rogério Ribeiro Macêdo**

GitHub: <https://github.com/rogerioribeiromacedo>

LinkedIn: <https://linkedin.com/in/rogerioribeiromacedo>

---

## License

This project is distributed under the MIT License.
