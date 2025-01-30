
from xspec import *
import os

model_collection_folder = 'model_collection'

def create_model(exprString:str, setPars:dict=None, save=None):
    model_name = exprString.replace("*","_")
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


if not os.path.exists(model_collection_folder):
    print('no model collection folder found, making one')
    os.makedirs(model_collection_folder)
else:
    print('model_collection folder exists.')
create_model(exprString='tbabs*bbody+bbody', save=f'{model_collection_folder}/Model_mymodel')