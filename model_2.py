import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        # 1. Grafo NON orientato
        self._graph = nx.Graph()
        self._idMap = {}

    def creaGrafo(self, city, anno):
        self._graph.clear()
        self._idMap.clear()

        # PASSO 1: Aggiungere TUTTI i nodi (quelli senza ordini rimarranno isolati)
        clienti = DAO.getAllNodes(city)
        for c in clienti:
            self._idMap[c.customer_id] = c
            self._graph.add_node(c)

        # PASSO 2: Ottenere la mappa dei dati aggregati dal DAO
        spesa_map = DAO.getSpesaClienti(city, anno)

        # PASSO 3: Filtrare gli ID dei nodi che hanno dati e appartengono al grafo
        candidati = [c_id for c_id in spesa_map.keys() if c_id in self._idMap]

        # PASSO 4: Doppio ciclo standard con range(i + 1, len(...))
        for i in range(len(candidati)):
            for j in range(i + 1, len(candidati)):
                id1 = candidati[i]
                id2 = candidati[j]

                c1 = self._idMap[id1]
                c2 = self._idMap[id2]

                s1 = spesa_map[id1]
                s2 = spesa_map[id2]

                # Calcolo del peso richiesto
                peso = s1 + s2

                # Nessuna condizione sul verso: basta aggiungere l'arco una volta sola
                self._graph.add_edge(c1, c2, weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)