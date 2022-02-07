import sys
import time


from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from kysymykset import lataa_kysymykset_netistä
from quiz_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tiedot = lataa_kysymykset_netistä() 
        self.vaihda_kysymys_ja_vastaus(0)
        self.kytke_napit()
        self.pisteet = 0
        self.indeksi = 0

    def vaihda_kysymys_ja_vastaus(self, indeksi):
        tekstit = self.tiedot[indeksi]
        uudet_tekstit = []
        for (numero, teksti) in enumerate(tekstit):
            if teksti.startswith("*"):
                teksti = teksti[1:]
                self.oikea_vastaus = numero
            uudet_tekstit.append(teksti)
        self.aseta_tekstit(uudet_tekstit)
        self.ui.nro_label.setText(f"Kierros {indeksi+1} / {len(self.tiedot)}")

    def aseta_tekstit(self, tekstit):
        self.aseta_kysymys(tekstit[0])
        self.aseta_nappien_tekstit(tekstit[1:])

    def aseta_nappien_tekstit(self, tekstit):
        (t1, t2, t3, t4) = tekstit
        self.ui.button1.setText(t1)
        self.ui.button2.setText(t2)
        self.ui.button3.setText(t3)
        self.ui.button4.setText(t4)

    def aseta_kysymys(self, kysymys):
        self.ui.label.setText(kysymys)

    def kytke_napit(self):
        self.ui.button1.clicked.connect(self.nappia_painettu)
        self.ui.button2.clicked.connect(self.nappia_painettu)
        self.ui.button3.clicked.connect(self.nappia_painettu)
        self.ui.button4.clicked.connect(self.nappia_painettu)

    def nappia_painettu(self):
        if self.sender() == self.ui.button1:
            nappi = 1
        elif self.sender() == self.ui.button2:
            nappi = 2
        elif self.sender() == self.ui.button3:
            nappi = 3
        elif self.sender() == self.ui.button4:
            nappi = 4
        else:
            return

        painettu_nappi = self.sender()

        if nappi == self.oikea_vastaus:
            print("Oikein!")
            self.pisteet += 1
            napin_vari = "rgb(0,255,0)"
        else:
            napin_vari = "rgb(255,0,0)"

        painettu_nappi.setStyleSheet("* {background: " + napin_vari + ";}")
        QApplication.processEvents()
        time.sleep(0.5)
        painettu_nappi.setStyleSheet("")

        self.seuraava_kysymys()


    def seuraava_kysymys(self):
        self.indeksi += 1
        if self.indeksi >= len(self.tiedot):
            laatikko = QMessageBox(self)
            laatikko.setText(f"Peli päättyi. Sait {self.pisteet} pistettä!")
            laatikko.exec()
            self.indeksi = 0
            self.pisteet = 0

        self.vaihda_kysymys_ja_vastaus(self.indeksi)

    @property
    def pisteet(self):
        return self._pisteet

    @pisteet.setter
    def pisteet(self, arvo):
        self._pisteet = arvo
        self.ui.statusbar.showMessage(f"Pisteet: {self.pisteet}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())