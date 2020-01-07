import shutil
import kivy
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import json
from kivy.uix.label import Label
import os
from functools import partial


class Start(Screen):
    class Login(Widget):
        class wrong_login(FloatLayout):
            pass

        class account_exists(FloatLayout):
            pass

        password = ObjectProperty(None)
        username = ObjectProperty(None)

        def check_for_account(self): #Checks if you already have an account (UNUSED)
            with open('check_account.json') as f:
                number_account = json.load(f)
            if number_account != 0:
                self.existing()
                return False
            elif number_account == 0:
                return True

        def read_files(self):  # reads currently existing files to match textinput with saved username and password
            if self.username.text != '' or self.password.text != '':
                with open('login_counter.json') as cou:
                    counter = json.load(cou)
                if counter != 0:
                    while counter != 0:
                        with open(f'./Account_{counter}/passwrd.json') as file_object:  # remember to change so that it reads a variable instead of a specific file
                            read_password = json.load(file_object)
                        with open(f'./Account_{counter}/username.json') as file_object:
                            read_username = json.load(file_object)
                        if self.password.text == read_password and self.username.text == read_username:
                            self.password.text = '' #resets input to none
                            self.username.text = ''
                            with open('account_counter.json', 'w') as acc_cou:
                                json.dump(counter, acc_cou)
                            return True
                        elif self.password.text != read_password or self.username.text != read_username and counter != 0:
                            counter -= 1
                    if self.password.text != read_password or self.username.text != read_username and counter == 0:
                        self.password.text = ''
                        self.username.text = ''
                        self.wrong_popup()
                elif counter == 0:
                    self.password.text = ''
                    self.username.text = ''
                    self.wrong_popup()
                else:
                    return False

        def read_files_version_2(self):
            if self.username.text != '' or self.password.text != '':
                with open('account_list.json') as acc_list:
                    account_list = json.load(acc_list)
                counter = 0
                for count in account_list:
                    counter += 1
                for every_account in account_list:
                    if self.username.text in account_list[every_account] and self.password.text in account_list[every_account]:
                        with open('account_counter.json', 'w') as f:
                            json.dump(every_account, f)
                        self.clear_text()
                        return True
                        break
                    elif self.username.text not in account_list[every_account] or self.password.text not in account_list[every_account]:
                        counter -= 1
                if counter == 0:
                    self.password.text = ''
                    self.username.text = ''
                    self.wrong_popup()

        def wrong_popup(self):
            show = self.wrong_login()
            wrong_login_popup = Popup(title='', content=show, size_hint=(None, None), size=(400, 200))
            wrong_login_popup.open()

        def existing(self):
            show = self.account_exists()
            acc = Popup(title='', content=show, size_hint=(None, None), size=(400, 200))
            acc.open()
        def clear_text(self):
            self.username.text = ''
            self.password.text = ''
        pass


class Main_Menu(Screen):
    class Menu_Select(Widget):
        logger = ObjectProperty()

        def reset_dict(self):
            self.logger.App_Dic = {}
            self.logger.Pass_Dic = {}
            self.logger.Del_Btn = {}
            print('dictionaries reset')

        def checkforlogs(self):
            self.logger.count_log()

        def render_logs(self):
            with open('account_counter.json') as acc_cou:
                account_counter = json.load(acc_cou)
            with open(f'./{account_counter}/widget_counter.json') as counter:
                number_count = json.load(counter)
            while number_count != 0:  # loads the saved logs
                with open(f'./{account_counter}/App_{number_count}') as p:
                    App_Log = json.load(p)
                with open(f'./{account_counter}/Password_{number_count}') as p_2:
                    Pass_Log = json.load(p_2)
                self.logger.App_Dic['Application{0}'.format(number_count)] = Label(text=f'Application: {App_Log}')  # stores labels into dictionary in the logger class
                self.logger.Pass_Dic['Password{0}'.format(number_count)] = Label(text=f'Password: {Pass_Log}')
                self.logger.Del_Btn[f'{number_count}'] = Button(text='Delete Log')
                self.logger.assign_btn_function(number_count)
                self.logger.log_grid.add_widget(self.logger.App_Dic[f'Application{number_count}'])
                self.logger.log_grid.add_widget(self.logger.Pass_Dic[f'Password{number_count}'])
                self.logger.log_grid.add_widget(self.logger.Del_Btn[f'{number_count}'])
                number_count -= 1
            print(self.logger.Del_Btn)
            print(self.logger.App_Dic)
            print(self.logger.Pass_Dic)

        def render_logs_version_2(self):
            with open('account_counter.json') as acc_cou:
                account_counter = json.load(acc_cou)
            with open(f'./{account_counter}/log_lists.json') as f:
                log_list = json.load(f)
            with open(f'./{account_counter}/widget_counter.json') as f:
                number_count = json.load(f)
            log_list_temp = log_list
            while log_list_temp != []:
                App_Log = log_list_temp[0]
                Pass_Log = log_list_temp[1]
                self.logger.App_Dic['Application{0}'.format(number_count)] = Label(text=f'Application: {App_Log}')  # stores labels into dictionary in the logger class
                self.logger.Pass_Dic['Password{0}'.format(number_count)] = Label(text=f'Password: {Pass_Log}')
                self.logger.Del_Btn[f'{number_count}'] = Button(text='Delete Log')
                self.logger.assign_btn_function(number_count)

                self.logger.log_grid.add_widget(self.logger.App_Dic[f'Application{number_count}'])
                self.logger.log_grid.add_widget(self.logger.Pass_Dic[f'Password{number_count}'])
                self.logger.log_grid.add_widget(self.logger.Del_Btn[f'{number_count}'])
                del log_list_temp[0]
                del log_list_temp[0]
                number_count -= 1

        pass

class Create_Screen(Screen):
    class Create(Widget):
        class blank_login(FloatLayout):
            pass

        class creation_made(FloatLayout):
            pass

        create_username = ObjectProperty(None)
        create_password = ObjectProperty(None)

        def clear_text(self):
            self.create_password.text = ''
            self.create_username.text = ''
        def save_account(self):  # saves username and password inside of a json file
            if self.create_password.text != '' and self.create_username.text != '':
                with open('login_counter.json') as cou:
                    counter = json.load(cou)
                folder =  f'Account_{counter+1}' #organizes folder names with the number in counter file
                try:
                    os.mkdir(folder) #creates a directory to store passwords and usernames
                except FileExistsError:
                    print('directory already exists')
                user_file = f'./{folder}/Username.json'  # saves username and password inside specific directory
                passwrd_file = f'./{folder}/Passwrd.json'
                username = self.create_username.text
                passwrd = self.create_password.text
                with open(user_file, 'w') as f:
                    json.dump(username, f)
                    print('username saved')
                with open(passwrd_file, 'w') as f:
                    json.dump(passwrd, f)
                    print('password saved')

                special_list = []
                special_list.append(self.create_username.text)
                special_list.append(self.create_password.text)
                acc_list = {}

                with open('account_list.json') as f:
                    acc_list = json.load(f)
                acc_list[folder] = special_list
                with open('account_list.json', 'w') as f:
                    json.dump(acc_list, f)

                with open(f'./{folder}/widget_counter.json', 'w') as f:
                    json.dump(0,f)
                with open('login_counter.json', 'w') as wid:
                    json.dump(counter+1, wid)
                empty_list = []
                with open(f'./{folder}/log_lists.json', 'w') as f:
                    json.dump(empty_list, f)
                show_create_successful = self.creation_made()
                create_yes = Popup(title='', content=show_create_successful, size_hint=(None, None), size=(400, 200))
                create_yes.open()
                self.clear_text()
                return True
            elif self.create_username.text == '' or self.create_password.text == '':  # renders popup for when an account is created
                show = self.blank_login()
                blank = Popup(title='', content=show, size_hint=(None, None), size=(400, 200))
                blank.open()
                return False

        pass


class Create_Log(Screen):
    class Create_Log_GUI(Widget):
        app_password = ObjectProperty(None)
        application = ObjectProperty(None)
        logger = ObjectProperty()

        class log_save_popup(FloatLayout):  # class for the popup when a save is created
            pass
        def clear_text(self):
            self.app_password.text = ''
            self.application.text = ''

        def save_log(self):
            self.logger.log_counter_create() #scans for any update in log counters
            with open('account_counter.json') as acc_cou: #grabs counter in order to be used to tell which account to save data
                account_counter = json.load(acc_cou)
            if self.app_password.text != '' and self.application.text != '':
                self.logger.log_counter += 1  # remember to create json file for log counter
                print(self.logger.log_counter)
                log_count_var = 0 + self.logger.log_counter
                with open(f'./{account_counter}/widget_counter.json', 'w') as f:
                    json.dump(log_count_var, f)  # this changes the counter so the app recognizes when log isn't empty
                app_widget = f'./{account_counter}/App_{log_count_var}' #stores logs into respected account
                app_password_widget = f'./{account_counter}/Password_{log_count_var}'
                with open(app_widget, 'w') as app_name:
                    json.dump(self.application.text, app_name)
                with open(app_password_widget, 'w') as app_secret:
                    json.dump(self.app_password.text, app_secret)  # saves log into files


                with open(f'./{account_counter}/log_lists.json') as f:
                    list_file = json.load(f)
                print(list_file)
                list_file.append(self.application.text)
                with open(f'./{account_counter}/log_lists.json', 'w') as f:
                    json.dump(list_file, f)

                with open(f'./{account_counter}/log_lists.json') as f:
                    list_file = json.load(f)
                print(list_file)
                list_file.append(self.app_password.text)
                with open(f'./{account_counter}/log_lists.json', 'w') as f:
                    json.dump(list_file, f)


                self.app_password.text = ''
                self.application.text = ''
                self.log_popup()
            else:
                pass

        def log_popup(self):  # renders popup when a log is saved
            show = self.log_save_popup()
            popup_log = Popup(title='', content=show, size_hint=(None, None), size=(400, 200))
            popup_log.open()


class Log_Screen(Screen):
    class Log(Widget):
        menu_select = ObjectProperty()
        App_Dic = {}
        Pass_Dic = {}
        Del_Btn = {}

        class No_Logs_Popup(FloatLayout):
            pass

        class are_you_sure(FloatLayout): #UNUSED
            yes_button = ObjectProperty(None)
            no_button = ObjectProperty(None)
            delete = None

            def Yes(self):
                self.delete = True

            def No(self):
                self.delete = False

            pass
        log_counter = 0 #helps associate with accounts
        def log_counter_create(self):
            with open('account_counter.json') as ax:
                account_counter = json.load(ax)
            file_log_counter = f'./{account_counter}/widget_counter.json'  # widget counter is created in a json file outside of the program
            with open(file_log_counter) as file_counter:
                self.log_counter = json.load(file_counter)
        log_grid = ObjectProperty(None)
        widget_list = []

        def count_log(self):  # if it sees that the counter is 0, it creates a popup that lets the user know
            with open('account_counter.json') as acc_cou:
                account_counter = json.load(acc_cou)
            with open(f'./{account_counter}/log_lists.json') as acc_list:
                accounts = json.load(acc_list)
            if accounts == []:
                self.log_zero()
            else:
                pass

        def reset_widgets(self):
            with open('account_counter.json') as acc_cou:
                account_counter = json.load(acc_cou)
            with open(f'./{account_counter}/widget_counter.json') as counter:
                max = json.load(counter)
            if max < 2 and max > 0:
                x = 1
                self.log_grid.remove_widget(self.App_Dic[f'Application{x}'])
                self.log_grid.remove_widget(self.Pass_Dic[f'Password{x}'])
                self.log_grid.remove_widget(self.Del_Btn[f'{x}'])
                print(self.App_Dic[f'Application{x}'])
            elif max >= 2:
                for x in range(1, max + 1):
                    self.log_grid.remove_widget(self.App_Dic[f'Application{x}'])
                    self.log_grid.remove_widget(self.Pass_Dic[f'Password{x}'])
                    self.log_grid.remove_widget(self.Del_Btn[f'{x}'])
                    print(self.App_Dic[f'Application{x}'])
            else:
                pass
            self.App_Dic = {}
            self.Pass_Dic = {}
            self.Del_Btn = {}
        def reset_widgets_version_2(self):
            with open('account_counter.json') as f:
                account_counter = json.load(f)
            with open(f'./{account_counter}/log_lists.json') as f:
                log_list = json.load(f)
            with open(f'./{account_counter}/widget_counter.json') as f:
                x = json.load(f)
            log_list_temp = log_list
            print(log_list_temp)
            while log_list_temp != []:
                self.log_grid.remove_widget(self.App_Dic[f'Application{x}'])
                self.log_grid.remove_widget(self.Pass_Dic[f'Password{x}'])
                self.log_grid.remove_widget(self.Del_Btn[f'{x}'])
                del log_list_temp[0]
                del log_list_temp[0]
                x-= 1

        def log_zero(self):  # renders popup of 0 widgets in the log view
            show = self.No_Logs_Popup()
            create_no_logs_popup = Popup(title='', content=show, size_hint=(None, None), size=(400, 200))
            create_no_logs_popup.open()

        def delete_log(self, number):
            with open('account_counter.json') as acc_cou:
                account_counter = json.load(acc_cou)
            with open(f'./{account_counter}/log_lists.json') as f:
                log_list = json.load(f) #log lists allows for specific logs to be deleted
            number = number
            print(f'error {number}')
            self.are_you_sure.delete = None
            self.log_grid.remove_widget(number)
            for name, btn in self.Del_Btn.items():
                if btn == number:
                    self.log_grid.remove_widget(self.App_Dic[f'Application{name}'])
                    self.log_grid.remove_widget(self.Pass_Dic[f'Password{name}'])
                    del self.App_Dic[f'Application{name}']
                    print(self.Del_Btn)
                    for every in self.Del_Btn:
                        if every == f'{number}':
                         del self.Del_Btn[every]
                    del self.Pass_Dic[f'Password{name}']
                    try:
                        os.remove(f'./{account_counter}/App_{name}')
                        os.remove(f'./{account_counter}/Password_{name}')
                    except FileNotFoundError:
                        print('file not found')
                    del log_list[0]
                    del log_list[0]
                    with open(f'./{account_counter}/log_lists.json', 'w') as override:
                        json.dump(log_list, override)

            self.log_counter -= 1
            self.count_log()




        def assign_btn_function(self, num):
            num = num
            self.Del_Btn[f'{num}'].bind(on_press=partial(self.delete_log))

        def are_you_sure_popup(self):
            show = self.are_you_sure()
            show_popup = Popup(title='', content=show, size_hint=(None, None), size=(500, 200))
            show_popup.open()

        pass

class Acc_Set(Screen):
    class Account(Widget):
        class Change_Password(FloatLayout):
            class Empty(FloatLayout):
                pass
            class Wrong_Password(FloatLayout):
                pass
            old_input = ObjectProperty(None)
            new_input = ObjectProperty(None)
            wrong_label = ObjectProperty(None)

            def reset_password(self):
                with open('account_counter.json') as f:
                    account_counter = json.load(f)
                with open(f'./{account_counter}/Passwrd.json') as f:
                    old_password = json.load(f)
                print(self.old_input.text, self.new_input.text)
                if self.old_input.text == old_password:
                    with open(f'./{account_counter}/Passwrd.json', 'w') as f:
                        json.dump(self.new_input.text, f)
                    self.popup.dismiss()
                elif self.old_input.text != old_password:
                    self.old_input.text = ''
                    self.new_input.text = ''
                    self.wrong_pass_popup()

            def wrong_pass_popup(self):
                show = self.Wrong_Password()
                show_popup = Popup(title='', content=show, size_hint=(None, None), size=(500, 200))
                show_popup.open()

            def empty_input(self):
                show = self.Empty()
                show_popup = Popup(title='', content=show, size_hint=(None, None), size=(500, 200))
                show_popup.open()
            pass

        class Del_Acc(FloatLayout):
            def delete_account(self):
                with open('account_counter.json') as f:
                    account_counter = json.load(f)

                shutil.rmtree(f'{account_counter}')
            def close_popup(self):
                self.show_popup.dismiss()
            pass

        def delete_account_popup(self):
            show = self.Del_Acc()
            self.Del_Acc.show_popup = Popup(title='', content=show, size_hint=(None, None), size=(500, 200))
            self.Del_Acc.show_popup.open()

        def change_password_popup(self):
            show = self.Change_Password()
            self.Change_Password.popup = Popup(title='', content=show, size_hint=(None, None), size=(500, 400))
            self.Change_Password.popup.open()

        pass

class ScreenManager(ScreenManager):
    pass


kv = Builder.load_file('master.kv')


class Master(App):
    def build(self):
        return kv


if __name__ == '__main__':
    Master().run()
