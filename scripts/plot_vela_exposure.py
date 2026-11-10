import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.visualization.wcsaxes import SphericalCircle
import astropy.units as u

# Files
exposure_file = "data_processed/vela_exposure_cube.fits"
counts_file = "data_processed/vela_counts_map.fits"

# Load exposure
with fits.open(exposure_file) as hdul:
    exposure_cube = hdul[0].data.astype(float)
    header = hdul[0].header
    energies = hdul["ENERGIES"].data.field(0)

# Select plane nearest 1 GeV
idx = np.argmin(np.abs(energies - 1000))
exposure = exposure_cube[idx]

# Load counts map
with fits.open(counts_file) as hdul:
    counts = hdul[0].data.astype(float)
    counts_wcs = WCS(hdul[0].header).celestial

wcs = WCS(header).celestial

# Logarithmic exposure
log_exposure = np.log10(np.maximum(exposure, 1))

# Figure
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection=wcs)

im = ax.imshow(
    log_exposure,
    origin="lower",
    cmap="cividis",
    interpolation="nearest"
)

# Overlay counts contours
levels = [1, 2, 4, 8, 16, 32]
ax.contour(
    counts,
    levels=levels,
    colors="white",
    linewidths=0.7,
    alpha=0.65,
    transform=ax.get_transform(counts_wcs)
)

# Vela position
vela = SkyCoord(128.836*u.deg, -45.176*u.deg, frame="icrs")

ax.plot_coord(
    vela,
    marker="*",
    color="red",
    markersize=14,
    markeredgecolor="white",
    markeredgewidth=0.8
)

# 10-degree ROI boundary
roi = SphericalCircle(
    vela,
    10*u.deg,
    edgecolor="red",
    facecolor="none",
    linewidth=1.5,
    linestyle="--",
    transform=ax.get_transform("world")
)
ax.add_patch(roi)

# Coordinate grid
ax.coords.grid(
    color="white",
    alpha=0.4,
    linestyle=":"
)

ax.set_xlabel("Right Ascension (J2000)")
ax.set_ylabel("Declination (J2000)")

ax.set_title(
    "Fermi-LAT Vela Field\n"
    "Exposure at 1 GeV with Photon Count Contours",
    fontsize=14,
    pad=18
)

cbar = plt.colorbar(im, ax=ax, pad=0.08)
cbar.set_label(r"$\log_{10}(\mathrm{Exposure}/[\mathrm{cm^2\,s}])$")

plt.tight_layout()

plt.savefig(
    "plots/vela_exposure_publication.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
