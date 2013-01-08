#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_vehiclerentaldlg


class VehicleRentalDlg(QDialog,
        ui_vehiclerentaldlg.Ui_VehicleRentalDlg):

    def __init__(self, parent=None):
        super(VehicleRentalDlg, self).__init__(parent)
        self.setupUi(self)
        self.vehicleComboBox.setFocus()


    @pyqtSignature("QString")
    def on_vehicleComboBox_currentIndexChanged(self, text):
        if text == "Car":
            self.mileageLabel.setText("1000 miles")
        else:
            self.on_weightSpinBox_valueChanged(
                    self.weightSpinBox.value())


    @pyqtSignature("int")
    def on_weightSpinBox_valueChanged(self, amount):
        self.mileageLabel.setText("%d miles" % (8000 / amount))


app = QApplication(sys.argv)
form = VehicleRentalDlg()
form.show()
app.exec_()

