from xspec import *
from astropy.table import Table

def parameters(m:Model):
    component_dict = {}
    for component in m.componentNames:
        component_obj = getattr(m, component)
        component_name = component_obj.name 
        component_dict[component_name] = {} 
        for param in component_obj.parameterNames:
            param_obj = getattr(component_obj, param)
            component_dict[component_name][param_obj.name] = param_obj.values
    # Create an empty list to store the data for each component
    data = []
    # Iterate through the components and their parameters
    for i, (component, parameters) in enumerate(component_dict.items()):
        for param_name, param_values in parameters.items():
            row_data = {
                'component_index': i + 1,
                'component': component,
                'parameter': param_name,
                'value': param_values[0],
                'step': param_values[1],
                'Elow': param_values[2],
                'Emin': param_values[3],
                'Emax': param_values[4],
                'Eup': param_values[5]
            }
            data.append(row_data)
    # Create the Astropy Table
    parameters = Table(rows=data, names=('component_index', 'component', 'parameter', 'value', 'step', 'Elow', 'Emin', 'Emax', 'Eup'))
    return parameters

def parameters_pd(m:Model):
    return parameters(m).to_pandas()

def save_model(m:Model, fileName=None):
     if not fileName:
         fileName = f"Model_{m.expression}"
     Xset.save(fileName=fileName, info='m')
     return

def load_model(path):
    Xset.restore(path)
    model = AllModels(1)
    return model

# class XspecModel:
#     Xset.abund = 'wilm'
#     def __init__(self, exprString, **kwargs):
#         m = Model(exprString, **kwargs)
#         self.exprString = exprString
#         self.expression = m.expression
#         self.parameters = parameters(m)
#         self.parameters_pd = parameters_pd(m)
#         self.Model = m
#         return
#     def save(self, fileName=None):
#         save_model(self.Model, fileName=fileName)
    
#     def load(self, path):
#         self.Model = load_model(path)
        

        
        
        
        
