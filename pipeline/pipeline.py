import random


class Compose():
    
    def __init__(self, operations: list):
        self.operations = operations
    
    def __call__(self):
        
        all_artifacts = {}
        for op in self.operations:
            artifacts = None
            if isinstance(op, list):
                artifacts = {}
                for sub_op in op:
                    res = sub_op(all_artifacts)
                    artifacts.update(res)
            else:
                artifacts = op(all_artifacts)
            
            # TODO add stage info
            assert artifacts is not None, 'Results in stage is None'
            all_artifacts.update(artifacts)

        return all_artifacts

class RandomOptions():
    
    def __init__(self):
        self.options = None
        self.available_options = None
        self.artifact_key = None
        self.mutable_options = None
        self.call_options = None
                        
    def __call__(self, artifacts):
        
        res_options = {}
        
        for name, opt in self.options.items():
            
            opt_value = opt
            
            if name not in self.available_options:
                msg = f'Invalid option {name}, valid options are {self.available_options}'
                raise AssertionError(msg)
            
            if name in self.mutable_options:
                if isinstance(opt, (list, tuple)):
                    if len(opt) != 2:
                        msg = f'Valid options must be of lenght two: (start, end)'
                        raise AssertionError(msg)

                    opt_value = random.uniform(opt[0], opt[1])
            
            res_options[name] = opt_value
         
        self.call_options = res_options
        
        return {self.artifact_key: self.call_options}
    
    def __getitem__(self, key):
        return self.call_options[key]

def get_atrtifacts_names():
    '''
        'gt_volume': np.array,  (GT) ground truth volume with values 0 ... num_classes
        'phantom':   Phantom, class from tomotwin (GT with materials)
        'flat_field': np.array, Flat field array
        'theta': tuple, (start_angle, end_angle, n_projections)
        'projections': np.array, projections
        'reconstructed': reconstructed sample
    '''
    
    return {'gt_volume',
            'phantom',   
            'flat_field',
            'theta',
            'projections',
            'reconstructed'  
    }
        
class DetectorOptions(RandomOptions):
    
    def __init__(self, options):
        self.options = options
        
        self.available_options = [
            'detector_dist',
            'blur_size',
            'noise',
            'energy_pts',
            'pixel_size',
            'n_projections',
            'projections_range',
            'FOV'
        ]
        
        self.mutable_options = [
            'detector_dist',
            'blur_size',
            'noise'
        ]
        
        self.artifact_key = 'detector_options'
    
class ReconstructionOptions(RandomOptions):
    def __init__(self, options):
        self.options = options
        
        self.available_options = [
            'pad_frac',
            'mask_ratio',
            'contrast_s'
        ]
        
        self.mutable_options = [
            'contrast_s'
        ]
        
        self.artifact_key = 'reconstruction_options'

