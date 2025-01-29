import subprocess
from astropy.table import Table, Column
import numpy as np
from astropy import units as u
import os
import sys

input_catalog = sys.argv[1]
# Read and generate the src_merged
table = Table.read(input_catalog)

Infiles = []
#create SIMPUT file for each source
for source in table:
    cmd_string = [
        "simputfile",
        f"RA={source['RA']}",
        f"Dec={source['DEC']}",
        f"srcFlux={source['FLUX']}",
        f"Simput=src_{source['SRC_ID']:03}.fits",
        f"XSPECFile=model_collection/{source['SPECTRUM']}",
        "Emin=0.2",
        "Emax=2.0",
        "clobber=yes",
    ]    
    print(cmd_string)
    subprocess.run(cmd_string, check=True)
    Infiles.append(f"src_{source['SRC_ID']:03}.fits")

#Merge SIMPUTs
Infiles_str = ",".join(Infiles)
cmd = [
    "simputmerge",
    f"Infiles={Infiles_str}",
    f"Outfile=SIMPUT_{input_catalog}",
    "clobber=yes",
    "FetchExtensions=yes"
]
print(cmd)
subprocess.run(cmd, check=True)
subprocess.run(['rm','src_*.fits'], check=True)