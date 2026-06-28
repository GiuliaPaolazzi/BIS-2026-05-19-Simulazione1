import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenere = None
        self._choiceArtista = None
        self.booleano = False

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        for a in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(data=a,
                                                                  key=a,
                                                                  on_click=self._choiceDDGenere))
    def _choiceDDGenere(self,e):
        self._choiceGenere = e.control.data
        print(f"Il genere selezionato è {self._choiceGenere}")

    def fillDDArtista(self):
        artisti = self._model.getAllArtisti()
        for a in artisti:
            self._view._ddArtist.options.append(ft.dropdown.Option(data=a,
                                                                  key=a,
                                                                  on_click=self._choiceDDArtista))
    def _choiceDDArtista(self,e):
        self._choiceArtista = e.control.data
        print(f"L'artista selezionato è {self._choiceArtista}")
    def handleCreaGrafo(self, e):
        if self._choiceGenere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un genere", color="red"))
            self._view.update_page()

        self._model._buildGraph(self._choiceGenere)
        nN = self._model.getNumNodes()
        nA = self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nN}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi:{nA}"))
        top5 = self._model.getTop5()
        artInfl, inf= self._model.getArtistaInfluente()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {artInfl} con influenza {inf}"))
        self._view.txt_result.controls.append(ft.Text(f"Ecco i 5 archi di peso maggiore:"))
        for t in top5:
            self._view.txt_result.controls.append(ft.Text(f"{t[0]}->{t[1]} - peso: {t[2]["weight"]} "))
        self.fillDDArtista()
        self.booleano = True
        self._view.update_page()


    def handleCammino(self,e):
        if self._choiceArtista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Selezionare un artista", color="red"))
            self._view.update_page()
        if self.booleano==False:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Creare prima il grafo", color="red"))
            self._view.update_page()
            return
        percorso = self._model.getBestPath(self._choiceArtista)
        lun= len(percorso)
        if lun==1:
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato un percorso"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Ecco il percorso di lunghezza {lun} a partire dal nodo {self._choiceArtista}"))
        for p in percorso:
            self._view.txt_result.controls.append(
                ft.Text(f"{p} "))
        self._view.update_page()