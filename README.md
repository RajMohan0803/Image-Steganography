# Image-Steganography
The aim is to develop a set of effective steganography techniques for concealing information within an image.
In the event that secret information is decoded, the target is encrpted using AES-128.
To avoid detection that the image is detected we aim to decrease to modification by encoding via the least significant bit.

In the real world, images are shared freely and are compressed. We explore using reed solo forward error correction through qr and by zfec. This allows for a greater chance that the image preserves the information we want to encode.

It is worth noting that this fec increases image size, however unless people have access to the ORIGINAL image, it doesnt pose significant increase in risk.
