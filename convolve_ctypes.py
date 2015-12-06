import ctypes as c
import sys
import os

if (len(sys.argv) < 5):
    print("Not enough args.")
    sys.exit(0)

if (len(sys.argv) != ((int(sys.argv[3]) ** 2))+4):
    print("Filter matrix is incorrectly formatted. Make sure it's filter width ^ 2.")
    sys.exit(0)

c.cdll.LoadLibrary("libc.so.6")
c.cdll.LoadLibrary("libfast_filter.so")
libc = c.CDLL("libc.so.6")
ff = c.CDLL("libfast_filter.so")
filter_width = int(sys.argv[3])
fw_sq = filter_width ** 2
input_bmp = open(sys.argv[1], "rb")
output_bmp = open(sys.argv[2], "wb")

# We need a filter matrix of ctype floats and a ctype filter_width
a = 0
filter_matrix = []
while a < fw_sq:
    filter_matrix.append(float(sys.argv[4+a]))
    a += 1
cfloat = c.c_float * len(filter_matrix)
cfilter_matrix = cfloat(*filter_matrix)
cfilter_width = c.c_int(filter_width)

# Now we need to store the input_bmp data.
input_string = input_bmp.read()
input_info = os.stat(sys.argv[1])
sz = input_info.st_size

func_input = c.c_char_p(input_string)
func_output = c.create_string_buffer(sz)

# We now have the input data pointer (func_input), output data pointer (func_output),
# filter weight matrix(cfilter_matrix), and filter width (cfilter_width).

ff.doFiltering(func_input, cfilter_matrix, cfilter_width, func_output)

output_bmp.write(func_output)

input_bmp.close()
output_bmp.close()
