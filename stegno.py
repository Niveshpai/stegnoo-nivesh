import cv2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

# Create GUI window
root = tk.Tk()
root.withdraw()  

# Open file dialog to select the image
file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
if not file_path:
    print("No file selected. Program closed.")
    exit()

img = cv2.imread(file_path)

# secret message and password in encryption
msg = simpledialog.askstring("Input", "Enter secret message:")
password = simpledialog.askstring("Input", "Enter a passcode:")

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

m = 0
n = 0
z = 0

for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

encrypted_image_path = "encryptedImage.jpg"
cv2.imwrite(encrypted_image_path, img)

os.system(f"start {encrypted_image_path}")

# Decryption
message = ""
n = 0
m = 0
z = 0
pas = simpledialog.askstring("Input", "Enter passcode for Decryption")

if password == pas:
    for i in range(len(msg)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    print("Decryption message:", message)
else:
    print("You are not authorized")
