import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class DecryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography - Decryption")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.image_path = ""
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Image Steganography Decryption", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=10)

        # Image selection frame
        image_frame = ttk.LabelFrame(self.main_frame, text="Image Selection", padding="10")
        image_frame.pack(fill=tk.X, padx=5, pady=5)

        select_btn = ttk.Button(
            image_frame, 
            text="Select Encrypted Image",
            command=self.select_image
        )
        select_btn.pack(pady=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(self.main_frame, text="Image Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(pady=5)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Decryption Input", padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Password entry
        ttk.Label(input_frame, text="Enter Password:").pack(pady=2)
        self.password_entry = ttk.Entry(input_frame, width=60, show="*")
        self.password_entry.pack(pady=5)
        
        # Decrypt button
        decrypt_btn = ttk.Button(
            self.main_frame,
            text="Decrypt Message",
            command=self.decrypt_image,
            style='Accent.TButton'
        )
        decrypt_btn.pack(pady=20)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.main_frame, text="Decrypted Message", padding="10")
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, height=4, width=50, wrap=tk.WORD)
        self.result_text.pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            font=('Helvetica', 10)
        )
        self.status_bar.pack(pady=5)
        
    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("PNG Files", "*.png")]
        )
        if self.image_path:
            try:
                # Show preview
                preview = Image.open(self.image_path)
                # Calculate resize dimensions maintaining aspect ratio
                display_size = (300, 300)
                preview.thumbnail(display_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(preview)
                self.preview_label.configure(image=photo)
                self.preview_label.image = photo
                self.status_var.set("Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {str(e)}")
                self.status_var.set("Error loading image!")
            
    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        password = self.password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter the password!")
            return
            
        try:
            img = cv2.imread(self.image_path)
            
            # Create character mappings
            c = {i: chr(i) for i in range(255)}
            
            # Decrypt message
            message = ""
            n, m, z = 0, 0, 0
            
            while True:
                if n >= img.shape[0] or m >= img.shape[1]:
                    break
                
                char = c[img[n, m, z]]
                message += char
                
                # Check if we've reached the end marker
                if message.endswith('#END#'):
                    message = message[:-5]  # Remove the end marker
                    break
                
                n = n + 1
                m = m + 1
                z = (z + 1) % 3
                
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, message)
            self.status_var.set("Decryption completed successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Decryption failed!")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
    app = DecryptionGUI(root)
    root.mainloop()
