import numpy as np

class Augmentation:
    def __call__(self, artifacts):
        pass

class RingsAugmentation(Augmentation):
    '''
        Create ring by affecting flat_field
    '''
    def __init__(self, detector_options, shift=3):
        self.detector_opt = detector_options
        self.shift = shift
    
    def __call__(self, artifacts):
        
        n_projections = self.detector_opt['n_projections']
        flat_field = artifacts['flat_field']
        
        flat_field = np.roll(flat_field, self.shift, axis=1)
        
        return {'flat_field': flat_field}