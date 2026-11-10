
import os
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

files = {
    "Events": "data_processed/vela_gti.fits",
    "Counts cube": "data_processed/vela_counts_cube_full.fits",
    "Livetime cube": "data_processed/vela_ltcube.fits",
    "Exposure cube": "data_processed/vela_exposure_cube.fits",
}

print("=" * 65)
print("VELA FERMI-LAT: LIKELIHOOD INPUT VALIDATION")
print("=" * 65)

for name, path in files.items():
    print(f"\n{name}: {path}")
    print("Exists:", os.path.exists(path))

    if not os.path.exists(path):
        continue

    with fits.open(path) as hdul:
        hdul.info()

        if name == "Events":
            print("Event count:", len(hdul["EVENTS"].data))
            print("GTI intervals:", len(hdul["GTI"].data))

        elif name == "Counts cube":
            data = hdul[0].data
            print("Shape:", data.shape)
            print("Total counts:", np.sum(data))
            print("Energy extensions:",
                  [h.name for h in hdul])
            if "EBOUNDS" in hdul:
                eb = hdul["EBOUNDS"].data
                print("Energy columns:", eb.names)
                print("Energy lower bounds:", eb["E_MIN"])
                print("Energy upper bounds:", eb["E_MAX"])
            print("WCS:")
            print(WCS(hdul[0].header).celestial)

        elif name == "Exposure cube":
            data = hdul[0].data
            print("Shape:", data.shape)
            print("Minimum:", np.nanmin(data))
            print("Maximum:", np.nanmax(data))

            if "ENERGIES" in hdul:
                energy_data = hdul["ENERGIES"].data
                print("Energy columns:", energy_data.names)
                print("Energy values:")
                print(energy_data.field(0))

            print("WCS:")
            print(WCS(hdul[0].header).celestial)

        elif name == "Livetime cube":
            print("Extensions:", [h.name for h in hdul])

print("\n" + "=" * 65)
print("SOFTWARE VERSIONS")
print("=" * 65)

import fermipy
import astropy
import scipy

print("Fermipy:", fermipy.__version__)
print("Astropy:", astropy.__version__)
print("NumPy:", np.__version__)
print("SciPy:", scipy.__version__)

print("\nVALIDATION INSPECTION COMPLETE")
