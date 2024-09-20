"""
Directory crawler and associated file-locating functions.
"""

import os
import logging

from configs import image_files_pattern, sidecar_files_pattern

logger = logging.getLogger('Crawler')
logger.setLevel(logging.WARNING)

def get_images(directory:str, verbose:bool = False) -> dict:
  """
  Crawls through the given directory, and add any image to the registry.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  logger.info(f'Crawling folder: {directory}')

  tree = os.walk(directory)
  images = dict()
  for directory, _, files in tree:
    directory = f'{directory}/'
    
    logger.debug(f'Folder `{directory}` has {len(files)} entry(ies).')

    for filename in files:
      relative_path = os.path.relpath(os.path.join(directory, filename))
      extension = os.path.splitext(filename)[-1]
      if filename.lower().endswith(image_files_pattern):
        if filename not in images.keys():
          images.update({filename: dict()})
          logger.debug(f'New key `{filename}` added to registry.')

        images[filename].update({'directory': directory, 'image':{'filename': filename, 'extension': extension, 'path': relative_path}})
      
  return images

def locate_sidecars(images, verbose:bool = False):
  """
  Look for sidecar file for all items in the registry.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  for id, key in enumerate(images.keys()):

    for sidecar_extension in sidecar_files_pattern:

      extension = sidecar_extension
      filename = f"{images[key]['image']['filename']}{extension}"
      expected_sidecar_path = f"{images[key]['image']['path']}{extension}"

      if os.path.exists(expected_sidecar_path):
        logger.debug(f'Found sidecar `{expected_sidecar_path}` for registry `{key}`')
        images[key].update({'sidecar': {'path': expected_sidecar_path, 'filename': filename, 'extension': extension}})

  return images