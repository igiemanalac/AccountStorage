from tkinter import *
from tkinter import messagebox
import tkinter.messagebox as mb
from encryption import Encrypter

# GLOBAL VARIABLES

objects = []
window = Tk()
window.withdraw()
window.title('Account Storage')

# Secret key for encryption
encrypter = Encrypter('m@st3r')


class popupWindow(object):
    loop = False
    attempts = 0

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title('Password')
        top.geometry('{}x{}'.format(250, 100))
        top.resizable(width=False, height=False)
        self.label = Label(top, text=" Password: ",
                           font=('Courier', 14), justify=CENTER)
        self.label.pack()
        self.entry = Entry(top, show='*', width=30)
        self.entry.pack(pady=7)
        self.submit = Button(top, text='Submit',
                             command=self.cleanup, font=('Courier', 14))
        self.submit.pack()

    def cleanup(self):
        # Get input password
        self.value = self.entry.get()
        # TODO: Master password setup
        # Login password
        access = 'm@st3r'

        if self.value == access:
            self.loop = True
            self.top.destroy()
            window.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                window.quit()
            self.entry.delete(0, 'end')
            mb.showerror(
                'Incorrect Password', 'Password incorrect, attempts remaining: ' + str(3 - self.attempts))


class Account:
    def __init__(self, master, account_name, username, password, email):
        self.account_name = account_name
        self.username = username
        self.password = password
        self.email = email
        self.window = master

    def add_to_storage(self):
        # TODO: Add fleixibility to file accessing
        f = open('accounts.txt', 'a')

        # Encrypt the data before storing in the text file
        encrypted_account_name = encrypter.encrypt_text(self.account_name)
        encrypted_username = encrypter.encrypt_text(self.username)
        encrypted_email = encrypter.encrypt_text(self.email)
        encrypted_password = encrypter.encrypt_text(self.password)

        f.write(encrypted_account_name.decode('utf-8') + ',' + encrypted_username.decode('utf-8') +
                ',' + encrypted_email.decode('utf-8') +
                ',' + encrypted_password.decode('utf-8') + ', \n')


class AccountStorage:

    def __init__(self, master, account_name, username, email, password, count):
        self.account_name = encrypter.decrypt_text(
            account_name.encode('utf-8'))
        self.username = encrypter.decrypt_text(username.encode('utf-8'))
        self.email = encrypter.decrypt_text(email.encode('utf-8'))
        self.password = encrypter.decrypt_text(password.encode('utf-8'))
        self.window = master
        self.count = count

        self.label_account_name = Label(
            self.window, text=self.account_name, font=('Courier', 14))
        self.label_email = Label(
            self.window, text=self.email, font=('Courier', 14))
        self.label_username = Label(
            self.window, text=self.username, font=('Courier', 14))
        self.label_pass = Label(
            self.window, text=self.password, font=('Courier', 14))
        self.deleteButton = Button(
            self.window, text='X', fg='red', command=self.delete_account)

    def display(self):
        self.label_account_name.grid(row=7 + self.count, sticky=W)
        self.label_username.grid(row=7 + self.count, column=1, sticky=W)
        self.label_email.grid(row=7 + self.count, column=2, sticky=W)
        self.label_pass.grid(row=7 + self.count, column=3, sticky=W)
        self.deleteButton.grid(row=7 + self.count, column=4, sticky=W)

    # TODO:
    # - Add account method
    # - Modify account details method
    def add_account(self):
        pass

    def delete_account(self):
        answer = mb.askquestion(
            'Delete Account', 'Are you sure you want to delete this account?')

        if answer == 'yes':
            for i in objects:
                i.destroy()

            f = open('accounts.txt', 'r')
            lines = f.readlines()
            f.close()

            f = open('accounts.txt', "w")
            count = 0

            for line in lines:
                if count != self.count:
                    f.write(line)
                    count += 1

            f.close()
            read_file()

    def destroy(self):
        self.label_account_name.destroy()
        self.label_username.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.deleteButton.destroy()


# Functions

def on_submit():
    e = email.get()
    pw = password.get()
    uname = username.get()
    aname = account_name.get()
    entry = Account(window, aname, uname, pw, e)
    entry.add_to_storage()
    account_name.delete(0, 'end')
    username.delete(0, 'end')
    email.delete(0, 'end')
    password.delete(0, 'end')
    messagebox.showinfo('Added Account', 'Successfully Added, \n' +
                        'Account Name: ' + aname + '\nEmail: ' + e +
                        '\nUsername: ' + uname + '\nPassword: ' + pw)
    read_file()


def clear_file():
    f = open('accounts.txt', "w")
    f.close()


def read_file():
    f = open('accounts.txt', "r")
    count = 0

    for line in f:
        account_details = line.split(',')
        account = AccountStorage(
            window, account_details[0], account_details[1], account_details[2], account_details[3], count)

        objects.append(account)
        account.display()
        count += 1

    f.close()


# GRAPHICS


m = popupWindow(window)

entity_label = Label(window, text='Add Entity', font=('Courier', 18))
account_name_label = Label(window, text='Acount Name: ', font=('Courier', 14))
username_label = Label(window, text='Username: ', font=('Courier', 14))
email_label = Label(window, text='Email: ', font=('Courier', 14))
pass_label = Label(window, text='Password: ', font=('Courier', 14))
account_name = Entry(window, font=('Courier', 14))
username = Entry(window, font=('Courier', 14))
email = Entry(window, font=('Courier', 14))
password = Entry(window, show='*', font=('Courier', 14))
submit = Button(window, text='Add Email',
                command=on_submit, font=('Courier', 14))

entity_label.grid(columnspan=4, row=0)
account_name_label.grid(row=1, sticky=E, padx=3)
username_label.grid(row=2, sticky=E, padx=3)
email_label.grid(row=3, sticky=E, padx=3)
pass_label.grid(row=4, sticky=E, padx=3)

account_name.grid(columnspan=4, row=1, column=1, padx=2, pady=2, sticky=W)
username.grid(columnspan=4, row=2, column=1, padx=2, pady=2, sticky=W)
email.grid(columnspan=4, row=3, column=1, padx=2, pady=2, sticky=W)
password.grid(columnspan=4, row=4, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=4, pady=4)

account_name_table_header = Label(
    window, text='Account Name: ', font=('Courier', 14))
username_table_header = Label(window, text='Username: ', font=('Courier', 14))
email_table_header = Label(window, text='Email: ', font=('Courier', 14))
password_table_header = Label(window, text='Password: ', font=('Courier', 14))

account_name_table_header.grid(row=6)
username_table_header.grid(row=6, column=1)
email_table_header.grid(row=6, column=2)
password_table_header.grid(row=6, column=3)

read_file()

window.mainloop()
