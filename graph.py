from enum import Enum
class Color(Enum):
    BLACK = 0
    WHITE = 1

#
graph =  { 'g1': [('g2', 'g10'),[],(100,50)],
    'g2': [('g1', 'g3', 'g5'),[],(350,50)],
    'g3': [('g2', 'g15'),[],(600,50)],
    'g4': [('g5', 'g11'),[],(180,125)],
    'g5': [('g2', 'g4','g6', 'g8'),[],(350,125)],
    'g6': [('g5', 'g14'),[],(525,125)],
    'g7': [('g8', 'g12'),[],(250,200)],
    'g8': [('g5', 'g7', 'g9'),[],(350,200)],
    'g9': [('g8', 'g13'),[],(450,200)],
    'g10': [('g1', 'g11','g22'),[],(100,300)],
    'g11': [('g5', 'g10','g12', 'g19'),[],(180,300)],
    'g12': [('g7', 'g11', 'g16'),[],(250,300)],
    'g13': [('g9', 'g14', 'g18'),[],(450,300)],
    'g14': [('g6', 'g13', 'g15', 'g21'),[],(525,300)],
    'g15': [('g3', 'g14', 'g24'),[],(600,300)],
    'g16': [('g12', 'g17'),[],(250,400)],
    'g17': [('g16', 'g18', 'g20'),[],(350,400)],
    'g18': [('g13', 'g17'),[],(450,400)],
    'g19': [('g11', 'g20'),[],(180,475)],
    'g20': [('g17', 'g19', 'g21', 'g23'),[],(350,475)],
    'g21': [('g14', 'g20'),[],(525,475)],
    'g22': [('g10', 'g23'),[],(100,550)],
    'g23': [('g10', 'g22', 'g24'),[],(350,550)],
    'g24': [('g15', 'g23'),[],(600,550)]
}

#return tuple of (x,y) of node1
def getStationXY(node1):
    #printNodeValue(node1)
    return graph[node1][2]

#this function get x,y and check if it is close ( less than 30)
#from any of the 24 points
#if it is, it return the number of station of the 24 stations of board
def findHit(x,y):
     for key, value in graph.items():
         xs = value[2][0]
         ys = value[2][1]
         v = (xs-x)**2 + (ys - y)**2
         v = v ** 0.5
         #print(x,y,xs,ys,v)
         if v < 10:
            print (key)
            return key
     #if we are here we did not find hit - the coin is not at one of 24 stations
     return 100

def printNodeValue(node1):
    print(graph[node1])

#check if there is already some coin in node1
def checkCoinInNode(node1):
    if len(graph[node1][1]) == 1:
        return True
    else:
        return False

def clearCoinInNode(node1):
    #print ("clearCoinInNode", node1)
    printNodeValue(node1)
    if len(graph[node1][1]) == 1:
        graph[node1][1].pop()
    #printNodeValue(node1)
    #no need to return value, in any case value of node1 will be empty

def setCoinInNode(node1, val):
    #print ("setCoinInNode", node1, val)
    printNodeValue(node1)
    if len(graph[node1][1]) == 0:
        graph[node1][1].append(val)
        #printNodeValue(node1)
        #printGraph()
        return True
    #it is not possible to set coin on a non empty node
    return False
    
    

def checkIfConnect(node1, node2):
    if node1 == node2:
        return False
    for key, value in graph.items():
        if key == node1:
            print ("1111")
            print (key, value[0])
            if node2 in value[0]:
                return True
    #if we are here we scan the whole graph and there is
    # no connection between both nodes
    print ("2222")
    return False



def printGraph():
    for key, value in graph.items():
        print (key, value)

def main():
    findHit(700,555)
    #node1 = 'g1'
    #val = setCoinInNode(node1, Color.BLACK)
    #print (val)
    #val = setCoinInNode(node1, Color.BLACK)
    #print (val)
    #val = clearCoinInNode(node1)
    #print (val)
    #val = clearCoinInNode(node1)
    #print (val)
    #node2 = 'g2'
    #print (node1, node2, checkIfConnect(node1,node2))

    

    printGraph()
    #print(graph)

if __name__ == "__main__":
    main()