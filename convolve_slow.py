'''**************************************************************************
*
* FILE: convolve_slow.py
*
* BRIEF: Implements image filtering from the Unix command-line 
*
* USAGE EXAMPLE: Apply an edge detector
* $python convolve_slow.py utah.bmp utah_edges.bmp 3 -1 -1 -1 -1 8 -1 -1 -1 -1
* 
* COMMAND-LINE ARGUMENTS:
*  1)                   Input filename (must be bmp format).
*  2)                   Output filename (will be bmp format).
*  3)                   Filter width (an odd integer).
*  4 to filter_width^2) The floating point weights that define the filter, 
*                       ordered left->right and top->bottom.
*                   
* AUTHOR: David Meger, 2015
*
***************************************************************************'''

#!/usr/bin/python
import sys
import struct
import copy
import cProfile

# Reads a BMP image from disk into a convenient array format
def loadBMPImage( img_name ):

  img_in = open( img_name, 'rb' )

  # The following lines read important book-keeping information kept at the
  # start of each BMP file, in its header
  header_data = img_in.read(54)
  bmp_size = struct.unpack('i',header_data[2:6])[0]
  img_width = struct.unpack('i',header_data[18:22])[0]
  img_height = struct.unpack('i',header_data[22:26])[0]
  bpp = struct.unpack('i',header_data[28:30]+'\x00'+'\x00')[0]
  first_pixel = struct.unpack('i',header_data[10:14])[0]
  header_size = struct.unpack('i',header_data[14:18])[0]

  # Some BMP files have larger headers.
  # We dont need any of the extra fields, but need to store so we can write to output.
  if header_size > 40:
    header_data = header_data + img_in.read(header_size-40)
  
  # Now read the actual image data into a list of integers for convenience
  img_data = []
  for row in range(img_height):
    img_data.append([])
    for col in range(img_width):
      img_data[row].append([])
      img_data[row][col].append(struct.unpack('i', img_in.read(1)+'\x00'+'\x00'+'\x00')[0])
      img_data[row][col].append(struct.unpack('i', img_in.read(1)+'\x00'+'\x00'+'\x00')[0])
      img_data[row][col].append(struct.unpack('i', img_in.read(1)+'\x00'+'\x00'+'\x00')[0])

  img_in.close()
  
  return ( img_data, header_data, img_height, img_width )

# Read the filter information from command line and 
# set it up to be used on the image  
def parseFilterCmdArgs( cmd_args ):

  filter_width = int( cmd_args[3] )
  filter_weights = []
  filter_offsets = []

  for i in range(0,filter_width*filter_width):
    filter_weights.append( float(cmd_args[4+i] ))

  return ( filter_width, filter_weights )

# Do the actual filtering operation by applying
# the filter to the data and storing the result in out_img_data
def doConvolution( img_data, filter_width, filter_weights, img_height, img_width ):
  
  out_img_data = copy.deepcopy(img_data)
  for row in range(filter_width/2,img_height-filter_width/2-1):
    for col in range(filter_width/2,img_width-filter_width/2-1):
      for color in range(0,3):
        out_img_data[row][col][color] = 0
        filter_index = 0
        for row_offset in range(-filter_width/2,filter_width/2):
          for col_offset in range(-filter_width/2,filter_width/2):
            weight = filter_weights[filter_index]
            out_img_data[row][col][color] += weight*img_data[row+row_offset][col+col_offset][color]
            filter_index = filter_index+1
          
  return out_img_data     
  
# Write the output image to file  
def saveBMPImage( out_img_data, header_data, out_fname, img_height, img_width ):
  img_out = open( out_fname, 'wb' )
  img_out.write( header_data )
  for row in range(img_height):
    for col in range(img_width):
      for color in range(0,3): 
        img_out.write(struct.pack('1B', max(min(out_img_data[row][col][color],255),0)))

  img_out.close()

# The main code starts here 
def main():
    (img_data, header_data, img_height, img_width) = loadBMPImage( sys.argv[1] )
    (filter_width, filter_weights) = parseFilterCmdArgs( sys.argv )
    out_img_data = doConvolution( img_data, filter_width, filter_weights, img_height, img_width )
    saveBMPImage( out_img_data, header_data, sys.argv[2], img_height, img_width )

cProfile.run("main()")
