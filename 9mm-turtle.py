# part of the code here was copy from turtleDemo/tangram.py program
# mainly, the drag/release code
from turtle import Turtle, Screen, Vec2D 


screen = Screen()   
listCross = []
turtle = Turtle(visible=False)
    
class coin(Turtle):
    def __init__(self, color, x, y):      
        Turtle.__init__(self)
        self.penup()
        self.shape("circle")
        self.color(color)
        self.shapesize(3, 3)
        self.goto(x,y)
        self.onclick(self.store, 1)
        self.ondrag(self.move, 1)
        self.onrelease(self.match, 1)
        screen.update()
    def store(self,x,y):
        self.clickpos = Vec2D(x,y)
    def move(self,x,y):
        neu = Vec2D(x,y)
        self.goto(self.pos() + (neu-self.clickpos))
        self.clickpos = neu
        screen.update()
    def match(self, x=None, y=None):
        pos = self.pos()
        x = pos[0]
        y = pos[1]
        print("x:{0} y:{1}".format(x,y))
        for i in listCross:
            rc = pointInsideCircle(pos,i,7)
            if rc == True:
                print ("match") #the coin is places on one of 24 stations
            
  
#https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle  
def pointInsideCircle(point,circleCenter, circleRadius):
    x=point[0]
    y=point[1]
    circleCenterX = circleCenter[0]
    circleCenterY = circleCenter[1]
    temp=(x - circleCenterX)**2 + (y - circleCenterY)**2 
    if temp < circleRadius**2:
        return True
    else:
        return False
  
def drawCoins():
    tess = coin(color = "black",x=300, y=280)
    tess = coin(color = "black",x=300, y=210)
    tess = coin(color = "black",x=300, y=140)
    tess = coin(color = "black",x=300, y=70)
    tess = coin(color = "black",x=300, y=0)
    tess = coin(color = "black",x=300, y=-70)
    tess = coin(color = "black",x=300, y=-140)
    tess = coin(color = "black",x=300, y=-210)
    tess = coin(color = "black",x=300, y=-280)

    tess = coin(color = "white",x=-300, y=280)
    tess = coin(color = "white",x=-300, y=210)
    tess = coin(color = "white",x=-300, y=140)
    tess = coin(color = "white",x=-300, y=70)
    tess = coin(color = "white",x=-300, y=0)
    tess = coin(color = "white",x=-300, y=-70)
    tess = coin(color = "white",x=-300, y=-140)
    tess = coin(color = "white",x=-300, y=-210)
    tess = coin(color = "white",x=-300, y=-280)

  
def drawX( v,size):
    x = v[0]
    y = v[1]
    turtle.penup()
    turtle.goto(x,y)
    s = 0.5**0.5
    offset = s*size
    turtle.goto(x-offset,y+offset)
    turtle.pendown()
    turtle.goto(x+offset,y-offset)
    turtle.penup()
    turtle.goto(x-offset,y-offset)
    turtle.pendown()
    turtle.goto(x+offset,y+offset)
    turtle.penup()

# on the board there are 24 stations(station is a place you might place the coin)
# in each station draw little x
def drawAllX():

    turtle.pensize(4)
    b = [100,175,250]
    ss = 10
    for i in b:
        temp = Vec2D(i,i)
        listCross.append(temp)
        drawX(temp,ss)

        temp = Vec2D(-i,i)
        listCross.append(temp)
        drawX(temp,ss)

        temp = Vec2D(i,-i)
        listCross.append(temp)
        drawX(temp,ss)
        
        temp = Vec2D(-i,-i)
        listCross.append(temp)
        drawX(temp,ss)

        temp = Vec2D(i,0)
        listCross.append(temp)
        drawX(temp,ss)

        temp = Vec2D(0,i)
        listCross.append(temp)
        drawX(temp,ss)

        temp = Vec2D(0,-i)
        listCross.append(temp)
        drawX( temp,ss)
        
        temp = Vec2D(-i,0)
        listCross.append(temp)
        drawX( temp,ss)


def drawBoard():    
    turtle.pensize(3)
    turtle.penup()
    turtle.goto(-250,250)
    turtle.pendown()
    turtle.goto(250,250)
    turtle.penup()
    turtle.goto(-175,175)
    turtle.pendown()
    turtle.goto(175,175)
    turtle.penup()
    turtle.goto(-100,100)
    turtle.pendown()
    turtle.goto(100,100)

    turtle.penup()
    turtle.goto(-250,-250)
    turtle.pendown()
    turtle.goto(250,-250)
    turtle.penup()
    turtle.goto(-175,-175)
    turtle.pendown()
    turtle.goto(175,-175)
    turtle.penup()
    turtle.goto(-100,-100)
    turtle.pendown()
    turtle.goto(100,-100)

    turtle.penup()
    turtle.goto(-250,250)
    turtle.pendown()
    turtle.goto(-250,-250)
    turtle.penup()
    turtle.goto(-175,175)
    turtle.pendown()
    turtle.goto(-175,-175)
    turtle.penup()
    turtle.goto(-100,100)
    turtle.pendown()
    turtle.goto(-100,-100)

    turtle.penup()
    turtle.goto(250,250)
    turtle.pendown()
    turtle.goto(250,-250)
    turtle.penup()
    turtle.goto(175,175)
    turtle.pendown()
    turtle.goto(175,-175)
    turtle.penup()
    turtle.goto(100,100)
    turtle.pendown()
    turtle.goto(100,-100)


    turtle.penup()
    turtle.goto(0,250)
    turtle.pendown()
    turtle.goto(0,100)
    turtle.penup()
    turtle.goto(-250,0)
    turtle.pendown()
    turtle.goto(-100,0)
    turtle.penup()
    turtle.goto(0,-100)
    turtle.pendown()
    turtle.goto(0,-250)
    turtle.penup()
    turtle.goto(100,0)
    turtle.pendown()
    turtle.goto(250,0)

def main():
    screen.bgcolor("yellow")
    screen.tracer(False) #do not update the screen 
    
    drawBoard()
    drawAllX()
    drawCoins() #also handle click/drag/drop events
    
    screen.update() # now update the screen

    screen.mainloop()  #run forever

if __name__ == "__main__":
    main()
