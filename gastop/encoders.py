"""encoders.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module contains the ConfigEncoder and PopulationEncoder classes.

"""
import numpy as np
import json

from gastop import Truss


class ConfigEncoder(json.JSONEncoder):
    ''' Encodes config file in JSON format.

    If the object is a numpy array, converts it to a list and appends '__numpy__'
    metadata for decoding.
    '''
    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return {'data': obj.tolist(), '__numpy__': True}
            else:
                return obj.item()
        return super().default(self, obj)


class PopulationEncoder(json.JSONEncoder):
    ''' Encodes population file in JSON format.

    If the object is a numpy array, converts it to a list and appends
    '__numpy__' metadata for decoding. Handles that population is composed
    of truss objects.
    '''
    def default(self, obj):
        if isinstance(obj, Truss):
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
    ''' Decodes JSON files to config and population.

    If the object is has '__numpy__' metadata, converts it to a numpy array.

    Args:
        dct (dict): Dictionary in JSON file.
    Returns:
        dct (dict): Dictionary with numpy arrays decoded.
    '''
    if '__numpy__' in dct:
        return np.array(dct['data'])
    return dct
