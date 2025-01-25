import subprocess
from astropy.table import Table, Column
import numpy as np
from astropy import units as u
import os

# generate random sources

# Number of sources in the table
n_rows = 10

# Generate random values for RA and Dec within realistic ranges
ra_values = np.random.uniform(350, 360, n_rows).astype(np.float32)  # Right Ascension in degrees
dec_values = np.random.uniform(85, 90, n_rows).astype(np.float32)  # Declination in degrees

# Generate random flux values (arbitrary positive values)
flux_values = np.random.uniform(1e-15, 1e-10, n_rows).astype(np.float32)

# Generate random model names (choosing from a few predefined models)
model_names = np.random.choice(os.listdir("model_collection"), n_rows)

# Generate source numbers
source_numbers = np.arange(1, n_rows + 1)

# Create the table
table = Table()
table.add_column(Column(data=source_numbers, name='SourceNumber'))
table.add_column(Column(data=ra_values, name='RA', unit=u.deg, dtype=np.float32))
table.add_column(Column(data=dec_values, name='Dec', unit=u.deg, dtype=np.float32))
table.add_column(Column(data=flux_values, name='srcFlux', dtype=np.float32))
table.add_column(Column(data=model_names, name='XSPECFile'))

# Write the table to a FITS file
table.write("catalog1.fits", format='fits', overwrite=True)





# Read and generate the src_merged
table = Table.read("catalog1.fits")

Infiles = []
#create SIMPUT file for each source
for source in table:
    cmd_string = [
        "simputfile",
        f"RA={source['RA']}",
        f"Dec={source['Dec']}",
        f"srcFlux={source['srcFlux']}",
        f"Simput=src_{source['SourceNumber']:03}.fits",
        f"XSPECFile=model_collection/{source['XSPECFile']}",
        "Emin=0.2",
        "Emax=2.0",
        "clobber=yes",
    ]    
    print(cmd_string)
    subprocess.run(cmd_string, check=True)
    Infiles.append(f"src_{source['SourceNumber']:03}.fits")

#Merge SIMPUTs
Infiles_str = ",".join(Infiles)
cmd = [
    "simputmerge",
    f"Infiles={Infiles_str}",
    f"Outfile=src_merged.fits",
    "clobber=yes",
    "FetchExtensions=yes"
]
print(cmd)
subprocess.run(cmd, check=True)
