from tkinter import Tk, Label, Button, filedialog, Frame, Entry, messagebox
from PIL import Image, ImageTk
import os, sys


class ImageViewer:
    def __init__(self, root, initial_dir=None):
        self.root = root
        self.root.title("Image Viewer")
        
        # 创建一个框架用于放置控制按钮
        self.control_frame = Frame(root)
        self.control_frame.pack(fill="x", side="top")

        # 将"Open Directory"按钮放在左上角
        self.button_frame = Button(self.control_frame, text="Open Directory", command=self.open_directory)
        self.button_frame.pack(side="left", padx=5, pady=5)

        # 将"Previous"和"Next"按钮放在右上角
        self.prev_button = Button(self.control_frame, text="Next>>", command=self.next_image)
        self.prev_button.pack(side="right", padx=5, pady=5)

        self.next_button = Button(self.control_frame, text="<<Prev", command=self.prev_image)
        self.next_button.pack(side="right", padx=5)

        # 在控制按钮下方创建一个新框架用于放置显示路径的Entry
        self.path_frame = Frame(root)
        self.path_frame.pack(fill="x", side="top", pady=5)
        
        # 在新框架中添加一个Entry用于显示路径
        self.path_entry = Entry(self.path_frame, state='readonly', readonlybackground='white', fg='black')
        self.path_entry.pack(fill='x', expand=True, padx=5)

        # 图像显示在路径显示的下方
        self.image_label = Label(root)
        self.image_label.pack(fill="both", expand=True, pady=5)

        self.images = []
        self.current_image = 0
        root.geometry("1024x768")  # 设置窗口的初始大小为1024x768

        # 绑定键盘事件
        root.bind('<Left>', self.prev_image_event)
        root.bind('<Right>', self.next_image_event)

        if initial_dir and os.path.isdir(initial_dir):
            self.load_images_recursive(initial_dir)
            self.show_image()
            
    def prev_image_event(self, event):
        self.prev_image()

    def next_image_event(self, event):
        self.next_image()

    def open_directory(self):
        directory = filedialog.askdirectory()
        if not directory:  # askdirectory returns '' if the user cancels.
            return

        self.images = [os.path.join(directory, f) for f in os.listdir(directory)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                       
        # self.images.sort()  # Optional: sort files by name
        self.current_image = 0
        self.show_image()

    def show_image(self):
        if not self.images:
            self.image_label.config(text="No images found in the directory")
            return

        image_path = self.images[self.current_image]
        pil_image = Image.open(image_path)

        # 设定最大宽度和高度，这里可以根据你的窗口内容区的实际可用大小进行调整
        max_width = 800
        max_height = 600
        if pil_image.width > max_width or pil_image.height > max_height:
            ratio = min(max_width / pil_image.width, max_height / pil_image.height)
            pil_image = pil_image.resize((int(pil_image.width * ratio), int(pil_image.height * ratio)), Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(pil_image)
        
        self.image_label.config(image=img)
        self.image_label.image = img  # Keep a reference!
        self.root.title(f"Image Viewer - {os.path.basename(image_path)}")

        # 显示当前图像的路径
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, 'end')
        self.path_entry.insert(0, image_path)
        self.path_entry.config(state='readonly')
        
        # 绑定点击事件以复制路径
        self.path_entry.bind('<Button-1>', self.copy_path_to_clipboard)        

    def prev_image(self):
        if self.images and self.current_image > 0:
            self.current_image -= 1
            self.show_image()

    def next_image(self):
        if self.images and self.current_image < len(self.images) - 1:
            self.current_image += 1
            self.show_image()

    def load_images(self, directory):
        self.images = [os.path.join(directory, f) for f in os.listdir(directory)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.images.sort()  # Optional: sort files by name
        self.current_image = 0

    def load_images_recursive(self, directory):
        self.images = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    self.images.append(os.path.join(root, file))
        self.images.sort()  # 排序图像
        self.current_image = 0

    def copy_path_to_clipboard(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.path_entry.get())
        messagebox.showinfo("Info", "Path copied to clipboard")


if __name__ == "__main__":
    root = Tk()
    root.geometry("1024x768")  # 设置窗口的初始大小为1024x768
    root.resizable(width=False, height=False)  # 禁止调整窗口大小
    # 检查是否有命令行参数提供，并传递给ImageViewer
    initial_dir = sys.argv[1] if len(sys.argv) > 1 else None
    viewer = ImageViewer(root, initial_dir=initial_dir)    
    #viewer = ImageViewer(root)
    root.mainloop()    
