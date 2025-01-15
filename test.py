from astropy import units as u
import subprocess
import os
from xspec import *

# s = SIMPUT(XSPECFile="mymodel.xcm", Simput="file.fits", Src_Name='rxj1856')
# s.generate()

class Simulation:
    def __init__(self, name):
        self.name = name
              
    class SIMPUT: 
        def __init__(self, XSPECFile, Simput, 
                    sixte_path='/home/suro/SIXTE/installation',
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
            self.sixte_path = sixte_path
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
                f"{self.sixte_path}/bin/simputfile",
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
            except FileNotFoundError:
                print(f"Error: `simputfile` command not found in {self.sixte_path}.")
        
    def generateFolder(self):
        if not os.path.exists(self.name):
            os.mkdir(self.name)
            for subfolder in ['model','simput','products']:
                os.mkdir(os.path.join(self.name, subfolder))
            
    def create_model(self, modelstring:str, setPars:dict=None, frozen=None, save=None):
        self.model_name = modelstring.replace("*","_")
        Xset.chatter = 0
        Xset.abund = 'wilm'
        m = Model(modelstring, setPars=setPars)
        if (type(save)==str) and (save!=modelstring):
            if os.path.exists(f'{save}.xcm'):
                print('WARNING: overwriting model')
                os.remove(f'{save}.xcm')
            Xset.save(fileName=save, info='m')
        elif save:
            if os.path.exists(f'{modelstring}.xcm'):
                print('WARNING: overwriting model')
                os.remove(f'{modelstring}.xcm')
            Xset.save(fileName=modelstring, info='m')
        Xset.chatter = 10 
        return m
    
    def create_SIMPUT(self):
        s = self.SIMPUT(XSPECFile=f"{self.name}/model/mymodel.xcm", Simput=f"{self.name}/simput/{self.name}_{self.model_name}.fits", Src_Name='rxj1856')
        s.generate()
simulation = Simulation('rxj1856')
simulation.generateFolder()
simulation.create_model(modelstring="TBabs*bbodyrad", save=f"{simulation.name}/model/mymodel.xcm")
simulation.create_SIMPUT()