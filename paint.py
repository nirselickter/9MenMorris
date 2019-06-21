import wx 
 
class Mywin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title,size = (500,300))  
      self.shapes = []
      
      self.InitUI() 
         
   def InitUI(self): 
      self.Bind(wx.EVT_PAINT, self.OnPaint) 
      self.Centre() 
      self.Show(True)
	
   def drawCoins(self, dc):
      brush = wx.Brush("white")  
      dc.SetBrush(brush) 
      x = 100
      y = 200
      for i in range(9):
        dc.DrawCircle(x,y,30) 
        y = y + 50
    
      brush = wx.Brush("black")  
      dc.SetBrush(brush) 
      x = 700
      y = 200
      for i in range(9):
        dc.DrawCircle(x,y,30) 
        y = y + 50


    
   def drawBoard(self,dc):
      offset = 400  
        
      pen = wx.Pen(wx.Colour(0,0,255)) 
      dc.SetPen(pen) 
      dc.DrawLine(offset-250,offset+250,offset+250,offset+250) 
      dc.DrawLine(offset-175, offset+175,offset+175,offset+175) 
      dc.DrawLine(offset-100, offset+100,offset+100,offset+100) 
      
      dc.DrawLine(offset-250,offset-250,offset + 250,offset-250) 
      dc.DrawLine(offset-175, offset-175,offset + 175,offset-175) 
      dc.DrawLine(offset-100, offset-100,offset + 100,offset-100) 
      
      dc.DrawLine(offset - 250, offset +250,offset - 250,offset - 250) 
      dc.DrawLine(offset - 175, offset + 175,offset - 175,offset - 175) 
      dc.DrawLine(offset - 100, offset + 100,offset - 100,offset - 100) 
      
      dc.DrawLine( offset +250, offset +250, offset +250,offset - 250) 
      dc.DrawLine( offset +175, offset + 175, offset +175,offset - 175) 
      dc.DrawLine( offset +100, offset + 100, offset +100,offset - 100)
      
      dc.DrawLine( offset +0, offset +250, offset +0, offset +100) 
      dc.DrawLine(offset - 250, offset + 0,offset - 100,offset +0) 
      dc.DrawLine( offset +0, offset - 100, offset +0,offset - 250)
      dc.DrawLine( offset +100, offset + 0, offset +250, offset +0)  
	
   def OnPaint(self, e): 
      dc = wx.PaintDC(self) 
      brush = wx.Brush("yellow")  
      dc.SetBackground(brush)  
      dc.Clear() 
		
      self.drawBoard(dc)
      self.drawCoins(dc)
      
		
ex = wx.App() 
Mywin(None,'Drawing demo') 
ex.MainLoop()