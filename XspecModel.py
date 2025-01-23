from xspec import *
from astropy.table import Table


class XspecModel:
    def __init__(self, exprString, **kwargs):
        self.exprString = exprString
        m = Model(exprString, **kwargs)
        self.expression = m.expression
        # Create a dictionary to store component and parameter information
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
                    'val': param_values[0],
                    'step': param_values[1],
                    'Elow': param_values[2],
                    'Emin': param_values[3],
                    'Emax': param_values[4],
                    'Eup': param_values[5]
                }
                data.append(row_data)
        # Create the Astropy Table
        model_params = Table(rows=data, names=('component_index', 'component', 'parameter', 'val', 'step', 'Elow', 'Emin', 'Emax', 'Eup'))
        # Print the model_params
        self.model_params_pd = model_params.to_pandas()
        self.model_params = Table.from_pandas(self.model_params_pd)
        return
    
    # def save(self, self)
        
        
        
