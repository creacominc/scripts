#!/usr/bin/env python3
import os
import requests
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    handlingAnchor = False
    m_url  = None
    m_path = None

    def setup( self, purl, ppath ) :
        self.m_url  = purl
        self.m_path = ppath

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'a' :
            self.handlingAnchor = True

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.hanglingAnchor = False

    def handle_data(self, data):
        # print( f"Encountered some data  : [{data}]" )
        # if len( data ) > 4 :
        #     print( f"   ending with: {data[-4:]}" )
        if self.handlingAnchor :
            if data[-1] == '/' :
                print( f'  Folder: {self.m_path + data}' )
                # create a folder for this
                sub = self.m_path + data
                if os.path.exists( sub ) :
                    if os.path.isdir( sub ) :
                        print( f'WARN:  Path exits: {sub}' )
                    else :
                        print( f'ERROR:  Non-folder item exists: {sub}' )
                        exit -1
                else :
                    os.mkdir( sub )
                # get the contents for this folder
                suburl = self.m_url + self.m_path + data
                print( f'     Fetching: {suburl}' )
                subrsp = requests.get( suburl, allow_redirects=False )
                subParser = MyHTMLParser( )
                subParser.setup( self.m_url, self.m_path + data )
                subParser.feed( str( subrsp.content ) )
            elif ( (len(data) > 4) and (data[-4:] == '.exr') ) :
                print( f'    Downloading: {self.m_path + data}' )
                exrsp = requests.get( self.m_url + self.m_path + data, allow_redirects=False )
                open( self.m_path + data, "wb" ).write( exrsp.content )

pth = "tearsofsteel/tearsofsteel-frames-exr/"
url = "https://media.xiph.org/"
# create folder for tree
if not os.path.exists( pth ) :
    os.makedirs( pth )
print( f'Fetching: {url + pth}' )
rsp = requests.get( url + pth, allow_redirects=False )
# open( pth + "index.html", "wb" ).write( rsp.content )
# iterate over all DIR entries in the html
parser = MyHTMLParser(  )
parser.setup( url, pth )
parser.feed( str(rsp.content) )
