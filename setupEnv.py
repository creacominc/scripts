#!/usr/bin/env python3

import os
import shutil
import argparse
import time
import logging
import logging.handlers
import shutil

share = '/Volumes/ParaMobile2T/haroldt_sync'

def log_setup():
    log_handler = logging.handlers.RotatingFileHandler( filename='setupEnv.log', maxBytes=1024000, mode='a', backupCount=10 )
    formatter = logging.Formatter( '%(asctime)s setupEnv [%(levelname)s]: %(message)s' )
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter( formatter )
    log_handler.doRollover()
    logger = logging.getLogger( __name__ )
    logger.addHandler( log_handler )
    logger.setLevel( logging.INFO )
    # logging.basicConfig( filename='setupEnv.log', filemode='w', format='%(asctime)-15s %(levelname)s %(message)s' )

def setupFolder( folder, share ):
  """
  Remove all current links and, for each entry in the share, create a link in folder.
  """
  logger = logging.getLogger( __name__ )
  # confirm folder exists
  if( not (os.path.exists( folder ) and os.path.isdir( folder )) ):
    logger.fatal( f'folder {folder} not found or not a folder.' )
    exit( -1 )
  # confirm share exists
  if( not (os.path.exists( share ) and os.path.isdir( share )) ):
    logger.fatal( f'share {share} not found or is not a folder.' )
    exit( -1 )
  shutdownFolder( folder )
  # move any files/folders to the share
  logger.info( f'testing folder: {folder}' )
  for name in os.listdir( folder ):
    if( not ( name[0] == '.' ) ):
      logger.debug( f'testing file: {folder}/{name}' )
      fullpath = os.path.join( folder, name )
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
    if( name[0] == '.' ):
      logger.debug( f'Ignoring sources starting with .  for: {name}' )
      continue
    trgname = share + '/' + name
    srcname = folder + '/' + name
    logger.debug( f'linking {srcname} to {trgname}' )
    os.symlink( trgname, srcname )

def shutdownFolder( folder ):
  logger = logging.getLogger( __name__ )
  # remove all links in the folder
  for name in os.listdir( folder ):
    if( os.path.islink( folder + '/' + name ) ):
      logger.debug( f'removing link: {folder} / {name}' )
      os.unlink( folder + '/' + name )

def main():
  log_setup()
  logger = logging.getLogger( __name__ )
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
  folders = ['Documents', 'Desktop' ]
  for fldr in folders :
    logger.debug( "folder: " + fldr )
    if( args.setup == True ):
      setupFolder( fldr, share + '/' + fldr )
    else:
      shutdownFolder( fldr )
  

if __name__ == "__main__":
   main()
