from tomo_twin.recon import *


class ReconReconstruction:
    '''
        Reconstruction from TOMO twin
    '''
    def __init__(self, reconstruction_options, detector_options):
        self.recon_ops = reconstruction_options
        self.detector_opt = detector_options
    
#     def __sample_flat_field(self, flat_field):
#         samples = flat_field.shape[0]
#         flat_field_sample = flat_field[random.randint(0, samples-1), :, :]
#         flat_field_sample = cv2.resize(flat_field_sample,  self.detector_opt['FOV'])
#         flat_field_sample = np.expand_dims(flat_field_sample, axis=0)
#         return flat_field_sample
    
    def __call__(self, artifacts):
        projs = artifacts['projections']
        flat_field = artifacts['flat_field']
        theta = artifacts['theta']
        
#         flat_field_sample = self.__sample_flat_field(flat_field)
                
        reconstructed = recon_wrapper(projs, flat_field, theta, pad_frac=self.recon_ops['pad_frac'],
                                  mask_ratio=self.recon_ops['mask_ratio'], contrast_s=self.recon_ops['contrast_s'])
    
        return {'reconstructed': reconstructed, 'recon_flat_field': flat_field}