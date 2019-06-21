#http://wxpython-users.1045709.n5.nabble.com/Drag-and-drop-circles-td5714000.html
# in this code you can wite in console 0 100 200 and the white coin number 0 is going to place x =100 y=200

import wx 
from threading import Thread
from wx.lib.pubsub import pub


from enum import Enum
class Color(Enum):
    BLACK = 0
    WHITE = 1

class consoleThread(Thread):

    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.daemon = True
        self.start()    # start the thread
     
    def run(self):
        """Run Worker Thread."""
        while True:
            data = input("enter move (coin, x, y - e.g 4 100 300):")
            pub.sendMessage("update", msg="server response " +data)


class MyPanel(wx.Panel): 
    
    def __init__(self, parent, id): 
        wx.Panel.__init__(self, parent, id) 

        
        self.r = 30
        self.j = 0 
        self.t = Color.BLACK 
        self.d = 0 
        self.black =[]
        self.white = []
        self.hit = 0 #if 0 - mouse did not press any circle


        dc = wx.MemoryDC() #when drawing not in OnPaint, use MemoryDC
        self.initCircles(dc)
        self.Buffer = None 
        
        self.thread = consoleThread()
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

    def drawCircle(self): 
        self.dc.SetPen(wx.Pen("red", style=wx.TRANSPARENT)) 

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
        Receives data from thread and updates the display
        """
        t = msg
        tmp = t[len("server response")+1:]
        info = tmp.split(" ")
        print(tmp, info)
        i = int(info[0])
        x = int(info[1])
        y = int(info[2])
        print(info, i, x, y)
        self.white[i][0] = x
        self.white[i][1] = y      
        
        self.InitBuffer() 
        self.dc = wx.ClientDC(self) #when drawing in OnPaint, use PaintDC      
        self.drawBoard(self.dc)
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

            self.drawCircle() 
            self.Refresh() 
            self.InitBuffer() 
        
        else: 
            pass 
        

    def MouseUp(self, e): 
        self.d = 0 
        self.hit = 0
        x, y = e.GetPosition() 
        print(x,y) #this print the position of circle afterrelease the mouse - it can be white or black. depend which one you drag

    def MouseDown(self, e): 
        self.d = 1 

        x, y = e.GetPosition() 
        
        for i in range(9): 
            x_w = abs(self.white[i][0]-abs(x))//self.r 
            y_w = abs(self.white[i][1]-abs(y))//self.r 
            
            x_b = abs(self.black[i][0]-abs(x))//self.r 
            y_b = abs(self.black[i][1]-abs(y))//self.r 
            #print("\n333",x_w,y_w,x_b, y_b)

            if x_w == 0 and y_w == 0: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.WHITE 
                    self.hit = 1
                    print("111", self.j, self.t)
            elif x_b == 0 and y_b == 0: 
                    self.j = i #find which coin from 0 to 8 was press
                    self.t = Color.BLACK
                    self.hit = 1
                    print("222", self.j, self.t)
            else: 
                pass 
        


app = wx.App() 
frame = wx.Frame(None, -1, "Moving a Circle...", size = (700, 700)) 
MyPanel(frame,-1) 
frame.Show(True) 

app.MainLoop()