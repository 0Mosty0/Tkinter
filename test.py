import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

class NetworkElement:
    def __init__(self, canvas, element_type, x, y, name, image_path):
        self.canvas = canvas
        self.element_type = element_type
        self.name = name
        self.image = self.load_png_image(image_path)
        self.image_item = self.canvas.create_image(x, y, anchor=tk.NW, image=self.image, tags=(element_type, "Element"))
        self.name_item = self.canvas.create_text(x, y, text=name, anchor=tk.SW, tags=(element_type, "ElementName"))

    def load_png_image(self, path):
        image = Image.open(path)
        return ImageTk.PhotoImage(image)

class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Architecture Designer")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.elements = []

        # Dictionary to store PhotoImage objects
        self.images = {}

        self.create_menu()
        self.canvas.bind("<Button-3>", self.show_properties_menu)

        # Variables pour le déplacement
        self.selected_item = None
        self.start_x = 0
        self.start_y = 0

        # Variables pour la liaison
        self.selected_elements = []

        # Liaison des événements de souris pour le déplacement
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Compteur pour le suivi des noms
        self.counter = {'Client': 1, 'Switch': 1, 'Routeur': 1}

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        item_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Add Item", menu=item_menu)
        item_menu.add_command(label="Add Client", command=lambda: self.add_element("Client"))
        item_menu.add_command(label="Add Switch", command=lambda: self.add_element("Switch"))
        item_menu.add_command(label="Add Router", command=lambda: self.add_element("Routeur"))

        link_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Draw Link", menu=link_menu)
        link_menu.add_command(label="Draw Link", command=self.draw_link)

    def add_element(self, element_type):
        x, y = self.get_random_position()

        # Load the image if not loaded yet
        if element_type not in self.images:
            self.images[element_type] = f"{element_type.lower()}.png"

        # Generate a unique name based on the element type
        name = f"{element_type}{self.counter[element_type]}"
        self.counter[element_type] += 1

        # Create a NetworkElement instance
        element = NetworkElement(self.canvas, element_type, x, y, name, self.images[element_type])
        self.elements.append(element)

    def get_random_position(self):
        return 50, 50  # You can implement a more sophisticated logic to get random positions.

    def draw_link(self):
        if len(self.selected_elements) == 2:
            element1, element2 = self.selected_elements
            x1, y1 = self.canvas.coords(element1.image_item)
            x2, y2 = self.canvas.coords(element2.image_item)
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

            # Clear the selection
            self.selected_elements = []

    def show_properties_menu(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        element_type = tags[0]

        if "Element" in tags:
            self.show_element_properties(item, element_type)

    def show_element_properties(self, item, element_type):
        # Currently, only the name is editable
        new_name = simpledialog.askstring("Properties", "Enter name:")

        # Update the name of the NetworkElement instance
        for element in self.elements:
            if element.element_type == element_type and (element.image_item == item or element.name_item == item):
                element.name = new_name
                self.canvas.itemconfig(element.name_item, text=new_name)

    def on_left_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        if "Element" in tags:
            if len(self.selected_elements) < 2:
                self.selected_elements.append(item)

            self.selected_item = item
            self.start_x = event.x
            self.start_y = event.y

    def on_drag(self, event):
        if self.selected_item is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.selected_item, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def on_release(self, event):
        self.selected_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()
