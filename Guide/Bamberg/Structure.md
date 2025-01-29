

# 1. Generate a catalog (pre-SIMPUT)
This catalog should contain the sources.
RA, Dec, srcFlux, ModelParameters

The model parameters column would contain the pandas dataframe/ astropy table of the model parameters that are extracted from the wrapper function I made.

(additionally new columns can be included for extended sources and images for aligning and conataining the data according to SIMPUT standards)

# 2. Generate the SIMPUT
We make a function that:
1. takes in the pre-SIMPUT catalog and generates the spectra from the model parameters.
2. takes in the model spectra generated and create the SIMPUT file
## 2.1. Generate the model spectra from ModelParameters column
Instead of linking to the spectrum, the model parameters are contained in the catalog before. This information the then actually the ideal model spectrum instead of the actual spectrum.
These need to be generated using xspec. This introduces a dependency on xspec being available.

## 2.2. Generating the SIMPUT catalog
From the catalog made in 1. and the models made accordingly, we can generate SIMPUT files for the sources.

# 3. Generate the simulated data using SIXTE
Using the SIMPUT files created, the simulation can be run with chosen exposure times.
For flexibility and comparison purposes, the function here should also be useful for other instruments. 