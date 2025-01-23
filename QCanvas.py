import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Forms import Point, Points, Rectangle, Rectangles
from RadarData import cste_global
from math import sqrt
from Export import ExJsonRectangle, ExJsonPoint, ExJsonNone

CURSOR_DEFAULT = Qt.CursorShape.ArrowCursor
CURSOR_POINT = Qt.CursorShape.PointingHandCursor
CURSOR_DRAW = Qt.CursorShape.CrossCursor
CURSOR_MOVE = Qt.CursorShape.ClosedHandCursor
CURSOR_GRAB = Qt.CursorShape.OpenHandCursor

#Ajouter les lignes

class Canvas:
    def __init__(self, figure: Figure, axes, parent, scope_axes=None, scopeFigure:Figure = None):
        self.canvas = FigureCanvas(figure)
        self.canvasScope = FigureCanvas(scopeFigure)
        self.canvas.setStyleSheet("background-color: transparent;")
        self.axes = axes
        self.parent = parent
        self.axes_scope = scope_axes
        self.Pointer = Pointer(None, None, self.parent)
        self.Point = None
        self.Rectangle = None

        self.Points = Points()
        self.Rectangles = Rectangles()
        self.shapes = []

        self._cursor = CURSOR_DRAW

        self.mode = "Pointer"
        self._prec = None

        self.canvas.mpl_connect('button_press_event', self.MousePressEvent)
        self.canvas.mpl_connect('motion_notify_event', self.MouseMoveEvent)
        self.canvas.mpl_connect('button_release_event', self.MouseReleaseEvent)

    def getYPointeur(self):
        return self.Pointer.y
    

    def getXPointeur(self):
        return self.Pointer.x
    
    def set_mode(self, mode: str, button):
        """
        Méthode qui permet de définir le mode de la classe.
        """
        if(self._prec == button):
            button.setStyleSheet("")
            self.mode = "Pointer"
            self._prec = None
        else:
            if(self._prec != None):
                self._prec.setStyleSheet("")
            button.setStyleSheet("""     
            QPushButton:active {
                background-color: #45a049;}""")
            self.mode = mode
            self._prec = button

    def MousePressEvent(self, event):
        if event.button == 1:
            x = event.xdata
            y = event.ydata
            # Vérifier si les coordonnées sont valides
            if x is not None and y is not None:
                if(self.mode == "Pointer"):
                    self.Pointer.set(x, y)
                    #self.parent.pt.setText(str(int(y)))
                    self.parent.plot_scope()
                    self.Pointer.plot(self.axes,self.axes_scope)
                    self.canvas.draw()
                    #self.canvasScope.draw()
                    
                else:
                    if(self.mode == "Rectangle"):
                        # Sauvegarder le fond de la toile pour utiliser blit
                        #self.background = self.canvas.copy_from_bbox(self.axes.bbox)
                        # Dessiner le Rectangle temporaire
                        self.Rectangle = Rectangle(self.parent.class_choice.currentText(), x, y, 0., 0.)
                        self.Rectangle.plot(self.axes)
        else:
            if(event.button == 3):
                print("test")

    def MouseMoveEvent(self, event):
        if(self.mode == "Rectangle"):
            if(event.button == 1):
                # Récupérer les coordonnées de la souris pendant le glissement
                x2 = event.xdata
                y2 = event.ydata

                # Vérifier si les coordonnées sont valides
                if x2 is not None and y2 is not None:
                    # Mettre à jour les propriétés du Rectangle temporaire
                    self.Rectangle.update_rectangle(x2, y2)

                    # Utiliser blit pour mettre à jour seulement le Rectangle
                    #self.canvas.restore_region(self.background)
                    self.Rectangle.temporay_plot(self.axes)
                    #self.canvas.blit(self.axes.bbox)

    def MouseReleaseEvent(self, event):
        if(self.mode == "Point"):
            if(event.button == 1):
                # Récupérer les coordonnées du relâchement de la souris
                x = event.xdata
                y = event.ydata
                # Vérifier si les coordonnées sont valides
                if(x is not None and y is not None):
                    self.Point = Point(self.parent.class_choice.currentText(), x, y)
                    self.Points.add(self.Point)
                    self.shapes.append(self.Point)
                    self.parent.shape_list.addItem(str(self.Point.label)+"(Point,"+str(round(x,2))+","+str(round(y,2))+")")

                    self.Point.plot(self.axes)

                    self.canvas.draw()
        else:
            if(self.mode == "Rectangle"):
                if(event.button == 1):
                    # Récupérer les coordonnées du relâchement de la souris
                    x = event.xdata
                    y = event.ydata

                    # Vérifier si les coordonnées sont valides
                    if(x is not None and y is not None):
                        # Dessiner le Rectangle final
                        self.Rectangle.update_rectangle(x, y)
                        if(self.Rectangle.x1 != self.Rectangle.x2 and self.Rectangle.y1 != self.Rectangle.y2):
                            self.Rectangle.plot(self.axes)
                            self.Rectangles.add(self.Rectangle)
                            self.shapes.append(self.Rectangle)

                            x1, y1, x2, y2 = self.Rectangle.get_ord_data()
                            self.parent.shape_list.addItem(str(self.Rectangle.label)+"(Rectangle,"+str(round(x1,2))+","+str(round(y1,2))+","+str(round(x2,2))+","+str(round(y2,2))+")")

                        self.canvas.draw()

    def reset_axes(self, axes, parent):
        # Réinitialisation de l'axe
        self.axes = axes
        
        self.Pointer = Pointer(None, None, parent)
        self.Point = None
        self.Rectangle = None

        self.Points = Points()
        self.Rectangles = Rectangles()
        self.shapes.clear()

    def clear_pointer(self):
        self.Pointer.clear(self.axes)
        self.canvas.draw()

    def clear_point(self, index):
        point = self.shapes[index]
        if point in self.Points.points:
            self.parent.shape_list.takeItem(index)
            self.shapes.remove(point)
            self.Points.clear(point)
            self.canvas.draw()

    def clear_points(self):
        for point in self.Points.points:
            index = self.shapes.index(point)
            self.parent.shape_list.takeItem(index)
            self.shapes.remove(point)
        self.Points.clear_all()
        self.canvas.draw()

    def clear_rectangle(self, index):
        rectangle = self.shapes[index]
        if rectangle in self.Rectangles.rectangles:
            self.parent.shape_list.takeItem(index)
            self.shapes.remove(rectangle)
            self.Rectangles.clear(rectangle)
            self.canvas.draw()

    def clear_rectangles(self):
        for rectangle in self.Rectangles.rectangles:
            index = self.shapes.index(rectangle)
            self.parent.shape_list.takeItem(index)
            self.shapes.remove(rectangle)
        self.Rectangles.clear_all()
        self.canvas.draw()

    def clear_canvas(self):
        self.clear_pointer()
        self.clear_points()
        self.clear_rectangles()
        
        self.canvas.draw()

    def del_ele_list(self):
        #print("Avant suppression:")
        #self.test_list()
        selected_item = self.parent.shape_list.currentItem()  # Récupère l'élément sélectionné
        if selected_item:
            text = selected_item.text()  # Récupère le texte de l'élément
            index = self.parent.shape_list.row(selected_item)  # Récupère l'index de l'élément

            if "Point" in text:
                self.clear_point(index)
            elif "Rectangle" in text:
                self.clear_rectangle(index)
        #print("Après Suppression:")
        #self.test_list()

    def export_json(self): #A débug ? 
        n_tr = self.parent.feature[0]
        n_samp = self.parent.feature[1]
        if(self.parent.def_value != None):
            d_max = self.parent.def_value
        else:
            d_max = self.parent.feature[2]
        t_max = self.parent.feature[3]
        p_max = (t_max * 10.**(-9)) * (cste_global["c_lum"] / sqrt(self.parent.epsilon)) / 2
        step_time = self.parent.feature[5]

        L_xmax = [d_max, step_time*n_tr, n_tr]
        L_ymax = [p_max, t_max, n_samp]

        xindex = self.parent.Xunit.index(self.parent.abs_unit.currentText())
        yindex = self.parent.Yunit.index(self.parent.ord_unit.currentText())

        if(self.parent.cb_value != 0 and self.parent.ce_value == None):
            #print(f"Avant:{L_ymax[yindex]}")
            L_ymax[yindex] = L_ymax[yindex] - (self.parent.cb_value / n_samp) * L_ymax[yindex]
            #print(f"Après:{L_ymax[yindex]}")

        else:
            if(self.parent.cb_value != 0 and self.parent.ce_value != None):
                #print(f"Avant:{L_ymax[yindex]}")
                L_ymax[yindex] = L_ymax[yindex] * (self.parent.ce_value - self.parent.cb_value) / n_samp
                #print(f"Après:{L_ymax[yindex]}")
            else:
                if(self.parent.cb_value == 0 and self.parent.ce_value != None):
                    #print(f"Avant:{L_ymax[yindex]}")
                    L_ymax[yindex] = (self.parent.ce_value / n_samp) * L_ymax[yindex]
                    #print(f"Après:{L_ymax[yindex]}")
        if(len(self.shapes) != 0):
            for shape in self.shapes:
                if isinstance(shape,Rectangle):
                    x1, y1, x2, y2 = shape.get_ord_data()
                    x1, x2 = x1 / L_xmax[xindex], x2 / L_xmax[xindex]
                    y1, y2 = y1 / L_ymax[yindex], y2 / L_ymax[yindex]
                    ExJsonRectangle(self.parent.img_modified, self.parent.selected_file[:-4], shape.label, x1, y1, x2, y2)
                else:
                    if(isinstance(shape, Point)):
                        x, y = shape.x,shape.y
                        x = x / L_xmax[xindex]
                        y = y / L_ymax[yindex]
                        ExJsonPoint(self.parent.img_modified, self.parent.selected_file[:-4], shape.label, shape.x, shape.y)
            self.clear_canvas()
        else:
            ExJsonNone(self.parent.img_modified, self.parent.selected_file[:-4])

    def test_list(self):
        print(f"Taille de la liste QListWidget: {self.parent.shape_list.count()}")
        print(f"Taille de shapes: {len(self.shapes)}")
        print(f"Taille des Points: {len(self.Points.points)}")
        print(f"Taille de Rectangles: {len(self.Rectangles.rectangles)}")
        print(self.parent.abs_unit.currentText())
        print(self.parent.feature)
 
class Pointer: #------> Pointeur 
    def __init__(self, x: None | float, y: None | float, parent):
        self.x = x
        self.y = y
        self.parent = parent

        self.vline = None
        self.hline = None
        self.hlineS = None

    def set(self, x: float, y: float):
        self.x = x
        self.y = y

    def plot(self, axes, axes_scope=None ): 
        xindex = self.parent.Xunit.index(self.parent.abs_unit.currentText())
        yindex = self.parent.Yunit.index(self.parent.ord_unit.currentText())
        self.parent.xpointer_label.setText("{:.2f} {}".format(self.x, self.parent.xLabel[xindex]))
        self.parent.ypointer_label.setText("{:.2f} {}".format(self.y, self.parent.yLabel[yindex]))

        if(self.vline != None and self.hline != None): #Delete si déjà existant
            axes.lines[0].remove()
            axes.lines[0].remove()
            
        #if(self.hlineS != None):
            #axes_scope.line[0].remove()

        #self.vline = axes.plot([self.x, self.x], [0, self.y + 0.15], color='green', linewidth=0.5)
        self.vline = axes.axvline(self.x, color='red', linewidth=1)
        #self.hline = axes.plot([0, self.x + 0.15], [self.y, self.y], color='green', linewidth=0.5)
        self.hline = axes.axhline(self.y, color='red', linewidth=1)
        if(axes_scope != None):
            #self.hlineS = axes_scope.axhline(self.y, color='red', linewidth=10)
            self.hlineS = axes_scope.axhline(0.2, color='red', linewidth=10)

    def clear(self, _axes):
        if(self != None):
            if(self.vline != None and self.hline != None):
                _axes.lines[0].remove()
                _axes.lines[0].remove()
                self.vline = None
                self.hline = None
            self.parent.xpointer_label.setText("")
            self.parent.ypointer_label.setText("")
    