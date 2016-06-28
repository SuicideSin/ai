
import sys, math, random, time
import matplotlib.pyplot as plt

class graph:
    def __init__(self, numVertices, numEdges):
        self.numVertices = numVertices
        self.numEdges = numEdges
        self.network = []
        self.Pk = {}
        self.diameter = 0

    #CALCULATING P(k)
    def calcPk(self):
        for edges in self.network:
            degree = len(edges)
            if degree in self.Pk:
                self.Pk[degree] += 1
            else:
                self.Pk[degree] = 1
        return self.Pk

    #FINDING MAX P(k)
    def maxPk(self):
        return max(self.Pk.keys())

    #FINDING DIAMETER - COPIED OVER FROM WORDLADDER LAB BFS
    def calcDiameter(self):
        print("\tCalculating Diameter...")
        highestLevel = 0
        discoveredWords = set()
        for key in range(len(self.network)):
            sys.stdout.write("\t\tVertices Checked: {}/{}".format(key+1,self.numVertices) + "\r")
            sys.stdout.flush()
            if(key not in discoveredWords):
                start = key
                level = {start: 0}
                parent = {start: None}
                i = 1
                queue = [start]
                lastWord = start
                while (len(queue) != 0):
                    nextLevel = []
                    for parentVertex in queue:
                        for vert in self.network[parentVertex]:
                            if vert not in level:
                                level[vert] = i
                                parent[vert] = parentVertex
                                nextLevel.append(vert)
                                lastWord = vert
                    queue = nextLevel
                    i += 1
                discoveredWords.add(key)
                discoveredWords.add(lastWord)
            if i > highestLevel:
                highestLevel = i
        self.diameter = highestLevel
        sys.stdout.write("\n\tDone\n")
        return highestLevel


#Erdős-Rényi
class graphER(graph):
    def __init__(self, numVertices, numEdges):
        self.numVertices = numVertices
        self.numEdges = numEdges
        self.network = [set() for i in range(numVertices)]
        self.Pk = {}
        self.diameter = 0
        
    #CREATING THE NETWORK
    def createNetwork(self):
        print("\tCreating Network...")
        for i in range (self.numEdges):
            while True:
                v1 = random.randint(0, self.numVertices-1)
                v2 = random.randint(0, self.numVertices-1)
                if v2 not in self.network[v1] and (v1 != v2):
                    self.network[v1].add(v2)
                    self.network[v2].add(v1)
                    break
            sys.stdout.write("\t\tEdges: {}/{}".format(i+1, self.numEdges) + "\r")
            sys.stdout.flush()
        sys.stdout.write("\n\tDone\n")
        return self.network


#Barabási-Albert
class graphBA(graph):
    def __init__(self, initM, numEdges):
        self.numVertices = initM
        self.initM = initM
        self.numEdges = numEdges
        self.network = [set(k for k in range(initM) if k != i) for i in range(initM)]
        self.Pk = {}
        self.diameter = 0

    #COUNT THE NUMBER OF EDGES IN THE CURRENT NETWORK
    def countEdges(self):
        numEdges = 0
        for edges in self.network:
            numEdges += len(edges)
        return int(numEdges/2)

    #CREATING THE NETWORK
    def createNetwork(self):
        print("\tCreating Network...")
        #COUNT NUMBER OF EDGES IN THE INITIAL
        totEdges = self.countEdges()
        #INTRODUCE NEW VERTICES UNTIL GRAPH HAS THE SAME NUMBER OF EDGES AS Erdős-Rényi
        while totEdges < self.numEdges:
            v1 = self.numVertices
            self.network.append(set())
            self.numVertices += 1
            edgesAdded = 0
            #M < M_0
            for v2 in range (len(self.network)-1):
                current = self.network[v2]
                chance = len(current)/totEdges
                if random.random() <= chance and (v2 not in self.network[v1]):
                    self.network[v1].add(v2)
                    self.network[v2].add(v1)
                    edgesAdded += 1
                    totEdges += 1
                    sys.stdout.write("\t\tEdges: {}/{}".format(totEdges,self.numEdges) + "\r")
                    sys.stdout.flush()
                if edgesAdded > self.initM or totEdges >= self.numEdges:
                    break
        sys.stdout.write("\n\tDone\n")
        return self.network
    

#GRAPHING THE DATA
def graphPk(ER_PkData, BA_PkData):
    #Erdős-Rényi
    xAxisER = list(ER_PkData.keys())
    yAxisER = [ER_PkData[k] for k in xAxisER]

    plt.figure(1)
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.title('Erdos-Renyi')
    plt.scatter(xAxisER, yAxisER)

    #Barabási-Albert
    xAxisBA = [i for i in BA_PkData.keys() if i < 300]
    print(xAxisBA)
    yAxisBA = [BA_PkData[i] for i in xAxisBA]
    print(yAxisBA)

    plt.figure(2)
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.title('Barabasi-Albert')
    plt.scatter(xAxisBA, yAxisBA)

    plt.show()

def main():
    #Erdős-Rényi
    print("Creating Erdos-Renyi Graph...")
    er = graphER(10000, 50000)
    er.createNetwork()
    er.calcPk()
    #CALCULATING DIAMETER
    # er.calcDiameter()

    #Barabási-Albert
    print("\nCreating Barabasi-Albert Graph...")
    ba = graphBA(200, 50000)
    ba.createNetwork()
    ba.calcPk()
    #CALCULATING DIAMETER
    # ba.calcDiameter()

    #DISPLAY RESULTS
    print("\nErdos-Renyi")
    print("  Number of Vertices: {}".format(er.numVertices))
    print("  Number of Edges: {}".format(er.numEdges))
    print("  Highest Vertex Degree: {}".format(er.maxPk()))
    # print("  Diameter: {}".format(er.diameter))
    print("\nBarabasi-Albert")
    print("  Number of Vertices: {}".format(ba.numVertices))
    print("  Number of Edges: {}".format(ba.numEdges))
    print("  Highest Vertex Degree: {}".format(ba.maxPk()))
    # print("  Diameter: {}".format(ba.diameter))
    graphPk(er.Pk, ba.Pk)
main()