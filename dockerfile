FROM python:3.6
WORKDIR /Users/rajmohan/Desktop/Steganogrtaphy/Image-Steganography/
COPY original.png /Image-Steganography/
COPY requirements.txt /Image-Steganography/
ADD stegano.py ./
ADD requirements.txt ./
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
CMD python stegano.py
