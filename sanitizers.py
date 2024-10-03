"""
Independent sanitation functions.
"""

import os
import logging
import subprocess

from datetime import datetime

from configs import lens_configurations
from exifs import refresh_exif

logger = logging.getLogger('Sanitizers')
logger.setLevel(logging.WARNING)

def sanitize_author( images:dict, key:str, artist:str=None, test_run:bool = True, verbose:bool = False, force:bool = False) -> dict:
  """
  If the Artist information is not what is defined in configs.py or what was given in the command call --artist, it will be overwritten.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  logger.debug('  ⨽ Validating author/artist information.')
  logger.debug(f"  ⨽ Author of `{images[key]['image']['filename']}` is `{images[key]['exif']['data'].get('Artist', 'undef')}`")

  if not artist:
    return images

  if images[key]['exif']['data'].get('Artist') != artist:

    if not images[key]['exif']['data'].get('Artist') or force:
      logger.debug(f"  ⨽ Authoring `{images[key]['image']['filename']}` to {artist}.")
      
      if not test_run:
        subprocess.run(
          [
            'exiftool', 
            f'-artist={artist}',
            '-overwrite_original', 
            images[key]['image']['path']
          ],
          stdout=subprocess.DEVNULL,
          stderr=subprocess.STDOUT
        )
      else:
        pass

    else:
      logger.debug(f"  ⨽ Lens data was left unchanged. Use --force is this was not intended.")
  else:
    pass

  return images

def sanitize_lens_documentation( images:dict, key:str, lens:str=None, test_run:bool = True, verbose:bool = False, force:bool = False) -> dict:
  """
  If the lens information is not what is defined in configs.py, it will be overwritten.
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  logger.debug("  ⨽ Validating Lens information.")
  old_make = images[key]['exif']['data'].get('LensMake')
  old_model = images[key]['exif']['data'].get('LensModel')
  
  logger.debug(f"  ⨽ Lens information of `{images[key]['image']['filename']}` is `{old_make}`:`{old_model}`.")

  if not lens:
    return images
  
  if lens not in lens_configurations.keys():
    logger.error(f'  ⨽ Lens configuration `{lens}` unknown. Ignoring.')
    return images

  if old_make != lens_configurations[lens].get('LensMake') or old_model != lens_configurations[lens].get('LensModel') or force:
    logger.debug(f"  ⨽ Setting lens data of `{images[key]['image']['filename']}` to {lens_configurations[lens].get('LensMake')}:{lens_configurations[lens].get('LensModel')}.")
    if not test_run:
      subprocess.run(
        [
          'exiftool', 
          f"-LensMake={lens_configurations[lens].get('LensMake', '')}", 
          f"-LensModel={lens_configurations[lens].get('LensModel', '')}", 
          f"-LensInfo={lens_configurations[lens].get('LensInfo', '')}", 
          f"-MinFocalLength={lens_configurations[lens].get('MinFocalLength', 0)}",
          f"-MaxFocalLength={lens_configurations[lens].get('MaxFocalLength', 0)}",
          f"-MaxApertureValue={lens_configurations[lens].get('MaxApertureValue', 0.0)}",
          f"-MaxApertureAtMinFocal={lens_configurations[lens].get('MaxApertureAtMinFocal', 0.0)}",
          f"-MaxApertureAtMaxFocal={lens_configurations[lens].get('MaxApertureAtMaxFocal', 0.0)}",
          f"-FocalLengthIn35mmFormat={lens_configurations[lens].get('FocalLengthIn35mmFormat', '')}",
          f"-LensSerialNumber={lens_configurations[lens].get('LensSerialNumber', '')}",
          '-overwrite_original', 
          images[key]['image']['path']
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
      )
    else:
      pass
  else:
    logger.debug(f"  ⨽ Lens data was left unchanged.")


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

  logger.debug(f"  ⨽ Validating name format.")

  if target_filename not in images[key]['image']['filename']:

    logger.debug(f"  ⨽ Name `{images[key]['image']['filename']}` does not conform to format. Renaming.")

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

      logger.debug(f"  ⨽ Renaming sidecar file `{images[key]['sidecar']['filename']}` to `{target_sidecar_filename}`.")
      if not test_run:
        try:
          os.rename(images[key]['sidecar']['path'], target_sidecar_path)
        except Exception as msg:
          logger.error('  ⨽ Renaming operation failed. Ignoring.')
        
      images[key]['sidecar']['filename'] = target_sidecar_filename
      images[key]['sidecar']['path'] = target_sidecar_path

  return images
