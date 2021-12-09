import tkinter
import tempfile
from tkinter import filedialog, messagebox
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from skimage import io, img_as_float
from skimage.filters import unsharp_mask
from tempfile import NamedTemporaryFile, SpooledTemporaryFile
import bm3d

input_img=''
trim=''
ent=''
lab_img=''
rr= ''
ee=''
input=''

#input citra
def File():
    global input_img
    global input
    global lab_img
    global trim
    global rr
    global ee

    # input file
    input_img = filedialog.askopenfilename(initialdir="/", title="select file",
                                     filetypes=(
                                     ("tiff", "*.tiff"), ("tif","*.tif"), ("jpg", "*.jpg"),("png", "*.png"),("all file", "*.txt")))
    # Value image
    ui=cv2.imread(input_img,0)
    lab_img=cv2.imread(input_img)
    input_img=cv2.imread(input_img,cv2.COLOR_BGR2GRAY)
    path = tempfile.gettempdir()
    cv2.imwrite(os.path.join(path, 'lab.tiff'), lab_img)
    cv2.imwrite(os.path.join(path, 'Asli.tiff'), input_img)
    trim = input_img

    # image to 8 bit
    input_img = (input_img / 256).astype('uint8')
    input_img = cv2.normalize(input_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    cv2.imwrite(os.path.join(path, 'seg.tiff'), input_img)

    # UI
    print(ui.shape)
    e, r = ui.shape

    if r >0 and r < 1500:
        rr=2.3
        ee=2.1
        size = (int(r / rr), int(e /ee))
        Tampil = cv2.resize(lab_img, size, interpolation=cv2.INTER_AREA)
        pillow_img = Image.fromarray(Tampil)
        uu = ImageTk.PhotoImage(pillow_img)
        label.configure(image=uu)
        label.image = uu

    if r >1500 and r < 3700:
        rr=2.95
        ee=2.4
        size = (int(r / rr), int(e /ee))
        Tampil = cv2.resize(lab_img, size, interpolation=cv2.INTER_AREA)
        pillow_img = Image.fromarray(Tampil)
        uu = ImageTk.PhotoImage(pillow_img)
        label.configure(image=uu)
        label.image = uu

    if r > 3700 and r < 3899:
        rr = 5.8
        ee = 6
        size = (int(r / rr), int(e / ee))
        Tampil = cv2.resize(lab_img, size, interpolation=cv2.INTER_AREA)
        pillow_img = Image.fromarray(Tampil)
        uu = ImageTk.PhotoImage(pillow_img)
        label.configure(image=uu)
        label.image = uu

    if r > 3900 and r < 5700:
        rr = 6.15
        ee = 6
        size = (int(r / rr), int(e / ee))
        Tampil = cv2.resize(lab_img, size, interpolation=cv2.INTER_AREA)
        pillow_img = Image.fromarray(Tampil)
        uu = ImageTk.PhotoImage(pillow_img)
        label.configure(image=uu)
        label.image = uu

    if r > 5701 :
        rr = 9.4
        ee = 10.1
        size = (int(r / rr), int(e / ee))
        Tampil = cv2.resize(lab_img, size, interpolation=cv2.INTER_AREA)
        pillow_img = Image.fromarray(Tampil)
        uu = ImageTk.PhotoImage(pillow_img)
        label.configure(image=uu)
        label.image = uu

#CLAHE
def CLAHE():

    def OK():
        global lab_img
        global trim

        #value clahe
        value_clahe = float(ent1.get())
        print('value CLAHE :', value_clahe)

        #value unshrap
        value_unsharp = float(ent3.get())
        print('value Unshrap :', value_unsharp)

        root3.destroy()

        path = tempfile.gettempdir()
        lab_img= cv2.imread(os.path.join(path, 'lab.tiff'))

        img = np.array(lab_img, dtype=np.uint8)
        img1 = cv2.normalize(img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Converting image to LAB image for CLAHE
        lab_img = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_img)

        ###########CLAHE#########################
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=value_clahe, tileGridSize=(8, 8)) #value input
        clahe_img = clahe.apply(l)

        # Combine the CLAHE enhanced L with A and B channels
        updated_lab_img2 = cv2.merge((clahe_img, a, b))

        # Convert LAB image to RGB
        CLAHE_img = cv2.cvtColor(updated_lab_img2, cv2.COLOR_LAB2BGR)

        cv2.imwrite(os.path.join(path,'sampel.jpg'), CLAHE_img)


        ### sharpng ###
        img = io.imread(os.path.join(path,'sampel.jpg'))
        unsharped_img = unsharp_mask(img, radius=value_unsharp, amount=1) #value input unsharep
        io.imsave(os.path.join(path,'sampel.jpg'), unsharped_img)

        img = cv2.imread(os.path.join(path, 'sampel.jpg'))

        # image change 8-bit
        img = np.array(img, dtype=np.uint8)
        img1 = cv2.normalize(img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)  # 8 bit
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        # value 8 bit to 16 bit
        img = np.array(img1, dtype=np.uint16)
        img = cv2.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)  # 16 bit

        e, r = img1.shape
        size = (int(r / rr), int(e / ee))
        tampilkan2 = cv2.resize(img1, size, interpolation=cv2.INTER_AREA)
        pillow_img2 = Image.fromarray(tampilkan2)
        xx = ImageTk.PhotoImage(pillow_img2)
        label2.configure(image=xx)
        label2.image = xx
        trim = img

    # Layout
    root3 = tkinter.Tk()
    root3.minsize(width=200, height=200)
    root3.maxsize(width=200, height=200)

    # input
    lab = tkinter.Label(root3, text="CLAHE")
    lab.place(x=20, y=20)
    ent1 = tkinter.Entry(root3, width=5)
    ent1.place(x=110, y=23)

    lab = tkinter.Label(root3, text="Unsharp")
    lab.place(x=20, y=70)
    ent3 = tkinter.Entry(root3, width=5)
    ent3.place(x=110, y=73)

    btn_file = tkinter.Button(root3, text="OK", width=10, command=OK)
    btn_file.place(x=60, y=160)

    root3.title("CLAHE")
    root3.mainloop()

#Save Image
def save():
    global trim # value image CLAHE

    files = [("file tiff", "*.tiff"), ("file jpg", "*.jpg"), ("file png", "*.png"),
             ("all file", "*.txt")]
    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='save image', filetypes=files,
                                        defaultextension=files)
    io.imsave(file, trim)

#reset
def reset():
    global trim

    path = tempfile.gettempdir()
    Asli=cv2.imread(os.path.join(path, 'Asli.tiff'))

    # convert image to 8 bit
    x = np.array(Asli, dtype=np.uint8)
    x = cv2.normalize(x, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # convert image to 16-bit
    Hasil = np.array(x, dtype=np.uint16)
    Hasil = cv2.normalize(Hasil, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
    cv2.imwrite(os.path.join(path, 'sampel.jpg'), Hasil)
    Hasil = cv2.cvtColor(Hasil, cv2.COLOR_BGR2GRAY)

    #UI
    e, r = Hasil.shape
    size = (int(r / rr), int(e / ee))
    tampilkan2 = cv2.resize(x, size, interpolation=cv2.INTER_AREA)
    # tampilkan2 = cv2.rotate(tampilkan2, cv2.ROTATE_90_COUNTERCLOCKWISE) # jika harus dirotate
    pillow_img2 = Image.fromarray(tampilkan2)
    xx = ImageTk.PhotoImage(pillow_img2)
    label2.configure(image=xx)
    label2.image = xx

    trim=Hasil
    path = tempfile.gettempdir()
    cv2.imwrite(os.path.join(path, 'sampel.jpg'), x)

root = tkinter.Tk()
ww=1.5
t1 = tkinter.StringVar()
t2 = tkinter.StringVar()
root.minsize(width=770, height=1260)
root.maxsize(width=770, height=1260)

root.resizable(True,True)

#wraper
wrapper = tkinter.LabelFrame(root, text='Image', width=455*ww, height=360*ww)
wrapper.pack(side=tkinter.LEFT)
wrapper.place(x=15*ww, y=10*ww)

wrapper2 = tkinter.LabelFrame(root, text='Image Processing',width=455*ww, height=360*ww)
wrapper2.pack(side=tkinter.LEFT)
wrapper2.place(x=15*ww, y=400*ww)

#label
label = tkinter.Label(wrapper)
label.pack(side=tkinter.LEFT)
label.place(x=10, y=5)
label.grid_propagate(0)
label.columnconfigure(1, weight=1)

label2 = tkinter.Label(wrapper2)
label2.pack(side=tkinter.LEFT)
label2.place(x=10, y=5)
label2.grid_propagate(0)
label2.columnconfigure(1, weight=1)

#menubar
my_menu=tkinter.Menu(root)
root.config(menu=my_menu)

#create a menu item
file_menu=tkinter.Menu(my_menu)
my_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='Open', command=File)
file_menu.add_command(label='Save', command=save)

# Button
btn_file = tkinter.Button(root, text="Clahe", width=10, command=CLAHE)
btn_file.place(x=5*ww, y=780*ww)

btn_file = tkinter.Button(root, text="Reset", width=15, command=reset)
btn_file.place(x=75*ww, y=780*ww)

root.title("ImagePro")
root.mainloop()
