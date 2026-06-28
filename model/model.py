import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo= nx.DiGraph()
        self._idMapArtisti = {}
        self._bestPath = []
        self._bestLunghezza = 0


    def getBestPath(self, source):
        self._bestPath = []
        parziale=[source]
        pop = self.idMapPopolarita[source.ArtistId]
        self._ricorsione(parziale,pop)
        return self._bestPath

    def _ricorsione(self, parziale, pop):
        ultimo= parziale[-1]

        successori = list(self._grafo.successors(ultimo))
        if len(successori)==0:
            if len(parziale)> self._bestLunghezza:
                self._bestLunghezza=len(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        for s in successori:
            popi = pop +self.idMapPopolarita[s.ArtistId]
            if s not in parziale and popi>pop:
                parziale.append(s)
                self._ricorsione(parziale,popi)
                parziale.pop()

        pass



    def getAllGeneri(self):
        generi = DAO.getAllGeneri()
        return generi
    def getAllArtisti(self):
        artisti = self._grafo.nodes
        return artisti
    def getAllPop(self, genere):
        popi = DAO.getAllPopolarita(genere)
        return popi
    def getTop5(self):
        archi = self._grafo.edges
        return sorted(archi(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]
    def getArtistaInfluente(self):
        maxInf = max(self._idMappaInfluenza.values())
        for a in self._grafo.nodes:
            if self._idMappaInfluenza[a.ArtistId] == maxInf:
                return a, maxInf

    def _buildGraph(self, genere):
        self._grafo.clear()
        artisti = DAO.getAllArtisti(genere)
        self._grafo.add_nodes_from(artisti)
        for a in artisti:
            self._idMapArtisti[a.ArtistId] = a
        self.idMapPopolarita = DAO.getAllPopolarita(genere)
        self._idMappaInfluenza = {}
        for n in self._grafo.nodes:
            self._idMappaInfluenza[n.ArtistId] = 0
        archi = DAO.getAllArchi(genere, self._idMapArtisti)
        for a in archi:
            a1= a.a1
            a2= a.a2
            pop1 = self.idMapPopolarita[a1.ArtistId]
            pop2 = self.idMapPopolarita[a2.ArtistId]
            peso= pop1 + pop2
            if pop1>pop2:
                self._grafo.add_edge(a1, a2, weight=peso)
                self._idMappaInfluenza[a1.ArtistId] += peso
                self._idMappaInfluenza[a2.ArtistId] -= peso
            elif pop1<pop2:
                self._grafo.add_edge(a2, a1, weight=peso)
                self._idMappaInfluenza[a1.ArtistId] -= peso
                self._idMappaInfluenza[a2.ArtistId] += peso
            else:
                self._grafo.add_edge(a1, a2, weight=peso)
                self._grafo.add_edge(a2, a1, weight=peso)

    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)


