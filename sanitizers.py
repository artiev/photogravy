"""
Independent sanitation functions.
"""

import os
import logging
import subprocess

from datetime import datetime

from configs import artist_name
from exifs import refresh_exif

logger = logging.getLogger('Sanitizers')
logger.setLevel(logging.WARNING)

def sanitize_author( images:dict, key:str, test_run:bool = True, verbose:bool = False) -> dict:
  """
  If the Artist information is not what is defined in configs.py, it will be overwritten.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  logger.info(f"  ⨽ Validating author/artist information.")

  if images[key]['exif']['data'].get('Artist', '') != artist_name:

    logger.debug(f"  ⨽ Authoring `{images[key]['image']['filename']}` to {artist_name}.")
    if not test_run:
      subprocess.run(['exiftool', f'-artist={artist_name}', images[key]['image']['path']])

    images[key]['exif']['data']['Artist'] = artist_name #todo clean

    refresh_exif(images, key, test_run)

  return images

def sanitize_filenames( images:dict, key:str, test_run:bool = True, verbose:bool = False) -> dict:
  """
  Renaming images, sidecar and exif files to a date/time format.
  If the name is taken, `-Rx` where x is an integer will be automatically appended to the filename until a suitable integer is found.

  Caveat: Not designed to handle mixed lower/upper case file extensions.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)
    
  datetime_original = datetime.strptime(images[key]['exif']['data']['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
  target_filename = datetime_original.strftime('%Y-%m-%d-%H%M%S')

  logger.info(f"  ⨽ Validating name format.")

  if target_filename not in images[key]['image']['filename']:

    logger.info(f"  ⨽ Name `{images[key]['image']['filename']}` does not conform to format. Renaming.")

    final_extension = images[key]['image']['extension'].lower()
    final_filename = f'{target_filename}{final_extension}'
    final_filepath = os.path.relpath(os.path.join(images[key]['directory'], final_filename))
    
    counter = 1
    while os.path.exists(final_filepath):
      logger.debug(f'  ⨽ Filename `{final_filename}` is taken. Working.')
      filename_without_extension = target_filename.replace(images[key]['image']['extension'], '')
      final_filename = f"{filename_without_extension}-R{counter}{final_extension}"  
      final_filepath = os.path.relpath(os.path.join(images[key]['directory'], final_filename))
      counter += 1
    
    logger.debug(f"  ⨽ Renaming image `{images[key]['image']['filename']}` to `{final_filename}`.")
    if not test_run:
      try:
        os.rename(images[key]['image']['path'], final_filepath)
      except Exception as msg:
        logger.error('  ⨽ Renaming operation failed. Ignoring.')
      
    images[key]['image'].update( {'path': final_filepath, 'filename': final_filename, 'extension': final_extension})

    target_exif_filename = f"{images[key]['image']['filename']}{images[key]['exif']['extension']}"
    target_exif_path = os.path.relpath(os.path.join(images[key]['directory'], target_exif_filename))

    logger.debug(f"  ⨽ Renaming exif file `{images[key]['exif']['filename']}` to `{target_exif_filename}`.")
    if not test_run:
      try:
        os.rename(images[key]['exif']['path'], target_exif_path)
      except Exception as msg:
        logger.error('  ⨽ Renaming operation failed. Ignoring.')
      
    images[key]['exif']['filename'] = target_exif_filename
    images[key]['exif']['path'] = target_exif_path

    if images[key].get('sidecar') is not None:

      target_sidecar_filename = f"{images[key]['image']['filename']}{images[key]['sidecar']['extension']}"
      target_sidecar_path = os.path.relpath(os.path.join(images[key]['directory'], target_sidecar_filename))

      logger.debug(f"→ Renaming sidecar file `{images[key]['sidecar']['filename']}` to `{target_sidecar_filename}`.")
      if not test_run:
        try:
          os.rename(images[key]['sidecar']['path'], target_sidecar_path)
        except Exception as msg:
          logger.error('  ⨽ Renaming operation failed. Ignoring.')
        
      images[key]['sidecar']['filename'] = target_sidecar_filename
      images[key]['sidecar']['path'] = target_sidecar_path

  return images
