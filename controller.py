import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        ruolo = self._view._ddRuolo.value

        if ruolo is None:
            self._view.create_alert("No role selected, please select a role")
            return

        self._model.buildGraph(ruolo)

        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodes()}"
                                                      f" nodi e {self._model.getNumEdges()} archi"))

        self._view._btnCompConnessa.disabled = False
        self._view._btnCercaPercorso.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        connessi = self._model.getConnessi()

        for c in connessi:
            self._view.txt_result.controls.append(ft.Text(f"{c[0][0]} <--> {c[0][1]}, peso={c[1]}"))

        self._view.update_page()


    def handleCercaPercorso(self, e):
        artista = self._view._txtIdArtista.value

        try:
            artID = int(artista)

        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Please insert an integer number of artist id"))
            self._view.update_page()
            return

        if not self._model.verificaID(artID):
            self._view.create_alert("Insert a correct artist id")
            self._view.update_page()
            return

        path, lun, nMostre = self._model.getPercorso(artID)

        a = self._model.getArtista(artID)

        self._view.txt_result.controls.append(ft.Text(f"Percorso trovato per {a} di lunghezza massima pari a {lun}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di mostre={nMostre}"))

        for i in range(len(path)-1):
            peso = self._model.getPeso(path[i], path[i+1])
            self._view.txt_result.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}, peso={peso}"))

        self._view.update_page()


    def fillDD(self):
        ruoli = self._model._ruoli

        for r in ruoli:
            self._view._ddRuolo.options.append(ft.dropdown.Option(r))

        self._view.update_page()
