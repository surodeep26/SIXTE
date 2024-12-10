# Introduction
[[SIXTE_manual.pdf#page=38&selection=9,0,11,43|SIXTE_manual, page 38]]
SIXTE is a Monte Carlo based simulation tool that can simulate observations of astrophysical sources for a wide variety of different current and future X-ray satellites.

A SIXTE simulation consists of three steps:
1. **Preparation of the input [[SIXTE_manual.pdf#page=9&selection=9,0,56,49|SIMPUT files]]**: A model for the target is made. One or more targets can be simulated in a field of view, including point and extended sources. 
2. **Running the simulation**: Photons from all sources that are visible to the instrument are generated using a [[SIXTE_manual.pdf#page=11&selection=0,12,19,12|Monte Carlo algorithm ]]. These photons are then projected onto the focal plane of the instrument using a model for the [[SIXTE_manual.pdf#page=12&selection=49,0,76,38|instrumental optics]] where they are detected using one of the available [[SIXTE_manual.pdf#page=17&selection=221,0,223,19|instrument models]].
3. **Analyzing the simulation**: Step 2 produces one or more FITS event files following HEASARC standards. Standard data products such as spectra and images can be created from the generated event files.
# A Simple Simulation
Until now, the installation must be complete. If not, follow the [[Installation Guide]].
To see if everything is in order so far, we can check the `plist` command to see the parameters of the `simputfile`.

The default parameters of the `simputfile` can be seen using the FTOOL `plist`:
>[!info]
Programs distributed with HEASOFT are called “ftools”. If you want to know more about the parameters of an FTOOL, use the command `fhelp ftoolname` where `ftoolname` is the name of the FTOOL. To get a list of all available FTOOLS, use `fhelp` `ftools`.

To initialize SIXTE and SIMPUT, use the ==`run_script.sh` script:==
```bash
source run_sixte.sh 
```
which contains
```bash
#!/bin/bash
export SIMPUT=/home/suro/SIXTE/installation
export SIXTE=/home/suro/SIXTE/installation

source /home/suro/heasoft-6.34/hea_init.sh
source ${SIXTE}/bin/sixte-install.sh
```
and then run the commands:
```command-line
suro@legion:~/SIXTE$ plist simputfile
Parameters for /home/suro/pfiles/simputfile.par
       Simput = mcrab.fits       output SIMPUT catalog file
      (Src_ID = 1)               source ID
    (Src_Name = none)            source name
          (RA = 0.0)             right ascension (deg)
         (Dec = 0.0)             declination (deg)
     (srcFlux = 0.0)             source flux (erg/s/cm^2)
        (Elow = 0.1)             lower bound of the generated spectrum (keV)
         (Eup = 100.0)           upper bound of the generated spectrum (keV)
       (Estep = 0.0)             deprecated (resolution of the spectrum (keV) )
       (Nbins = 1000)            number of energy bins created from Elow to Eup
    (logEgrid = no)              use a logarithmic energy grid (from Elow to Eup with Nbins)
  (plPhoIndex = 2.0)             power law index
      (plFlux = 0.0)             power law flux (erg/s/cm^2)
        (bbkT = 1.0)             black body temperature (keV)
      (bbFlux = 0.0)             black body flux (erg/s/cm^2)
     (flSigma = 1.0e-3)          Fe line sigma (keV)
      (flFlux = 0.0)             Fe line flux (erg/s/cm^2)
     (rflSpin = 0.0)             rel. Fe line spin
     (rflFlux = 0.0)             rel. Fe line flux (erg/s/cm^2)
          (NH = 0.0)             N_H (10^22 atoms/cm^2)
        (Emin = 1.0)             E_min of reference energy band for fluxes (keV)
        (Emax = 10.0)            E_max of reference energy band for fluxes (keV)
    (ISISFile = none)            ISIS spectral parameter file (*.par)
    (ISISPrep = none)            Additional ISIS script to be executed before loading parameter file.
   (XSPECFile = none)            XSpec spectral model file (*.xcm)
	 .
	 .
	 .
```
A large number of parameters can be used.
In the output of `plist` arguments that are *not* given in parentheses are mandatory, arguments that are listed in parentheses are not mandatory.
## [[SIXTE_manual.pdf#page=39&selection=18,0,20,32|Step 1: Preparing the SIMPUT file]]
**Goal: Produce a SIMPUT file (a FITS file) to be used for SIXTE simulation**

We need a file that will describe the target, i.e., what we want to observe. 
This description is saved in a SIMPUT file. 
A SIMPUT file can be generated manually or with the program `simputfile`. 
A `simputfile` runs as a command line tool and uses the `parfile`-interface, similar to the HEASOFT software.

Generate a SIMPUT-file for a *non-variable* source with a spectrum that can be described by a **simple absorbed power law**.
We can see from the output list above that, in principle, we can specify the source spectrum with the `plPhoIndex`, `plFlux`, and `NH` parameters.
It is better to use the interface: `simputfile` to read a file produced by `XSPEC` and `isis`. This means that as long as a best-fit model for a source is available, it can be used to generate a SIMPUT file.

### 1.1 Generate a model using `XSPEC`
We will produce an `xcm` file for a source that has an absorbed power law spectrum with:
- `norm = 21.6` ($\times 10^{-12}$ ): an unabsorbed flux of $2.16 \times 10^{-11} \text{erg} \ \text{cm}^{-2} \ \text{s}^{-1}$ 
- `PhoIndex = 2.05`: a photon index of $\Gamma=2.05$ and 
- `nH = 0.2`  ($\times10^{22}$): a foreground absorption with an equivalent hydrogen column of $2\times10^{21}\,{\mathrm{cm}}^{-2}$.

To generate this `xcm` file:
```
suro@legion:~/SIXTE$ xspec

		XSPEC version: 12.14.1
	Build Date/Time: Fri Nov 22 16:23:20 2024

XSPEC12>model phabs*pegpwrlw

Input parameter value, delta, min, bot, top, and max values for ...
              1      0.001(      0.01)          0          0     100000      1e+06
1:phabs:nH>0.2
              1       0.01(      0.01)         -3         -2          9         10
2:pegpwrlw:PhoIndex>2.05
              2      -0.01(      0.02)       -100       -100      1e+10      1e+10
3:pegpwrlw:eMin>2
             10      -0.01(       0.1)       -100       -100      1e+10      1e+10
4:pegpwrlw:eMax>10
              1       0.01(      0.01)          0          0      1e+20      1e+24
5:pegpwrlw:norm>21.6

========================================================================
Model phabs<1>*pegpwrlw<2> Source No.: 1   Active/Off
Model Model Component  Parameter  Unit     Value
 par  comp
   1    1   phabs      nH         10^22    0.200000     +/-  0.0          
   2    2   pegpwrlw   PhoIndex            2.05000      +/-  0.0          
   3    2   pegpwrlw   eMin       keV      2.00000      frozen
   4    2   pegpwrlw   eMax       keV      10.0000      frozen
   5    2   pegpwrlw   norm                21.6000      +/-  0.0          
________________________________________________________________________
```

Then produce the flux in the region 2 keV to 10 keV.
```
XSPEC12>flux 2 10
 Model Flux 0.0032845 photons (2.1157e-11 ergs/cm^2/s) range (2.0000 - 10.000 keV)
XSPEC12>save model mcrab.xcm
XSPEC12>quit
Do you really want to exit? (y) 
 XSPEC: quit
```
==This produces the file `mcrab.xcm`==

The `xcm` file looks as follows:
```xcm
method leven 10 0.01
abund angr
xsect vern
cosmo 70 0 0.73
xset delta 0.01
systematic 0
model  phabs*pegpwrlw
            0.2      0.001          0          0     100000      1e+06
           2.05       0.01         -3         -2          9         10
              2      -0.01       -100       -100      1e+10      1e+10
             10      -0.01       -100       -100      1e+10      1e+10
           21.6       0.01          0          0      1e+20      1e+24
bayes off
```

Using `XSPEC` you can see the spectrum defined by the model in `mcrab.xcm`:
(if `XSPEC` was closed before, load it and load the model using `@mcrab.xcm`)
```xspec
cpd /xs
dummyrsp 0.1 15 1000 log
plot model
```
This block opens the `/xs` plotting window, defines a diagonal response matrix from 0.1 to 15 keV with 1000 energy bins on a logarithmic grid, and plots the model.

[[SIXTE_manual.pdf#page=42&selection=24,0,44,8|Exercise]]

### 1.2 Generate the SIMPUT file
`simputfile` allows us to override the flux that is encoded in the `xcm` file when generating the SIMPUT file. This is to allow to use the same model (spectral shape) for multiple sources in order to save disk space.
Shell scripts can be written for generating SIMPUT files:
```bash
#!/bin/bash
base=mcrab
$SIXTE/bin/simputfile \
	Simput=${base}.fits \
	Src_Name=first \
	RA=0.0 \
	Dec=0.0 \
	srcFlux=2.137e-11 \
	Elow=0.1 \
	Eup=15 \
	NBins=1000 \
	logEgrid=yes \
	Emin=2 \
	Emax=10 \
	XSPECFile=${base}.xcm
```
==save this and give it a name, say `mcrab.bash`== and make it executable and execute it. The script makes use of `XSPEC` to get the photon flux as a function of energy on the energy grid specified by the `Elow` and `Eup` arguments.
**==This produces a SIMPUT file called `mcrab.fits`.==**

>[!info]
>Inspect the contents of `mcrab.fits` that we created using HEASOFT.
>First initialize HEASOFT. (simply type heasoft in the command line. [See inside `.bashrc` for the alias](file:///home/suro/.bashrc).)
>Then use `fstruct mcrab.fits` to see an overview of the structure of the file.
```command-line
suro@legion:~/SIXTE$ fstruct mcrab.fits 
  No. Type     EXTNAME      BITPIX Dimensions(columns)      PCOUNT  GCOUNT
 
   0  PRIMARY                 16     0                           0    1
   1  BINTABLE SRC_CAT         8     168(12) 1                   0    1
 
      Column Name                Format     Dims       Units     TLMIN  TLMAX
      1 SRC_ID                     J
      2 SRC_NAME                   32A
      3 RA                         D                   deg
      4 DEC                        D                   deg
      5 IMGROTA                    E                   deg
      6 IMGSCAL                    E
      7 E_MIN                      E                   keV
      8 E_MAX                      E                   keV
      9 FLUX                       E                   erg/s/cm**2
     10 SPECTRUM                   32A
     11 IMAGE                      32A
     12 TIMING                     32A
 
   2  BINTABLE SPECTRUM        8     64(3) 1                  8000    1
 
      Column Name                Format     Dims       Units     TLMIN  TLMAX
      1 ENERGY                     1PE(1000            keV
      2 FLUXDENSITY                1PE(1000            photon/s/cm**2/keV
      3 NAME                       48A

```
The data stored in FITS tables is in FORTRAN data types:
**J**: a 16 bit integer
**32A**: an ASCII-string of 32 characters length
**D**: a double precision floating point number
**E**: a single precision floating point number

This FITS file contains 3 individual tables, called the FITS extensions. 
These are:
`PRIMARY` : contains the header of the FITS file itself.
`BINTABLE SRC_CAT` : made by SIMPUT. Contains the source catalogue. It has 12 columns and 1 row. Each row has a length of 168 bytes: `168(12) 1`
`BINTABLE SPECTRUM` : made by SIMPUT. Contains the spectrum of 1 object in a row with 3 columns (`ENERGY`, `FLUXDENSITY`, `NAME`) of information, each row being 64 bytes in length: `64(3) 1`

## [[SIXTE_manual.pdf#page=44&selection=150,0,152,30|Step 2: Running the simulation]]
With the SIMPUT file `mcrab.fits`, we can run the simulation.
### 2.1 Specify instrument files
The properties of the instruments are stores in XML files. These describe [[SIXTE_manual.pdf#page=17&selection=221,0,223,19|properties like the pixel size, quantum efficiency, etc. ]]
These instrument-specific files can be downloaded from https://www.sternwarte.uni-erlangen.de/sixte/instruments/.
These contain the XML files which are to be stored as `installation/share/sixte/instruments/<instrument_folder>`
In the [current installation](file:///home/suro/SIXTE/installation/share/sixte/instruments), athena-wfi (Athena WFI) and srg (eROSITA) have been installed.
### 2.2 Run the simulation using `sixtesim`
To run the simulation using `sixtesim` we need to:
- specify (locate) the XML file for the instrument
- Point the detector to the target location on the sky
- Set the exposure to a desired value
This is done using the following `bash` script (we call it `athena_sim.bash`):
```bash
#!/bin/bash
base=mcrab
xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_w_filter
xml=${xmldir}/ld_wfi_ff_large.xml

$SIXTE/bin/sixtesim \
	XMLFile=${xml} \
	RA=0.000 Dec=0.000 \
	Prefix=sim_ \
	Simput=${base}.fits \
	EvtFile=evt_${base}.fits \
	Exposure=1000
```
make it executable and execute it. (While executing, if the line `$SIXTE/bin/sixtesim \` produces the error of file not found, try giving the path manually instead of using the `$SIXTE` variable)
NOTE: for this particular code, an incorrect directory is set the manual. 
`xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_w_filter`
and not 
`xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_wo_filter`
==This produces a simulated observation (event file) called `sim_evt_mcrab.fits`==

>[!note]
>Executing the script multiple times overwrites the `sim_evt_mcrab.fits` file
## [[SIXTE_manual.pdf#page=45&selection=94,0,96,32|Step 3: Analyzing the simulation]]
`fstruct` and `fv` or `fdump` can be used to take a look at the structure of the event file.
The number of events simulated differs in each run of the simulation. It was 159616, 239677 etc.

### 3.1 Create an image
>[!note]
>Image can be plotted by simply plotting RAWX and RAWY using `fv`'s plot functionality (very handy).

An image can be generated using `imgev`. Use this directly or as a script:
```bash
$SIXTE/bin/imgev \
	EvtFile=sim_evt_mcrab.fits \
	Image=img_mcrab.fits \
	CoordinateSystem=0 Projection=TAN \
	NAXIS1=512 NAXIS2=512 CUNIT1=deg CUNIT2=deg \
	CRVAL1=0.0 CRVAL2=0.0 CRPIX1=256.5 CRPIX2=256.5 \
	CDELT1=-6.207043e-04 CDELT2=6.207043e-04 \
	history=true clobber=yes
```
==This creates the image in a new file called `img_mcrab.fits`.== 
(This is much smaller in filesize than the event file itself because it only contains a part of the data: the positions of the detections, and not the timestamps and energies for instance)
This can be viewed using DS9.
>[!exercise]
> **Change Pointing**  
> Change the pointing direction of the instrument away from the source in steps of 4' in right ascension and declination simultaneously. Take a look at the images of the source and the source count rate. What do you observe?  
> 
> **Solution:**  
> Use `athena_sim.bash` as the template and edit the `RA` and `DEC` along with the filenames to be produced `Prefix` to:
>
> ```bash
> #!/bin/bash
> base=mcrab
> xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_w_filter
> xml=${xmldir}/ld_wfi_ff_large.xml
> 
> $SIXTE/bin/sixtesim \
> 	XMLFile=${xml} \
> 	RA=0.067 Dec=0.067 \
> 	Prefix=sim_exercise_ \
> 	Simput=${base}.fits \
> 	EvtFile=evt_${base}.fits \
> 	Exposure=1000
> ```
> save it as `athena_sim_exercise.bash` and execute it. This will produce the file `sim_exercise_evt_mcrab.fits` (which 7.7 MB compared to 73.4 MB for `sim_evt_mcrab.fits`.
> Create the image by changing the `CRVAL1` and `CRVAL2` (which define the center of the map. They should in general equal the pointing direction of the simulated observation):
> ```bash
> $SIXTE/bin/imgev \
>	EvtFile=sim_exercise_evt_mcrab.fits \
>	Image=img_exercise_mcrab.fits \
>	CoordinateSystem=0 Projection=TAN \
>	NAXIS1=512 NAXIS2=512 CUNIT1=deg CUNIT2=deg \
>	CRVAL1=0.067 CRVAL2=0.067 CRPIX1=256.5 CRPIX2=256.5 \
>	CDELT1=-6.207043e-04 CDELT2=6.207043e-04 \
>	history=true clobber=yes
>```
> ![[Pasted image 20241210131925.png|450]] ![[Pasted image 20241210131832.png|450]]
> We see that the image appears smaller and to the right (less RA), bottom (less DEC) compared to the previous. This is because the telescope is pointing to a higher RA and DEC.
>The decrease in count rate is due to the vignetting of the telescope, while the increase in image size is due to the astigmatism of the Wolter optics (which is not yet modeled correctly in SIXTE due to lack of information about the precise form of the astigmatism of this telescope).
### 3.2 Create the spectrum
To produce a spectrum, we make use of the tool `makespec`. Like before, the following can be make into a script or simply copy-pasted.
```bash
$SIXTE/bin/makespec \
	EvtFile=sim_evt_mcrab.fits \
	Spectrum=spec_mcrab.pha \
	EventFilter="(RA>359.95 || RA<0.05) && Dec>-0.05 && Dec<+0.05" \
	RSPPath=${xmldir} clobber=yes
```
Note:
- `clobber=yes` overwrites the spectrum file. 
- Make sure to specify the `${xmldir}` directory in previous steps. This is the `RSPPath` that tells SIXTE where the `.rmf` and `.arf` files lie. Otherwise manually enter `xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_w_filter/`
- The `EventFilter` can perform selections on all columns of the FITS file. The selection expression uses the standard C-syntax for logicals, i.e., && means a logical AND, || means a logical OR, and parentheses can be used. SIXTE uses the standard selection syntax offered by the cfitsio-library. Use the command `fhelp rowfilter` to obtain more information about this syntax.
- A `ds9` region file can also be used to perform spatial filtering. For this, you first have to add X,Y sky coordinates and a WCS to the event file with the `radec2xy` tool.
```bash
$SIXTE/bin/radec2xy \
	EvtFile=sim_evt_mcrab.fitsprojection=TAN \
	RefRA=0 RefDec=0
```
where  `RefRA` and `RefDec` define the WCS reference point (which should in general correspond to the pointing direction), and projection sets the WCS projection type. You can then specify the region file in the `makespec` command with
```bash
regfile=ds9.reg
```

The first code produces a `.pha` file that contains the spectrum. This also requires two additional files: `.rmf` and `.arf` which are linked to it. Their location can be found using:
```
fkeyprint
```
and then specifying the keywords `RESPFILE` and `ANCRFILE`.

Loading the spectrum data also displays the location of these files. To simplify things, shortcuts can be made in the current directory to these files using
```bash
ln -s $xmldir/athena_wfi_pirmf_v20230609.rmf 
ln -s $xmldir/athena_wfi_sixte_13rows_w_filter_LDA_v20240209.arf
```

Now we can load the spectrum into XSPEC for analysis:

```xspec
data spec_mcrab.pha
```
and plot it 
```xspec
cpd /xs
plot ldata
setplot energy
plot
```

![[Pasted image 20241210120936.png|450]] ![[Pasted image 20241210120956.png|450]]
There are low counts at low and high energies. Note the feature at 2 keV due to the M-edge of iridium in the mirror material of *Athena*.
To fit a model spectrum, we must ignore these bands where the SNR is small.
```xspec
ignore **-0.3
ignore 4.-**
plot
```
![[Pasted image 20241210121711.png|450]]
now that a spectrum is made, we can fit a model to it.

### 3.3 Fitting model
```xspec
model phabs*power
```
and hit enter 3 times to keep the default values of `nH`, `PhoIndex` and `norm`.

For a better fit, we should rebin the spectrum.
```xspec
grppha spec_mcrab.pha spec_mcrab_rebin.pha
group min 20 & exit
```
for binning with each bin having at least 20 counts. ==This saves the new re-binned spectrum into `spec_mcrab_rebin.pha`==
Now 
```xspec
fit 
```
and then 
```xspec
plot
```
Fitting the spectrum yields a photon index `PhoIndex` of $\Gamma=1.976$ instead of $\Gamma=2.05$ as expected. This is that the flux is so bright that detector effects become important.
Pile up is caused by arrival of 2 or more photons in the same pixel during one read-out cycle of the detector.
Multiple photons hitting adjacent pixels produces valid split patterns that are incorrectly identified with a single photon.
In both cases, the charge, when converted into energy gives the sum of the energies of the photons that hit the detector, resulting in more harder X-ray photons (hardening of the spectrum).

An advantage of simulations over real observations is that we can see and keep track of how these emerged.
We can look at the diagnostic information that is contained in the FITS file and see if the `PILEUP` column has nonzero values. We can use `fstatistic`.
```xspec
fstatistic sim_evt_mcrab.fits PILEUP -
```
which shows
```output
 The sum of the selected column is                   2353.0000
 The mean of the selected column is                 5.16844110E-03
 The standard deviation of the selected column is   7.17059245E-02
 The minimum of selected column is                   0.0000000
 The maximum of selected column is                   1.0000000
 The number of points used in calculation is           455263
```
In this, we see that 2,353 photons were piled up (out of 455,263). I.e., about 0.5% of all events are affected by pileup. This changes the spectral shape compared to the input model.

**complete the exercises [[SIXTE_manual.pdf#page=51&selection=65,0,87,44|SIXTE_manual, page 51]]**

### 3.4 Time Variability
#### 3.4.1 Light Curve
`simputfile` command can be used to create a SIMPUT file with a light curve describing the time variability.
This requires an input ASCII format light curve data. A sample can be downloaded [here](https://www.sternwarte.uni-erlangen.de/~sixte/downloads/example_lightcurve.dat).

The `simputifle` call then looks like this

```bash
#!/bin/bash
$SIXTE/bin/simputfile Simput=mcrab_lightcurve.fits \
	Src_Name=first \
	RA=0.0 \
	Dec=0.0 \
	srcFlux=2.137e-11 \
	Elow=0.1 \
	Eup=15 \
	NBins=1000 \
	logEgrid=yes \
	Emin=2 \
	Emax=10 \
	MJDREF=55000 \
	LCFile=example_lightcurve.dat \
	XSPECFile=mcrab.xcm
```
==This generates a new file called `mcrab_lightcurve.fits`==
This is our SIMPUT file that we will use to simulate a light curve using `sixte`. 
To run the simulation:
```bash
#!/bin/bash
base=mcrab_lightcurve
xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_w_filter
xml=${xmldir}/ld_wfi_ff_large.xml

$SIXTE/bin/sixtesim \
	XMLFile=${xml} \
	RA=0.000 Dec=0.000 \
	Prefix=sim_ \
	Simput=${base}.fits \
	EvtFile=evt_${base}.fits \
	Exposure=1000
```
To make the lightcurve use the `makelc` tool:
```bash
makelc EvtFile=sim_evt_mcrab_lightcurve.fits \
	Lightcurve=sim_mcrab.lc \
	length=1000.0 \
	dt=1.0
```
==This produces the file `sim_mcrab.lc`==

A plot of this lightcurve can be made using:
```bash
suro@legion:~/SIXTE/work/mcrab_athena$ fplot sim_mcrab.lc
Name of X Axis Parameter[error][-] 
Name of Y Axis Parameter[error] up to 8 allowed[ ] counts
Lists of rows[-] 
Device: /XWindow, /XTerm, /TK, /PS, etc[/xs] 
Any legal PLT command[ ]
```
Note: in the X axis, we simply plot the row number of the file – because the output of
`makelc` does not contain TIME column. Instead, it provides header keys that map the row number to
the time of the corresponding bin of the light curve, following conventions for equispaced binned light curves.

**skipping few pages**

# Deep Field Simulations of the WFI

