import tkinter as tk
from tkinter import ttk
import hashlib
from base64 import b64encode, b64decode
import os
from tkinter import messagebox
import hmac
from version import get_version
from about import About
from sponsor import Sponsor

# Constants matching PHP implementation
PBKDF2_HASH_ALGORITHM = 'SHA256'
PBKDF2_SALT_BYTE_SIZE = 24
PBKDF2_HASH_BYTE_SIZE = 24
HASH_SECTIONS = 4
HASH_ALGORITHM_INDEX = 0
HASH_ITERATION_INDEX = 1
HASH_SALT_INDEX = 2
HASH_PBKDF2_INDEX = 3

class PasswordHasher:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Hash Generator")
        self.root.geometry("600x400")  # Increased height to show all content
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for better layout
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Password input
        ttk.Label(self.main_frame, text="Enter Password:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*", width=40)
        self.password_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Iterations input
        ttk.Label(self.main_frame, text="Iterations (1000-1000000): ").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.iterations_entry = ttk.Entry(self.main_frame, width=10)
        self.iterations_entry.insert(0, "1000")  # Default value
        self.iterations_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Add validation for iterations input
        self.iterations_entry.bind("<FocusOut>", self.validate_iterations)
        self.iterations_entry.bind("<Return>", self.validate_iterations)

        # Generate button
        self.generate_btn = ttk.Button(self.main_frame, text="Generate Hash", command=self.generate_hash)
        self.generate_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Output
        ttk.Label(self.main_frame, text="Generated Hash:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.hash_output = ttk.Entry(self.main_frame, width=60)  # Increased width to show full hash
        self.hash_output.grid(row=3, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Copy and Reset buttons
        self.copy_btn = ttk.Button(self.main_frame, text="Copy", command=self.copy_to_clipboard)
        self.copy_btn.grid(row=4, column=0, pady=10)
        
        self.reset_btn = ttk.Button(self.main_frame, text="Reset", command=self.reset_fields)
        self.reset_btn.grid(row=4, column=1, pady=10)

    def validate_iterations(self, event=None):
        """Validate and adjust the iterations input"""
        try:
            value = int(self.iterations_entry.get())
            if value < 1000:
                messagebox.showwarning("Warning", "Iterations must be at least 1000")
                self.iterations_entry.delete(0, tk.END)
                self.iterations_entry.insert(0, "1000")
            elif value > 1000000:
                messagebox.showwarning("Warning", "Iterations cannot exceed 1000000")
                self.iterations_entry.delete(0, tk.END)
                self.iterations_entry.insert(0, "1000000")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number")
            self.iterations_entry.delete(0, tk.END)
            self.iterations_entry.insert(0, "1000")

        
    def generate_hash(self):
        try:
            # Get password
            password = self.password_entry.get()
            print(f"Password: {password}")  # Debug
            if not password:
                messagebox.showwarning("Warning", "Please enter a password")
                return
                
            # Get iterations
            try:
                iterations = int(self.iterations_entry.get())
                print(f"Iterations: {iterations}")  # Debug
                if iterations < 1000 or iterations > 1000000:
                    messagebox.showwarning("Warning", "Iterations must be between 1000 and 1000000")
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid number")
                return
            
            # Generate salt
            salt = os.urandom(PBKDF2_SALT_BYTE_SIZE)
            print(f"Salt length: {len(salt)}")  # Debug
            
            # Generate hash using PBKDF2 with SHA256
            key = hashlib.pbkdf2_hmac(
                PBKDF2_HASH_ALGORITHM,
                password.encode('utf-8'),
                salt,
                iterations,
                PBKDF2_HASH_BYTE_SIZE
            )
            print(f"Key length: {len(key)}")  # Debug
            
            # Format hash as algorithm:iterations:salt:hash
            hash_result = f"{PBKDF2_HASH_ALGORITHM}:{iterations}:{b64encode(salt).decode()}:" + \
                          b64encode(key).decode()
            print(f"Final hash: {hash_result}")  # Debug
            
            self.hash_output.delete(0, tk.END)
            self.hash_output.insert(0, hash_result)
        except Exception as e:
            print(f"Error generating hash: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate hash: {str(e)}")
            raise

    def validate_password(self, password, correct_hash):
        """Validate a password against a stored hash"""
        try:
            params = correct_hash.split(":")
            if len(params) < HASH_SECTIONS:
                return False
                
            # Extract parameters from hash
            algorithm = params[HASH_ALGORITHM_INDEX]
            iterations = int(params[HASH_ITERATION_INDEX])
            salt = b64decode(params[HASH_SALT_INDEX])
            expected_hash = b64decode(params[HASH_PBKDF2_INDEX])
            
            # Generate hash to compare
            test_hash = hashlib.pbkdf2_hmac(
                algorithm,
                password.encode('utf-8'),
                salt,
                iterations,
                len(expected_hash)
            )
            
            return self.slow_equals(expected_hash, test_hash)
        except (ValueError, TypeError, binascii.Error):
            return False

    def slow_equals(self, a, b):
        """Compare two strings in constant time to prevent timing attacks"""
        diff = len(a) ^ len(b)
        for i in range(min(len(a), len(b))):
            diff |= ord(a[i]) ^ ord(b[i])
        return diff == 0
        
    def copy_to_clipboard(self):
        hash_value = self.hash_output.get()
        if hash_value:
            self.root.clipboard_clear()
            self.root.clipboard_append(hash_value)
            messagebox.showinfo("Success", "Hex hash copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No hash to copy")
            
    def reset_fields(self):
        self.password_entry.delete(0, tk.END)
        self.iterations_entry.delete(0, tk.END)
        self.iterations_entry.insert(0, "1000")
        self.hash_output.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordHasher(root)
    
    # Configure grid weights to make the window resizable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Add menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: About.show_about(root))
    help_menu.add_command(label="Sponsor", command=lambda: Sponsor(root).show_sponsor())
    
    # Make sure the window is at least this size
    root.minsize(600, 400)
    
    root.mainloop()
