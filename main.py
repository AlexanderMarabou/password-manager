from tkinter import *
from tkinter import messagebox
import secrets
import string
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for number in range(20))
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()

    try:
        with open("passwords.json", "r") as password_file:
            # Reading old data
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="No password is yet saved")
    else:
        if website in data:
            messagebox.showinfo(title=f"{website}", message=f"\nWebsite: {website}" 
                                                            f"\nEmail: {data[website]["email"]} " 
                                                            f"\nPassword: {data[website]["password"]}")
        else:
            messagebox.showerror(title="Error", message="No details for the website exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nWebsite: {website}"
                                                              f"\nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("passwords.json", "r") as password_file:
                    # Reading old data
                    data = json.load(password_file)
                    # Checking if the entry is already in database
                    if website in data:
                        overwrite_data_ok = messagebox.askokcancel(title="Website already exists in database",
                                                                   message=f"The website: "
                                                                           f"{website} already exists in database"
                                                                           f"\nDo you want to update password?")
                        if overwrite_data_ok is not True:
                            messagebox.showinfo(title=f"{website} not updated",
                                                message=f"Password for {website} NOT updated")
                            return
            except (FileNotFoundError, json.JSONDecodeError):
                # Handling errors if passwords.json doesn't exist or is empty
                with open("passwords.json", "w") as password_file:
                    json.dump(new_data, password_file, indent=4)
            else:
                data.update(new_data)
                with open("passwords.json", "w") as password_file:
                    json.dump(data, password_file, indent=4)

            finally:
                # Clearing entries upon saving new data
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_username_entry = Entry(width=37)
email_username_entry.insert(0, "example@example.com")
email_username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=12, command=find_password)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate Password", width=12, command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
