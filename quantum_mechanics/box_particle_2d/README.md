# 2D Particle in a Box

A Python program to visualize the stationary states of a quantum particle in a two-dimensional infinite potential well.

The program plots the probability density \(|\psi(x,y)|^2\) as a 3D surface.

## Requirements

- Python 3
- NumPy
- Matplotlib

## Usage

```bash
python box_particle_2d.py NX NY LX LY
```

Where:
- `NX`, `NY`: Positive integer quantum numbers.
- `LX`, `LY`: Positive box dimensions.

To display the plot instead of saving it:

```bash
python box_particle_2d.py NX NY LX LY --show
```

## Example

```bash
python box_particle_2d.py 2 3 10 15
```

## License

See the repository license for details.