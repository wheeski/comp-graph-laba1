import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

root = tk.Tk()
root.title("Лаба 1")
root.geometry("900x900")
img = None
marked_points = set()
preview_label = tk.Label(root)

def  update_preview():
    display_img = img.copy()
    display_img.thumbnail((700, 700))
    tk_img = ImageTk.PhotoImage(display_img)
    preview_label.configure(image=tk_img)
    preview_label.image = tk_img
    preview_label.pack()
    
def open_image():
    global img
    path = filedialog.askopenfilename()
    if not path:
        return
    img = Image.open(path).convert("RGB")
    update_preview()

def process_image():
    global img, marked_points
    width, height = img.size
    top_left = (0, 0)
    top_center = (width // 2, 0)
    center = (width // 2, height // 2)
    img.putpixel(top_left, (0,0,255))
    img.putpixel(top_center, (255,255,0))
    img.putpixel(center, (255,0,255))
    marked_points = {top_center, top_left, center}
    update_preview()
    
def save_png():
    path = filedialog.asksaveasfilename(defaultextension=".png")
    if not path:
        return
    img.save(path)
    
def save_pbm():
    path = filedialog.asksaveasfilename(defaultextension=".pbm")
    if not path:
        return
    width, height = img.size
    with open(path, "w") as f:
        f.write(f"P1\n{width} {height}\n")
        for y in range(height):
            row = []
            for x in range(width):
                if (x, y) in marked_points:
                    row.append("0")
                else:
                    row.append("1")
            f.write(" ".join(row) + "\n")
            
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=10)

tk.Button(button_frame, text="Открыть", command=open_image, width=20).pack(side=tk.LEFT, padx=5, pady=10)
tk.Button(button_frame, text="Обработать", command=process_image, width=20).pack(side=tk.LEFT, padx=5, pady=10)
tk.Button(button_frame, text="Сохранить в png", command=save_png, width=20).pack(side=tk.LEFT, padx=5, pady=10)
tk.Button(button_frame, text="Сохранить в pbm", command=save_pbm, width=20).pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()