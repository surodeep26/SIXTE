import os
import subprocess
from xspec import *
from astropy.io import fits


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
                ra=0, 
                dec=0, 
                srcFlux=2e-11,
                Elow=0.1,
                Eup=10,
                Nbins=1000,
                logEgrid="yes",
                Emin=0.2,
                Emax=2):
        # required
        self.XSPECFile = XSPECFile # input model
        self.Simput = Simput #output SIMPUT file
        
        # optional default
        self.Src_Name = Src_Name
        self.ra = ra
        self.dec = dec
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
            f"RA={self.ra}",
            f"Dec={self.dec}",
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
                ra=0, 
                dec=0):
        # required
        self.Prefix = Prefix #output SIMPUT file
        self.Simput = Simput #output SIMPUT file
        self.Exposure = Exposure
        # optional default
        xmldir = "/home/suro/SIXTE/installation/share/sixte/instruments/srg/erosita"
        self.XMLFile = XMLFile
        if not XMLFile:
            self.XMLFile = f"{xmldir}/erosita_1.xml,{xmldir}/erosita_2.xml,{xmldir}/erosita_3.xml,{xmldir}/erosita_4.xml,{xmldir}/erosita_5.xml,{xmldir}/erosita_6.xml,{xmldir}/erosita_7.xml" # telescope
        self.ra = ra
        self.dec = dec
        self.MJDREF=MJDREF
        self.EvtFile="evt.fits"
    def generate(self):
        sixte_cmd = [
            f"sixtesim",
            f"Prefix={self.Prefix}_",
            f"Simput={self.Simput}",
            f"XMLFile={self.XMLFile}",
            f"MJDREF={self.MJDREF}",
            f"RA={self.ra}",
            f"Dec={self.dec}",
            f"Exposure={self.Exposure}",
            f"EvtFile={self.EvtFile}",
            f"clobber=yes",
        ]
        try:
            subprocess.run(sixte_cmd, check=True)
            print(f"SIXTE event file: '{self.Prefix}_{self.EvtFile}' successfully created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating SIXTE event file: {e}")

class generateSIXTE:
    def __init__(self, name):
        self.name = name
        if not os.path.exists(self.name):
            os.makedirs(os.path.join(self.name, 'products'))
    def generate_model(self, exprString="tbabs*bbodyrad",setPars=None):
        create_model(self, exprString=exprString, 
                     setPars=setPars,
                     save=f"{self.name}/Model_{exprString.replace("*","_")}")
        self.model_file = f"{self.name}/Model_{exprString.replace("*","_")}"
    def generate_SIMPUT(self):
        simput_seed = SIMPUT(XSPECFile=self.model_file,
                             Simput=f"{self.name}/SIMPUT_{self.name}")
        simput_seed.generate()
        self.SIMPUT = f"{self.name}/SIMPUT_{self.name}"
        with fits.open(self.SIMPUT) as f:
            self.SIMPUT_fits = f
    def generate_evts(self):
        sixte_seed = SIXTE(Prefix=self.name, Simput=self.SIMPUT, Exposure=1000)
        sixte_seed.generate()
        self.SIXTE = f"{self.name}/{self.name}_evt.fits"
        with fits.open(self.SIXTE) as f:
            self.event_file = f
        pass
        

s = generateSIXTE('rxj1856')
s.generate_model(exprString="tbabs*bbodyrad", setPars=(12,24,36))
s.generate_SIMPUT()
s.generate_evts()