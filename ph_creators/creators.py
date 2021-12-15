import numpy as np
from tomo_twin import ray

class PhantomCreator():
    def __init__(self, detector_options: dict,
                 ground_truth_creator,
                 materials_dict: dict,
                 materials_path: str
                ):
        
        self.detector_opt = detector_options
        self.gt_creator = ground_truth_creator
        self.mat_dict = materials_dict
        self.materials_path = materials_path
    
    
    def __validate_materials(self, gt_volume):
        n_classes = len(np.unique(gt_volume))
        n_materials = len(self.mat_dict)
        if n_classes != n_materials:
            raise AssertionError(f'Num classes in gt volume != Num materials, {n_classes} != {n_materials}')
        
    def __call__(self, artifacts):
        
        proj_shape = self.detector_opt['FOV']
        
        vol_shape = (proj_shape[0], proj_shape[1], proj_shape[1])

        gt_volume = self.gt_creator(vol_shape)
        
        self.__validate_materials(gt_volume)
        
        phantom = ray.Phantom(gt_volume, self.mat_dict,
                     self.detector_opt['pixel_size'],
                     self.detector_opt['energy_pts'],
                     data_path = self.materials_path
                    )
        
        return {'gt_volume': gt_volume, 'phantom': phantom}