## I. Product report.
### 1. Explain the assignment:

1.1.	Image processing:
+ After uploading photos from the folder, image processing will be performed. The processing here is smoothing, light balance, noise reduction, and contrast.
+ Perform an average calculation of the parameters of the original image to provide the most accurate data. Based on data to classify images and apply processing to each individual case.

1.2. Display photos:
+ Use tkinter Library to upload photos from the device.
+ When the image has been processed, QR code recognition in the image will be performed. The QR code will be found using the decode library. Then, proceed to determine the position of the image, display the location of the QR code and determine the content of the QR code with the content displayed in the image.

### 2. Results:

2.1. When running the program, the "tkinter" library helps open the device's folder box to select images to scan for QR.

2.2. Scan one QR to many QRs in 1 image.

2.3. Scan images automatically, calculate brightness, smoothness,... of the image, then specifically process each image to determine the qr code.

2.4. Print the parameters to the screen:
+ Average brightness level of the image.
+ Content of the QR code scanned from the image.
+ Number of qr detected in the scanned image.

## II. User manual

### 1. Preparation:
- Language used: Python
- Libraries: Open cv2, Matplotlib, tkinter, PyZbar
- Photos containing QR codes are in the folder.

### 2. Use code scanning facility:
+ Launch the program (For visual: select Run Python -> Run Python File in Terminal)

### 3. Displays on the image when scanning the code.
- Successfully scanned, giving 3 interfaces (original image, image after preprocessing, code detected image).
- The image of the detected code will have content above the QR (red), and a border to indicate the location of the found code (blue).

### 4. Displays are printed when the program is run.
- Average brightness level of the image.
- Content of the QR code scanned from the image.
- QR number detected in the scanned image.
