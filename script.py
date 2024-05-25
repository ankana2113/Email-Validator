import pandas as pd
from disposable_email_domains import blocklist
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# get the list of disposable email domains
disposable_domains_set = set(blocklist)


def is_disposable(email, disposable_domains):
    domain = email.split('@')[-1]
    return domain in disposable_domains


def get_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'])
    else:  # macOS and Linux
        return os.path.join(os.path.expanduser('~'))


def process_email(input_file):
    try:
        # loading input file from user
        df = pd.read_excel(input_file)

        # checking for presence of email addresses
        if 'Email' not in df.columns:
            raise ValueError('The input file must contain Email column.')

        # separating valid and disposable emails
        disposable_emails = df[df['Email'].apply(lambda email: is_disposable(email, disposable_domains_set))]
        valid_emails = df[~df['Email'].apply(lambda email: is_disposable(email, disposable_domains_set))]

        # Get the user's desktop path
        file_path = get_path()

        # Define output file paths on the desktop
        disposable_file_path = os.path.join(file_path, 'DisposableEmails.xlsx')
        valid_file_path = os.path.join(file_path, 'ValidEmails.xlsx')

        # write the results to new Excel files
        disposable_emails.to_excel(disposable_file_path, index=False)
        valid_emails.to_excel(valid_file_path, index=False)

        # show processing message
        messagebox.showinfo(title="Success", message="Processing complete. Saved as 'DisposableEmails.xlsx' and 'ValidEmails.xlsx'.")

        return disposable_file_path, valid_file_path

    except Exception as e:
        messagebox.showerror(title='Error.', message=str(e))
        return None, None


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        disposable_file, valid_file = process_email(file_path)
        # You can handle the returned file paths here if needed
        if disposable_file and valid_file:
            print(f"Disposable emails saved to: {disposable_file}")
            print(f"Non-disposable emails saved to: {valid_file}")


# Set up the GUI
root = tk.Tk()
root.title("Email Validator")

canvas = tk.Canvas(root, height=200, width=400)
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

label = tk.Label(frame, text="Select an Excel file to process", bg="white")
label.pack(pady=20)

button = tk.Button(frame, text="Browse", padx=10, pady=5, fg="white", bg="#263D42", command=browse_file)
button.pack()
root.mainloop()