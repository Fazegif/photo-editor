from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import os
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import *

app = QApplication([])
win = QWidget()
btn_dir = QPushButton('Папка')
btn_1 = QPushButton('Лево')
btn_2 = QPushButton('Право')
btn_3 = QPushButton('Зеркало')
btn_4 = QPushButton('Резкость')
btn_5 = QPushButton('Ч/Б')
text = QLabel('Картинка')
the_list = QListWidget()

win.resize(700, 400)

row = QHBoxLayout()
row1 = QHBoxLayout()
row2 = QVBoxLayout()
row3 = QVBoxLayout()
row1.addWidget(btn_1)
row1.addWidget(btn_2)
row1.addWidget(btn_3)
row1.addWidget(btn_4)
row1.addWidget(btn_5)
row3.addWidget(btn_dir)
row2.addWidget(text)
row2.addLayout(row1)
row3.addWidget(the_list)
row.addLayout(row3, 20)
row.addLayout(row2, 80)

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    result = list()
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkdir()
    filenames = os.listdir(workdir)
    extensions = ['png','jpg']
    result = filter(filenames, extensions)
    the_list.clear()
    for res in result:
        the_list.addItem(res)

class ImageEditor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadimage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        text.hide()
        pixmapimage = QPixmap(path)
        w, h = text.width(), text.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        text.setPixmap(pixmapimage)
        text.show()
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)

workimage = ImageEditor()

def showChoosenImage():
    if the_list.currentRow() >= 0:
        filename = the_list.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

btn_dir.clicked.connect(showFilenamesList)
the_list.currentRowChanged.connect(showChoosenImage)
btn_5.clicked.connect(workimage.do_bw)
btn_3.clicked.connect(workimage.do_flip)
btn_1.clicked.connect(workimage.do_left)
btn_2.clicked.connect(workimage.do_right)
btn_4.clicked.connect(workimage.do_sharpen)
    
win.setLayout(row)
win.show()
app.exec()