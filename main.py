from PIL import Image
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('shab.ui', self)
        self.initUI()

    def initUI(self):
        try:
            self.lbl = QLabel(self)
            self.pixmap = QPixmap('r1.jpg')
            self.pixmap = self.pixmap.scaled(1000, 700)
            self.lbl.setPixmap(self.pixmap)
            self.lbl.move(20, 250)
            self.pushButton.clicked.connect(self.run)
            self.pushButton_2.clicked.connect(self.changed)
            self.pushButton_3.clicked.connect(self.run2)
            self.im = Image.open('r1.jpg').copy()
            self.label_24.setText('{}, {}'.format(self.im.size[0], self.im.size[1]))
        except Exception:
            pass

    def get(self, pict):
        x = 0
        y = 0
        if Image.open(pict).size[0] < 1000:
            x = Image.open(pict).size[0]
        else:
            x = 1000
        if Image.open(pict).size[1] < 700:
            y = Image.open(pict).size[1]
        else:
            y = 700
        n_pixmap = QPixmap(pict)
        n_pixmap = n_pixmap.scaled(x, y)
        self.lbl.setPixmap(n_pixmap)
        self.lbl.move(20, 250)

    def run2(self):
        try:
            x1 = int(self.lineEdit_7.text())
            y1 = int(self.lineEdit_8.text())
            x2 = int(self.lineEdit_9.text())
            y2 = int(self.lineEdit_10.text())
            area = (x1, y1, x2, y2)
            nim = self.im.crop(area)
            self.im = nim
            self.im.save('r3.jpg')
            self.get('r3.jpg')
            self.label_24.setText('{}, {}'.format(self.im.size[0], self.im.size[1]))
            self.label_16.setText('Обрезание картинки:')
        except Exception:
            self.label_16.setText('ОШИБКА')

    def run(self):
        try:
            file = self.lineEdit.text()
            if file != '':
                im = Image.open(file)
                self.im = im.copy()
                self.im.save('r3.jpg')
                self.get('r3.jpg')
            else:
                im = Image.open('r1.jpg')
                self.im = im.copy()
                self.im.save('r3.jpg')
                self.get('r3.jpg')
            self.label_24.setText('{}, {}'.format(self.im.size[0], self.im.size[1]))
        except Exception:
            self.label.setText('Укажите существующий файл')

    def changed(self):
        try:
            if self.checkBox_7.isChecked():
                self.makeanagliph(self.im, int(self.lineEdit_2.text()))
            if self.checkBox_3.isChecked():
                self.negative(self.im)
            if self.checkBox_4.isChecked():
                self.overlay(self.im)
            if self.checkBox_6.isChecked():
                name = self.lineEdit_3.text()
                x, y = self.im.size
                im2 = Image.open(name)
                im2 = im2.resize((x, y), Image.ANTIALIAS)
                self.transparency(self.im,im2)
            if self.checkBox_5.isChecked():
                k = int(self.lineEdit_4.text())
                self.sepiy(self.im, k)
            if self.checkBox_2.isChecked():
                f = int(self.lineEdit_5.text())
                self.add_noise(self.im, f)
            if self.checkBox.isChecked():
                f = int(self.lineEdit_6.text())
                self.brightness(self.im, f)
            self.im.save('r3.jpg')
            self.get('r3.jpg')
            self.label_2.setText('Фильтры и рофлянки:')
        except Exception:
            self.label_2.setText('ОШИБКА')

    def makeanagliph(self, im, delta):
        m = im.copy()
        pixels = m.load()
        pixels1 = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                if i < delta:
                    r, g, b = pixels[i, j]
                    pixels1[i, j] = 0, g, b
                else:
                    r, g, b = pixels[i - delta, j]
                    rr, gg, bb = pixels[i, j]
                    pixels1[i, j] = r, gg, bb
        return None

    def transparency(self, im, im1):
        pixels = im.load()
        pixels1 = im1.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                rr, gg, bb = pixels1[i, j]
                pixels[i, j] = int(0.5 * r + 0.5 * rr), int(0.5 * g + 0.5 * gg), int(0.5 * b + 0.5 * bb)
        return None

    def negative(self, im):
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 255 - r, 255 - g, 255 - b
        return None

    def overlay(self, im):
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                s = (r + g + b) // 3
                pixels[i, j] = s, s, s
        return None

    def sepiy(self, im, k):
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                s = (r + g + b) // 3
                r = s + 2 * k
                g = s + k
                b = s
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                pixels[i, j] = r, g, b
        return None

    def add_noise(self, im, f):
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                rand = random.randint(-f, f)
                r, g, b = pixels[i, j]
                r = r + rand
                g = g + rand
                b = b + rand
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                if r < 0:
                    r = 0
                if g < 0:
                    g = 0
                if b < 0:
                    b = 0
                pixels[i, j] = r, g, b
        return None

    def brightness(self, im, f):
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                r = r + f
                g = g + f
                b = b + f
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                if r < 0:
                    r = 0
                if g < 0:
                    g = 0
                if b < 0:
                    b = 0
                pixels[i, j] = r, g, b
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
