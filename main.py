import tkinter as tk
from tkinter import messagebox
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- DATABASE CONNECTION ----------------
conn = mysql.connector.connect(
    host= os.getenv("DB_HOST"),
    user= os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    database= os.getenv("DB_NAME")
)

cursor = conn.cursor()

# ---------------- EMAIL FUNCTION ----------------
def send_email(name, email, password, gender, country):


    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    app_password = os.getenv("EMAIL_PASS")

    subject = "📩 New Enquiry Received"

    body = f"""
=========================
NEW ENQUIRY ALERT
=========================

Name     : {name}
Email    : {email}
Password : {password}
Gender   : {gender}
Country  : {country}

-------------------------
This enquiry was submitted from your Tkinter app.
-------------------------
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()

        print("Enquiry Email Sent Successfully")

    except Exception as e:
        print("Email Error:", e)

# ---------------- SUBMIT FUNCTION ----------------
def submit_form():

    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    gender = gender_var.get()
    country = country_entry.get()

    query = """
    INSERT INTO users (name, email, password, gender, country)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (name, email, password, gender, country)

    try:
        cursor.execute(query, values)
        conn.commit()

        print("Data Inserted Successfully")

        # Send Email
        send_email(name, email, password, gender, country)

        messagebox.showinfo("Success", "Registration Successful")

        # Clear Fields
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        country_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- TKINTER WINDOW ----------------
root = tk.Tk()

root.title("Registration Form")
root.geometry("400x450")

# Name
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Email
tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

# Password
tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# Gender
tk.Label(root, text="Gender").pack()

gender_var = tk.StringVar(value="Male")

tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").pack()
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").pack()

# Country
tk.Label(root, text="Country").pack()
country_entry = tk.Entry(root, width=30)
country_entry.pack(pady=5)

# Submit Button
submit_btn = tk.Button(
    root,
    text="Submit",
    bg="green",
    fg="white",
    command=submit_form
)

submit_btn.pack(pady=20)

root.mainloop()

# Close DB Connection
cursor.close()
conn.close()