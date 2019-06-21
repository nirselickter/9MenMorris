import threading
import socket
import sys
import wx 
from threading import Thread
from wx.lib.pubsub import pub
#from pubsub import pub
import graph 
import comm
from time import sleep
from queue import Queue
import argparse
import pickle

from enum import Enum
class Color(Enum):
    BLACK = 0
    WHITE = 1

class GAME_STATE(Enum):
    START = 0
    MIDDLE = 1
    END = 2

class GAME_TURN(Enum):
    CLIENT_TURN = 0
    SERVER_TURN = 1

#when debug, change it to 3 , 5. the tests are faster
NMB_OF_COINS = 9

flag = 0

server = False
my_color = Color.WHITE
other_color = Color.BLACK



class ChatPanel(wx.Panel):

    def __init__(self, parent, mysize):
        super().__init__(parent,-1, size = mysize, style=wx.SIMPLE_BORDER)
        
        main = wx.BoxSizer(wx.HORIZONTAL)
        
        msg = "your turn"
        if server == True:
            msg = "other side turn"
        
        self.lbl = wx.StaticText(self, label=msg)
        font = wx.Font(18, wx.MODERN, wx.ITALIC, wx.NORMAL)
        self.lbl.SetFont(font)
        main.Add(self.lbl ) 
        
        pub.subscribe(self.writeMsg, "message2")

        
        self.SetSizer(main)     
        
        self.Show()
   
    # note , it is important to write msg and not other variable name. it took me one hour to get it
    def writeMsg(self,msg):
        self.lbl.SetLabel(msg)
        
        


class SidePanel(wx.Panel):

    def __init__(self, parent, mysize):
        super().__init__(parent,-1, size = mysize, style=wx.SIMPLE_BORDER)

class MyPanel(wx.Panel): 
    
    def __init__(self, parent, id , mysize): 
        wx.Panel.__init__(self, parent, id,size = mysize, style=wx.SIMPLE_BORDER) 

        #ChatPanel.writeMsg(val="Hello world !")
        
        #print(parent.__dict__.keys)
        
        self.r = 30
        self.j = 0 
        self.t = Color.BLACK 
        self.d = 0 
        self.black =[]
        self.white = []
        self.hit = 0 #if 0 - mouse did not press any circle
        self.saveX = 0
        self.saveY = 0
        self.saveStation = "g100"
        self.state = GAME_STATE.START
        self.nmbOfCoinsOnBoard = 0
        self.nmbOfCoinsPlaced = 0
        self.turn = GAME_TURN.CLIENT_TURN
        self.WeGotMill = False
        self.nmbOfMills = 0

        dc = wx.MemoryDC() #when drawing not in OnPaint, use MemoryDC
        self.initCircles(dc)
        self.Buffer = None 
        
        #self.thread = TestThread
        if server == True :
            commThread = threading.Thread(target=comm.server_recv, args=())
        else:
            commThread = threading.Thread(target=comm.client_send, args=())
        commThread.start()

        # create a pubsub receiver
        pub.subscribe(self.updateDisplay, "update")
        
        self.SetBackgroundColour("yellow") 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown) 
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp) 
        self.Bind(wx.EVT_MOTION, self.MouseMove) 


    def InitBuffer(self): 
        size=self.GetClientSize() 
        self.Buffer = wx.Bitmap(size.width,size.height) 
        self.dc = wx.MemoryDC() 
        self.dc.SelectObject(self.Buffer) 


        
    def OnPaint(self, evt): 
        self.InitBuffer() 
        self.dc = wx.PaintDC(self) #when drawing in OnPaint, use PaintDC      
        self.drawBoard(self.dc)
        self.drawSmallCircle()
        self.drawCircle() 


    def initCircles(self, dc):
        brush = wx.Brush("white")  
        dc.SetBrush(brush) 
        x = 50
        y = 100
        for i in range(NMB_OF_COINS):
            tmp = [x,y]
            self.white.append(tmp);
            dc.DrawCircle(x,y,30) 
            y = y + 50

        brush = wx.Brush("black")  
        dc.SetBrush(brush) 
        x = 650
        y = 100
        for i in range(NMB_OF_COINS):
            tmp = [x,y]
            self.black.append(tmp);
            dc.DrawCircle(x,y,30) 
            y = y + 50


    def drawSmallCircle(self): 
        self.dc.SetBrush(wx.Brush("blue", wx.SOLID)) 
        for key, value in graph.graph.items():
            x = value[2][0]
            y = value[2][1]
            self.dc.DrawCircle(x, y, 5) 
            self.dc.DrawText(key[1:], x, y-20) 



    def drawCircle(self): 
        self.dc.SetBrush(wx.Brush("white", wx.SOLID)) 
        for i in range(NMB_OF_COINS): 
            self.dc.DrawCircle(self.white[i][0], self.white[i][1], self.r) 
            
        self.dc.SetBrush(wx.Brush("black", wx.SOLID))             
        for i in range(NMB_OF_COINS): 
            self.dc.DrawCircle(self.black[i][0], self.black[i][1], self.r) 

    def drawBoard(self,dc):
        offset_x = 350  
        offset_y = 300  

        pen = wx.Pen(wx.Colour(0,0,255)) 
        dc.SetPen(pen) 
        dc.DrawLine(offset_x-250,offset_y+250,offset_x+250,offset_y+250) 
        dc.DrawLine(offset_x-175, offset_y+175,offset_x+175,offset_y+175) 
        dc.DrawLine(offset_x-100, offset_y+100,offset_x+100,offset_y+100) 

        dc.DrawLine(offset_x-250,offset_y-250,offset_x + 250,offset_y-250) 
        dc.DrawLine(offset_x-175, offset_y-175,offset_x + 175,offset_y-175) 
        dc.DrawLine(offset_x-100, offset_y-100,offset_x + 100,offset_y-100) 

        dc.DrawLine(offset_x - 250, offset_y +250,offset_x - 250,offset_y - 250) 
        dc.DrawLine(offset_x - 175, offset_y + 175,offset_x - 175,offset_y - 175) 
        dc.DrawLine(offset_x - 100, offset_y + 100,offset_x - 100,offset_y - 100) 

        dc.DrawLine( offset_x +250, offset_y +250, offset_x +250,offset_y - 250) 
        dc.DrawLine( offset_x +175, offset_y + 175, offset_x +175,offset_y - 175) 
        dc.DrawLine( offset_x +100, offset_y + 100, offset_x +100,offset_y - 100)

        dc.DrawLine( offset_x +0, offset_y +250, offset_x +0, offset_y +100) 
        dc.DrawLine(offset_x - 250, offset_y + 0,offset_x - 100,offset_y +0) 
        dc.DrawLine( offset_x +0, offset_y - 100, offset_x +0,offset_y - 250)
        dc.DrawLine( offset_x +100, offset_y + 0, offset_x +250, offset_y +0)  

    def updateDisplay(self, msg):
        """
        Receives update message about move in other side
        """
        global other_color
        t = msg
        tmp = t[len("server response")+1:]
        info = tmp.split(" ")
        #print("wx rcv from remote", msg)
        if len(info) == 4:
            if info[0] == "put":
                coin = int(info[1])
                nmb  = int(info[2])
                nmb1 = int(info[3])
                prvStation = "g"+str(nmb)
                station = "g"+str(nmb1)
                                               
                x,y = graph.getStationXY(station)
                if prvStation != "g100":
                    graph.clearCoinInNode(prvStation)     
                graph.setCoinInNode(coin, station, other_color)
                #print("updateDisplay put", station, x, y)
                if (other_color == Color.BLACK):
                    self.black[coin][0] = x
                    self.black[coin][1] = y
                else:
                    self.white[coin][0] = x
                    self.white[coin][1] = y
                
                    
                #for debug
                val = graph.getGraphDb()
                val = pickle.dumps(val)
                val = val.decode('latin-1')
                msg = "checkDb "+ val
                comm.out_q.put(msg)
                
                self.InitBuffer() 
                self.dc = wx.ClientDC(self) #when drawing in OnPaint, use PaintDC      
                self.drawBoard(self.dc)
                self.drawSmallCircle()
                self.drawCircle() 
                self.Hide()
                self.Show()
        elif len(info) == 3:
            if info[0] == "take":
                coin = int(info[1])
                station = info[2]
                print("other side take coin")
                if (my_color == Color.BLACK):
                    self.black[coin][0] = 700
                    self.black[coin][1] = 600
                else:
                    self.white[coin][0] = 0
                    self.white[coin][1] = 600
                graph.clearCoinInNode(station)
                
                self.nmbOfCoinsOnBoard = self.nmbOfCoinsOnBoard - 1
                if self.state == GAME_STATE.MIDDLE and self.nmbOfCoinsOnBoard == 3:
                    print("change state to end game")
                    self.state = GAME_STATE.END
                
                
                #for debug
                val = graph.getGraphDb()
                val = pickle.dumps(val)
                val = val.decode('latin-1')
                msg = "checkDb "+ val
                comm.out_q.put(msg)

                
                self.InitBuffer() 
                self.dc = wx.ClientDC(self) #when drawing in OnPaint, use PaintDC      
                self.drawBoard(self.dc)
                self.drawSmallCircle()
                self.drawCircle() 
                self.Hide()
                self.Show()
        if tmp[:3] == "che":
             tmp = tmp[8:]
             tmp = tmp.encode('latin-1')
             tmp = pickle.loads(tmp)
             graph.compareDb(tmp)
             #print("111111111111111111111111")
             #print(tmp)
        if tmp == "your turn":
            pub.sendMessage("message2", msg="your turn")
            if server == True :
                self.turn = GAME_TURN.SERVER_TURN
                print("you are server and now you got the turn")
            elif server == False:
                self.turn = GAME_TURN.CLIENT_TURN
                print("you are client and now you got the turn")
        if tmp == "mill":
            pub.sendMessage("message2", msg="your rival got mill, please wait")


    def MouseMove(self, e): 
        x, y = e.GetPosition() 

        if self.d == 1 and self.hit == 1:  #move circle only when mouse is press
            if self.t == Color.BLACK: 
                self.black[self.j][0] = x 
                self.black[self.j][1] = y 
            elif self.t == Color.WHITE: 
                self.white[self.j][0] = x 
                self.white[self.j][1] = y 
            else: 
                pass 

            self.drawSmallCircle()
            self.drawCircle() 
            self.Refresh() 
            self.InitBuffer() 
        
        else: 
            pass 
        
    def returnTheCoinBack(self,reason):
        #this function is call if whenthe user drag and drop the coin on illegal place
        # illegal can be because
        #  1. the station is occupy with other coind
        #  2. release not in stationat all
        #  3. try to move coin in the first state of the game
        #print("return to beginning {0} {1} {2} {3}".format(self.j , self.saveX, self.saveY , reason))
        if self.t == Color.BLACK: 
            self.black[self.j][0] = self.saveX 
            self.black[self.j][1] = self.saveY
        elif self.t == Color.WHITE: 
            self.white[self.j][0] = self.saveX 
            self.white[self.j][1] = self.saveY 
        self.drawSmallCircle()
        self.drawCircle() 
        self.Refresh() 
        self.InitBuffer()

    def MouseUp(self, e):

        if self.d == 1 and self.hit == 1:  #move circle only when mouse is press
            self.d = 0 
            self.hit = 0
            x, y = e.GetPosition() 
            #print("MouseUp", x,y) #this print the position of circle afterrelease the mouse - it can be white or black. depend which one you drag
            station = graph.findHit(x,y)
            if station == "g100":
                # the coin was not dropped on one of 24 stations
                self.returnTheCoinBack(2) 
                return
            val = graph.checkCoinInNode(station)
            if val == True:
                # do not drop the coin on other coin 
                self.returnTheCoinBack(1) 
                #graph.printNodeValue("returnTheCoinBack(1)",station)
                return

            if self.state == GAME_STATE.MIDDLE:
                val = graph.checkIfConnect(self.saveStation, station)
                if val == False:
                    # user try to drop the coin not in a neighbour station
                    #graph.printNodeValue("returnTheCoinBack(4)",self.saveStation)
                    #graph.printNodeValue("returnTheCoinBack(4)",station)
                    self.returnTheCoinBack(4) 
                    return
                
            if self.state == GAME_STATE.START:
                if self.saveStation != "g100" :
                    # user try to move coin from station in the start state. this is prohibited
                    # in the start state, it is possible just to put coins on the board
                    self.returnTheCoinBack(3) 
                    return

                self.nmbOfCoinsOnBoard = self.nmbOfCoinsOnBoard + 1
                self.nmbOfCoinsPlaced  = self.nmbOfCoinsPlaced + 1
                if self.nmbOfCoinsPlaced == NMB_OF_COINS:
                    print("change state to middle")
                    self.state = GAME_STATE.MIDDLE
           
            if self.saveStation != "g100":
                graph.clearCoinInNode(self.saveStation)      
            graph.setCoinInNode(self.j, station, my_color)
            
            # the user release the coin very close to the station, so we found hit
            # we want to park the coin exactly on station's x,y, so we change alittle
            #the position of the coin. in the next paint event we will see it.
            x,y = graph.getStationXY(station)
            if (my_color == Color.BLACK):
                self.black[self.j][0] = x
                self.black[self.j][1] = y
            else:
                self.white[self.j][0] = x
                self.white[self.j][1] = y
            
            
            msg = "put "+ str(self.j) +" " + self.saveStation[1:] +" " + station[1:]
            #print("wx send to remote" + msg)
            comm.out_q.put(msg)
            
                            
            # we check if number of mills in this step is larger than previous step
            # if it is, it is necessary to take coin of your rival
            # you got the turn until you take coin of your rival
            nmbOfMills  = graph.checkMill(my_color)
            if nmbOfMills > self.nmbOfMills:
                print("\n>>>>>new mill, you need to take coin from your rival" )
                self.WeGotMill = True
                pub.sendMessage("message2", msg="new mill, you can take coin from your rival")
                comm.out_q.put("mill")
            else:              
                self.WeGotMill = False
            self.nmbOfMills = nmbOfMills
            
            if self.WeGotMill == False:
                pub.sendMessage("message2", msg="other side turn")
                comm.out_q.put("your turn")
                if server == True :
                    self.turn = GAME_TURN.CLIENT_TURN
                    print("You are server and the turn change to client")
                elif server == False:
                    self.turn = GAME_TURN.SERVER_TURN
                    print("You are client and the turn change to server")

               
            

    def MouseDown(self, e): 
        if server == True :
            if self.turn == GAME_TURN.CLIENT_TURN:
                if self.WeGotMill == False:
                    print("You are server and you try to play in client turn")
                    return
            else:
               self.turn = GAME_TURN.SERVER_TURN 
        elif server == False:
            if self.turn == GAME_TURN.SERVER_TURN:
                if self.WeGotMill == False:
                    print("You are client and you try to play in server turn")
                    return
            else:
                self.turn = GAME_TURN.CLIENT_TURN 
         
        self.d = 1 

        x, y = e.GetPosition() 
        
        for i in range(NMB_OF_COINS): 
            x_w = abs(self.white[i][0]-abs(x))//self.r 
            y_w = abs(self.white[i][1]-abs(y))//self.r 
            
            x_b = abs(self.black[i][0]-abs(x))//self.r 
            y_b = abs(self.black[i][1]-abs(y))//self.r 
            #print("\n333",x_w,y_w,x_b, y_b)

            # we check if my_color == something to disable from user to drag and drop otherside coins
            # if we got mill, the only thing that we can do is press on a coin of the rival
            if x_w == 0 and y_w == 0 and my_color ==  Color.WHITE and self.WeGotMill == False: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.WHITE 
                    self.hit = 1
                    self.saveX = self.white[i][0]
                    self.saveY = self.white[i][1] 
                    self.saveStation = graph.findHit(self.saveX,self.saveY) #if i game starting ,selfStation will be g100
                    #print("mouseDown white", self.j, self.t , self.saveX, self.saveY , self.saveStation)
            elif x_b == 0 and y_b == 0 and my_color ==  Color.BLACK and self.WeGotMill == False: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.BLACK
                    self.hit = 1
                    self.saveX = self.black[i][0]
                    self.saveY = self.black[i][1] 
                    self.saveStation = graph.findHit(self.saveX,self.saveY)
                    #print("mouseDown black", self.j, self.t , self.saveX, self.saveY , self.saveStation)
            elif x_w == 0 and y_w == 0 and my_color ==  Color.BLACK and self.WeGotMill == True:
                    print("You take white from rival", )
                    self.d = 0
                    self.j = i #find which coin from 0 to 8 was press
                    self.white[self.j][0] = 0 
                    self.white[self.j][1] = 600 
                    self.WeGotMill = False
                    self.Hide()
                    self.Show()
                    station = graph.findHit(x,y)
                    #print("mouseDown take white info",x,y,station)
                    coin = graph.getCoinNmbInStation(station)
                    graph.clearCoinInNode(station)
                    msg = "take "+ str(coin) + " " + station
                    #print("wx send to remote" + msg)
                    comm.out_q.put(msg)
              
                    pub.sendMessage("message2", msg="other side turn")
                    if server == True :
                        self.turn = GAME_TURN.CLIENT_TURN
                        print("You are server and the turn change to client")
                    elif server == False:
                        self.turn = GAME_TURN.SERVER_TURN
                        print("You are client and the turn change to server")
                    comm.out_q.put("your turn")                   
                    
            elif x_b == 0 and y_b == 0 and my_color ==  Color.WHITE and self.WeGotMill == True: 
                    #print("You take black from rival")
                    self.d = 0
                    self.j = i #find which coin from 0 to 8 was press
                    self.black[self.j][0] = 700 
                    self.black[self.j][1] = 600 
                    self.WeGotMill = False
                    self.Hide()
                    self.Show()
                    station = graph.findHit(x,y)
                    coin = graph.getCoinNmbInStation(station)
                    graph.clearCoinInNode(station)
                    msg = "take "+ str(coin)  + " " + station
                    #print("wx send to remote" + msg)
                    comm.out_q.put(msg)

                    pub.sendMessage("message2", msg="other side turn")
                    if server == True :
                        self.turn = GAME_TURN.CLIENT_TURN
                        print("You are server and the turn change to client")
                    elif server == False:
                        self.turn = GAME_TURN.SERVER_TURN
                        print("You are client and the turn change to server")
                    comm.out_q.put("your turn")

            else: 
                pass 
        
class MainFrame(wx.Frame):
    def __init__(self):
        #wx.Frame.__init__(self, None, title="9 Men Morris", size=(700,700))
        #panel = MyPanel(self,-1)
        
        wx.Frame.__init__(self, None, title="9 Men Morris", size=(900,900))
        self.createWidgets()
        
        
        main = wx.BoxSizer(wx.VERTICAL)
        
        row = wx.BoxSizer(wx.HORIZONTAL)   
        row1 = wx.BoxSizer(wx.HORIZONTAL)

        
        col1 = wx.BoxSizer(wx.VERTICAL)
        col2 = wx.BoxSizer(wx.VERTICAL)

        sidePanel = SidePanel(self, mysize=(200,700))
        gamePanel = MyPanel(self, -1,mysize=(700,700))
        self.chatPanel = ChatPanel(self, mysize=(900,200))

        

        col1.Add(sidePanel)
        col2.Add(gamePanel)
        
        row.Add(col1)
        row.Add(col2)

        row1.Add(self.chatPanel)
        
        main.Add(row)
        main.Add(row1)
     
        self.SetSizer(main)     
        
        self.Show()
        
    def createWidgets(self):   
        self.CreateStatusBar()      # wxPython built-in method
        self.createMenu()
        #self.createNotebook()
        
    def createMenu(self):      
        menu= wx.Menu()
        printGraph = menu.Append(wx.ID_NEW, "Print Graph", "Create something new")
        self.Bind(wx.EVT_MENU, self.printGraph, printGraph)
        
        menu.AppendSeparator()
        
        _exit = menu.Append(wx.ID_EXIT, "Exit", "Exit the GUI")
        self.Bind(wx.EVT_MENU, self.exitGUI, _exit)
        
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "File")   
        
        menu1= wx.Menu()    
        menu1.Append(wx.ID_ABOUT, "About", "wxPython GUI")
        menuBar.Append(menu1, "Help")     
        self.SetMenuBar(menuBar)     
        
    def exitGUI(self, event):       # callback
        self.Destroy()

    def printGraph(self, event):    # callback
        graph.printGraph("debug")

def main():
    app = wx.App() 
    frame = MainFrame()
    app.MainLoop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Say hello')
    parser.add_argument('server', help='choose client or server')
    parser.add_argument('color',  help='choose white or black')
    args = parser.parse_args()
    

    if args.server == "server":
        server = True

    if args.color == "black":
        my_color = Color.BLACK 
        other_color = Color.WHITE
    print ("server:{0} my:{1} other:{2}:".format(server, my_color, other_color))
    main()