"""
Deals with the .exif file. Create, load.
"""

import os
import subprocess
import logging
import json

logger = logging.getLogger('Exifs')
logger.setLevel(logging.WARNING)

def refresh_exif( images:dict, key:str, test_run:bool = True, verbose:bool = False, force:bool = False) -> dict:
  """
  (re)Create the exif file depending on options, then reloads the exif into the registry.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  exif_path, exif_filename, exif_extension = generate_exif_file(images, key, test_run=test_run, verbose=verbose, force=force)
  images[key].update({
    'exif':{
      'path': exif_path, 
      'filename': exif_filename, 
      'extension':exif_extension, 
      'data': load_exif_from_file(exif_path)
    }
  })

  return images

def generate_exif_file(images, key, test_run:bool = False, verbose:bool = False, force:bool = False) -> tuple[str, str, str]:
  """
  Create a dedicated exif file in JSON format, extracting information from the given path in the registry.
  """
  
  if verbose:
    logger.setLevel(logging.DEBUG)

  extension = '.exif'
  filename = f"{images[key]['image']['filename']}{extension}"
  path = f"{images[key]['directory']}{filename}"

  logger.debug(f'  ⨽ Unpacking EXIF from `{key}` and generating exif file.')
  if not os.path.exists(path) or force:
      if force:
        logger.debug(f'  ⨽ Exif data `{path}` will be overwritten (--force).')
      else:
        logger.debug(f'  ⨽ Exif data `{path}` is missing. Creating.')
      with open(path, 'w') as exif_file:
        subprocess.run(['exiftool', '-json', images[key]['image']['path']], stdout=exif_file, text=True)
  else:
    logger.debug(f'  ⨽ Exif data `{path}` exists.')

  return path, filename, extension

def load_exif_from_file(path:str, verbose:bool = False) -> dict:
  """
  Returns a dictionary representation of the exif data loaded from JSON.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  logger.debug(f'  ⨽ Loading EXIF data from `{path}`.')
  output = dict()

  path = os.path.relpath(os.path.normpath(os.path.join("/", path)), "/")

  try:
    with open(path, 'r') as json_file:
      output = json.load(json_file)[0]
  except:
    logger.error(f'Corrupted `{path}` file.')

  return output
