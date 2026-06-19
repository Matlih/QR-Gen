# QR Code Generator

A simple, beautiful, and modern QR code generator written strictly in Python. It provides a clean Desktop Interface (GUI) and a powerful Command Line Interface (CLI).

![Sample QR Code](sample_qr.jfif)

## 🌟 Features
- **Generate QR Codes:** Convert any URL or text into a scannable QR code.
- **Custom Colors:** Pick your own foreground and background colors.
- **Add Logos:** Embed your custom logo right in the center of the QR code.
- **Quick Save:** Instantly save QR codes to a dedicated `generated` folder, or use "Save As" to pick your own location.
- **Dark Mode Support:** The desktop app automatically matches your system's dark/light theme.

---

## 🚀 Installation & Setup

**Prerequisites:**
- Python 3.8 or higher is required.

**Step 1:** Clone or download the repository, then open your terminal in the project folder.

**Step 2:** Install the package. We recommend using a virtual environment:
```bash
pip install -e .
```
*(This installs the app and its dependencies so that the commands are available globally in your environment.)*

---

## 💻 How to Use

### 1. Desktop GUI (Recommended)
Launch the graphical interface by running this simple command in your terminal:
```bash
qr-gen-gui
```
*(Or run `python -m qr_gen.gui`)*

### 2. Command Line Interface (CLI)
You can also use the tool entirely from your terminal using the `qr-gen` command.

**Basic Generation:**
```bash
qr-gen "https://example.com"
```

**Save with a Custom Name:**
```bash
qr-gen "https://example.com" -o my_qr_code.png
```

**Change Colors & Add Logo:**
```bash
qr-gen "https://example.com" -fc blue -bc white -l my_logo.png
```
*(Use `qr-gen --help` to see all available terminal options!)*

---

## 🛠️ Development
To run unit tests:
```bash
pip install -e .[dev]
pytest
```
