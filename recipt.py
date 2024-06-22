import tkinter as tk
from tkinter import messagebox, StringVar, ttk
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

# Define subscription types and their prices
subscriptions = {
    "Bronze": 2000,
    "Prime": 5000,
    "Gold": 10000
}

# Header and description for KK GYM
header = "KK GYM"
description = """
KK's Gym is a globally renowned fitness brand that has made its mark in India. KK’s Gym India carries the legacy ahead in the home country since its inception in 2002. World-class fitness facilities and a comprehensive range of workout programs tailored to meet the needs of diverse fitness enthusiasts is what sets us apart from others.

KK's Gym India, a part of this esteemed legacy, has expanded its presence across various cities, aiming to empower individuals to achieve their fitness goals, regardless of their fitness levels or aspirations. It's a fitness haven that combines state-of-the-art equipment, expert trainers, and a supportive community to foster a holistic approach to wellness.
"""

def generate_pdf():
    DATA = get_user_data()
    if DATA:
        # Ensure the directory exists
        if not os.path.exists("receipts"):
            os.makedirs("receipts")

        # Save the PDF to the 'receipts' directory
        pdf_path = "receipts/receipt.pdf"
        pdf = SimpleDocTemplate(pdf_path, pagesize=A4)

        styles = getSampleStyleSheet()

        # Title header for KK GYM
        title_header = Paragraph(f"<b>{header}</b>", styles["Title"])

        # Description for KK GYM
        description_para = Paragraph(description, styles["Normal"])

        title_style = styles["Heading1"]
        title_style.alignment = 1
        title = Paragraph("Receipt", title_style)

        # Add subscription details dynamically to the PDF
        subscription_info = "\n".join([f"{subscription}: Rs. {price}" for subscription, price in subscriptions.items()])
        subscription_paragraph = Paragraph(f"<br/><b>Subscription Details:</b><br/>{subscription_info}", styles["Normal"])

        style = TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (3, len(DATA) - 1), 1, colors.black),
            ("BACKGROUND", (0, 0), (3, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ])
        table = Table(DATA, style=style)

        elements = [title_header, Spacer(1, 12), description_para, Spacer(1, 12), title, Spacer(1, 12), subscription_paragraph, Spacer(1, 12), table]
        pdf.build(elements)
        messagebox.showinfo("Success", f"Receipt generated successfully! Saved in '{pdf_path}'.")

def add_item():
    new_row = len(entries) + 1
    if new_row <= 10:
        new_date_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1)
        new_name_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1)
        new_subscription_entry = ttk.Combobox(root, values=list(subscriptions.keys()), state="readonly")
        new_subscription_entry.set("Bronze")
        new_price_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1, state="readonly")
        new_subscription_entry.bind("<<ComboboxSelected>>", lambda event, entry=new_price_entry, sub_entry=new_subscription_entry: update_price(entry, sub_entry))

        new_date_entry.grid(row=new_row, column=1, padx=10, pady=5)
        new_name_entry.grid(row=new_row, column=2, padx=10, pady=5)
        new_subscription_entry.grid(row=new_row, column=3, padx=10, pady=5)
        new_price_entry.grid(row=new_row, column=4, padx=10, pady=5)
        entries.append((new_date_entry, new_name_entry, new_subscription_entry, new_price_entry))
        update_button_positions()
    else:
        messagebox.showinfo("Info", "Maximum limit reached.")

def remove_item():
    if len(entries) > 1:
        for widget in entries[-1]:
            widget.destroy()
        entries.pop()
        update_button_positions()
    else:
        messagebox.showinfo("Info", "At least one item is required.")

def update_price(price_entry, sub_entry):
    subscription = sub_entry.get()
    price = subscriptions.get(subscription, 0)
    price_entry.config(state="normal")
    price_entry.delete(0, tk.END)
    price_entry.insert(0, price)
    price_entry.config(state="readonly")

def update_button_positions():
    new_row = len(entries) + 1
    add_button.grid(row=new_row, column=1, columnspan=2, pady=10)
    remove_button.grid(row=new_row, column=3, columnspan=2, pady=10)
    generate_button.grid(row=new_row + 1, column=1, columnspan=4, pady=10)
    if len(entries) >= 10:
        add_button.config(state="disabled")
    else:
        add_button.config(state="normal")

def get_user_data():
    data = [["Date", "Name", "Subscription", "Price (Rs.)"]]
    total_price = 0
    for entry_set in entries:
        date = entry_set[0].get()
        name = entry_set[1].get()
        subscription = entry_set[2].get()
        price = entry_set[3].get()
        if not date or not name or not subscription or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", f"Invalid price: {price}")
            return None
        total_price += price
        data.append([date, name, subscription, f"{price}/-"])
    data.append(["", "", "Total", f"{total_price}/-"])
    return data

# Create GUI
root = tk.Tk()
root.title("Receipt Generator")
root.configure(bg="#f0f0f0")
root.geometry("800x600")

# Labels
tk.Label(root, text="Date (DD/MM/YYYY):", bg="#f0f0f0").grid(row=0, column=1, padx=10, pady=5)
tk.Label(root, text="Name:", bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=5)
tk.Label(root, text="Subscription:", bg="#f0f0f0").grid(row=0, column=3, padx=10, pady=5)
tk.Label(root, text="Price (Rs.):", bg="#f0f0f0").grid(row=0, column=4, padx=10, pady=5)

# Entry fields for the first item
date_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1)
name_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1)
subscription_entry = ttk.Combobox(root, values=list(subscriptions.keys()), state="readonly")
subscription_entry.set("Bronze")
price_entry = tk.Entry(root, bg="white", relief="solid", borderwidth=1, state="readonly")
subscription_entry.bind("<<ComboboxSelected>>", lambda event: update_price(price_entry, subscription_entry))

date_entry.grid(row=1, column=1, padx=10, pady=5)
name_entry.grid(row=1, column=2, padx=10, pady=5)
subscription_entry.grid(row=1, column=3, padx=10, pady=5)
price_entry.grid(row=1, column=4, padx=10, pady=5)

# List to store entry fields
entries = [(date_entry, name_entry, subscription_entry, price_entry)]
update_price(price_entry, subscription_entry)

# Add and Remove item buttons
add_button = tk.Button(root, text="Add Item", command=add_item, bg="#4CAF50", fg="white", relief="raised", borderwidth=1)
add_button.grid(row=2, column=1, columnspan=2, pady=10)

remove_button = tk.Button(root, text="Remove Item", command=remove_item, bg="#F44336", fg="white", relief="raised", borderwidth=1)
remove_button.grid(row=2, column=3, columnspan=2, pady=10)

# Generate PDF Button
generate_button = tk.Button(root, text="Generate Receipt", command=generate_pdf, bg="#4CAF50", fg="white", relief="raised", borderwidth=1)
generate_button.grid(row=3, column=1, columnspan=4, pady=10)

root.mainloop()
