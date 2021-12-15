
from tomo_twin.gt_generators import make_porous_material, make_spheres


class GroundTruthCreator():
    def __call__(self, volume_shape):
        pass

class PorousCreator(GroundTruthCreator):
    '''
        Create porouse ground truth mask
    '''
    def __init__(self, phantom_params):
        self.params = phantom_params
    
    def __call__(self, volume_shape):
        
        return make_porous_material(volume_shape, **self.params)


class GranulesCreator(GroundTruthCreator):
    '''
        Create granules ground truth mask
    '''
    def __init__(self, phantom_params):
        self.params = phantom_params
    
    def __call__(self, volume_shape):
        
        return make_spheres(volume_shape, **self.params)