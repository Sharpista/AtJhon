import os

import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel

Builder.load_file('style.kv')


class MyLayout(TabbedPanel):
    pass

    def getCaminho(self):
        dir = self.ids['caminho'].text

        if os.path.isdir(dir):
            somador = 0
            lista = os.listdir(dir)
            for i in lista:
                caminho = os.path.join(dir, i)
                if os.path.isfile(caminho):
                    somador = somador + os.stat(caminho).st_size
           
            return self.ids['mybox'].add_widget(
                Label(text=f"Tamanho: {str(somador / 1000)} KB", size_hint=(None,None ), width=100 ))

        else:
            return self.ids['mybox'].add_widget(Label(text=f"O diretório {dir} não existe.", size_hint=(.4, None)))


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MyApp().run()
