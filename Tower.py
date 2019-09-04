from graphics import *

# pointlist is a list to store all points, and it is declared as an empty list
pointlist = []
towerlocation=(0,0)
towerlength=0
# reading from file
f = open("input.txt", "r")
for x in f:
    if x!=str("@\n") and x!=str("@@\n"):
        tupleinput=tuple(int(inp.strip()) for inp in x.split(','))
        pointlist.append(tupleinput)
    elif x==str("@\n"):
        x=f.readline()
        k=int(x)
    # The following lines should be removed when we are computing the location of tower, and remember to modify the first case if condition and remove the statement after and
    elif x==str("@@\n"):
        x=f.readline()
        towerlocation=tuple(int(inp.strip()) for inp in x.split(','))
        towerlength=int(f.readline())

n=len(pointlist)

#Print the points' coordinates
print("Points are ",pointlist)


class TerrainLines:
    #we use intersection list to store coordinates of intersections of diiferent rays from tower and the line
    #and we stroe the impact of each intersection in impact list
    def __init__(self,theline):
        self.theline=theline
        self.intersection = []
        self.impact = []

    def AddIntersectionPoint(self,x,y,count):
        self.intersection.append((x,y))
        self.impact.append(count)

# function to determine the intersection point of two lines
def line_intersection(line1, line2):
    #xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    #ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    xdiff = (line1.getP1().getX() - line1.getP2().getX(), line2.getP1().getX() - line2.getP2().getX())
    ydiff = (line1.getP1().getY() - line1.getP2().getY(), line2.getP1().getY() - line2.getP2().getY())

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       #raise Exception('lines do not intersect')
       return -1, -1
    else:
        #converting object line to a matrix
        matline1=[(line1.getP1().getX(),line1.getP1().getY()),(line1.getP2().getX(),line1.getP2().getY())]
        matline2=[(line2.getP1().getX(),line2.getP1().getY()),(line2.getP2().getX(),line2.getP2().getY())]
        d = (det(*matline1), det(*matline2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

win = GraphWin('terrain',500,500)
#When you first create a GraphWin, the y coordinates increase down the screen.
#To reverse to the normal orientation use my GraphWin yUp method.
win.yUp()

#drawing points
for i in range(n):
    x=pointlist[i][0]
    y=pointlist[i][1]
    pt = Point(x, y)
    pt.setFill('red')
    pt.setOutline('red')
    pt.draw(win)

#drawing tower
towerx1=towerlocation[0]
towery1=towerlocation[1]
towerpt1 = Point(towerx1, towery1)
towerx2=towerx1
towery2=towery1+towerlength
towerpt2 = Point(towerx2, towery2)
towerpt2.setFill('red')
towerpt2.setOutline('red')
towerpt2.draw(win)
line = Line(towerpt1, towerpt2)
line.draw(win)

#drawing lines (the terrain) and storing them in an array
LinesList=[]
for i in range(n-1):
    x=pointlist[i][0]
    y=pointlist[i][1]
    pt1 = Point(x, y)

    x2=pointlist[i+1][0]
    y2=pointlist[i+1][1]
    pt2 = Point(x2, y2)

    line = Line(pt1, pt2)
    line.draw(win)

    #we need a modifed version of Class Line than the one in graphics.py so I created another class name TerrainLines
    LineOfTerrain=TerrainLines(line)
    LinesList.insert(i,LineOfTerrain)

#drawing lines between tower and each point
for i in range(n):
    x=pointlist[i][0]
    y=pointlist[i][1]
    #pt = Point(x, y)
    #Finding an end point on the line to draw the line completely
    if towerpt2.getX()!=x:
        #if the tower is on the left of the vertex
        if towerpt2.getX()<x:
            endx=pointlist[n-1][0]
            shib=(y-towery2)/(x-towerx2)
            endy=(shib*(endx-towerx2))+towery2
            endpt=Point(endx,endy)
            line = Line(towerpt2,endpt)
            #comment 3 following lines if you do not want to draw the lines between tower and each endpoint of terrain.
            line.setFill('blue')
            line.setOutline('blue')
            line.draw(win)
            counter=0;
            for j in range(len(LinesList)):
                if LinesList[j].theline.getP2().getX()>towerpt2.getX():
                    (intersectX,intersectY)=line_intersection(line,LinesList[j].theline)
                    if (intersectX,intersectY)==(-1,-1) or intersectX<towerpt2.getX() or intersectX<LinesList[j].theline.getP1().getX() or intersectX>LinesList[j].theline.getP2().getX():
                        pass
                    else:
                        LinesList[j].AddIntersectionPoint(intersectX,intersectY,counter)
                        counter=counter+1
                else:
                    pass

        #if the tower is on the right of the vertex
        elif towerpt2.getX()>x:
            endx=pointlist[0][0]
            shib=(towery2-y)/(towerx2-x)
            endy=towery2-(shib*(towerx2-endx))
            endpt=Point(endx,endy)
            line = Line(endpt,towerpt2)
            #comment 3 following lines if you do not want to draw the lines between tower and each endpoint of terrain.
            line.setFill('blue')
            line.setOutline('blue')
            line.draw(win)
            counter=0;
            for j in reversed(range(len(LinesList))):
                if LinesList[j].theline.getP1().getX()<towerpt2.getX():
                    (intersectX,intersectY)=line_intersection(line,LinesList[j].theline)
                    if (intersectX,intersectY)==(-1,-1) or intersectX>towerpt2.getX() or intersectX<LinesList[j].theline.getP1().getX() or intersectX>LinesList[j].theline.getP2().getX():
                        pass
                    else:
                        LinesList[j].AddIntersectionPoint(intersectX,intersectY,counter)
                        counter=counter+1
                else:
                    pass

    #if tower is exactly on one of the vertices.... the line between tower and the point that tower is on
    else:
        (intersectX,intersectY)=(towerx1, towery1)
        counter=0
        for j in range(len(LinesList)):
            if LinesList[j].theline.getP2().getX()==towerx1 or LinesList[j].theline.getP1().getX()==towerx1:
                LinesList[j].intersection.append((intersectX,intersectY))
                LinesList[j].impact.append(counter)
                counter=counter+1

#detecting visibility region and color it as green on Terrain. Black areas on Terrain are not visible
for nuLi in range(len(LinesList)):
    #sort intersections and impacts respectively based on intersections first element x
    list1, list2 = (list(t) for t in zip(*sorted(zip(LinesList[nuLi].intersection, LinesList[nuLi].impact))))
    LinesList[nuLi].impact=list2
    LinesList[nuLi].intersection=list1
    for i in range(len(LinesList[nuLi].impact)-1):
        if LinesList[nuLi].impact[i]<=k or LinesList[nuLi].impact[i+1]<=k:
            pt1=Point(LinesList[nuLi].intersection[i][0],LinesList[nuLi].intersection[i][1])
            pt2=Point(LinesList[nuLi].intersection[i+1][0],LinesList[nuLi].intersection[i+1][1])
            visible=Line(pt1,pt2)
            visible.setFill('green')
            visible.setOutline('green')
            visible.draw(win)
        else:
            pass

#The final result
print("Location of tower and its length are:")
print(towerlocation)
print(towerlength)
print("**************")

#Click on the graphic window to exit
win.getMouse()


#Implementation: Kasra
