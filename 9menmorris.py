import threading
import socket
import sys
import wx 
from threading import Thread
from wx.lib.pubsub import pub
import graph 
import comm
from time import sleep
from queue import Queue
import argparse

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



flag = 0

server = False
my_color = Color.WHITE
other_color = Color.BLACK

class MyPanel(wx.Panel): 
    
    def __init__(self, parent, id ): 
        wx.Panel.__init__(self, parent, id) 

        
        self.r = 30
        self.j = 0 
        self.t = Color.BLACK 
        self.d = 0 
        self.black =[]
        self.white = []
        self.hit = 0 #if 0 - mouse did not press any circle
        self.saveX = 0
        self.saveY = 0
        self.saveStation = 100
        self.state = GAME_STATE.START
        self.nmbOfCoinsOnBoard = 0
        self.turn = GAME_TURN.CLIENT_TURN

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

    def initCircles(self, dc):
        brush = wx.Brush("white")  
        dc.SetBrush(brush) 
        x = 50
        y = 100
        for i in range(9):
            tmp = [x,y]
            self.white.append(tmp);
            dc.DrawCircle(x,y,30) 
            y = y + 50

        brush = wx.Brush("black")  
        dc.SetBrush(brush) 
        x = 650
        y = 100
        for i in range(9):
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
        for i in range(9): 
            self.dc.DrawCircle(self.white[i][0], self.white[i][1], self.r) 
            
        self.dc.SetBrush(wx.Brush("black", wx.SOLID))             
        for i in range(9): 
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
        print("145", tmp, info)
        if len(info) == 3:
            if info[0] == "put":
                coin = int(info[1])
                nmb1 = int(info[2])
                station = "g"+str(nmb1)
                                               
                x,y = graph.getStationXY(station)
                graph.setCoinInNode(station, other_color)
                print("iuy", station, x, y)
                if (other_color == Color.BLACK):
                    self.black[coin][0] = x
                    self.black[coin][1] = y
                else:
                    self.white[coin][0] = x
                    self.white[coin][1] = y
                
                if server == True :
                    self.turn = GAME_TURN.SERVER_TURN
                    print("4a3", "you are server and now you got the turn")
                elif server == False:
                    self.turn = GAME_TURN.CLIENT_TURN
                    print("4i3", "you are client and now you got the turn")
                
                self.InitBuffer() 
                self.dc = wx.ClientDC(self) #when drawing in OnPaint, use PaintDC      
                self.drawBoard(self.dc)
                self.drawSmallCircle()
                self.drawCircle() 
                self.Hide()
                self.Show()


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
        print("return to beginning {0} {1} {2} {3}".format(self.j , self.saveX, self.saveY , reason))
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
            print("545", x,y) #this print the position of circle afterrelease the mouse - it can be white or black. depend which one you drag
            station = graph.findHit(x,y)
            if station != 100:
                val = graph.checkCoinInNode(station)
                if val == True:
                    # do not drop the coin on other coin 
                    self.returnTheCoinBack(1) 
                    return
                if self.saveStation != 100 and self.state == GAME_STATE.START:
                    # user try to move coin from station in the start state. this is prohibited
                    # in the start state, it is possible just to put coins on the board
                    self.returnTheCoinBack(3) 
                    return
                if self.state == GAME_STATE.START:
                    self.nmbOfCoinsOnBoard =self.nmbOfCoinsOnBoard + 1
                    if self.nmbOfCoinsOnBoard == 9:
                        print("9u9","change state to middle")
                        self.state = GAME_STATE.MIDDLE
                graph.setCoinInNode(station, my_color)
                msg = "put "+ str(self.j) +" " +  station[1:]
                print("232 " + msg)
                comm.out_q.put(msg)
                if server == True :
                    self.turn = GAME_TURN.CLIENT_TURN
                    print("4w3", "you are server and the turn change to client")
                elif server == False:
                    self.turn = GAME_TURN.SERVER_TURN
                    print("4w3", "you are client and the turn change to server")
            else:
                # the coin was not dropped on one of 24 stations
                self.returnTheCoinBack(2) 
            

    def MouseDown(self, e): 
        if server == True :
            if self.turn == GAME_TURN.CLIENT_TURN:
                print("2w3", "you are server and you try to play in client turn")
                return
            else:
               self.turn = GAME_TURN.SERVER_TURN 
        elif server == False:
            if self.turn == GAME_TURN.SERVER_TURN:
                print("4w3", "you are client and you try to play in server turn")
                return
            else:
                self.turn = GAME_TURN.CLIENT_TURN 
         
        self.d = 1 

        x, y = e.GetPosition() 
        
        for i in range(9): 
            x_w = abs(self.white[i][0]-abs(x))//self.r 
            y_w = abs(self.white[i][1]-abs(y))//self.r 
            
            x_b = abs(self.black[i][0]-abs(x))//self.r 
            y_b = abs(self.black[i][1]-abs(y))//self.r 
            #print("\n333",x_w,y_w,x_b, y_b)

            # we check if my_color == something to disable from user to drag and drop otherside coins
            if x_w == 0 and y_w == 0 and my_color ==  Color.WHITE: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.WHITE 
                    self.hit = 1
                    self.saveX = self.white[i][0]
                    self.saveY = self.white[i][1] 
                    self.saveStation = graph.findHit(self.saveX,self.saveY)
                    print("111", self.j, self.t , self.saveX, self.saveY , self.saveStation)
            elif x_b == 0 and y_b == 0 and my_color ==  Color.BLACK: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.BLACK
                    self.hit = 1
                    self.saveX = self.black[i][0]
                    self.saveY = self.black[i][1] 
                    self.saveStation = graph.findHit(self.saveX,self.saveY)
                    print("222", self.j, self.t , self.saveX, self.saveY , self.saveStation)
            else: 
                pass 
        

def main():
    app = wx.App() 
    frame = wx.Frame(None, -1, "Moving a Circle...", size = (700, 700)) 
    MyPanel(frame,-1 ) 
    frame.Show(True) 
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