import astropy
import healpy
import fermipy
import subprocess

print("Python environment OK")
print("Astropy OK")
print("Healpy OK")
print("Fermipy OK")

gtselect_path = subprocess.check_output(["which", "gtselect"]).decode().strip()
print("gtselect:", gtselect_path)
