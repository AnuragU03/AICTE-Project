import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class EncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography - Encryption")
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
            text="Image Steganography Encryption", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=10)

        # Image selection frame
        image_frame = ttk.LabelFrame(self.main_frame, text="Image Selection", padding="10")
        image_frame.pack(fill=tk.X, padx=5, pady=5)

        select_btn = ttk.Button(
            image_frame, 
            text="Select Image",
            command=self.select_image
        )
        select_btn.pack(pady=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(self.main_frame, text="Image Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(pady=5)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Message Input", padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Message entry
        ttk.Label(input_frame, text="Enter Secret Message:").pack(pady=2)
        self.msg_entry = ttk.Entry(input_frame, width=60)
        self.msg_entry.pack(pady=5)
        
        # Password entry
        ttk.Label(input_frame, text="Enter Password:").pack(pady=2)
        self.password_entry = ttk.Entry(input_frame, width=60, show="*")
        self.password_entry.pack(pady=5)
        
        # Encrypt button
        encrypt_btn = ttk.Button(
            self.main_frame,
            text="Encrypt and Save",
            command=self.encrypt_image,
            style='Accent.TButton'
        )
        encrypt_btn.pack(pady=20)
        
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
            filetypes=[("Image Files", "*.jpg *.png *.bmp")]
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
            
    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        msg = self.msg_entry.get()
        password = self.password_entry.get()
        
        if not msg or not password:
            messagebox.showerror("Error", "Please enter both message and password!")
            return
            
        try:
            img = cv2.imread(self.image_path)
            
            # Add end marker to the message
            msg = msg + '#END#'
            
            # Check if image is large enough for the message
            max_chars = (img.shape[0] * img.shape[1] * 3) // 3
            if len(msg) > max_chars:
                messagebox.showerror(
                    "Error", 
                    f"Message is too long for this image!\nMaximum characters allowed: {max_chars}"
                )
                return
            
            # Create character mappings
            d = {chr(i): i for i in range(255)}
            
            # Encrypt message
            n, m, z = 0, 0, 0
            for i in range(len(msg)):
                img[n, m, z] = d[msg[i]]
                n = n + 1
                m = m + 1
                z = (z + 1) % 3
                
            # Save encrypted image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile="encrypted_image.png"
            )
            if save_path:
                cv2.imwrite(save_path, img)
                messagebox.showinfo("Success", "Image encrypted successfully!")
                self.status_var.set("Encryption completed successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Encryption failed!")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
    app = EncryptionGUI(root)
    root.mainloop()
