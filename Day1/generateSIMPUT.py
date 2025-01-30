from astropy.io import fits
import numpy as np
import os
from xspec import *

# Number of sources in the table
n_rows = 100

# Generate random values for RA and Dec within realistic ranges
ra_values = np.random.uniform(340, 351, n_rows).astype(np.float32)  # Right Ascension in degrees
dec_values = np.random.uniform(85, 88, n_rows).astype(np.float32)  # Declination in degrees

# Generate random flux values
flux_values = np.random.uniform(1e-13, 1e-12, n_rows).astype(np.float32)

# Choose models from the model_collection
model_names = np.random.choice(os.listdir("model_collection"), n_rows)

# Generate source numbers
source_numbers = np.arange(1, n_rows + 1).astype(np.int32)

# Create FITS columns
col1 = fits.Column(name='SRC_ID', array=source_numbers, format='J')
col2 = fits.Column(name='RA', array=ra_values, format='E', unit='deg')
col3 = fits.Column(name='DEC', array=dec_values, format='E', unit='deg')
col4 = fits.Column(name='IMGROTA', array=np.zeros(n_rows), format='E', unit='deg')
col5 = fits.Column(name='IMGSCAL', array=np.ones(n_rows), format='E', unit='deg')
col6 = fits.Column(name='E_MIN', array=np.ones(n_rows)*0.2, format='E', unit='keV')
col7 = fits.Column(name='E_MAX', array=np.ones(n_rows)*2, format='E', unit='keV')
col8 = fits.Column(name='FLUX', array=flux_values, format='E', unit='erg/s/cm**2')
col9 = fits.Column(name='SPECTRUM', array=model_names, format='100A')  # Temporary placeholder
col10 = fits.Column(name='IMAGE', array=['NULL']*n_rows, format='100A')
col11 = fits.Column(name='TIMING', array=['NULL']*n_rows, format='100A')

# Create Binary Table HDU
cols = fits.ColDefs([col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11])
hdu1 = fits.BinTableHDU.from_columns(cols)

# Add required headers
hdu1.header['HDUCLASS'] = 'HEASARC/SIMPUT'
hdu1.header['HDUCLAS1'] = 'SRC_CAT'
hdu1.header['HDUVERS'] = '1.1.0'
hdu1.header['EXTNAME'] = 'SRC_CAT'
hdu1.header['RADESYS'] = 'FK5'
hdu1.header['EQUINOX'] = 2000.0

# Write the first catalog
hdu1.writeto('catalog1.fits', overwrite=True)

# Read the catalog and generate spectral data
pretable = fits.open('catalog1.fits')[1].data

src = []
energies = []
values = []

Xset.chatter = 0

def load_model(path):
    Xset.restore(path)
    model = AllModels(1)
    return model

for src_id, model_filename_string in enumerate(pretable['SPECTRUM']):
    # modelstring = model_filename_string.replace('Model_', '').replace('.xcm', '')
    m = load_model('model_collection/'+model_filename_string)
    # m = Model(modelstring)
    src.append(str(src_id+1))
    energies.append(m.energies(0)[1:])  # Take the center of the bins
    values.append(m.values(0))

# Create Spectral FITS Table
c1 = fits.Column(name='NAME', array=src, format='100A')
c2 = fits.Column(name='ENERGY', array=energies, format=f'{len(energies[0])}D', unit='keV')
c3 = fits.Column(name='FLUXDENSITY', array=values, format=f'{len(values[0])}D', unit='photon/s/cm**2/keV')

hdu2 = fits.BinTableHDU.from_columns([c1, c2, c3])

# Add required headers for the spectrum table
hdu2.header['HDUCLASS'] = 'HEASARC/SIMPUT'
hdu2.header['HDUCLAS1'] = 'SPECTRUM'
hdu2.header['HDUVERS'] = '1.1.0'
hdu2.header['EXTNAME'] = 'SPECTRUM'

# Write the intermediate FITS file
hdulist = fits.HDUList([fits.PrimaryHDU(), hdu1, hdu2])
hdulist.writeto('final.fits', overwrite=True)

# Replace values in SPECTRUM column (NOT adding a new column)
with fits.open('final.fits', mode='update') as hdul:
    table_data = hdul[1].data  # Get HDU1 data
    spec_column = table_data['SPECTRUM']

    for i in range(len(spec_column)):
        spec_column[i] = f"[SPECTRUM,1][NAME=='{table_data['SRC_ID'][i]}']"

    # Save changes to the file
    hdul.flush()

# Cleanup intermediate files
os.remove('catalog1.fits')

print("Final FITS file 'final.fits' created successfully with updated SPECTRUM column!")
