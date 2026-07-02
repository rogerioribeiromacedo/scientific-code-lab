"""
This program is part of the Master's project.

Description
-----------
Computes the center of mass of a molecular structure and, optionally,
translate the atomic coordinates so that the center of mass is located at the origin.

Input
-----
 - Molecular structure file (e.g. PDB or XYZ).

Output
------
 - Center of mass coordinates.
 - Molecular structure file with the atomic coordinates translated so that the center
   of mass is at the origin.

Usage
-----
    python center_of_mass.py --file <input_file>

    python center_of_mass.py --file <input_file> --translate

    python center_of_mass.py --file <input_file> --translate --output <translated_structure_file>

    python center_of_mass.py --about

"""
from pathlib import Path
import sys
import textwrap

# Command-line arguments.
import argparse
from functools import partial

# Numpy
import numpy as np

#
# About program
# 
NAME = "center_of_mass"
VERSION = "0.0.1"
AUTHOR = "Rogério Ribeiro Macêdo"
GITHUB = "https://github.com/rogerioribeiromacedo"
LINKEDIN = "https://linkedin.com/in/rogerioribeiromacedo"
DESCRIPTION = """The objective of this program is to compute the center of mass of a molecular structure and,
optionally, translate the atomic coordinates so that the center of mass is located at the origin.
"""
USAGE="""python center_of_mass.py --file <input_file>

python center_of_mass.py --file <input_file> --translate

python center_of_mass.py --file <input_file> --translate --output <translated_structure_file>

python center_of_mass.py --about
"""

#
# Atomic masses (amu)
# Source: IUPAC 2021 atomic weights
# https://iupac.org/what-we-do/periodic-table-of-elements/
#
ATOMIC_MASSES: dict[str, float] = {
     "H":   1.008,  "He":   4.003,  "Li":   6.941,  "Be":   9.012,  "B":  10.811,
     "C":  12.011,   "N":  14.007,  "O":   15.999,  "F":   18.998,  "Ne": 20.180,
    "Na":  22.990,  "Mg":  24.305,  "Al":  26.982,  "Si":  28.086,  "P":  30.974,
     "S":  32.060,  "Cl":  35.450,  "Ar":  39.948,  "K":   39.098,  "Ca": 40.078,
    "Fe":  55.845,  "Cu":  63.546,  "Zn":  65.380,  "Br":  79.904,  "Ag": 107.868,
     "I": 126.904,  "Au": 196.967,  "Hg": 200.592,  "Pb": 207.200    
}

class Geometry:
    """
    Class that represents a molecular structure.

    Note
    ----
    The attributes 'coords' and 'coords_translated' are numpy arrays with shape
    (N, 3), where N is the number of atoms in the structure. Each row corresponds to an atom,
    and the columns represent the x, y, and z coordinates, respectively. The choice of using
    numpy arrays allows for effcient manipulation of the atomic coordinates, especially for 
    operations like calculating the center of mass and translating the structure.
    """

    def __init__(self) -> None:
        """
        Initialize attributes.
        
        Returns
        -------
        None

        """
        self.atoms: list[str] = []
        self.coords: np.ndarray = np.zeros((0, 3), dtype=np.float64)            # 0 lines and 3 columns ()x, y, z)
        self.coords_translated: np.ndarray = np.zeros((0, 3), dtype=np.float64) # 0 lines and 3 columns ()x, y, z)
        self.atom_lines: list[str] = []       # Every ATOM/HETATM line in the structure file
        self.start: list[str] = []            # Start part of the structure file
        self.end: list[str] = []              # End part of the structure file

def show_about() -> None:
    """
    Display information about the program.
   
    Returns
    -------
    None

    """
    print("=" * 75)
    print(f"{NAME}  (v{VERSION})")
    print("=" * 75)

    print(f"Author   : {AUTHOR}")
    print(f"GitHub   : {GITHUB}")
    print(f"LinkedIn : {LINKEDIN}")

    print("\nDescription")
    print("-" * 75)
    print(textwrap.fill(DESCRIPTION, width=75))

    print("\nUsage")
    print("-" * 75)
    print(textwrap.dedent(USAGE))

    print("=" * 75)

def valid_file(value: str, expected_ext: list[str]) -> Path:
    """
    Validate the existence and extension of an input file.

    Parameters
    ----------
    value : str
        Path to the file provided by the user.
    expected_ext : list[str]
        Expected file extensions (e.g., ['.pdb', '.xyz', ...])

    Returns
    -------
    Path
        A Path object pointing to the file.

    """
    path = Path(value)

    # File or path not found
    if not path.exists():
        raise argparse.ArgumentTypeError(
            f"File or path not found: {str(path)}"
        )

    # Is file
    if not path.is_file():
        raise argparse.ArgumentTypeError(
            f"Not a file: {str(path)}"
        )
    
    # Suffix
    if path.suffix not in expected_ext:
        raise argparse.ArgumentTypeError(
            f"Expected a file with one of the following extensions: '{expected_ext}' file, got '{path.suffix}'"
        )
    
    return path

def valid_output(value: str, expected_ext: list[str]) -> Path:
    """
    Validate the existence of the directory and output file name informed.

    Parameters
    ----------
    value: str
        Path to the output file provided by the user.
    expected_ext : list[str]
        Expected file extensions (e.g., ['.pdb', '.xyz', ...])
        
    Returns
    -------
    Path
        A Path object pointing to the output file.    

    """
    path = Path(value)

    # Directory not found
    if not path.parent.exists():
        print(f"Error: directory not found: {str(path.parent)}")
        sys.exit(1)

    # Suffix
    if path.suffix not in expected_ext:
        raise argparse.ArgumentTypeError(
            f"Expected a file with one of the following extensions: '{expected_ext}' file, got '{path.suffix}'"
        )

    return path

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed commnad-line arguments

    """
    parser = argparse.ArgumentParser(
        prog="center_of_mass",
        description="Computes the center of mass of a molecular structure."
    )
    #
    # Optional arguments
    #
    optional = parser.add_argument_group(
        title="Optional",
        description="Optional arguments."
    )    
    optional.add_argument(
        "-t", "--translate",
        action="store_true",
        help="Translate the atomic coordinates so that the center of mass is at the origin."        
    )
    optional.add_argument(
        "-o", "--output",
        type=partial(valid_output, expected_ext=[".pdb", ".xyz"]),
        help="Output file name for the translated structure."
    )

    #
    # Required arguments
    #
    required = parser.add_argument_group(
        title="Required",
        description="Required arguments."
    )
    required.add_argument(
        "--file",
        required=True,
        metavar="FILE",
        type=partial(valid_file, expected_ext=[".pdb", ".xyz"]),
        help="Path to the input molecular structure file (e.g., PDB or XYZ)."
    )
    parsed = parser.parse_args()

    return parsed

def print_header() -> None:
    """
    Print the header of the program.

    Returns
    -------
    None

    """
    header = textwrap.dedent(
        '''
        | ---------------------------------------------------------------------------
        |
        | Center of mass calculation program
        |
        | ---------------------------------------------------------------------------
        | Computes the center of mass of a molecular structure.
        | ---------------------------------------------------------------------------
        '''
    )
    print(header)

def read_pdb_file(file_path: Path, geometry: Geometry) -> Geometry:
    """
    Read a PDB file and extract atomic coordinates.

    Parameters
    ----------
    file_path : Path
        Path to the PDB file.
    geometry : Geometry
        Geometry object to store the extracted atomic coordinates.

    Returns
    -------
    Geometry
        Updated Geometry object with atomic coordinates.

    """
    # The variable 'start' indicate if is the initial part of a PDB file.
    # It's necessary for reconstruct the file when --translate is chosen
    start = True
    try:
        with open(file_path) as file:            
            coords = []
            for line in file:
                # Start/End Section
                if start:
                    if line.startswith('ATOM') or line.startswith('HETATM'):
                        start = False
                        geometry.atom_lines.append(line)
                    else:
                        geometry.start.append(line)
                else:
                    if line.startswith('ATOM') or line.startswith('HETATM'):
                        geometry.atom_lines.append(line)
                    else:
                        geometry.end.append(line)

                # Section ATOM/HETATM
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    # Element
                    element = line[76:78].strip()
                    if element not in ATOMIC_MASSES:
                        raise ValueError(f"Unknown atom: {element}")
                    else:
                        geometry.atoms.append(element)

                    # Structure
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append((x, y, z))

            # Adding geometry
            #geometry.set_coords(np.array(coords, dtype=np.float64))
            geometry.coords = np.array(coords, dtype=np.float64)

        if not len(geometry.coords) >= 1:
            raise ValueError("Structure without atoms.")
    except IOError as e:
        print(f"[!]An error occured while reading the file: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"[!]Error: {e}")
        sys.exit(1)

    # Return geometry
    return geometry

def read_xyz_file(file_path: Path, geometry: Geometry) -> Geometry:
    """
    Read an XYZ file and extract atomic coordinates.
    
    Parameters
    ----------
    file_path : Path
        Path to the PDB file.
    geometry : Geometry
        Geometry object to store the extracted atomic coordinates.

    Returns
    -------
    Geometry
        Updated Geometry object with atomic coordinates.

    """
    with open(file_path) as file:
        # Read number of atoms
        num_atoms = int(file.readline().strip())
        geometry.start.append(f"{num_atoms}\n")

        # Read comment line
        comment_line = file.readline().strip()
        geometry.start.append(f"{comment_line}\n")

        # Read atomic coordinates
        coords = []
        for _ in range(num_atoms):
            line = file.readline().strip()
            parts = line.split()
            if len(parts) < 4:
                raise ValueError("Invalid XYZ format: not enough columns.")
            
            element = parts[0]
            if element not in ATOMIC_MASSES:
                raise ValueError(f"Unknown atom: {element}")
            else:
                geometry.atoms.append(element)

            x, y, z = map(np.float64, parts[1:4])
            coords.append((x, y, z))
            
            geometry.atom_lines.append(line + "\n")

        # Adding geometry
        geometry.coords = np.array(coords, dtype=np.float64)

    # Return geometry
    return geometry

def calculate_com(geometry: Geometry) -> np.ndarray:
    """
    Calculate the center of mass of structure.

    Parameters
    ----------
    geometry : Geometry
        Geometry object to store the extracted atomic coordinates.

    Returns
    -------
    np.ndarray:
        Array with the coordinates of center of mass.

    """
    if len(geometry.atoms) == 0:
        raise ValueError("Empty structure.")

    # Atomic mass
    masses = np.array([ATOMIC_MASSES[atom] for atom in geometry.atoms],
                      dtype=np.float64)    

    # Coord
    coords = geometry.coords # geometry.get_coords()

    # Total Mass
    total_mass = np.sum(masses)

    # Center of mass
    com = np.sum(coords * masses[:, None], axis=0) / total_mass

    # Return
    return com

def translate_structure(geometry: Geometry, com: np.ndarray) -> np.ndarray:
    """
    Translates the atomic coordinates so that the center of mass is at the origin.

    Parameters
    ----------
    geometry : Geometry
        Geometry object to store the extracted atomic coordinates.
    com : np.ndarray
        Coordinates of the center of mass.

    Returns
    -------
    np.ndarray
        Array with the translated coordinates.

    """
    coords = geometry.coords # get_coords()
    translated_coords = coords - com

    # Return
    return translated_coords

def write_translated_structure(geometry: Geometry, output_file: Path) -> None:
    """
    Write the translated structure to a file.

    Parameters
    ----------
    geometry : Geometry
        Geometry object to store the extracted atomic coordinates.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        
    """
    with open(output_file, "w") as file:
        # Write start part
        for line in geometry.start: # get_start():
            file.write(line)

        # Translated section
        coords = geometry.coords_translated # get_coords_trans()
        for line, (x, y, z) in zip(geometry.atom_lines, coords):     # get_atom_lines(), coords):
            new_line = (
                line[:30] +
                f"{x:8.3f}{y:8.3f}{z:8.3f}" +
                line[54:]
            )
            if output_file.suffix == ".xyz":
                file.write(new_line + "\n")
            elif output_file.suffix == ".pdb":
                file.write(new_line)

        # Final part
        for line in geometry.end: # .get_end():
            file.write(line)

def main() -> None:
    """
    Main function to execute the center of mass calculation.

    Returns
    ------
    None

    """
    # Arguments
    if "--about" in sys.argv or "-a" in sys.argv:
        show_about()
        sys.exit(0)
    args = parse_args()

    # Translate output file name if not provided
    if args.translate and args.output == None:
        name = args.file.stem + "_translated" + args.file.suffix
        output_file = args.file.parent / name
    else:
        output_file = args.output

    # Print header
    print_header()

    # About file
    print("+ About file.")
    print(f" - Path.....: {args.file.parent}")
    print(f" - {args.file.suffix.replace(".", "").upper()} file.: {args.file.name}")

    # Read structure
    geometry = Geometry()
    file_path = Path(args.file)
    if file_path.suffix == ".pdb":
        geometry = read_pdb_file(file_path=file_path, geometry=geometry)
    elif file_path.suffix == ".xyz":
        geometry = read_xyz_file(file_path=file_path, geometry=geometry)

    # Center of mass
    com = calculate_com(geometry=geometry)
    print("\n+ Center of mass.")
    print(f"  - x = {com[0]:>.6f}\n" \
          f"  - y = {com[1]:>.6f}\n" \
          f"  - z = {com[2]:>.6f}")

    # Translate structure?!
    if args.translate:
        geometry.coords_translated = translate_structure(geometry=geometry, com=com)
        write_translated_structure(geometry=geometry, output_file=output_file)
        print("\n+ Translate structure.")
        print(f"  - Path........: {output_file.parent}")
        print(f"  - Output file.: {output_file.name}")

if __name__ == "__main__":
    main()
