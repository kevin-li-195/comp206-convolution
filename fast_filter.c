#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function doFiltering. See the header fast_filter.h for details
void doFiltering( unsigned char* img_data, float* filter_weights,       
                  int filter_width,        unsigned char* out_img_data )
{
  unsigned int   data_size        = *((unsigned int*)(img_data+2));  
  unsigned int   header_size      = *((unsigned int*)(img_data+10));
  unsigned int   img_width        = *((unsigned int*)(img_data+18));
  unsigned int   img_height       = *((unsigned int*)(img_data+22));
  unsigned int   num_colors       = *((unsigned int*)(img_data+28)) / 8;
  unsigned char* start_of_out_img = out_img_data;

  memcpy( out_img_data, img_data, header_size );
  out_img_data+=header_size;
  img_data+=header_size;

  unsigned int row, col, color, filter_row, filter_col;
  for( row=0; row<img_height-filter_width; row++ )
    for( col=0; col<img_width-filter_width; col++ )
      for( color=0; color<num_colors; color++ )
      {
        float result = 0;
        for( filter_row=0; filter_row<filter_width; filter_row++ )
          for( filter_col=0; filter_col<filter_width; filter_col++ )
            result += filter_weights[filter_row*filter_width+filter_col] * 
                      img_data[(row+filter_row)*img_width*num_colors+(col+filter_col)*num_colors+color];

        if(result<0) result=0;
        if(result>255) result=255;
        out_img_data[(row+filter_width/2)*img_width*num_colors+(col+filter_width/2)*num_colors+color] = result;
      }
}

