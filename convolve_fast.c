#include <fast_filter.h>

void main(int argc, char *argv[]) {
    FILE *input_bmp, *output_bmp;
    int filter_width;
    input_bmp = fopen(argv[1], "r");
    output_bmp = fopen(argv[2], "w");
    filter_width = atoi(argv[3]);
    filter_width_sq = (int)pow((double) filter_width, 2);

}

