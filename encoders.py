import numpy as np
import json

import Truss

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return {'data': obj.tolist(), '__numpy__': True}
            else:
                return obj.item()
        return super().default(self, obj)

class PopulationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Truss.Truss):
            a = obj.__dict__
            for key, val in a.items():
                if type(val).__module__ == np.__name__:
                    if isinstance(val, np.ndarray):
                        a[key] = {'data': val.tolist(), '__numpy__': True}
                    else:
                        a[key] = val.item()
            return a
        return super().default(self, obj)

def numpy_decoder(dct):
    if '__numpy__' in dct:
        return np.array(dct['data'])
    return dct
