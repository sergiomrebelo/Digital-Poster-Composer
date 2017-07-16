from genetics import *
from functions import *

#population size; generation number; number of runs
nInd=30; nGen=100; nRuns=0;
#selective pression; #mut prob; #xover prob
#sp=2; pm = (1-1./sp)*.9 #px= .55;
#sp=2; pm = .4; px = .6;
sp=2; pm = .3; px = .7;
#current generation
i = 0 
#text string
string = ["you", "know", "more", "than", "you", "think", "you", "do"]

def setup ():
    global pop, interface
    folder = "data/output/"+str(day())+"_"+str(month())+"_"+str(year())+"_"+str(hour())+"_"+str(minute())+"_"+str(second())
    print 'results saved in', folder
    #frameRate(12)
    size(960, 720)
    string=loadt('data/input/testfile2.txt')
    typefaces = loadf('data/fonts/fonts2.csv')
    if (string == None or typefaces ==None):
        exit()
    pop = Population (string, typefaces, nInd, folder)
    #print "init new population with sp:", sp, "pm", pm, "px", px
    interface = initInteface()
    

def draw():
    global i
    if (i<nGen):
        background (200)
        #pop.estocasticSearch()
        pop.run(sp, pm, px)
        pop.draw(1,3,False)
        #print 'history -1', pop._bestDetailedCost
        #img = pop[-1].draw()
        #image (img,10,10,img.width, img.height)
        print ('g.'+str(i)+':'), 'cost of the best individual: ', round(pop._cost[-1],5), pop[-1].dtcost
        i=i+1
    elif(i==nGen):
        pop.exportResults(nGen, nRuns)
        print "best:", pop[-1]
        i=i+1
        
    displayControls()

def keyPressed():
    if key == 's':
        #save the screen
        filename = "output_"+str(day())+"_"+str(month())+"_"+str(year())+"__"+str(hour())+"_"+str(minute())+".png"
        save(filename)
        print 'screen saved in', filename
    elif key == 'r':
        #continue run
        global i, nRuns
        nRuns = nRuns+1
        i=0
        print 'start a new run'
    elif key =='e':
        #start/end export population
        global pop
        pop.export = not pop.export
        print 'population export = ', pop.export


#interface
def initInteface ():
    """
    initialise the interface, using CP5 library
    :return: cp5 inteterface
    """
    global fontratiox, fontratioy,serif
    global r1
    cp5 = ControlP5(this)
    #fontratiox
    cp5.addSlider("fontratiox").setPosition(20,height-70).setRange(-1,1).setNumberOfTickMarks(7).setHeight(12).setValue(fontratiox).setDecimalPrecision(1)
    cp5.getController("fontratiox").setColorBackground(color(200)).setColorForeground(color(160)).setColorActive(color(100)).setColorLabel(color(0)).setColorValueLabel(color(230))
    cp5.getController("fontratiox").getCaptionLabel().align(ControlP5.LEFT, ControlP5.TOP_OUTSIDE).setPaddingX(0).setPaddingY(5)
    cp5.getController("fontratiox").addListener(lambda self: updateFontRatioX(self))
    #fontratioy
    cp5.addSlider("fontratioy").setPosition(140,height-70).setRange(-1,1).setNumberOfTickMarks(7).setHeight(12).setValue(fontratioy).setDecimalPrecision(1)
    cp5.getController("fontratioy").setColorBackground(color(200)).setColorForeground(color(160)).setColorActive(color(100)).setColorLabel(color(0)).setColorValueLabel(color(230))
    cp5.getController("fontratioy").getCaptionLabel().align(ControlP5.LEFT, ControlP5.TOP_OUTSIDE).setPaddingX(0).setPaddingY(5)
    cp5.getController("fontratioy").addListener(lambda self: updateFontRatioY(self))
    #serif
    r1 = cp5.addRadioButton("serifs").setPosition(260,height-70).setSize(12,12).addItem("None",0).addItem("Fat",1).addItem("Slab",2).setItemsPerRow(3).setColorForeground(color(160)).setSpacingColumn(40).setColorBackground(color(200)).setColorActive(color(100)).setColorLabel(color(0)).activate(serif)
    return cp5    

def displayControls(hei=150, margin=10):
    global r1, serifs
    """
    display the interface 
    :param hei: height of the interface nav
    :param margin: padding of nav
    """
    fill(235)
    rectMode(CORNER)
    noStroke()
    hei = hei-margin
    rect (0,height-hei, width,hei)
    #update genetics.serif 
    updateSerif()

#update genetics 
def updateFontRatioX (e):
    """
    update genetics.fontratiox
    :param e: slider value
    """
    global fontratiox
    fontratiox = round(e.getValue(),2)
    print 'genetics.fontratiox updated to', fontratioy
    
def updateFontRatioY (e):
    """
    update genetics.fontratioy
    :param e: slider value
    """
    global fontratioy
    fontratioy = round(e.getValue(),2)
    print 'genetics.fontratioy updated to', fontratioy

def updateSerif():
    """
    update genetics.serif
    """
    global r1, serif
    r1value = int(r1.getValue())
    if (r1value != serif):
        serif = r1value
        r1.activate(serif)
        print 'genetics.serif updated to', serif


    