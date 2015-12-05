/************************************************************************
* FILE: fast_filter.h
* AUTHORS: David Meger, 2015
**************************************************************************/

//
// FUNCTION: doFiltering
// BRIEF: Implements efficient image convolution.
// ARGUMENTS:  
//    img_data       [IN]  A pointer to the complete raw binary data 
//                         of a BMP format image.
//    filter_weights [IN]  An array holding a filter. Size filter_width^2.  
//    filter_width   [IN]  The width of the filter. Since filters must be 
//                         square, this is equal to the height.
//    out_img_data   [OUT] Will hold the filtered result as a complete raw 
//                         BMP image suitable for writing to file 
//                         with fwrite(..). The memory at this pointer 
//                         must be allocated by the user and must be the 
//                         same size as img_data. 
//
void doFiltering( unsigned char* img_data, float* filter_weights,       
                  int filter_width,        unsigned char* out_img_data );
                  
