from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.core.window import Window

class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)
        self.line_color = (0, 0, 0, 1)
        self.line_width = 2

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.line_color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def clear_canvas(self):
        self.canvas.clear()

    def set_line_color(self, color):
        self.line_color = color

    def set_line_width(self, width):
        self.line_width = width

class PaintApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        self.paint_widget = PaintWidget()
        
        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        clear_button = Button(text='Очистить холст')
        clear_button.bind(on_press=self.clear_canvas)
        button_layout.add_widget(clear_button)
        
        color_button = Button(text='Выбор цвета')
        color_button.bind(on_press=self.show_color_picker)
        button_layout.add_widget(color_button)
        
        width_button = Button(text='Толщина линии')
        width_button.bind(on_press=self.show_width_slider)
        button_layout.add_widget(width_button)
        
        root.add_widget(self.paint_widget)
        root.add_widget(button_layout)
        
        return root

    def clear_canvas(self, instance):
        self.paint_widget.clear_canvas()

    def show_color_picker(self, instance):
        color_picker = ColorPicker()
        popup = Popup(title='Выбор цвета', content=color_picker, size_hint=(0.8, 0.8))
        
        def on_color(instance, value):
            self.paint_widget.set_line_color(value)
            popup.dismiss()
        
        color_picker.bind(color=on_color)
        popup.open()

    def show_width_slider(self, instance):
        slider = Slider(min=1, max=10, value=self.paint_widget.line_width)
        popup = Popup(title='Толщина линии', content=slider, size_hint=(0.8, 0.2))
        
        def on_value(instance, value):
            self.paint_widget.set_line_width(value)
            popup.dismiss()
        
        slider.bind(value=on_value)
        popup.open()

if __name__ == '__main__':
    PaintApp().run()