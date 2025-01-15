import os
import subprocess
from utils import create_model, SIMPUT
from xspec import *

class Simulation:
    def __init__(self, name, model_string="tbabs*bbodyrad"):
        self.name = name
        self.model_string = model_string
        if not os.path.exists(self.name):
            os.makedirs(os.path.join(self.name, 'products'))
        create_model(self, modelstring=self.model_string, save=f"{self.name}/Model_{model_string.replace("*","_")}")
        self.model_file = f"{self.name}/Model_{model_string.replace("*","_")}"
        self.SIMPUT = SIMPUT(XSPECFile=self.model_file,
                             Simput=f"{self.name}/SIMPUT_{self.name}")
        self.SIMPUT.generate()

s = Simulation('rxj1856')