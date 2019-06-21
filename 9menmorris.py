#in this code you can do two things
# 1. you can drag one of the white coins toward the board.
#     if you will be close enough (<10) from one of the 24 stations, it will write
#     the station number - for example it will write g19
# 2. the second thing you can do is write the console pair like 5 19 - it means
#    take coin 5 from the white and move it to be on station 19


import wx 
from threading import Thread
from wx.lib.pubsub import pub
import graph4


from enum import Enum
class Color(Enum):
    BLACK = 0
    WHITE = 1

class TestThread(Thread):
    """Test Worker Thread Class."""

    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.daemon = True
#        self.my_socket = socket.socket()
#        self.my_socket.connect(("127.0.0.1",8820))
        #self.text = text.encode('ascii') #this is for python 3
        self.start()    # start the thread
        

    def run(self):
        """Run Worker Thread."""
        while True:
            #self.my_socket.send(self.text)
            #data = self.my_socket.recv(1024)
            #data = data.decode('ascii') #this is for python 3
            data = input("enter move (coin, number - e.g 4 14):")
            if data == "":
                continue
            pub.sendMessage("update", msg="server response " +data)
            #self.my_socket.close()

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
        
        self.thread = TestThread()
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
        for key, value in graph4.graph.items():
            x = value[2][0]
            y = value[2][1]
            self.dc.DrawCircle(x, y, 5) 
            self.dc.DrawText(key[1:], x, y-20) 



    def drawCircle(self): 
        #self.dc.SetPen(wx.Pen("red", style=wx.TRANSPARENT)) 

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
        #if isinstance(t, int):
        #    self.displayLbl.SetLabel("server will answer here")
        #else:
        #    self.displayLbl.SetLabel("%s" % t)
        #    self.btn.Enable()
        tmp = t[len("server response")+1:]
        info = tmp.split(" ")
        print(tmp, info)
        #return
        i = int(info[0])
        nmb = int(info[1])
        coin = "g"+str(nmb)
        x,y = graph4.getCoinXY(coin)
        print(coin, x, y)
        #return
        self.white[i][0] = x
        self.white[i][1] = y
        #size=self.GetClientSize() 
        #self.Buffer = wx.Bitmap(size.width,size.height) 
        #self.dc = wx.ClientDC() 
        #self.dc.SelectObject(self.Buffer)
        
        
        self.InitBuffer() 
        self.dc = wx.ClientDC(self) #when drawing in OnPaint, use PaintDC      
        self.drawBoard(self.dc)
        self.drawSmallCircle()
        self.drawCircle() 
        self.Hide()
        self.Show()
       #wx.Update(self)
        #for i in range(9):
        #    print(self.white[i][0], self.white[i][1])







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
        

    def MouseUp(self, e): 
        self.d = 0 
        self.hit = 0
        x, y = e.GetPosition() 
        print(x,y) #this print the position of circle afterrelease the mouse - it can be white or black. depend which one you drag
        val = graph4.findHit(x,y)
        if val != 100:
            print("111",val)
            

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