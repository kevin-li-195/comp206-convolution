#include "fast_filter.h"
#include <stdlib.h>
#include <stdio.h>

void main(int argc, char *argv[]) {
    FILE *input_bmp, *output_bmp;
    int filter_width, filter_width_sq;
    unsigned char *func_input, *func_output;
    filter_width = atoi(argv[3]);
    filter_width_sq = filter_width*filter_width;

    if (!(argc == 4+filter_width_sq)) {
        printf("Incorrect filter matrix. Try again.\nMake sure filter size is filter width ^ 2.\n");
        exit(0);
    }

    input_bmp = fopen(argv[1], "rb");
    output_bmp = fopen(argv[2], "wb");

    // Need to malloc size of bmp for output of doFiltering
    fseek(input_bmp, 0L, SEEK_END);
    int sz = ftell(input_bmp);
    rewind(input_bmp);
    func_output = (unsigned char*)calloc(1, sz);
    func_input = (unsigned char*)calloc(1, sz);

    // Now we read the input file into the func_input char array.
    fread(func_input, sz, 1, input_bmp);

    // Here we build the filter array from cli args.
    float filter_array[filter_width_sq];
    int i;
    for (i=0; i<filter_width_sq; i++) {
        filter_array[i] = atof(argv[4+i]);
    }

    doFiltering(func_input, filter_array, filter_width, func_output);
    fwrite(func_output, 1, sz, output_bmp);
    fclose(input_bmp);
    fclose(output_bmp);
}
