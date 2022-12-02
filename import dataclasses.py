import dataclasses
import os
import numpy as np
import qrcode
import base64

from imageio import imread, imwrite

import argparse

max_value = 255 # max uint value per pixel per channel
header_len = 4*8 # uint32 bit length

def read_image(img_path):

    img = np.array(imread(img_path), dtype=np.uint8)
    orig_shape = img.shape
    return img.flatten(), orig_shape

def write_image(img_path, img_data, shape):
    
    img_data = np.reshape(img_data, shape)
    imwrite(img_path, img_data)

def bytes2array(byte_data):
   
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)
    return np.unpackbits(byte_array)

def array2bytes(bit_array):
   
    byte_array = np.packbits(bit_array)
    return byte_array.tobytes()

def read_file(file_path):
   
    file_bytes = open(file_path, "rb").read()
    return bytes2array(file_bytes)

def write_file(file_path, file_bit_array):
   
    bytes_data = array2bytes(file_bit_array)
    f = open(file_path, 'wb')
    f.write(bytes_data)
    f.close()

def encode_data(image, file_data):
   
    or_mask = file_data
    and_mask = np.zeros_like(or_mask)
    and_mask = (and_mask + max_value - 1) + or_mask 
    res = np.bitwise_or(image, or_mask)
    res = np.bitwise_and(res, and_mask)
    return res

def qrreedenc():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4)
    
    qr.add_data(dataclasses)
    qr.make(fit=True)
    immg = qr.make_image(fill_color="red", back_color="black")
    
    with open("immg.png", "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    
   #converted string should be sent as secret to stegano




def decode_data(encoded_data):

    file = open('encode.bin', 'rb')
    byte = file.read()
    file.close()

    decodeit = open('secret.png', 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()
   
    out_mask = np.ones_like(encoded_data)
    output = np.bitwise_and(encoded_data, out_mask)
    return output


    
def _main(args):
    """Main fuction of the script"""
    if args.image is not None and args.file is not None:
        if args.encode:
            img_path = args.image
            file_path = args.file
            if not os.path.isfile(img_path):
                print("Image file does not exist")
                return
            if not os.path.isfile(file_path):
                print("File does not exist")
                return

            output_path = args.output
            extension = os.path.splitext(output_path)[1][1:]
            if extension == '':  # if no extension, append png
                output_path = output_path + '.png'
            elif extension != 'png':  # replace the wrong extension with png
                li = output_path.rsplit(extension, 1)
                output_path = 'png'.join(li)

            image, shape_orig = read_image(img_path)
            file = read_file(file_path)
            file_len = file.shape[0]
            len_array = np.array([file_len], dtype=np.uint32).view(np.uint8)
            len_array = np.unpackbits(len_array)
            img_len = image.shape[0]

            if file_len >= img_len - header_len:  # 4 bytes are used to store file length
                print("File too big, error")
                return
            else:  #  Insert padding. Using random padding, otherwise values would all be even if padding with zeros (could be noticed in histogram).
                tmp = file
                file = np.random.randint(2, size=img_len, dtype=np.uint8)
                file[header_len:header_len+file_len] = tmp
                # file = np.pad(file, (header_len,img_len - file_len - header_len), 'constant', constant_values=(0, 0))

            file[:header_len] = len_array
            encoded_data = encode_data(image, file)

            write_image(output_path, encoded_data, shape_orig)
            print("Image encoded")
            return

        if args.decode:
            img_path = args.image
            if not os.path.isfile(img_path):
                print("Image file does not exist")
                return
            file_path = args.file
            encoded_data, shape_orig = read_image(img_path)
            data = decode_data(encoded_data)
            el_array = np.packbits(data[:header_len])
            extracted_len = el_array.view(np.uint32)[0]
            data = data[header_len:extracted_len+header_len]
            write_file(file_path, data)
            print("Image decoded")
            return

        print("Error, no action specified!")
        return

    print("Error, image or file not specified")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Conceal small files inside a PNG image and extract them back')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-e',
        '--encode',
        help='If present the script will conceal the file in the image and produce a new encoded image',
        action="store_true")
    group.add_argument(
        '-d',
        '--decode',
        help='If present the script will decode the concealed data in the image and produce a new file with this data',
        action="store_true")
    parser.add_argument(
        '-i',
        '--image',
        help='Path to an image to use for concealing or file extraction')
    parser.add_argument(
        '-f',
        '--file',
        help='Path to the file to conceal or to extract')
    parser.add_argument(
        '-o',
        '--output',
        help='Path where to save the encoded image. Specify only the file name, or use .png extension; png extension will be added automatically',
        default='encoded.png')

    _main(parser.parse_args())