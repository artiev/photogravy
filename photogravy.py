import logging
import click

from datetime import datetime

from crawler import get_images, locate_sidecars
from exifs import refresh_exif
from sanitizers import sanitize_author, sanitize_filenames

logging.basicConfig(format="%(levelname)6s: %(message)s")

logger = logging.getLogger('Main')
logger.setLevel(logging.WARNING)

@click.command()
@click.option('--directory', default='./', help='Image directory')
@click.option('--verbose', is_flag=True, help='Show logs')
@click.option('--force', is_flag=True, help='Force exif extraction (even if exists)')
@click.option('--test-run', is_flag=True, help='Do all checks but do not write changes to the directory.')
def main(directory:str, test_run:bool, verbose:bool, force:bool):
  """
  CLI entry point
  """

  if verbose:
    logger.setLevel(logging.DEBUG)

  print('Photogravy')
  print('‣ A Photography Sanitation Tool by Arthur Van de Wiele')
  print('‣ Check for Updates: https://github.com/artiev/photogravy')

  print('Working...')
  images = get_images(directory, verbose=verbose)
  locate_sidecars(images, verbose=verbose)
  sanitize(images, test_run=test_run, verbose=verbose, force=force)

  print('All Done. Bye.')

def sanitize(images:dict, test_run:bool = True, verbose:bool = False, force:bool = False):
  """
  Order discreet sanitation functions properly.
  """

  logger.info('Sanitation Process Started')
  if test_run:
    logger.warning('Test Run flag set. No updates to the directory will be made except creating missing .exif files.')
    if force:
      logger.warning('Option --force cannot be used in Test Mode. Ignoring.')

  for id, key in enumerate(images.keys()):
    logger.info(f'Sanitizing registry `{key}`.')
                    
    refresh_exif(images, key, test_run, verbose=verbose, force = force)
    sanitize_author(images, key, test_run, verbose=verbose)
    sanitize_filenames(images, key, test_run, verbose=verbose)

  return images

def log_registry(images:dict) -> None:
  """
  Output a human-readable breakdown of the registry using the standard logger.
  Note: Because exif data is HUGE, it is skipped in this output.
  """

  for key in images.keys():
    logger.info(f'Registry `{key}`')
    for key_two in images[key].keys():
      if not isinstance(images[key][key_two], dict):
        logger.info(f'  ⨽ `{key_two}` → {images[key][key_two]}')
      else:
        logger.info(f'  ⨽ `{key_two}`')
        for key_three in images[key][key_two].keys():
          if key_three == 'data':
            logger.info(f'     ⨽ `{key_three}` → {{...}}')
          else:
           logger.info(f'     ⨽ `{key_three}` → {images[key][key_two][key_three]}')


if __name__ == '__main__':
  main()