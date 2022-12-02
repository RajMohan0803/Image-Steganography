# Importing library
import qrcode

# Data to encode
data = "message"


qr = qrcode.QRCode(version = 1,
				box_size = 10,
				border = 1)

# Adding data to the instance 'qr'
qr.add_data(data)

qr.make(fit = True)
img = qr.make_image(fill_color = 'red',
					back_color = 'white')

img.save('MyQRCode2.png')
