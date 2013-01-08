Rapid GUI Programming with Python and Qt:
The Definitive Guide to PyQt Programming
by Mark Summerfield

ISBN: 0132354187

    IMPORTANT NOTE 

    The examples included in this archive are the ones shown in
    the book, and use Python 2.5/PyQt 4.3.
    
    Two other archives are available separately from the same web page,
    www.qtrac.eu/pyqtbook.html, one that has Python 2.6/PyQt 4.4
    versions of the examples, and another than has Python 3/PyQt
    4.5-7 versions.

All the example programs and modules are copyright (c) Qtrac Ltd. 2007-11.
They are free software: you can redistribute them and/or modify them
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 2 of the License, or version 3
of the License, or (at your option) any later version. They are provided
for educational purposes and are distributed in the hope that they will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public Licenses (in files gpl-2.0.txt and gpl-3.0.txt) for more
details.

Two helper programs are provided: mkpyqt.py (a console application), and
makepyqt.pyw (a GUI application). These programs both do the same thing:
They run pyuic4, pyrcc4, pylupdate4, and lrelease with the correct
command line arguments. In some cases you may need to set the path to
pyuic4 (pyuic4.bat on Windows), and possibly to the other programs as
well. For mkpyqt.py this means editing the file itself (the paths are in
variables near the top); for makepyqt.pyw, click "More->Options" and
set the paths there. The use of these programs is described in Chapter 7.

All the book's examples are designed to be educational, and many are
also designed to be useful. I hope that you find them helpful, and are
perhaps able to use some of them as starting points for your own
projects.

Qt is available with multiple licenses including the GPL and LGPL so in
many cases a commercial license is not necessary. To download Qt and for
the license terms visit http://www.qtsoftware.com. PyQt is dual
licensed, GPL and commercial. To download PyQt and for the license terms
visit http://www.riverbankcomputing.co.uk. Python itself can be obtained
from http://www.python.org and can be used for both commercial and
non-commercial purposes free of charge. See Appendix A for information
on obtaining and installing the necessary software.

Most of the icons are from KDE (The `K' Desktop Environment), and come
under KDE's LGPL license. (Visit http:///www.kde.org for more information.)

STOP PRESS

Chapter 3 describes an "OrderedDict". Unfortunately this name is
incorrect, it should have been called "SortedDict". (In Python mapping
terminology "ordered" means "order of insertion" and "sorted" means
"order of key"---I had used the C++ terminology.) I have kept the
wrongly named ordereddict.py module in the archive---after all, it works
fine---but also provided a correctly named SortedDict.py module that has
the same behavior, and that ought to be used instead. (The examples for
my book "Programming in Python 3" have an alternative SortedDict---and
SortedList---implementation.) Note that Python 3.1 comes with
collections.OrderedDict, an insertion ordered dictionary.

Chapter 4. I've now added a new example, currency2.pyw that has one
extra line (to include Canadian dollars) and one line different (to sort
currency names case-insensitively) compared to currency.pyw. I've also
done a small theoretical improvement to the code.

Chapter 9 shows an SDI text editor (sditexteditor.pyw) that has a Window
menu in every main window with the list of all the application's
windows. This application's Window menu works on the basis of window
titles. But window titles may not be unique. For this reason I have now
added a new version (sditexteditor2.pyw) that has more sophisticated
updateWindowMenu() and raiseWindow() methods that use each window's
unique id() rather than their possibly non-unique window title.
Note also that for tabbededitor.pyw, the file save and save as logic is
nicer in the Python 2.6 and 3 archives than in this one.

Chapter 12. The exercise solution pagedesigner_ans.pyw has an improved
setAlignment() implementation thanks to John Posner.

Chapter 13 shows a PythonHighlighter (color syntax highlighting) class
in the pythoneditor.pyw and pythoneditor_ans.pyw applications. I have
fixed bugs in the syntax highlighter used in both of these and now added
pythoneditor2.pyw which is a copy of pythoneditor_ans.pyw but with the
PythonHighlighter replaced with one that uses improved highlighting
logic since this works better in more corner cases (but is slower). I've
also added printing2.pyw which has a bugfix and some tiny improvements
for both HTML and QPainter printing.
