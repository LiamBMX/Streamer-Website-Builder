import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
from PIL import Image, ImageTk

class WebsiteEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Website Editor")
        self.logo_path = tk.StringVar()
        self.bg_path = tk.StringVar()
        self.links = []

        self.create_widgets()
        self.load_links()

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.theme_use('clam')  # Using clam theme
        style.configure('Custom.TButton', font=('Helvetica', 12), foreground='white', background='#4E6E8E')  # Blue
        style.map('Custom.TButton', background=[('active', '#607D8B')])  # Darker blue when active
        style.configure('Custom.TLabel', font=('Helvetica', 12), foreground='#9C27B0')  # Purple
        style.configure('Custom.TEntry', font=('Helvetica', 12))
        style.configure('Custom.TListbox', font=('Helvetica', 12), background='#ffffff', borderwidth=0)  # White background

        # Navigation Bar
        navbar = ttk.Frame(self.master, style='Custom.TLabel', padding=(10, 5))
        navbar.grid(row=0, column=0, sticky='ew')

        title_label = ttk.Label(navbar, text="Website Editor", style='Custom.TLabel')
        title_label.grid(row=0, column=0, padx=10, pady=5)

        # Creating the help button with SVG icon
        help_icon_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
        </svg>
        """
        help_img = self.svg_to_image(help_icon_svg, size=(24, 24))
        help_btn = tk.Button(navbar, image=help_img, command=self.show_help, bd=0, bg='#9C27B0', activebackground='#7B1FA2', highlightthickness=0)
        help_btn.image = help_img  # Keep a reference to prevent garbage collection
        help_btn.grid(row=0, column=1, padx=10, pady=5)

        # Container
        container = ttk.Frame(self.master, padding=20)
        container.grid(row=1, column=0)

        # Logo Section
        logo_section = ttk.LabelFrame(container, text="Logo Image", style='Custom.TLabel')
        logo_section.grid(row=0, column=0, padx=10, pady=5)

        self.logo_entry = ttk.Entry(logo_section, textvariable=self.logo_path, width=50)
        self.logo_entry.grid(row=0, column=0, padx=10, pady=5)

        browse_logo_btn = ttk.Button(logo_section, text="Browse", command=self.browse_logo, style='Custom.TButton')
        browse_logo_btn.grid(row=0, column=1, padx=10, pady=5)

        # Background Section
        bg_section = ttk.LabelFrame(container, text="Background Image", style='Custom.TLabel')
        bg_section.grid(row=1, column=0, padx=10, pady=5)

        self.bg_entry = ttk.Entry(bg_section, textvariable=self.bg_path, width=50)
        self.bg_entry.grid(row=0, column=0, padx=10, pady=5)

        browse_bg_btn = ttk.Button(bg_section, text="Browse", command=self.browse_bg, style='Custom.TButton')
        browse_bg_btn.grid(row=0, column=1, padx=10, pady=5)

        # Link Section
        link_section = ttk.LabelFrame(container, text="Add/Edit/Delete Links", style='Custom.TLabel')
        link_section.grid(row=2, column=0, padx=10, pady=5)

        self.link_entry = ttk.Entry(link_section, width=50)
        self.link_entry.grid(row=0, column=0, padx=10, pady=5)
        self.link_entry.insert(0, "Enter Link URL")

        self.label_entry = ttk.Entry(link_section, width=30)
        self.label_entry.grid(row=0, column=1, padx=10, pady=5)
        self.label_entry.insert(0, "Enter Label")

        add_link_btn = ttk.Button(link_section, text="Add Link", command=self.add_link, style='Custom.TButton')
        add_link_btn.grid(row=0, column=2, padx=10, pady=5)

        self.link_listbox = tk.Listbox(link_section, width=60, height=10, borderwidth=0)
        self.link_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        edit_link_btn = ttk.Button(link_section, text="Edit Link", command=self.edit_link, style='Custom.TButton')
        edit_link_btn.grid(row=2, column=0, padx=10, pady=5)

        remove_link_btn = ttk.Button(link_section, text="Remove Link", command=self.remove_link, style='Custom.TButton')
        remove_link_btn.grid(row=2, column=1, padx=10, pady=5)

        # Save Button
        save_btn = ttk.Button(container, text="Save Changes", command=self.save_changes, style='Custom.TButton')
        save_btn.grid(row=3, column=0, padx=10, pady=10)

    def browse_logo(self):
        filename = filedialog.askopenfilename(title="Select Logo Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
        self.logo_path.set(filename)
        shutil.copy(filename, "logo.png")

    def browse_bg(self):
        filename = filedialog.askopenfilename(title="Select Background Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
        self.bg_path.set(filename)
        shutil.copy(filename, "background.png")

    def add_link(self):
        link = self.link_entry.get()
        label = self.label_entry.get()
        if link:
            self.links.append((link, label))
            self.update_link_listbox()
            self.link_entry.delete(0, tk.END)
            self.label_entry.delete(0, tk.END)
            with open("index.html", "a") as f:
                f.write(f'<div class="links__item twitch_link">\n<a class="links__item links__item-twitch" href="{link}" target="_blank">{label}</a>\n</div>\n')

    def edit_link(self):
        selected_index = self.link_listbox.curselection()
        if selected_index:
            selected_link, selected_label = self.links[selected_index[0]]
            new_link = tk.simpledialog.askstring("Edit Link", "Enter new link:", initialvalue=selected_link)
            if new_link:
                new_label = tk.simpledialog.askstring("Edit Link", "Enter new label:", initialvalue=selected_label)
                if new_label:
                    self.links[selected_index[0]] = (new_link, new_label)
                    self.update_link_listbox()
                    with open("index.html", "r") as f:
                        lines = f.readlines()
                    with open("index.html", "w") as f:
                        for line in lines:
                            if selected_link in line:
                                new_line = line.replace(selected_link, new_link)
                                new_line = new_line.replace(selected_label, new_label)
                                f.write(new_line)
                            else:
                                f.write(line)

    def remove_link(self):
        selected_index = self.link_listbox.curselection()
        if selected_index:
            del self.links[selected_index[0]]
            self.update_link_listbox()
            with open("index.html", "r") as f:
                lines = f.readlines()
            with open("index.html", "w") as f:
                for line in lines:
                    if self.links[selected_index[0]][0] not in line:
                        f.write(line)

    def update_link_listbox(self):
        self.link_listbox.delete(0, tk.END)
        for link, label in self.links:
            self.link_listbox.insert(tk.END, f"{link} ({label})")

    def load_links(self):
        with open("index.html", "r") as f:
            content = f.read()
        div_start = '<div class="links__item twitch_link">'
        div_end = '</div>'
        start_index = content.find(div_start)
        while start_index != -1:
            start_index += len(div_start)
            end_index = content.find(div_end, start_index)
            link_start_index = content.find('href="', start_index) + len('href="')
            link_end_index = content.find('"', link_start_index)
            label_start_index = content.find('>', link_end_index) + 1
            label_end_index = content.find('<', label_start_index)
            link = content[link_start_index:link_end_index]
            label = content[label_start_index:label_end_index]
            self.links.append((link, label))
            start_index = content.find(div_start, end_index)
        self.update_link_listbox()

    def save_changes(self):
        print("Logo Image:", self.logo_path.get())
        print("Background Image:", self.bg_path.get())
        print("Links:", self.links)

    def show_help(self):
        help_popup = tk.Toplevel(self.master)
        help_popup.title("Help")
        help_text = """
        Welcome to Website Editor!

        To use the software:
        1. Select Logo Image and Background Image by clicking on the 'Browse' buttons.
        2. Add/Edit/Delete Links using the respective buttons and entry fields.
        3. Click 'Save Changes' to save your modifications.

        Enjoy editing your website!
        """
        help_label = ttk.Label(help_popup, text=help_text, style='Custom.TLabel', wraplength=400, justify='left')
        help_label.pack(padx=20, pady=10)

    def svg_to_image(self, svg_code, size):
        img = tk.Canvas(self.master, width=size[0], height=size[1])
        img.create_text(size[0] // 2, size[1] // 2, text=svg_code)
        img_data = tk.PhotoImage(master=img, width=size[0], height=size[1])
        img.image = img_data
        return img_data

def main():
    root = tk.Tk()
    editor = WebsiteEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
