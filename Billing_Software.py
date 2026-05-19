
import customtkinter as ctk
import mysql.connector
from tkinter import Listbox, END, messagebox


# ==========================================================
# DATABASE CONNECTION
# ==========================================================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9856",
    database="Food"
)

cursor = db.cursor()


# ==========================================================
# DATABASE FUNCTIONS
# ==========================================================
def load_menu():
    """
    Load all menu items from MySQL table: food_1
    Required columns:
        Item  (VARCHAR)
        Price (INT or DECIMAL)
    Returns:
        {"Momo": 120, "Burger": 150}
    """
    cursor.execute("SELECT Item, Price FROM food_1 ORDER BY Item")
    rows = cursor.fetchall()
    return {item: price for item, price in rows}


# Load menu initially
menu = load_menu()


# ==========================================================
# CUSTOMTKINTER SETTINGS
# ==========================================================
ctk.set_appearance_mode("dark")          # dark / light / system
ctk.set_default_color_theme("blue")      # blue / green / dark-blue


# ==========================================================
# MAIN WINDOW
# ==========================================================
app = ctk.CTk()
app.title("🍔 Fast Food POS System")
app.geometry("1200x850")
# app.resizable(False, False)


# ==========================================================
# DATA STORAGE
# ==========================================================
orders = {}   # Example: {"Momo": 2, "Burger": 1}


# ==========================================================
# ORDER FUNCTIONS
# ==========================================================
def update_order_list():
    """Refresh order list and total amount."""
    listbox.delete(0, END)

    total = 0

    for item, qty in orders.items():
        if item not in menu:
            continue

        price = menu[item]
        subtotal = price * qty
        total += subtotal

        listbox.insert(
            END,
            f"{item:<15} x {qty:<2} = ₹{subtotal}"
        )

    total_label.configure(text=f"Total: ₹{total}")


def add_item(item):
    """Add menu item to order."""
    orders[item] = orders.get(item, 0) + 1
    update_order_list()


def delete_selected():
    """Delete selected item from order."""
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Delete Item",
            "Please select an item to delete."
        )
        return

    selected_text = listbox.get(selected[0])
    item_name = selected_text.split(" x ")[0].strip()

    if item_name in orders:
        del orders[item_name]

    update_order_list()


def clear_order():
    """Clear entire order manually."""
    if not orders:
        return

    if messagebox.askyesno(
        "Clear Order",
        "Do you want to clear the current order?"
    ):
        orders.clear()
        update_order_list()


def place_order():
    """Show order summary and clear list automatically."""
    if not orders:
        messagebox.showwarning(
            "Order",
            "No items selected."
        )
        return

    total = 0
    lines = []

    for item, qty in orders.items():
        if item not in menu:
            continue

        subtotal = menu[item] * qty
        total += subtotal
        lines.append(f"{item} x {qty} = ₹{subtotal}")

    summary = "\n".join(lines)

    messagebox.showinfo(
        "Order Placed Successfully",
        f"{summary}\n\nTotal Amount: ₹{total}"
    )

    # Clear order after successful placement
    orders.clear()
    update_order_list()


def toggle_theme():
    """Switch between dark and light mode."""
    current_mode = ctk.get_appearance_mode()

    if current_mode == "Dark":
        ctk.set_appearance_mode("light")
        theme_button.configure(text="🌙 Dark Mode")
    else:
        ctk.set_appearance_mode("dark")
        theme_button.configure(text="☀ Light Mode")


# ==========================================================
# MENU BUTTON FUNCTIONS
# ==========================================================
def build_menu_buttons():
    """Create all menu buttons from the current menu dictionary."""
    # Remove old buttons
    for widget in buttons_frame.winfo_children():
        widget.destroy()

    # Create new buttons
    for index, item in enumerate(menu.keys()):
        row = index // 4
        column = index % 4

        btn = ctk.CTkButton(
            buttons_frame,
            text=f"{item}\n₹{menu[item]}",
            width=140,
            height=70,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            command=lambda x=item: add_item(x)
        )
        btn.grid(
            row=row,
            column=column,
            padx=10,
            pady=10
        )


def sync_menu():
    """
    Reload all menu items from MySQL and recreate all buttons.
    Any newly added records in food_1 will appear immediately.
    """
    global menu

    try:
        # Reload latest data from MySQL
        menu = load_menu()

        # Remove all existing buttons
        for widget in buttons_frame.winfo_children():
            widget.destroy()

        # Create buttons again from updated menu
        for index, item in enumerate(menu.keys()):
            row = index // 4
            column = index % 4

            btn = ctk.CTkButton(
                buttons_frame,
                text=f"{item}\n₹{menu[item]}",
                width=140,
                height=70,
                corner_radius=12,
                font=("Segoe UI", 14, "bold"),
                command=lambda x=item: add_item(x)
            )
            btn.grid(
                row=row,
                column=column,
                padx=10,
                pady=10
            )

        # Refresh order list and total
        update_order_list()

        # Success message
        messagebox.showinfo(
            "Sync Complete",
            f"{len(menu)} items loaded successfully."
        )

    except Exception as e:
        messagebox.showerror(
            "Sync Error",
            str(e)
        )


# ==========================================================
# HEADER
# ==========================================================
header = ctk.CTkFrame(app, corner_radius=15)
header.pack(fill="x", padx=20, pady=(20, 10))

title_label = ctk.CTkLabel(
    header,
    text="🍔 Fast Food POS System",
    font=("Segoe UI", 30, "bold")
)
title_label.pack(side="left", padx=20, pady=15)

theme_button = ctk.CTkButton(
    header,
    text="☀ Light Mode",
    width=140,
    command=toggle_theme
)
theme_button.pack(side="right", padx=20)

# Sync Button
sync_button = ctk.CTkButton(
    header,
    text="🔄 Sync",
    width=120,
    command=sync_menu
)
sync_button.pack(side="right", padx=10)


# ==========================================================
# MAIN FRAME
# ==========================================================
main_frame = ctk.CTkFrame(app, corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)


# ==========================================================
# LEFT PANEL - MENU ITEMS
# ==========================================================
left_panel = ctk.CTkFrame(main_frame, corner_radius=15)
left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(15, 10),
    pady=15
)

menu_label = ctk.CTkLabel(
    left_panel,
    text="📋 Menu Items",
    font=("Segoe UI", 22, "bold")
)
menu_label.pack(pady=(15, 10))

buttons_frame = ctk.CTkFrame(
    left_panel,
    fg_color="transparent"
)
buttons_frame.pack(padx=15, pady=10)


# ==========================================================
# RIGHT PANEL - ORDER SUMMARY
# ==========================================================
right_panel = ctk.CTkFrame(
    main_frame,
    width=340,
    corner_radius=15
)
right_panel.pack(
    side="right",
    fill="y",
    padx=(10, 15),
    pady=15
)
right_panel.pack_propagate(False)

order_label = ctk.CTkLabel(
    right_panel,
    text="🛒 Current Order",
    font=("Segoe UI", 22, "bold")
)
order_label.pack(pady=(15, 10))

# Tkinter Listbox inside CustomTkinter
listbox = Listbox(
    right_panel,
    width=35,
    height=16,
    font=("Consolas", 12),
    bg="#2b2b2b",
    fg="white",
    selectbackground="#1f6aa5",
    activestyle="none",
    bd=0
)
listbox.pack(padx=20, pady=10)

# Total Label
total_label = ctk.CTkLabel(
    right_panel,
    text="Total: ₹0",
    font=("Segoe UI", 20, "bold")
)
total_label.pack(pady=(10, 20))

# Place Order Button
place_btn = ctk.CTkButton(
    right_panel,
    text="✅ Place Order",
    height=45,
    font=("Segoe UI", 14, "bold"),
    command=place_order
)
place_btn.pack(fill="x", padx=20, pady=5)

# Delete Selected Button
delete_btn = ctk.CTkButton(
    right_panel,
    text="🗑 Delete Selected",
    height=45,
    font=("Segoe UI", 14, "bold"),
    fg_color="#C0392B",
    hover_color="#A93226",
    command=delete_selected
)
delete_btn.pack(fill="x", padx=20, pady=5)

# Clear Order Button
clear_btn = ctk.CTkButton(
    right_panel,
    text="♻ Clear Order",
    height=45,
    font=("Segoe UI", 14, "bold"),
    fg_color="#E67E22",
    hover_color="#CA6F1E",
    command=clear_order
)
clear_btn.pack(fill="x", padx=20, pady=5)


# ==========================================================
# INITIALIZE
# ==========================================================
build_menu_buttons()
update_order_list()


# ==========================================================
# START APPLICATION
# ==========================================================
app.mainloop()
