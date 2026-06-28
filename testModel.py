from model.model import Model

mm = Model()
generi = mm.getAllGeneri()
mm._buildGraph(generi[0])
print(mm.getNumNodes())
print(mm.getNumEdges())
for e in mm._grafo.edges(data=True):
    print(f"{e[0]}->{e[1]} - {e[2]["weight"]}")

