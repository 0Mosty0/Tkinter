import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk  # Ajout de l'import pour Pillow

class NetworkElement:
    def __init__(self, canvas, x, y, element_type, image_path, text):
        self.canvas = canvas
        self.element_type = element_type

        self.frame = tk.Frame(canvas, bd=1, relief=tk.RAISED)
        self.icon = self.load_and_resize_image(image_path)
        self.text = tk.Label(self.frame, text=text)

        self.frame.bind("<Button-1>", self.on_click)
        self.frame.bind("<B1-Motion>", self.on_drag)
        self.frame.bind("<ButtonRelease-1>", self.on_release)

        self.set_position(x, y)

    def load_and_resize_image(self, image_path):
        original_image = Image.open(image_path)
        resized_image = original_image.resize((50, 50), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    def initialize_ports(self):
        if self.element_type == "Client":
            return [self.create_port()]
        elif self.element_type == "Switch" or self.element_type == "Router":
            return [self.create_port(), self.create_port(), self.create_port(), self.create_port()]

    def create_port(self):
        return {"x": 0, "y": 0}  # You can initialize the port position as needed

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.frame.place(x=x, y=y, anchor=tk.CENTER)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        deltax = event.x - self.start_x
        deltay = event.y - self.start_y
        self.set_position(self.x + deltax, self.y + deltay)

    def on_release(self, event):
        pass

    def on_right_click(self, event):
        properties = {"Name": self.text.cget("text"), "Icon": self.element_type}
        updated_properties = simpledialog.askstring("Modify Properties", "Enter new values:", initialvalue=properties)
        if updated_properties:
            self.update_properties(updated_properties)

    def update_properties(self, properties):
        # Update the properties of the element based on user input
        name = properties.split(',')[0].split(':')[1].strip()  # Extracting the name from user input
        icon = properties.split(',')[1].split(':')[1].strip()  # Extracting the icon from user input
        self.text.config(text=name)
        # Update other properties as needed


class NetworkDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Designer")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.elements = []

        self.client_image = tk.PhotoImage(file="PC.png").subsample(3, 3)
        self.switch_image = tk.PhotoImage(file="switch.png").subsample(3, 3)
        self.router_image = tk.PhotoImage(file="routeur.png").subsample(3, 3)

        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(toolbar, text="Client", command=lambda: self.add_element("Client")).pack(pady=5)
        tk.Button(toolbar, text="Switch", command=lambda: self.add_element("Switch")).pack(pady=5)
        tk.Button(toolbar, text="Router", command=lambda: self.add_element("Router")).pack(pady=5)

        self.canvas.bind("<Button-1>", self.handle_left_click)

        self.current_element = None
        self.current_port = None
        self.draw_line_start = None

    def handle_left_click(self, event):
        clicked_item = self.canvas.find_withtag(tk.CURRENT)
        if clicked_item:
            item_tags = self.canvas.gettags(clicked_item)
            if "network_element" in item_tags:
                element_id = item_tags["network_element"]
                element = next((elem for elem in self.elements if elem.frame == element_id), None)
                if element:
                    self.set_current_element(element)

    def draw_line(self, event):
        if self.current_element and self.current_port:
            self.canvas.delete("temp_line")
            self.canvas.create_line(self.current_port["x"], self.current_port["y"], event.x, event.y, tags="temp_line")

    def add_element(self, element_type):
        x, y = 100, 100  # Position initiale
        if element_type == "Client":
            image = self.client_image
        elif element_type == "Switch":
            image = self.switch_image
        elif element_type == "Router":
            image = self.router_image

        element = NetworkElement(self.canvas, x, y, element_type, image, element_type)
        self.elements.append(element)
        self.current_element = element
        self.current_port = element.ports[0]

    def set_current_element(self, element):
        self.current_element = element
        self.current_port = element.ports[0]

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkDesigner(root)
    root.mainloop()
