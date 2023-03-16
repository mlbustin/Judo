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
from DBConnection import Database
import pyodbc


class Application:
    def __init__(self):
        self.font_pt_mono_h = ""
        self.font_pt_mono_p = ""
        self.db = Database()

    def login(self):
        name, password = dpg.get_value("username_input"), dpg.get_value("password_input")
        if name and password != "":
            if self.db.check_user_contain(username=name):
                print(True)

    def signup(self):
        name, age, = dpg.get_value("reg_username_input"), dpg.get_value("reg_age_input")
        password, confirm_password = dpg.get_value("reg_password_input"), dpg.get_value("reg_confirm_password_input")

        print(name, age, password, confirm_password)

        if self.db.check_user_contain(username=name):
            print("Такое имя уже существует")
        else:
            self.db.add_user(name, age)

        if password != confirm_password:
            print("Пароли не совпадают")

    def reg_fonts(self):
        with dpg.font_registry():
            self.font_pt_mono_h = dpg.add_font("src/fonts/PTMono-Regular.ttf", 22)
            self.font_pt_mono_p = dpg.add_font("src/fonts/PTMono-Regular.ttf", 16)

            dpg.bind_font(self.font_pt_mono_p)

    def open_reg_window(self, sender, data):
        window = dpg.get_item_parent(dpg.get_item_parent(sender))

        with dpg.window(tag="RegWindow", label="Registration Window"):
            label = dpg.add_text("Registration new account")
            dpg.bind_item_font(label, self.font_pt_mono_h)

            with dpg.child_window(label="Reg"):
                dpg.add_input_text(tag="reg_username_input",
                                   label="Name",
                                   hint="Enter your name...",
                                   on_enter=True)
                dpg.add_input_int(tag="reg_age_input",
                                  label="Age")
                dpg.add_input_text(tag="reg_password_input",
                                   label="Password",
                                   hint="Create new password...",
                                   on_enter=True)
                dpg.add_input_text(tag="reg_confirm_password_input",
                                   label="Confirm password",
                                   hint="Confirm password ...",
                                   on_enter=True)
                dpg.add_button(label="Create", callback=self.signup)

        dpg.delete_item(window)
        dpg.set_primary_window("RegWindow", True)

    def start_app(self):
        dpg.create_context()

        self.reg_fonts()

        with dpg.window(tag="MainWindow", label="Judo Manager"):
            label = dpg.add_text("log in to the system")
            dpg.bind_item_font(label, self.font_pt_mono_h)

            with dpg.child_window(label="Auth"):
                dpg.add_input_text(tag="username_input",
                                   label="You name",
                                   hint="Username or email...",
                                   on_enter=True,
                                   callback=self.login)
                dpg.add_input_text(tag="password_input",
                                   label="You password",
                                   hint="Password...",
                                   password=True,
                                   on_enter=True,
                                   callback=self.login)
                dpg.add_button(label="Log In", callback=self.login)
                dpg.add_spacer(height=5)
                dpg.add_button(label="Create Account",
                               callback=self.open_reg_window)

        dpg.create_viewport(title="MainWindow", width=600, height=300)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MainWindow", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
