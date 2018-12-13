import math

import cv2

src_img = cv2.imread('', 0)
src_height = src_img.shape[0]
src_width = src_img.shape[1]

template_img = cv2.imread('', 0)
temp_height = template_img.shape[0]
temp_width = template_img.shape[1]

result_list = []
result_list2 = []


# Using normalized cross-correlation formula:
# https://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html
def template_matching(i, j, template_img): #currently needs to be run in a loop of an image

    temporary_img = src_img[i:temp_height+i, j:temp_width+j]  # sub image made from the src image

    for k in range(int(temp_height/2),int(temp_height/2)+1):    # start in the middle pixel of the image, only runs once
        for l in range(int(temp_width/2), int(temp_width/2)+1): # start in the middle pixel of thet image, only runs once
            src_sum = 0                                         # makes it possible to save the sum after each iteration
            src_pow_sum = 0                                     # makes it possible to save the sum after each iteration

            template_sum = 0                                    # makes it possible to save the sum after each iteration
            template_pow_sum = 0                                # makes it possible to save the sum after each iteration

            for z in range(int(-temp_height/2), int(temp_width/2)):     # kernel size of the template image
                for x in range(int(-temp_height/2), int(temp_width/2)): # kernel size of the template image
                    src_kernel = temporary_img.item(k+z, l+x)           # get greyscale value of temporary image at location k+z and l+x
                    template_kernel = template_img.item(k+z, l+x)       # get greyscale value of template image at location k+z and l+x

                    src_sum = src_sum + src_kernel                      # adds every iteration of src kernel to the current value of src sum
                    template_sum = template_sum + template_kernel       # adds every iteration of template kernel to the current value of template sum


                    src_pow_sum = src_pow_sum + math.pow(src_kernel, 2)                   # squares the values of src kernel for each iteration
                    template_pow_sum = template_pow_sum + math.pow(template_kernel, 2)    # squares the values of template kernel for each iteration

                    kernel_sum = (src_kernel * template_sum)                              # The sum of greyscale intensities of src and template
                    math_pow = int(math.sqrt(src_pow_sum * template_pow_sum))             # sums the two squared kernels

            result = kernel_sum / math_pow
            result = math.floor(result * 10000) / 10000.0   # rounding down with 4 decimals
            if result == 1.0:
                print('i',i)
                print('j',j)
                print('is 1.0')

        return result, i, j


for i in range(1, src_height-temp_height):
    result_list2.append(result_list) #highest value of result_list and coordinates is stored
    del result_list2[:-1]

    for j in range(1, src_width-temp_width):
        a = template_matching(i, j, template_img)
        result_list.append(a)
        b = max(result_list)
        result_list.clear()
        result_list.append(b)


cv2.imshow('test', src_img)
cv2.waitKey()