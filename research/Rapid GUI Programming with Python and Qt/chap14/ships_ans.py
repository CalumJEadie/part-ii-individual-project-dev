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

import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import richtextlineedit


NAME, OWNER, COUNTRY, DESCRIPTION, TEU = range(5)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


class Ship(object):

    def __init__(self, name, owner, country, teu=0, description=""):
        self.name = QString(name)
        self.owner = QString(owner)
        self.country = QString(country)
        self.teu = teu
        self.description = QString(description)


    def __cmp__(self, other):
        return QString.localeAwareCompare(self.name.toLower(),
                                          other.name.toLower())


class ShipTableModel(QAbstractTableModel):

    def __init__(self, filename=QString()):
        super(ShipTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.ships = []
        self.owners = set()
        self.countries = set()


    def sortByName(self):
        self.ships = sorted(self.ships)
        self.reset()


    def sortByTEU(self):
        ships = [(ship.teu, ship) for ship in self.ships]
        ships.sort()
        self.ships = [ship for teu, ship in ships]
        self.reset()


    def sortByCountryOwner(self):
        def compare(a, b):
            if a.country != b.country:
                return QString.localeAwareCompare(a.country, b.country)
            if a.owner != b.owner:
                return QString.localeAwareCompare(a.owner, b.owner)
            return QString.localeAwareCompare(a.name, b.name)
        self.ships = sorted(self.ships, compare)
        self.reset()


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.ships)):
            return QVariant()
        ship = self.ships[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == NAME:
                return QVariant(ship.name)
            elif column == OWNER:
                return QVariant(ship.owner)
            elif column == COUNTRY:
                return QVariant(ship.country)
            elif column == DESCRIPTION:
                return QVariant(ship.description)
            elif column == TEU:
                return QVariant(QString("%L1").arg(ship.teu))
        elif role == Qt.TextAlignmentRole:
            if column == TEU:
                return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif role == Qt.TextColorRole and column == TEU:
            if ship.teu < 80000:
                return QVariant(QColor(Qt.black))
            elif ship.teu < 100000:
                return QVariant(QColor(Qt.darkBlue))
            elif ship.teu < 120000:
                return QVariant(QColor(Qt.blue))
            else:
                return QVariant(QColor(Qt.red))
        elif role == Qt.BackgroundColorRole:
            if ship.country in (u"Bahamas", u"Cyprus", u"Denmark",
                    u"France", u"Germany", u"Greece"):
                return QVariant(QColor(250, 230, 250))
            elif ship.country in (u"Hong Kong", u"Japan", u"Taiwan"):
                return QVariant(QColor(250, 250, 230))
            elif ship.country in (u"Marshall Islands",):
                return QVariant(QColor(230, 250, 250))
            else:
                return QVariant(QColor(210, 230, 230))
        elif role == Qt.ToolTipRole:
            msg = "<br>(minimum of 3 characters)"
            if column == NAME:
                return QVariant(ship.name + msg)
            elif column == OWNER:
                return QVariant(ship.owner + msg)
            elif column == COUNTRY:
                return QVariant(ship.country + msg)
            elif column == DESCRIPTION:
                return QVariant(ship.description)
            elif column == TEU:
                return QVariant(QString("%L1 twenty foot equivalents") \
                        .arg(ship.teu))
        return QVariant()


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == NAME:
                return QVariant("Name")
            elif section == OWNER:
                return QVariant("Owner")
            elif section == COUNTRY:
                return QVariant("Country")
            elif section == DESCRIPTION:
                return QVariant("Description")
            elif section == TEU:
                return QVariant("TEU")
        return QVariant(int(section + 1))


    def rowCount(self, index=QModelIndex()):
        return len(self.ships)


    def columnCount(self, index=QModelIndex()):
        return 5


    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.ships):
            ship = self.ships[index.row()]
            column = index.column()
            if column == NAME:
                ship.name = value.toString()
            elif column == OWNER:
                ship.owner = value.toString()
            elif column == COUNTRY:
                ship.country = value.toString()
            elif column == DESCRIPTION:
                ship.description = value.toString()
            elif column == TEU:
                value, ok = value.toInt()
                if ok:
                    ship.teu = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False


    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row,
                              Ship(" Unknown", " Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True


    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position,
                             position + rows - 1)
        self.ships = self.ships[:position] + \
                     self.ships[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True


    def load(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for loading"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError, "unrecognized file type version"
            self.ships = []
            while not stream.atEnd():
                name = QString()
                owner = QString()
                country = QString()
                description = QString()
                stream >> name >> owner >> country >> description
                teu = stream.readInt32()
                self.ships.append(Ship(name, owner, country, teu,
                                       description))
                self.owners.add(unicode(owner))
                self.countries.add(unicode(country))
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def save(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for saving"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_1)
            for ship in self.ships:
                stream << ship.name << ship.owner << ship.country \
                       << ship.description
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class ShipDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ShipDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        if index.column() == DESCRIPTION:
            text = index.model().data(index).toString()
            palette = QApplication.palette()
            document = QTextDocument()
            document.setDefaultFont(option.font)
            if option.state & QStyle.State_Selected:
                document.setHtml(QString("<font color=%1>%2</font>") \
                        .arg(palette.highlightedText().color().name())\
                        .arg(text))
            else:
                document.setHtml(text)
            color = palette.highlight().color() \
                if option.state & QStyle.State_Selected \
                else QColor(index.model().data(index,
                        Qt.BackgroundColorRole))
            painter.save()
            painter.fillRect(option.rect, color)
            painter.translate(option.rect.x(), option.rect.y())
            document.drawContents(painter)
            painter.restore()
        else:
            QItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        fm = option.fontMetrics
        if index.column() == TEU:
            return QSize(fm.width("9,999,999"), fm.height())
        if index.column() == DESCRIPTION:
            text = index.model().data(index).toString()
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())
        return QItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index):
        if index.column() == TEU:
            spinbox = QSpinBox(parent)
            spinbox.setRange(0, 200000)
            spinbox.setSingleStep(1000)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() == OWNER:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().owners))
            combobox.setEditable(True)
            return combobox
        elif index.column() == COUNTRY:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().countries))
            combobox.setEditable(True)
            return combobox
        elif index.column() == NAME:
            editor = QLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        elif index.column() == DESCRIPTION:
            editor = richtextlineedit.RichTextLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        else:
            return QItemDelegate.createEditor(self, parent, option,
                                              index)


    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)


    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole).toString()
        if index.column() == TEU:
            value = text.replace(QRegExp("[., ]"), "").toInt()[0]
            editor.setValue(value)
        elif index.column() in (OWNER, COUNTRY):
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        elif index.column() == NAME:
            editor.setText(text)
        elif index.column() == DESCRIPTION:
            editor.setHtml(text)
        else:
            QItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        if index.column() == TEU:
            model.setData(index, QVariant(editor.value()))
        elif index.column() in (OWNER, COUNTRY):
            text = editor.currentText()
            if text.length() >= 3:
                model.setData(index, QVariant(text))
        elif index.column() == NAME:
            text = editor.text()
            if text.length() >= 3:
                model.setData(index, QVariant(text))
        elif index.column() == DESCRIPTION:
            model.setData(index, QVariant(editor.toSimpleHtml()))
        else:
            QItemDelegate.setModelData(self, editor, model, index)


def generateFakeShips():
    for name, owner, country, teu, description in (
(u"Emma M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
 u"<font color=green>109,000 hp</font>"),
(u"MSC Pamela", u"MSC", u"Liberia", 90449,
 u"Draft <font color=green>15m</font>"),
(u"Colombo Express", u"Hapag-Lloyd", u"Germany", 93750,
 u"Main engine, <font color=green>93,500 hp</font>"),
(u"Houston Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Features a <u>twisted leading edge full spade rudder</u>. "
 u"Sister of <i>Savannah Express</i>"),
(u"Savannah Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Sister of <i>Houston Express</i>"),
(u"MSC Susanna", u"MSC", u"Liberia", 90449, u""),
(u"Eleonora M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Hallam</i>"),
(u"Estelle M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Wells</i>"),
(u"Evelyn M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
  u"Captain <i>Byrne</i>"),
(u"Georg M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gerd M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gjertrud M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Grete M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gudrun M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"Gunvor M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, u""),
(u"CSCL Le Havre", u"Danaos Shipping", u"Cyprus", 107200, u""),
(u"CSCL Pusan", u"Danaos Shipping", u"Cyprus", 107200,
 u"Captain <i>Watts</i>"),
(u"Xin Los Angeles", u"China Shipping Container Lines (CSCL)",
 u"Hong Kong", 107200, u""),
(u"Xin Shanghai", u"China Shipping Container Lines (CSCL)", u"Hong Kong",
 107200, u""),
(u"Cosco Beijing", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Hellas", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Guangzhou", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Ningbo", u"Costamare Shipping", u"Greece", 99833, u""),
(u"Cosco Yantian", u"Costamare Shipping", u"Greece", 99833, u""),
(u"CMA CGM Fidelio", u"CMA CGM", u"France", 99500, u""),
(u"CMA CGM Medea", u"CMA CGM", u"France", 95000, u""),
(u"CMA CGM Norma", u"CMA CGM", u"Bahamas", 95000, u""),
(u"CMA CGM Rigoletto", u"CMA CGM", u"France", 99500, u""),
(u"Arnold M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Morrell</i>"),
(u"Anna M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Lockhart</i>"),
(u"Albert M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>Tallow</i>"),
(u"Adrian M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496,
 u"Captain <i>G. E. Ericson</i>"),
(u"Arthur M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496, u""),
(u"Axel M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 93496, u""),
(u"NYK Vega", u"Nippon Yusen Kaisha", u"Panama", 97825, u""),
(u"MSC Esthi", u"MSC", u"Liberia", 99500, u""),
(u"MSC Chicago", u"Offen Claus-Peter", u"Liberia", 90449, u""),
(u"MSC Bruxelles", u"Offen Claus-Peter", u"Liberia", 90449, u""),
(u"MSC Roma", u"Offen Claus-Peter", u"Liberia", 99500, u""),
(u"MSC Madeleine", u"MSC", u"Liberia", 107551, u""),
(u"MSC Ines", u"MSC", u"Liberia", 107551, u""),
(u"Hannover Bridge", u"Kawasaki Kisen Kaisha", u"Japan", 99500, u""),
(u"Charlotte M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Clementine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Columbine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Cornelia M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Chicago Express", u"Hapag-Lloyd", u"Germany", 93750, u""),
(u"Kyoto Express", u"Hapag-Lloyd", u"Germany", 93750, u""),
(u"Clifford M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sally M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Skagen M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sofie M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sor\u00F8 M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Sovereing M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Susan M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Svend M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Svendborg M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"A.P. M\u00F8ller", u"M\u00E6rsk Line", u"Denmark", 91690,
 u"Captain <i>Ferraby</i>"),
(u"Caroline M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Carsten M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Chastine M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"Cornelius M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 91690, u""),
(u"CMA CGM Otello", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM Tosca", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM Nabucco", u"CMA CGM", u"France", 91400, u""),
(u"CMA CGM La Traviata", u"CMA CGM", u"France", 91400, u""),
(u"CSCL Europe", u"Danaos Shipping", u"Cyprus", 90645, u""),
(u"CSCL Africa", u"Seaspan Container Line", u"Cyprus", 90645, u""),
(u"CSCL America", u"Danaos Shipping ", u"Cyprus", 90645, u""),
(u"CSCL Asia", u"Seaspan Container Line", u"Hong Kong", 90645, u""),
(u"CSCL Oceania", u"Seaspan Container Line", u"Hong Kong", 90645,
 u"Captain <i>Baker</i>"),
(u"M\u00E6rsk Seville", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Santana", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sheerness", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sarnia", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"M\u00E6rsk Sydney", u"Blue Star GmbH", u"Liberia", 94724, u""),
(u"MSC Heidi", u"MSC", u"Panama", 95000, u""),
(u"MSC Rania", u"MSC", u"Panama", 95000, u""),
(u"MSC Silvana", u"MSC", u"Panama", 95000, u""),
(u"M\u00E6rsk Stralsund", u"Blue Star GmbH", u"Liberia", 95000, u""),
(u"M\u00E6rsk Saigon", u"Blue Star GmbH", u"Liberia", 95000, u""),
(u"M\u00E6rsk Seoul", u"Blue Star Ship Managment GmbH", u"Germany",
 95000, u""),
(u"M\u00E6rsk Surabaya", u"Offen Claus-Peter", u"Germany", 98400, u""),
(u"CMA CGM Hugo", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"CMA CGM Vivaldi", u"CMA CGM", u"Bahamas", 90745, u""),
(u"MSC Rachele", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"Pacific Link", u"NSB Niederelbe", u"Germany", 90745, u""),
(u"CMA CGM Carmen", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Don Carlos", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Don Giovanni", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"CMA CGM Parsifal", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"Cosco China", u"E R Schiffahrt", u"Liberia", 91649, u""),
(u"Cosco Germany", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"Cosco Napoli", u"E R Schiffahrt", u"Liberia", 89800, u""),
(u"YM Unison", u"Yang Ming Line", u"Taiwan", 88600, u""),
(u"YM Utmost", u"Yang Ming Line", u"Taiwan", 88600, u""),
(u"MSC Lucy", u"MSC", u"Panama", 89954, u""),
(u"MSC Maeva", u"MSC", u"Panama", 89954, u""),
(u"MSC Rita", u"MSC", u"Panama", 89954, u""),
(u"MSC Busan", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Beijing", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Toronto", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Charleston", u"Offen Claus-Peter", u"Panama", 89954, u""),
(u"MSC Vittoria", u"MSC", u"Panama", 89954, u""),
(u"Ever Champion", u"NSB Niederelbe", u"Marshall Islands", 90449,
 u"Captain <i>Phillips</i>"),
(u"Ever Charming", u"NSB Niederelbe", u"Marshall Islands", 90449,
 u"Captain <i>Tonbridge</i>"),
(u"Ever Chivalry", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Ever Conquest", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Ital Contessa", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"Lt Cortesia", u"NSB Niederelbe", u"Marshall Islands", 90449, u""),
(u"OOCL Asia", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Atlanta", u"OOCL", u"Hong Kong", 89000, u""),
(u"OOCL Europe", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Hamburg", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Long Beach", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Ningbo", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Shenzhen", u"OOCL", u"Hong Kong", 89097, u""),
(u"OOCL Tianjin", u"OOCL", u"Marshall Islands", 89097, u""),
(u"OOCL Tokyo", u"OOCL", u"Hong Kong", 89097, u"")):
        yield Ship(name, owner, country, teu, description)

