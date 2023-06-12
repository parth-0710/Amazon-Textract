import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import boto3

my_w = tk.Tk()
my_w.geometry("450x400")
my_w.title("AWS Textract")
my_font1 = ("Times", 18, "bold")
l1 = tk.Label(my_w, text='Upload An Image', width=30, font=my_font1)
l1.pack()
b1 = tk.Button(my_w, text='Upload File & See What it Has!!!', width=30, command=lambda: upload_file())
b1.pack()

def upload_file():
    aws_mag_con = boto3.session.Session(profile_name='parth_trivedi')
    client = aws_mag_con.client(service_name='textract', region_name='ap-south-1')
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    
    try:
        img = Image.open(filename)
        # Resizing
        img_resize = img.resize((400, 300))
        img = ImageTk.PhotoImage(img_resize)
        imgbytes = get_image_byte(filename)
        b2 = tk.Button(my_w, image=img)
        b2.pack()
        response = client.detect_document_text(Document={'Bytes': imgbytes})
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                print(item["Text"])
    except Exception as e:
        print("Error opening image:", e)

def get_image_byte(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

my_w.mainloop()
