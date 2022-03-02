#!/usr/bin/env python3

import argparse
import glob
import logging
import logging.handlers
import os
import shutil
import time

share = '/Volumes/ParaMobile2T/haroldt_sync'

def log_setup():
    log_handler = logging.handlers.RotatingFileHandler( filename='setupEnv.log', maxBytes=1024000, mode='a', backupCount=9 )
    formatter = logging.Formatter( '%(asctime)s setupEnv [%(levelname)s]: %(message)s' )
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter( formatter )
    log_handler.doRollover()
    logger = logging.getLogger( __name__ )
    logger.addHandler( log_handler )
    logger.setLevel( logging.DEBUG )
    # logging.basicConfig( filename='setupEnv.log', filemode='w', format='%(asctime)-15s %(levelname)s %(message)s' )

def setupFolder( folder, share ):
  """
  Remove all current links and, for each entry in the share, create a link in folder.
  """
  logger = logging.getLogger( __name__ )
  # confirm share exists
  if( not (os.path.exists( share ) and os.path.isdir( share )) ):
    logger.fatal( f'share {share} not found or is not a folder.' )
    exit( -1 )
  # confirm folder exists or create it
  if( not (os.path.exists( folder ) ) ):
    # create folder in path
    os.mkdir( folder )
  elif( not os.path.isdir( folder ) ):
    logger.fatal( f'local target {folder} exists but is not a folder.' )
    exit( -1 )
  else:
    # folder exists, clean it
    shutdownFolder( folder )
  # move any files/folders to the share
  logger.debug( f'testing folder: {folder}' )
  for name in os.listdir( folder ):
    # everything that does not start with a '.' - ignore hidden files/folders
    if( not ( name[0] == '.'  or  name[0] == "$" ) ):
      # check for links
      fullpath = os.path.join( folder, name )
      if ( os.path.islink( fullpath ) ):
        logger.warning( f'Found link in folder: {fullpath}' )
        continue
      logger.debug( f'testing file: {fullpath}' )
      # if this exists, is a file, and is not a link, move to the sync folder
      if( os.path.exists( fullpath ) and os.path.isfile( fullpath ) and not os.path.islink( fullpath ) ):
        logger.info( f'Moving {fullpath} to {share}' )
        try:
          # move file
          shutil.move( src=fullpath, dst=share )
        except Exception as excp:
          logger.fatal( f'Failed to move {fullpath} to {share}.  Exception: {str(excp)}' )
          raise
  # for each file in the share/folder, create a symbolic link
  for name in os.listdir( share ):
    if( name[0] == '.'  or  name[0] == "$"  ):
      logger.debug( f'Ignoring sources starting with .  for: {name}' )
      continue
    trgname = os.path.join( share, name )
    srcname = os.path.join( folder, name )
    # check that the link does not already exist
    if( os.path.islink( trgname ) ):
      logger.warning( f'Target is a link: {trgname}. Skipping' )
      continue
    logger.debug( f'linking {srcname} to {trgname}' )
    try:
      os.symlink( trgname, srcname )
    except:
      logger.warning( f'Failed to link "{srcname}" to "{trgname}"' )

def shutdownFolder( folder ):
  logger = logging.getLogger( __name__ )
  # cd to the home folder
  os.chdir( os.path.expanduser('~') )
  # # the Music folder is a bit different.  handle it separately
  # if ( folder == "Music" ):
  #   # remove the symlink from ~/Music/Music/Media/Music 
  #   folder = "Music/Music/Media/Music"
  # if the folder exists
  if not os.path.exists( folder ):
    logger.warning( f"Folder not found: {folder}" )
    return
  # remove all links in the folder
  for name in os.listdir( folder ):
    path = os.path.join( folder, name )
    if( os.path.islink( path ) ):
      logger.debug( f'removing link: {path}' )
      try:
        os.unlink( folder + '/' + name )
      except:
        logger.warning( f'Failed to remove: {folder}/{name}')
    else:
      # anything that is not a link and does not start with a '.' needs to be copied to the sync drive (with the exception of the Music folder)
      if name[0] != ".":
        target = os.path.join( share, path )
        logger.info( f"Moving {path} to sync: {target}" )
        try:
          # move file
          shutil.move( src=path, dst=target )
        except:
          logger.error( f"Failed to move {path} to {target}" )
          raise


def main():
  log_setup()
  logger = logging.getLogger( __name__ )
  # cd to the home folder
  os.chdir( os.path.expanduser('~') )
  parser = argparse.ArgumentParser()
  modeGroup = parser.add_mutually_exclusive_group( required=True )
  modeGroup.add_argument( '--setup', '-u', action='store_true' )
  modeGroup.add_argument( '--shutdown', '-d', action='store_false' )
  args = parser.parse_args()
  # confirm share exists
  if( not (os.path.exists( share ) and os.path.isdir( share )) ):
    logger.fatal( f'share {share} not found or is not a folder.' )
    exit( -1 )
  #folders = ['Documents', 'Desktop', 'Pictures' ]
  folders = [ f.path for f in os.scandir( share ) if f.is_dir() ]
  for folderPath in folders :
    fldr = os.path.basename( folderPath )
    logger.debug( f"folder: {fldr}" )
    if( args.setup == True ):
      setupFolder( fldr, folderPath )
    else:
      shutdownFolder( fldr )


if __name__ == "__main__":
   main()
