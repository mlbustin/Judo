"""
The Application class is defined with a constructor that takes three arguments:
    'screen_title', 'window_title', and 'data'.

These arguments are used to set the titles of the viewport
and window, and to display data in the window.

The 'start_app' method of the 'Application' class is used to create a Dear PyGui context,
create a window using the 'window' function of the library,
and display text in the window using the 'add_text' function.
The 'create_viewport' function is used to create a viewport for the application,
and the 'set_primary_window' function is used to set the main window of the application.

Finally, the 'setup_dearpygui', 'show_viewport', and 'start_dearpygui' functions are called
to initialize and start the Dear PyGui application.
Once the application is finished, the 'destroy_context' function is called
to clean up any resources used by the Dear PyGui library.
"""
import dearpygui.dearpygui as dpg
import logging
from DB import Database as db
from api import *
import threading as tr

connection_string = "mssql+pyodbc://localhost/Judo?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"


class Database:
    def __init__(self, url, base):
        self.base = base
        self.DB = db.UserDB(url)

    def signup(self):
        username, password, confirm_password, age = dpg.get_value("reg_username"), dpg.get_value("reg_password"), \
                                                    dpg.get_value("reg_confirm_password"), dpg.get_value("reg_age")

        self.DB.create_user(name=username, password=password, age=age) if password == confirm_password \
            else logging.warning("Passwords do not match")

    def login(self, username, password):
        if username and password:
            self.base.user = self.DB.get_user(username, password)
            if self.base.user:
                self.base.main_window.run(self.base.user)
        else:
            username, password = dpg.get_value("login_username"), dpg.get_value("login_password")
            if username and password:
                self.base.user = self.DB.get_user(username, password)
                if self.base.user:
                    self.base.main_window.run(self.base.user)

    def update(self):
        username, age, password = dpg.get_value("setting_username"), \
                                  dpg.get_value("setting_age"), \
                                  dpg.get_value("setting_password")
        self.DB.update_user(self.base.user[0].id, username, age, password)
        self.login(username=username, password=password)


class GUI:
    def __init__(self):
        # Fonts
        self.font_pt_mono_h = ""
        self.font_pt_mono_p = ""

        # Windows
        self.login_window = LoginWindow(self)
        self.signup_window = SignupWindow(self)
        self.main_window = MainWindow(self, None)
        self.settings_window = SettingsWindow(self)
        self.current_window = None

        # Database
        self.database = Database(connection_string, self)

        # Server
        self.server = Server("192.168.1.4", 12345)
        self.server_thread = tr.Thread(target=self.server.start)

    def reg_fonts(self):
        with dpg.font_registry():
            self.font_pt_mono_h = dpg.add_font("src/fonts/PTMono-Regular.ttf", 22)
            self.font_pt_mono_p = dpg.add_font("src/fonts/PTMono-Regular.ttf", 16)

            dpg.bind_font(self.font_pt_mono_p)

    def run(self):
        dpg.create_context()

        self.reg_fonts()
        self.login_window.run()

        self.server_thread.start()

        dpg.create_viewport(title="Judo", width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("LoginWindow", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


class LoginWindow:
    def __init__(self, base):
        self.base = base

    def run(self):
        with dpg.window(tag="LoginWindow", label="Judo Manager"):
            label = dpg.add_text("log in to the system")
            dpg.bind_item_font(label, self.base.font_pt_mono_h)

            with dpg.child_window(label="Auth"):
                dpg.add_input_text(tag="login_username",
                                   hint="Username or email...",
                                   on_enter=True,
                                   callback=self.base.database.login,
                                   user_data=self.base)
                dpg.add_input_text(tag="login_password",
                                   hint="Password...",
                                   on_enter=True,
                                   password=True,
                                   callback=self.base.database.login,
                                   user_data=self.base)
                dpg.add_button(label="Log In",
                               callback=self.base.database.login,
                               user_data=self.base)
                dpg.add_spacer(height=5)
                dpg.add_button(label="Create Account",
                               callback=self.base.signup_window.run)

        dpg.delete_item(self.base.current_window) if self.base.current_window else None
        self.base.current_window = "LoginWindow"
        dpg.set_primary_window("LoginWindow", True)


class SignupWindow:
    def __init__(self, base):
        self.base = base

    def run(self):
        with dpg.window(tag="RegWindow", label="Registration Window"):
            label = dpg.add_text("Registration new account")
            dpg.bind_item_font(label, self.base.font_pt_mono_h)

            with dpg.child_window(label="Reg"):
                dpg.add_input_text(tag="reg_username",
                                   hint="Enter your name...",
                                   on_enter=True)
                dpg.add_input_int(tag="reg_age")
                dpg.add_input_text(tag="reg_password",
                                   hint="Create new password...",
                                   on_enter=True)
                dpg.add_input_text(tag="reg_confirm_password",
                                   hint="Confirm password ...",
                                   on_enter=True)
                dpg.add_button(label="Create", callback=self.base.database.signup)
                dpg.add_spacer(height=5)
                dpg.add_button(label="Cancel", callback=self.base.login_window.run)

        dpg.delete_item(self.base.current_window) if self.base.current_window else None
        self.base.current_window = "RegWindow"
        dpg.set_primary_window("RegWindow", True)


class MainWindow:
    def __init__(self, base, user=None):
        self.base = base
        self.user = user

    def run(self, user=None):
        self.user = user if user else None

        with dpg.window(tag="MainWindow", label="Judo Manager"):
            label = dpg.add_text(f"Welcome {self.user[0].name} to Judo Manager")
            dpg.bind_item_font(label, self.base.font_pt_mono_h)

            with dpg.child_window(label="Main"):
                dpg.add_button(label="Account settings", callback=self.base.settings_window.run)
                dpg.add_spacer(height=5)

        dpg.delete_item(self.base.current_window) if self.base.current_window else None
        self.base.current_window = "MainWindow"
        dpg.set_primary_window("MainWindow", True)


class SettingsWindow:
    def __init__(self, base):
        self.base = base

    def run(self):
        with dpg.window(tag="SettingsWindow", label="Judo Manager"):
            label = dpg.add_text(f"Settings for {self.base.user[0].name}")
            dpg.bind_item_font(label, self.base.font_pt_mono_h)

            with dpg.child_window(label="Settings"):
                dpg.add_input_text(tag="settings_username",
                                   hint=f'{self.base.user[0].name}',
                                   on_enter=True,
                                   label="Username")
                dpg.add_input_int(tag="settings_age",
                                  label="Age")
                dpg.add_input_text(tag="settings_password",
                                   hint=f'{self.base.user[0].password}',
                                   on_enter=True,
                                   label="Password")
                dpg.add_spacer(height=5)
                dpg.add_button(label="Save", callback=self.base.database.update)

        dpg.delete_item(self.base.current_window) if self.base.current_window else None
        self.base.current_window = "SettingsWindow"
        dpg.set_primary_window("SettingsWindow", True)
