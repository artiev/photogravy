"""
Configurations
"""

image_files_pattern = ('.jpg','.jpeg','.tiff','.raf','.nef','.dng')
sidecar_files_pattern =('.xmp',) # Careful, without the comma, the tuple interprets each letter of a string as an item

artist_name = 'Arthur Van de Wiele'
lens_configurations = {
  'minolta-3570-35-x': {
    'LensMake': 'Minolta',
    'LensModel': 'MD 35-70mm f/3.5 + K&F Concept MD-FX Adapter',
    'LensInfo': '35-70 mm f/3.5',
    'MinFocalLength': 35,
    'MaxFocalLength': 70,
    'MaxApertureValue': 3.5,
    'MaxApertureAtMinFocal': 3.5,
    'MaxApertureAtMaxFocal': 3.5,
    'FocalLengthIn35mmFormat': 53,
    'LensSerialNumber': '8017780'
  },
  'tt-50-095-x': {
    'LensMake': 'TTArtisan',
    'LensModel': 'APS-C 50mm f/0.95 X-Mount',
    'LensInfo': '50 mm f/0.95',
    'MinFocalLength': 50,
    'MaxFocalLength': 50,
    'MaxApertureValue': 0.95,
    'MaxApertureAtMinFocal': 0.95,
    'MaxApertureAtMaxFocal': 0.95,
    'FocalLengthIn35mmFormat': 75,
    'LensSerialNumber': '850404641'
  },
  'tt-23-14-x': {
    'LensMake': 'TTArtisan',
    'LensModel': 'APS-C 23mm f/1.4 X-Mount',
    'LensInfo': '23mm f/1.4',
    'MinFocalLength': 23,
    'MaxFocalLength': 23,
    'MaxApertureValue': 1.4,
    'MaxApertureAtMinFocal': 1.4,
    'MaxApertureAtMaxFocal': 1.4,
    'FocalLengthIn35mmFormat': 35,
    'LensSerialNumber': ''
  }
}