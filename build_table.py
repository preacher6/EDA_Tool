#!/usr/bin/env python
"""
    pandastable examples
    Created January 2019
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

try:
    from tkinter import *
    from tkinter.ttk import *
except:
    from Tkinter import *
    from ttk import *
from pandastable.core import Table
from pandastable.data import TableModel
import pandas as pd

class MyTable(Table):
    """
      Custom table class inherits from Table.
      You can then override required methods
     """
    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        return

class MyApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, data, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('400x300')
        self.main.title('Tabla')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        make_table(f, data) 

def make_table(frame, data, **kwds):
    """make a sample table"""
    #data.set_index('date', inplace=True)
    #print(df.describe())
    pt = MyTable(frame, dataframe=data, showtoolbar=False, showstatusbar=True, editable=False, enable_menus=False)
    pt.show()
    pt.showIndex()  # Muestra el indice seteado sobre el dataframe