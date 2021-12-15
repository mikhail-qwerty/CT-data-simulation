import os
import cv2
import numpy as np
import random
from tomo_twin import ray

class ProjectionsCreator:
    
    def __init__(self, detector_options):
        self.detector_opt = detector_options
    
    def __validate_flat_field(self, flat_field):
        f_shape = flat_field.shape
        fov = self.detector_opt['FOV']
        n_projs = self.detector_opt['n_projections']
        
        valid_shape1 = (1, *fov)
        
        assertion = (f_shape[0] == 1) & \
        (f_shape[1] == fov[0]) & \
        (f_shape[2] == fov[1])

        if not assertion:
            msg = f'Invalid flat field shape: {f_shape}, must be ' \
                  f'{valid_shape1} '
            raise AssertionError(msg)
        
    def __sample_flat_field(self, flat_field):
        samples = flat_field.shape[0]
        flat_field_sample = flat_field[random.randint(0, samples-1), :, :]
        flat_field_sample = cv2.resize(flat_field_sample,  self.detector_opt['FOV'])
        flat_field_sample = np.expand_dims(flat_field_sample, axis=0)
        return flat_field_sample
    
    def __call__(self, artifacts):
        
        flat_field = artifacts['flat_field']
        phantom = artifacts['phantom']
        
        theta = (*self.detector_opt['projections_range'], self.detector_opt['n_projections'])
        
#         flat_field_sample = self.__sample_flat_field(flat_field)
            
        self.__validate_flat_field(flat_field)
        
#         print(flat_field_sample.shape)
        
        proj_beam, projs = phantom.get_projections(theta = theta, beam = flat_field, \
                               noise = self.detector_opt['noise'], \
                               detector_dist = self.detector_opt['detector_dist'], \
                               blur_size = self.detector_opt['blur_size'])
        
        return {'projections': projs, 'proj_beam': proj_beam, 'theta': theta, 'proj_flat_field': flat_field}

class FlatFieldCreator():
    def __call__(self, artifacts):
        pass

    
class FlatFieldFromNumpy(FlatFieldCreator):
    def __init__(self, source):
        self.source = source
    
    def __call__(self, artifacts):
        flat_field = np.load(self.source)
        
        shape = flat_field.shape
        
        # tiff, numpy
        
        # TODO create optioins (mean, random sample flat field)
        
        if len(shape) == 2:
            flat_field = np.expand_dims(flat_field, axis=0)
        
        return {'flat_field': flat_field}
        
    
class FlatFieldFromTomoTwinSource(FlatFieldCreator):
    def __init__(self, source, detector_options):
        self.detector_opt = detector_options
        self.source = source
    
    def __call__(self, artifacts):
    
        proj_shape = self.detector_opt['FOV']

        flat_field = ray.read_source(self.source, \
                           self.detector_opt['energy_pts'], \
                           res = self.detector_opt['pixel_size'], \
                           img_shape = proj_shape)
        
        return  {'flat_field': flat_field}