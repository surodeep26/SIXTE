# 1. First simulations
easy simulations to get used to the SIMPUT format for creating files.

Some notes
- [ ] 2 keV absorption effect in the manual which can be corrected using the PHS to PI and also more by including the RMF. these features are produced due to the arf. the arf plot has large changes in this energy region.  
- [ ] energies
	- [ ] emin, emax: energy in which the spectrum is generated to have the flux that has been given in the model. So this is what overrules the flux of the model. note that the relative normalisations do matter, so sixte reads the normalisation ratio of the different components and preserves this.
	- [ ] elow, ehi: energy ranges where the photons are generated. with some bins which can be set.

- [ ]  arf and rmf of eROSITA cannot be directly taken from caldb.

- [ ] background PHA
	- [ ] the sky backgrounds need to be given as a SIMPUT
	- [ ] the instrumental background is taken care of by SIXTE