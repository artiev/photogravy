Usage: photogravy.py [OPTIONS]

  Photogravy - A Photography Sanitation Tool by Arthur Van de Wiele

  Avoid getting overwhelmed with your photographs and keep your archives
  clean(er) by automatically renaming images (RAW, jpegs, etc...) and their
  sidecar with a datetime format, (re)setting the artist name and so on. Also
  create a dedicated .exif file (simple json text file) to have easy access to
  the metadata of an image.

  Examples:
    python photogravy.py --directory /my/new/images/folder --test-run --verbose
    or
    python photogravy.py --directory /my/new/images/folder --force

Options:
  --directory PATH  Image directory
  --verbose         Show logs
  --force           Force exif extraction (even if exists)
  --test-run        Do all checks but do not write changes to the directory
                    (except if .exif missing).
  --help            Show this message and exit.
