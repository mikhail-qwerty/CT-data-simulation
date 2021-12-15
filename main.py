import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from pipeline import Compose, DetectorOptions, ReconstructionOptions
from gt_creators import GranulesCreator, PorousCreator
from ph_creators import PhantomCreator
from projections import FlatFieldFromTomoTwinSource, ProjectionsCreator
from simulation import RingsAugmentation
from reconstruction import ReconReconstruction
from utils import seed_everything
from tqdm import tqdm


if __name__ == '__main__':

  seed_everything(42)

  # detector parameters
  detector_options = DetectorOptions({'detector_dist': 6.0, # detector distance in cm
                      'blur_size': 5, # kernel blur size
                      'noise': 0.0, # detector noise (0.0 to see the rings) 1.0 default
                      'energy_pts': 30.0, # keV
                      'pixel_size': 0.7, # res
                      
                      'n_projections': 500,
                      'projections_range': (0, 180),
                      'FOV': (300,300)
                    })

  # reconstruction parameters
  reconstruction_options = ReconstructionOptions({
                  'pad_frac': 0.8,
                  'mask_ratio': 0.95,
                  'contrast_s': (0.01, 0.05)
                  })



  # Define the phantom parameters  
  materials_dict = {"air" : 0.00122, "silica" : 2.7}
  sp = 18
  vs = 0.0745*sp - 0.4428
  # phantom_params = {"void_frac" : [0.35, 0.15], \
  #                   "void_size" : [vs, 0.2]}






  # porous
  phantom_params = {"void_frac" : [0.1, 0.0], \
                    "void_size" : [vs, 0.2]}
  # circles
  phantom_params = {'void_frac': 0.5, 'radius': 8, 'radius_std': 4}



  data_path = 'C:/Users/dkoro/PythonProjects/TOMO/project/TomoTwin/'
  beam_source = os.path.join(data_path, 'model_data/source_files/7BM/beam_profile_7BM.hdf5')
  materials_path = os.path.join(data_path, 'model_data')

              
  compose = Compose([
                      [detector_options, reconstruction_options],
      
                      # create input data: gt_volume, phantom, flat_field
                      [PhantomCreator(detector_options,
                                    GranulesCreator(phantom_params), # PorousCreator(phantom_params),
                                    materials_dict, materials_path
                                  ), FlatFieldFromTomoTwinSource(beam_source, detector_options)], # FlatFieldFromTomoTwinSource(beam_source, detector_options)
                  
                      # create projections: projections
                      ProjectionsCreator(detector_options),
                      
                      # add augmentations
                      RingsAugmentation(detector_options, shift=-50), # affect flat_field
      
                      # reconstruct phantom: reconstructed
                      ReconReconstruction(reconstruction_options, detector_options)
                    ])

  samples = []

  print('Generating samples...')
  for i in tqdm(range(10)):
      sample = compose()
      
      plt.figure(figsize=(14, 14))
      plt.imshow(sample['reconstructed'][40, :, :], cmap='gray')
      
      np.save(f'sample{i}.npy', sample)
      samples.append(sample)