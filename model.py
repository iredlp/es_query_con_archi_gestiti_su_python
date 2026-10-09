import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def creaGrafo(self, city, anno):
        self._graph.clear()
        self._idMap.clear()

        # PASSO 1: Aggiungere TUTTI i nodi (anche quelli isolati)
        clienti = DAO.getAllNodes(city)
        for c in clienti:
            self._idMap[c.customer_id] = c
            self._graph.add_node(c)

        # PASSO 2: Ottenere i dati aggregati (chi ha fatto ordini)
        # spesa_map è un dizionario: {customer_id: spesa}
        spesa_map = DAO.getSpesaClienti(city, anno)

        # PASSO 3: Filtrare i nodi idonei a creare archi
        # Prendiamo solo chi ha ordini registrati ed è presente tra i nodi
        candidati = [c_id for c_id in spesa_map.keys() if c_id in self._idMap]

        # PASSO 4: Doppio ciclo per confrontare le coppie (una sola volta: i + 1)
        for i in range(len(candidati)):
            for j in range(i + 1, len(candidati)):
                id1 = candidati[i]
                id2 = candidati[j]

                c1 = self._idMap[id1]
                c2 = self._idMap[id2]

                s1 = spesa_map[id1]
                s2 = spesa_map[id2]

                # Calcolo del peso secondo la traccia
                peso = abs(s1 - s2)

                # Regole di orientamento archi
                if s1 < s2:
                    # Da chi ha speso meno a chi ha speso di più
                    self._graph.add_edge(c1, c2, weight=peso)
                elif s1 > s2:
                    self._graph.add_edge(c2, c1, weight=peso)
                else:
                    # Parità: arco bidirezionale
                    self._graph.add_edge(c1, c2, weight=peso)
                    self._graph.add_edge(c2, c1, weight=peso)

