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

connection_string = "mssql+pyodbc://localhost/Judo?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"


class Database:
    def __init__(self, url):
        self.DB = db.UserDB(url)

    def signup(self):
        username, password, confirm_password, age = dpg.get_value("reg_username"), dpg.get_value("reg_password"), \
                                                    dpg.get_value("reg_confirm_password"), dpg.get_value("reg_age")

        self.DB.create_user(name=username, password=password, age=age) if password == confirm_password \
            else logging.warning("Passwords do not match")

    def login(self, username, password):
        return True if self.DB.check_user(username, password) else False


class GUI:
    def __init__(self):
        self.font_pt_mono_h = ""
        self.font_pt_mono_p = ""

        self.login_window = LoginWindow(self)
        self.signup_window = SignupWindow(self)
        self.current_window = None
        self.database = Database(connection_string)

    def reg_fonts(self):
        with dpg.font_registry():
            self.font_pt_mono_h = dpg.add_font("src/fonts/PTMono-Regular.ttf", 22)
            self.font_pt_mono_p = dpg.add_font("src/fonts/PTMono-Regular.ttf", 16)

            dpg.bind_font(self.font_pt_mono_p)

    def run(self):
        dpg.create_context()

        self.reg_fonts()
        self.login_window.run()

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
                dpg.add_input_text(tag="username_input",
                                   hint="Username or email...",
                                   on_enter=True,
                                   callback=self.base.database.login)
                dpg.add_input_text(tag="password_input",
                                   hint="Password...",
                                   on_enter=True,
                                   password=True,
                                   callback=self.base.database.login)
                dpg.add_button(label="Log In", callback=self.base.database.login)
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


Application = GUI()
Application.run()
