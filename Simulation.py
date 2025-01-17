import os
import subprocess
from xspec import *
from astropy.io import fits
import glob
from astropy.coordinates import Angle
from astropy import units as u


def create_model(self, exprString:str, setPars:dict=None, frozen=None, save=None):
    self.model_name = exprString.replace("*","_")
    Xset.chatter = 0
    Xset.abund = 'wilm'
    m = Model(exprString, setPars=setPars)
    if (type(save)==str) and (save!=exprString):
        if os.path.exists(f'{save}.xcm'):
            print('WARNING: overwriting model')
            os.remove(f'{save}.xcm')
        Xset.save(fileName=save, info='m')
    elif save:
        if os.path.exists(f'{exprString}.xcm'):
            print('WARNING: overwriting model')
            os.remove(f'{exprString}.xcm')
        Xset.save(fileName=exprString, info='m')
    Xset.chatter = 10 
    return m


class SIMPUT: 
    def __init__(self, XSPECFile, Simput, 
                Src_Name=None, 
                RA=0, 
                Dec=0, 
                srcFlux=2e-11,
                # Elow=0.1,
                Elow=0.2,
                # Eup=10,
                Eup=2,
                Nbins=1000,
                logEgrid="yes",
                Emin=0.2,
                Emax=2):
        # required
        self.XSPECFile = XSPECFile # input model
        self.Simput = Simput #output SIMPUT file
        
        # optional default
        self.Src_Name = Src_Name
        self.RA = RA
        self.Dec = Dec
        self.srcFlux = srcFlux
        self.Elow = Elow
        self.Eup = Eup
        self.Nbins = Nbins
        self.logEgrid = logEgrid
        self.Emin = Emin
        self.Emax = Emax
    def generate(self):
        simputfile_cmd = [
            f"simputfile",
            f"Simput={self.Simput}",
            f"Src_Name={self.Src_Name}",
            f"RA={self.RA}",
            f"Dec={self.Dec}",
            f"srcFlux={self.srcFlux}",
            f"Elow={self.Elow}",
            f"Eup={self.Eup}",
            f"NBins={self.Nbins}",
            f"logEgrid={self.logEgrid}",
            f"Emin={self.Emin}",
            f"Emax={self.Emax}",
            f"XSPECFile={self.XSPECFile}",
        ]
        try:
            subprocess.run(simputfile_cmd, check=True)
            print(f"SIMPUT file '{self.Simput}' successfully created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating SIMPUT file: {e}")

class SIXTE: 
    def __init__(self,
                Prefix,
                Simput,
                Exposure,
                XMLFile:str=None, 
                MJDREF=51543.8975,
                RA=0, 
                Dec=0):
        # required
        self.Prefix = Prefix #output SIMPUT file
        self.Simput = Simput #output SIMPUT file
        self.Exposure = Exposure
        # optional default
        self.xmldir = "/home/suro/SIXTE/installation/share/sixte/instruments/srg/erosita"
        self.XMLFile = XMLFile
        if not XMLFile:
            self.XMLFile = f"{self.xmldir}/erosita_1.xml,{self.xmldir}/erosita_2.xml,{self.xmldir}/erosita_3.xml,{self.xmldir}/erosita_4.xml,{self.xmldir}/erosita_5.xml,{self.xmldir}/erosita_6.xml,{self.xmldir}/erosita_7.xml" # telescope
        self.RA = RA
        self.Dec = Dec
        self.MJDREF=MJDREF
        self.EvtFile="evt.fits"
    def generate(self):
        sixte_cmd = [
            f"sixtesim",
            f"Prefix={self.Prefix}_",
            f"Simput={self.Simput}",
            f"XMLFile={self.XMLFile}",
            f"MJDREF={self.MJDREF}",
            f"RA={self.RA}",
            f"Dec={self.Dec}",
            f"Exposure={self.Exposure}",
            f"EvtFile={self.EvtFile}",
            f"clobber=yes",
        ]
        try:
            subprocess.run(sixte_cmd, check=True)
            print(f"SIXTE event file: '{self.Prefix}_{self.EvtFile}' successfully created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating SIXTE event file: {e}")

class Simulation:
    def __init__(self, name, RA=0, Dec=0, srcFlux=2e-11, Exposure=1000):
        self.name = name
        self.RA = RA
        self.Dec = Dec
        self.srcFlux = srcFlux
        self.Exposure = Exposure
        self.SIMPUT = f"{self.name}/SIMPUT_{self.name}.fits"
        self.SIXTE = f"{self.name}/products/{self.name}_evt.fits"
        self.xmldir = "/home/suro/SIXTE/installation/share/sixte/instruments/srg/erosita"
        
        if not os.path.exists(self.name):
            os.makedirs(os.path.join(self.name, 'products'))
    def generate_model(self, exprString="tbabs*bbodyrad",setPars=None):
        create_model(self, exprString=exprString, 
                     setPars=setPars,
                     save=f"{self.name}/Model_{exprString.replace("*","_")}")
        self.model_file = f"{self.name}/Model_{exprString.replace("*","_")}"
        # self.model_file = glob.glob(f"{self.name}/Model*")[0]
        
    def generate_SIMPUT(self):
        simput_seed = SIMPUT(XSPECFile=self.model_file,
                             Simput=f"{self.name}/SIMPUT_{self.name}.fits",
                             RA=self.RA,
                             Dec=self.Dec,
                             srcFlux=self.srcFlux)
        simput_seed.generate()
        # with fits.open(self.SIMPUT) as f:
        #     self.SIMPUT_fits = f
    def generate_evts(self):
        sixte_seed = SIXTE(Prefix=self.name, Simput=self.SIMPUT, Exposure=self.Exposure)
        sixte_seed.generate()
        merge_cmd = [
            f"ftmerge",
        ]
        merge_cmd.append(','.join(glob.glob("*.fits")))
        merge_cmd.append(f"{self.name}_evt.fits")
        merge_cmd.append("clobber=yes")
        subprocess.run(merge_cmd, check=True)
        subprocess.run(rf"mv {self.name}_*.fits {self.name}/products/", shell=True)
        # with fits.open(self.SIXTE) as f:
        #     self.event_file = f
        # pass
    
    def generate_image(self):
        cmd = [
            "imgev",
            f"EvtFile={self.SIXTE}",
            f"Image={self.name}/products/Image_{self.name}.fits",
            "CoordinateSystem=0",
            "Projection=TAN",
            "CUNIT1=deg",
            "CUNIT2=deg",
            "NAXIS1=384",
            "NAXIS2=384",
            "CRVAL1=0.0",
            "CRVAL2=0.0",
            "CDELT1=-0.0027778",
            "CDELT2=0.00277778",
            "CRPIX1=192.5",
            "CRPIX2=192.5",
            "clobber=yes"
        ]
        subprocess.run(cmd, check=True)

    def generate_spec(self):
        def coordinate_range_string(ra, dec, tolerance):
            # Convert inputs to Angle objects
            ra_angle = Angle(ra * u.deg).wrap_at(360 * u.deg)
            dec_angle = Angle(dec * u.deg)

            # Define the RA and Dec bounds
            ra_min = (ra_angle - tolerance * u.deg).wrap_at(360 * u.deg)
            ra_max = (ra_angle + tolerance * u.deg).wrap_at(360 * u.deg)
            dec_min = dec_angle - tolerance * u.deg
            dec_max = dec_angle + tolerance * u.deg

            # Construct the string
            return (
                f"(RA>{ra_min.degree:.2f} || RA<{ra_max.degree:.2f}) && "
                f"Dec>{dec_min.degree:.2f} && Dec<+{dec_max.degree:.2f}"
            )
        cmd = [
            "makespec",
            f"EvtFile={self.SIXTE}",
            f"Spectrum={self.name}/spectrum_{self.name}.pha",
            f'EventFilter={coordinate_range_string(self.RA,self.Dec,0.05)}', #check .reg file usage in manual
            f"RSPPath={self.xmldir}",
            "clobber=yes"
        ]
        subprocess.run(cmd, check=True)
        
s = Simulation('rxj1856_5k',Exposure=5_000)
s.generate_model(exprString="tbabs*bbodyrad", setPars=(5e-3,60e-3))
s.generate_SIMPUT()
s.generate_evts()
s.generate_image()
s.generate_spec()