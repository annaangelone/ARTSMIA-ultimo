import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._ruoli = DAO.getRoles()
        self._grafo = nx.Graph()
        self._idMap = {}
        self._artists = []

        self._bestPath = []
        self._bestObj = 0
        self._nMostre = 0


    def buildGraph(self, role):
        self._grafo.clear()

        self._artists = DAO.getArtists(role)

        for a in self._artists:
            self._idMap[a.artist_id] = a

        self._grafo.add_nodes_from(self._artists)

        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    peso = DAO.getPeso(u.artist_id, v.artist_id)
                    if peso:
                        self._grafo.add_edge(u, v, weight=peso[0])

    def getConnessi(self):

        listaConnessi = []

        for (u, v) in self._grafo.edges:
            listaConnessi.append(((u, v), self._grafo[u][v]["weight"]))

        listaConnessi.sort(key=lambda x:x[1], reverse=True)

        return listaConnessi


    def getPercorso(self, artID):
        self._bestPath = []
        self._bestObj = 0
        self._nMostre = 0

        artista = self._idMap[artID]

        for v in self._grafo.neighbors(artista):
            parziale = [artista]
            parziale.append(v)
            peso = self._grafo[artista][v]["weight"]
            self._ricorsione(parziale, peso)

        return self._bestPath, self._bestObj, self._nMostre


    def _ricorsione(self, parziale, peso):
        if len(parziale) > self._bestObj:
            self._bestObj = len(parziale)
            self._bestPath = copy.deepcopy(parziale)
            self._nMostre = peso

        for v in self._grafo.neighbors(parziale[-1]):
            if self.getPeso(parziale[-1], v) == peso and v not in parziale and v!=parziale[0]:
                parziale.append(v)
                self._ricorsione(parziale, peso)
                parziale.pop()





    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getPeso(self, n1, n2):
        return self._grafo[n1][n2]["weight"]

    def getArtista(self, artID):
        return self._idMap[artID]

    def verificaID(self, artID):
        if artID in self._idMap.keys():
            return True

        return False
