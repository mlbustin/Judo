"""
First, the get_table function is called to retrieve data
from a database table and return it as a list.
The Application constructor is then called with
the screen title, window title, and data list as arguments
to create an instance of the Application class.

Finally, the 'start_app' method of the 'Application' object
is called to start the GUI application and display the data in a window.
"""
from App import Application
from DB import Database as db
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import dearpygui.dearpygui as dpg
import pyodbc

App = Application()

App.start_app()
