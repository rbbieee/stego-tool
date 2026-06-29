import tkinter as tk
from tkinter import filedialog, messagebox

# Reuse the logic we already built
from stego import encode, decode


# Create the main window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x400")

# Variable to remember which image the user picked
selected_image = tk.StringVar()

# --- Title ---
title = tk.Label(root, text="Steganography Tool", font=("Arial", 16, "bold"))
title.pack(pady=10)

# --- Image picker ---
def choose_image():
    path = filedialog.askopenfilename(filetypes=[("PNG images", "*.png")])
    if path:
        selected_image.set(path)

choose_btn = tk.Button(root, text="Choose Image", command=choose_image)
choose_btn.pack(pady=5)

# Show the chosen file path
image_label = tk.Label(root, textvariable=selected_image, fg="gray", wraplength=450)
image_label.pack(pady=5)

# --- Message input ---
msg_label = tk.Label(root, text="Message:")
msg_label.pack()

msg_entry = tk.Entry(root, width=50)
msg_entry.pack(pady=5)

# Called when the Encode button is clicked
def handle_encode():
    image = selected_image.get()
    message = msg_entry.get()

    # Basic checks before running
    if not image:
        messagebox.showwarning("Missing image", "Please choose an image first.")
        return
    if not message:
        messagebox.showwarning("Missing message", "Please type a message to hide.")
        return

    # Ask where to save the result
    output = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG images", "*.png")]
    )
    if not output:
        return

    encode(image, message, output)
    result_label.config(text=f"Message hidden and saved to:\n{output}")


# Called when the Decode button is clicked
def handle_decode():
    image = selected_image.get()

    if not image:
        messagebox.showwarning("Missing image", "Please choose an image first.")
        return

    message = decode(image)
    if message:
        result_label.config(text=f"Hidden message:\n{message}")
    else:
        result_label.config(text="No hidden message found.")

# --- Action buttons ---
encode_btn = tk.Button(root, text="Encode", width=15, command=handle_encode)
encode_btn.pack(pady=5)

decode_btn = tk.Button(root, text="Decode", width=15, command=handle_decode)
decode_btn.pack(pady=5)

# --- Result area ---
result_label = tk.Label(root, text="", fg="green", wraplength=450)
result_label.pack(pady=10)

# Start the event loop (keeps the window open)
root.mainloop()