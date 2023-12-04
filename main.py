import tkinter as tk
from tkinter import messagebox

# Function to load user data from a file
def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            user_info = line.strip().split(',')
            data.append(user_info)
    return data

# Function to save user data to a file
def save_data(data, filename):
    with open(filename, 'w') as file:
        for user_info in data:
            line = ','.join(user_info)
            file.write(line + '\n')

# Function to create and show the balance window
def show_balance_window(main_window_instance, user_info, data):
    balance_window = tk.Toplevel(main_window_instance)
    balance_window.title("Balance and Transactions")

    # Display welcome message with user's first and last name
    welcome_message = "Welcome, {} {}!\nThank you for banking with {}!".format(user_info[0], user_info[1], user_info[2])
    welcome_label = tk.Label(balance_window, text=welcome_message)
    welcome_label.pack(pady=10)

    # Function to handle withdrawal
    def withdraw():
        nonlocal user_info, data
        amount = float(amount_entry.get())
        if amount > float(user_info[5]):
            messagebox.showerror("Error", "Insufficient funds.")
        else:
            user_info[5] = str(float(user_info[5]) - amount)
            messagebox.showinfo("Success", "Withdrawal successful. New balance: ${:,.2f}".format(float(user_info[5])))
            update_balance_label()
            save_data(data, 'updated_user_data.txt')

    # Function to handle deposit
    def deposit():
        nonlocal user_info, data
        amount = float(amount_entry.get())
        user_info[5] = str(float(user_info[5]) + amount)
        messagebox.showinfo("Success", "Deposit successful. New balance: ${:,.2f}".format(float(user_info[5])))
        update_balance_label()
        save_data(data, 'updated_user_data.txt')

    # Function to logout
    def logout():
        nonlocal data
        save_data(data, 'updated_user_data.txt')
        balance_window.destroy()
        login_window(main_window_instance, data)

    # Function to update the balance label
    def update_balance_label():
        balance_label.config(text="Current Balance: ${:,.2f}".format(float(user_info[5])))

    # display the current balance
    balance_label = tk.Label(balance_window, text="Current Balance: ${:,.2f}".format(float(user_info[5])))
    balance_label.pack(pady=10)

    # area for entering the amount for withdrawal or deposit
    amount_label = tk.Label(balance_window, text="Amount:")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(balance_window)
    amount_entry.pack(pady=5)

    # Buttons for withdrawal, deposit, and logout
    withdraw_button = tk.Button(balance_window, text="Withdraw", command=withdraw)
    withdraw_button.pack(side=tk.LEFT, padx=10)

    deposit_button = tk.Button(balance_window, text="Deposit", command=deposit)
    deposit_button.pack(side=tk.LEFT, padx=10)

    logout_button = tk.Button(balance_window, text="Logout", command=logout)
    logout_button.pack(side=tk.RIGHT, padx=10)


# Function to create and show the login window
def login_window(main_window_instance, data):
    login_window = tk.Toplevel(main_window_instance)
    login_window.title("Login")

    #  login process
    def login():
        nonlocal data
        card_number = card_entry.get()
        password = password_entry.get().strip()  # Strip whitespaces from the entered pin

        # Find matching users based on the entered card number
        matching_users = [user_info for user_info in data if str(user_info[3]).lstrip('0') == str(card_number).lstrip('0').zfill(16)]

        if matching_users:
            for user_info in matching_users:
                # Check if the entered pin is correct
                if str(user_info[4]) == password:
                    login_window.destroy()
                    show_balance_window(main_window_instance, user_info, data)
                    return
            messagebox.showerror("Error", "Invalid card number or pin.")
        else:
            messagebox.showerror("Error", "Invalid card number or pin.")

    # area to enter card number and button
    card_label = tk.Label(login_window, text="Card Number:")
    card_label.grid(row=0, column=0, padx=10)
    card_entry = tk.Entry(login_window)
    card_entry.grid(row=0, column=1, padx=10)

    password_label = tk.Label(login_window, text="Pin:")
    password_label.grid(row=1, column=0, padx=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10)

    #button to start logging in
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.grid(row=2, columnspan=2, pady=10)

# main window function
def main_window():
    root = tk.Tk()
    root.title("Wael and Damanjit's ATM Program")

    # Load user data from the file
    data = load_data('user_data.txt')

    # Buttons for login and exit
    login_button = tk.Button(root, text="Login", command=lambda: login_window(root, data))
    login_button.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=20)

    # Start the main window
    root.mainloop()

#start the program
if __name__ == "__main__":
    main_window()
