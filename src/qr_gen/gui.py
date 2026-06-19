import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from qr_gen.core import generate_qr

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QR Code Generator")
        self.geometry("600x750")
        self.minsize(500, 650)

        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.logo_path = None
        self.current_qr_path = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkLabel(self, text="QR Code Generator", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Main Frame
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 1. URL / Text Input
        self.data_label = ctk.CTkLabel(self.main_frame, text="URL or Text to encode:")
        self.data_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.data_entry = ctk.CTkEntry(self.main_frame, placeholder_text="https://example.com")
        self.data_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))

        # 2. Colors
        color_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        color_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 20))
        color_frame.grid_columnconfigure(0, weight=1)
        color_frame.grid_columnconfigure(1, weight=1)

        self.fg_color_label = ctk.CTkLabel(color_frame, text="Foreground Color:")
        self.fg_color_label.grid(row=0, column=0, sticky="w")
        self.fg_color_entry = ctk.CTkEntry(color_frame, placeholder_text="black, #000000, etc.")
        self.fg_color_entry.insert(0, "black")
        self.fg_color_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        self.bg_color_label = ctk.CTkLabel(color_frame, text="Background Color:")
        self.bg_color_label.grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.bg_color_entry = ctk.CTkEntry(color_frame, placeholder_text="white, #FFFFFF, etc.")
        self.bg_color_entry.insert(0, "white")
        self.bg_color_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0))

        # 3. Logo Embedding
        self.logo_label = ctk.CTkLabel(self.main_frame, text="Optional Logo:")
        self.logo_label.grid(row=3, column=0, sticky="w", padx=10)
        
        logo_btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        logo_btn_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        self.logo_btn = ctk.CTkButton(logo_btn_frame, text="Browse Logo...", command=self.browse_logo)
        self.logo_btn.pack(side="left")
        
        self.logo_path_label = ctk.CTkLabel(logo_btn_frame, text="No logo selected.", text_color="gray")
        self.logo_path_label.pack(side="left", padx=10)

        self.clear_logo_btn = ctk.CTkButton(logo_btn_frame, text="X", width=30, fg_color="red", command=self.clear_logo)
        
        # 4. Generate Button
        self.generate_btn = ctk.CTkButton(
            self.main_frame, 
            text="Generate Preview", 
            command=self.generate_preview_threaded,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.generate_btn.grid(row=5, column=0, sticky="ew", padx=10, pady=10)

        # 5. Preview Image
        self.preview_label = ctk.CTkLabel(self.main_frame, text="")
        self.preview_label.grid(row=6, column=0, pady=20)

        # 6. Save Buttons Frame (Hidden initially)
        self.save_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.save_as_btn = ctk.CTkButton(
            self.save_frame, 
            text="Save As...", 
            command=self.save_image,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.save_as_btn.pack(side="left", padx=5)

        self.quick_save_btn = ctk.CTkButton(
            self.save_frame, 
            text="Quick Save (generated folder)", 
            command=self.quick_save,
            fg_color="#0066cc",
            hover_color="#004c99"
        )
        self.quick_save_btn.pack(side="left", padx=5)

    def browse_logo(self):
        filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Select a logo", filetypes=filetypes)
        if filename:
            self.logo_path = filename
            self.logo_path_label.configure(text=Path(filename).name)
            self.clear_logo_btn.pack(side="left", padx=5)

    def clear_logo(self):
        self.logo_path = None
        self.logo_path_label.configure(text="No logo selected.")
        self.clear_logo_btn.pack_forget()

    def generate_preview_threaded(self):
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter URL or text to encode.")
            return

        self.generate_btn.configure(state="disabled", text="Generating...")
        thread = threading.Thread(target=self._generate_qr)
        thread.start()

    def _generate_qr(self):
        try:
            # We save a temporary file for the preview
            temp_output = "temp_preview_qr.png"
            generate_qr(
                url_or_text=self.data_entry.get().strip(),
                output_path=temp_output,
                fill_color=self.fg_color_entry.get().strip() or "black",
                back_color=self.bg_color_entry.get().strip() or "white",
                logo_path=self.logo_path
            )
            
            self.current_qr_path = temp_output
            self.show_preview(temp_output)
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Generation Error", str(e)))
        finally:
            self.after(0, lambda: self.generate_btn.configure(state="normal", text="Generate Preview"))

    def show_preview(self, path):
        try:
            img = Image.open(path)
            # Resize for preview
            img.thumbnail((300, 300))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            self.after(0, lambda: self._update_preview_ui(ctk_img))
        except Exception as e:
            print(f"Error loading preview: {e}")

    def _update_preview_ui(self, ctk_img):
        self.preview_label.configure(image=ctk_img, text="")
        self.save_frame.grid(row=7, column=0, pady=(0, 20))

    def save_image(self):
        if not self.current_qr_path:
            return

        filetypes = (("PNG files", "*.png"), ("All files", "*.*"))
        save_path = filedialog.asksaveasfilename(
            title="Save QR Code", 
            defaultextension=".png", 
            filetypes=filetypes,
            initialfile="qrcode.png"
        )
        
        if save_path:
            try:
                import shutil
                shutil.copy2(self.current_qr_path, save_path)
                messagebox.showinfo("Success", f"QR Code saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def quick_save(self):
        if not self.current_qr_path:
            return
            
        import shutil
        import datetime
        
        # Ensure 'generated' folder exists
        generated_dir = Path("generated")
        generated_dir.mkdir(exist_ok=True)
        
        # Generate a unique filename based on timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = generated_dir / f"qrcode_{timestamp}.png"
        
        try:
            shutil.copy2(self.current_qr_path, save_path)
            messagebox.showinfo("Success", f"QR Code quickly saved to:\n{save_path.resolve()}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to quick save image: {e}")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
