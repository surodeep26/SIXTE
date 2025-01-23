from xspec import *
from astropy.table import Table


class XspecModel:
    def __init__(self, exprString):
        self.exprString = exprString
        m = Model(self.exprString)
        m.values