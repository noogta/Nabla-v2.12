import matplotlib.pyplot as plt

color = {
    "": "black",
    "Acier": "brown", 
    "Anomalie franche": "red",
    "Anomalie hétérogène": "orange",
    "Réseaux": "blue", 
    "Autres": "purple"
}

class Point:
    def __init__(self, label: str, x: float, y: float):
        self.label = label
        self.x = x
        self.y = y
        self.create_point()
    
    def create_point(self):
        if(self.label == ""):
            self.point = plt.Circle((self.x, self.y), radius=0.075, color='black', alpha = 1)
        else:
            if(self.label in color):
                self.point = plt.Circle((self.x, self.y), radius=0.075, color=color[self.label], alpha = 1)

    def update_point(self, x: float, y: float):
        # Mise à jour des coordonnées
        self.x = x
        self.y = y
        self.point.center = (self.x, self.y)

    def plot(self, axes):
        axes.add_patch(self.point)

class Points:
    def __init__(self):
        self.points = []

    def add(self, point: Point):
        self.points.append(point)

    def clear(self, point: Point):
        if(point in self.points):   
            self.points.remove(point)
            point.point.remove()

    def clear_all(self):
        for point in self.points:
            point.point.remove()
        self.points.clear()

class Rectangle:
    def __init__(self, label: str, x1: float, y1: float, x2: float, y2: float):
        self.label = label
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.create_rectangle()
    
    def create_rectangle(self):
        if(self.label == ""):
            self.rectangle = plt.Rectangle((self.x1, self.y1), self.x2, self.y2, edgecolor="black", fill=False)
        else:
            if(self.label in color):
                self.rectangle = plt.Rectangle((self.x1, self.y1), self.x2, self.y2, edgecolor=color[self.label], fill=False)

    def update_rectangle(self, x2: float, y2: float):
        self.x2 = x2
        self.y2 = y2

        x_min = min(self.x1, self.x2)
        y_min = min(self.y1, self.y2)
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)

        """
        self.rectangle.set_width(width)
        self.rectangle.set_height(height)
        self.rectangle.set_xy((x_min, y_min))
        """
        if(self.label == ""):
            self.rectangle = plt.Rectangle((x_min, y_min), width, height, edgecolor="black", fill=False)
        else:
            if(self.label in color):
                self.rectangle = plt.Rectangle((x_min, y_min), width, height, edgecolor=color[self.label], fill=False)

    def get_ord_data(self):
        if(self.x1 > self.x2):
            x1 = self.x2
            x2 = self.x1
        else:
            x1 = self.x1
            x2 = self.x2
        if(self.y1 > self.y2):
            y1 = self.y2
            y2 = self.y1
        else:
            y1 = self.y1
            y2 = self.y2
        return x1, y1, x2, y2

    def temporay_plot(self, axes):
        axes.draw_artist(self.rectangle)

    def plot(self, axes):
        axes.add_patch(self.rectangle)

    def clear(self):
        self.rectangle.remove()

class Rectangles:
    def __init__(self):
        self.rectangles = []

    def add(self, rectangle: Rectangle):
        self.rectangles.append(rectangle)

    def clear(self,rectangle: Rectangle):
        if(rectangle in self.rectangles):   
            rectangle.rectangle.remove()
            self.rectangles.remove(rectangle)

    def clear_all(self):
        for rectangle in self.rectangles:
            rectangle.rectangle.remove()
        self.rectangles.clear()