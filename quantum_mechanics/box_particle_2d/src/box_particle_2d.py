"""
This program was developed as part of a mandatory teaching internship during my Master's
studies, specifically to address a topic in Physical Chemistry III (Quantum Chemistry).

Description
-----------
Visualize the stationary states of a quantum particle in a two-dimensional infinite
potential well. The user specifies the quantum numbers nx and ny and the box dimensions
Lx and Ly. The script plots the probability density |psi|^2 as as 3D surface.

Input
-----
 - nx: quantum number in the x direction.
 - ny: quantum number in the y direction.
 - Lx and Ly: box dimensions along the x and y directions, respectively.

Output
------
 - A 3D surface plot of the probabilitiy density.
 - An energy-level diagram highlighting the corresponding energy level.

Usage
-----
    python box_particle_2d.py <nx_value> <ny_value> <lx_value> <ly_value>

    python box_particle_2d.py <nx_value> <ny_value> <lx_value> <ly_value> --show

Future Update
-------------
 - Plotting the corresponding energy level in an energy-level diagram.

"""
import argparse
from pathlib import Path

# Numpy
import numpy as np

# Matplotlib
import matplotlib.pyplot as plt
# Setting parameters for Matplotlib
plt.rcParams.update({
    # Sets Helvetica as the preferred sans-serif font (Matplotlib's default is DejaVu Sans)
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"],
    "font.size": 14,

    # Allows True Type fonts to be embedded when saving the figure as a PDF (vector PDF)
    "pdf.fonttype": 42,

    # PNG
    "savefig.dpi": 300,

    # Figure
    "savefig.bbox": "tight",
})

def psi(x: np.ndarray,
        y: np.ndarray, 
        nx: int,
        ny: int,
        lx: float,
        ly: float) -> np.ndarray:
    """
    Calculate the value of wave function.

    Parameters
    ----------
    x, y: np.ndarray
        X and Y values for axis.
    nx, ny: int
        Quantum numbers in the x and y direction.
    lx, ly: float 
        Dimensions along the x and y directions, respectively.

    Returns
    -------
    np.ndarray
        Wave function value.

    """
    return np.sqrt(4 / (lx * ly)) * np.sin(nx * np.pi * x / lx) * np.sin(ny * np.pi * y / ly)

def positive_quantum_number(value: str) -> int:
    """
    Guarantee that quantum number is an integer number strictly positive.

    Parameters
    ----------
    value: str
        Quantum number informed.

    Returns
    -------
    int
        Quantum number

    """
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not a valid number for quantum number. Must be strictly posite."
        )
    if n <= 0:
        raise argparse.ArgumentTypeError(
            f"Quantum number must be strictly positive. Received: {value}."
        )
    
    return n

def positive_dimension(value: str) -> float:
    """
    Guarantee that box dimension is an float number strictly positive.

    Parameters
    ----------
    value: str
        Box dimension informed.

    Returns
    -------
    float
        Box dimension.

    """
    try:
        l = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not a valid number for box dimension. Must be strictly posite."
        )
    if l <= 0.0:
        raise argparse.ArgumentTypeError(
            f"Box dimension must be strictly positive. Received: {value}."
        )
    
    return l

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.

    """
    parser = argparse.ArgumentParser(
        prog="box_particle_2d",
        description="plots the probability density of a quantum particle in a box."
    )    
    parser.add_argument(
        "nx",
        type=positive_quantum_number,
        help="Quantum number in the x direction"
    )
    parser.add_argument(
        "ny",
        type=positive_quantum_number,
        help="Quantum number in the y direction"
    )
    parser.add_argument(
        "lx",
        type=positive_dimension,
        help="Box dimension along the x direction"
    )
    parser.add_argument(
        "ly",
        type=positive_dimension,
        help="Box dimension along the y direction"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the result and don't save."
    )    
    
    parsed = parser.parse_args()
    return parsed

def plot_state(args: argparse.Namespace, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> None:
    """
    Plot surface.

    Parameters
    ----------
    args: argparse.Namespace
        Arguments
    x, y, z: np.ndarray
        Axis values

    Returns
    -------
    None
    
    """
    # Figure
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(projection="3d")

    # Plotting surface
    ax.plot_surface(x, y, z,
                    cmap="cool",
                    antialiased=True,
                    rstride=1,
                    cstride=1,
                    shade=False)

    # Remove grid
    ax.grid(False)

    # Remove tick marks and numerical values
    ax.set_xticks([])
    ax.set_yticks([])
    ax.zaxis.set_ticks([])

    # Axis labels
    ax.set_xlabel("x", labelpad=-10)
    ax.set_ylabel("y", labelpad=-10)
    ax.set_zlabel("")

    # Title
    title = rf"$|\psi_{{{args.nx}, {args.ny}}}|^{2}$"
    ax.text2D(0.05, 0.95, title, transform=ax.transAxes,
              fontdict={"fontsize":30})

    # Configure the box walls
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane = getattr(axis, "pane", None)
        if pane is not None:
            pane.fill = True            
            pane.set_facecolor("#F4FFF8")
            pane.set_visible(True)

            # No line for zaxis
            if axis is ax.zaxis:
                line = getattr(axis, "line", None)
                if line is not None:
                    line.set_linewidth(0)

    # Save figure    
    if not args.show:
        current_dir = Path.cwd()                                                 # Current directory
        file_name = f"box_particle_2d_{args.nx}_{args.ny}_{args.lx}_{args.ly}.png"   # Figure name
        file_path = (current_dir / file_name)                # Path
        plt.savefig(file_path,
                    facecolor=ax.get_facecolor())

        # Close the window
        plt.close(fig)
    else:
        plt.show()

def main() -> None:
    """
    Main function.

    Returns
    ------
    None

    """
    # Command-line arguments
    args = parse_args()

    # Values
    x = np.linspace(0, args.lx, 100)
    y = np.linspace(0, args.ly, 100)
    X, Y = np.meshgrid(x, y)
    Z = psi(X, Y,
            nx=args.nx,
            ny=args.ny,
            lx=args.lx,
            ly=args.ly) ** 2

    # Plot surface
    plot_state(args=args, x=X, y=Y, z=Z)

if __name__ == "__main__":
    main()
