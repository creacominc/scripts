"""
This script will extract the JPG and Canon raw files from the Aperture libraries into folders which can be indexed by On1 Raw or other tools.
"""

import os
import glob
from pathlib import Path
import shutil

LIBRARY_LOCATION = os.path.expanduser( "/Volumes/ParaMobile2T/haroldt_sync/Documents/PhotoLibs" )
DESTINATION = os.path.expanduser( "~/Pictures/ApertureExtract" )

if not os.path.exists( DESTINATION ):
    print( f"ERROR: Destination ({DESTINATION}) folder not found." )
    exit()
if not os.path.isdir( DESTINATION ):
    print( f"Destination is not a folder.  ({DESTINATION})" )
    exit()
if not os.path.exists( LIBRARY_LOCATION ):
    print( f"ERROR:  Library ({LIBRARY_LOCATION}) folder not found." )
    exit()
if not os.path.isdir( LIBRARY_LOCATION ):
    print( f"Library Location is not a folder.  ({LIBRARY_LOCATION})" )
    exit()


"""
Find all folders inside the LIBRARY_LOCATION that match *.aplibrary.
Use the part before .aplibrary as the name of the new folder.  
"""

for root, dirs, files in os.walk( LIBRARY_LOCATION ):
    counter = 10
    for fln in files:
        file_ext = os.path.splitext( fln )[1]
        if file_ext.upper() in [ ".JPG", ".JPEG", ".CR2" ]:
            if fln[:6] != "thumb_":
                # find the .aplibrary in the path
                head = root
                tail = ""
                while (head != "/") and (".aplibrary" != os.path.splitext( tail )[1] ):
                    (head, tail) = os.path.split( head )
                library_name = os.path.splitext( tail )[0]
                #print( f"path: {root},  file: {fln},  extension: {file_ext},  library: {library_name}" )
                if 0 >= counter:
                    exit()
                counter -= 1
                # create folder if it does not exist
                sourceFile = Path( os.path.join( root, fln ) )
                targetFolder = Path( os.path.join( DESTINATION, library_name ) )
                if not targetFolder.exists():
                    print( f"   Creating folder: {targetFolder}" )
                    targetFolder.mkdir()
                # move file to new location
                targetFile = Path( os.path.join( targetFolder, fln ) )
                if targetFile.exists():
                    print( f"ERROR:  File exists: {os.path.join( targetFolder, fln )}" )
                    exit()
                print( f"Move {sourceFile} -> {targetFolder}" )
                shutil.move( sourceFile.as_posix(), targetFolder.as_posix() )
