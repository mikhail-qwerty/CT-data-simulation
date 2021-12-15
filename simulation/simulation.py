import numpy as np
import random
from functools import partial




class TimeFunction():
    def __call__(self, time_i):
        pass

class RandomTimeFunction(TimeFunction):

    def __init__(self, shift=10):
        self.shift = shift
        
    def __call__(self, time_i):
        shift_v = random.randint(-self.shift, self.shift)
        if isinstance(self.shift, (list, tuple)):
            shift_v = random.randint(self.shift[0], self.shift[1])
        return shift_v


class SinTimeFunction(TimeFunction):
    pass

def _shift_flat_filed(flat_field, shift_v, axis=1):

    repl_const = np.min(flat_field)
    flat_field_tr = np.roll(flat_field, shift_v, axis=axis)

    if shift_v < 0:
        shift_v = flat_field.shape[axis] + shift_v + 1
        flat_field_tr[:, shift_v:, :] = repl_const
    else:
        flat_field_tr[:, :shift_v, :] = repl_const
    
    return flat_field_tr


class Augmentation:
    def __call__(self, artifacts):
        pass


class ShiftRingsAugmentation(Augmentation):
    '''
        Create ring by affecting flat_field
    '''
    def __init__(self, detector_options, shift=10):
        self.detector_opt = detector_options
        self.shift = shift
    
    def __call__(self, artifacts):
        
        n_projections = self.detector_opt['n_projections']

        flat_field = artifacts['flat_field']
        
        shift_v = random.randint(-self.shift, self.shift)
        
        if isinstance(self.shift, (list, tuple)):
            shift_v = random.randint(self.shift[0], self.shift[1])
        
        flat_field_tr = _shift_flat_filed(flat_field, shift_v, axis=1)

        return {'flat_field': flat_field_tr, 'input_flat_filed': flat_field}

 

class TimeRingsAugmentation(Augmentation):
    '''
        Create ring by affecting flat_field
    '''
    def __init__(self, detector_options, time_function):
        self.detector_opt = detector_options
        self.time_func = time_function
    
    def __call__(self, artifacts):
        
        n_projections = self.detector_opt['n_projections']
        flat_field = artifacts['flat_field']

        flat_field_tr = self._apply_time_func(flat_field, self.time_func, n_projections)

        return {'flat_field': flat_field_tr, 'input_flat_filed': flat_field}

    def _apply_time_func(self, flat_field, tfunc, n_projs):
        shifted = []
        for i in range(n_projs):
            shift_v = tfunc(i / n_projs)
            shifted.append(_shift_flat_filed(flat_field, shift_v, axis=1))

        flat_field_tr = np.concatenate(shifted, axis=0)

        return flat_field_tr

