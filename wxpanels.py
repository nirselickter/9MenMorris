import wx
import wx.lib.inspection

    
class MyPanel(wx.Panel):

    def __init__(self, parent, mysize):
        super().__init__(parent,-1, size = mysize, style=wx.SIMPLE_BORDER)
        browse_btn = wx.Button(self, label='Browse') 
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(browse_btn, 0, wx.ALL, 5)
        self.SetSizer(main_sizer)
        self.Layout()
       
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Main App", size=(900,900))
        self.createWidgets()
        
        
        main = wx.BoxSizer(wx.VERTICAL)
        
        row = wx.BoxSizer(wx.HORIZONTAL)   
        row1 = wx.BoxSizer(wx.HORIZONTAL)

        
        col1 = wx.BoxSizer(wx.VERTICAL)
        col2 = wx.BoxSizer(wx.VERTICAL)

        sidePanel = MyPanel(self, mysize=(200,700))
        gamePanel = MyPanel(self, mysize=(700,700))
        chatPanel = MyPanel(self, mysize=(900,200))


        col1.Add(sidePanel)
        col2.Add(gamePanel)
        
        row.Add(col1)
        row.Add(col2)

        row1.Add(chatPanel)
        
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
        menu.Append(wx.ID_NEW, "New", "Create something new")
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

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
