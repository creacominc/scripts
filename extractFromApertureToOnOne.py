#!/usr/bin/env python3
"""
This script will extract the JPG and Canon raw files from the Aperture libraries into folders which can be indexed by On1 Raw or other tools.
"""

import os
import glob
from pathlib import Path
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('max', metavar='N', type=int, default=10,
                    help='max records')
args = parser.parse_args()

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

counter = args.max

for root, dirs, files in os.walk( LIBRARY_LOCATION ):
    for fln in files:
        if 0 >= counter:
            break
        file_ext = os.path.splitext( fln )[1]
        if file_ext.upper() in [ ".JPG", ".CR2", ".RW2", ".JPEG", ".PSD", ".TIFF", ".MP4", ".MOV", ".TIF", ".GIF" ]:
            if fln[:6] != "thumb_":
                # find the .aplibrary in the path
                head = root
                tail = ""
                while (head != "/") and (".aplibrary" != os.path.splitext( tail )[1] ):
                    (head, tail) = os.path.split( head )
                library_name = os.path.splitext( tail )[0]
                #print( f"path: {root},  file: {fln},  extension: {file_ext},  library: {library_name}" )
                # create folder if it does not exist
                sourceFile = Path( os.path.join( root, fln ) )
                targetFolder = Path( os.path.join( DESTINATION, library_name ) )
                if not targetFolder.exists():
                    print( f"   Creating folder: {targetFolder}" )
                    targetFolder.mkdir()
                # move file to new location
                targetFile = Path( os.path.join( targetFolder, fln ) )
                if targetFile.exists():
                    # attempt to move to _copy
                    copyPath = Path( os.path.join(  targetFolder, os.path.splitext( fln )[0] + "_copy" + os.path.splitext( fln )[1] ) )
                    if copyPath.exists():
                        print( f"ERROR:  File exists: {os.path.join( targetFolder, fln )} (copy also exists: {copyPath})" )
                        print( f"        path: {root},  file: {fln},  extension: {file_ext},  library: {library_name}" )
                        print( f"        source: {sourceFile} -> {targetFolder}" )
                        continue
                    else:
                        targetFolder = copyPath
                print( f"Move {sourceFile} -> {targetFolder}" )
                shutil.move( sourceFile.as_posix(), targetFolder.as_posix() )
                counter -= 1
            else:
                thumbPath = Path( os.path.join( root, fln ) )
                print( f"removing thumbnail: {thumbPath}" )
                thumbPath.unlink()
                counter -= 1
        elif file_ext.upper() in [ ".PLIST", ".APDB", ".DB", ".APALBUM", ".APDETECTED", ".APFOLDER", ".APMASTER", ".APVERSION", ".APVOLUME", ".DATA", ".APFACENAME", ".APVAULT", ".DB-CONCH", ".APDB-CONCH", ".BAK-CONCH", ".APTEMP-CONCH" ]:
            trashPath = Path( os.path.join( root, fln ) )
            print( f"removing trash: {trashPath}" )
            trashPath.unlink()
            counter -= 1
        elif fln in [ "ApertureDatabaseTimestamp", "Apple TV Photo Database", "Photo Database", "lockfile.pid" ]:
            trashPath = Path( os.path.join( root, fln ) )
            print( f"removing trash: {trashPath}" )
            trashPath.unlink()
            counter -= 1
    # remove empty folders
    for drn in dirs:
        if 0 >= counter:
            break
        fldrPath = Path( os.path.join( root, drn ) )
        #print( f"Checking folder: {fldrPath} " )
        if fldrPath.exists() and fldrPath.is_dir():
            try:
                record = next( fldrPath.iterdir() )
            except StopIteration:
                print( f"Removing empty folder: {fldrPath}" )
                os.removedirs( fldrPath )
        counter -= 1
