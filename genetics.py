from random import *
import copy as cp
import os as os
"""
at the moment poste grid and grid can be a population variables, 
but the future directions of the poster (generative grid) are also implemented
"""
#interface variables
#fontratiox = -0.66; fontratioy= 1;
fontratiox = 0; fontratioy= 0;
serif = 0
#typefaces list
typefaces = []

class Population:
    _best = []
    _bestDetailedCost = []
    export = True
    userRewardMethod = True

    def __init__ (self, string, typef, nInd=100, folder="output"):
        """
        :param string: poster content
        :param typef: typefaces in the poster
        :param nInd: population size
        """
        global typefaces
        self._string = string
        self._nInd = nInd
        typefaces = typef
        self._folder = folder
        self._individuals = self._initPopulation()
        self.assess()
        
    def _initPopulation (self):
        """
        init population
        """
        individuals=[]
        for i in range(self._nInd):
            ind = Individual(self._string)
            individuals.append(ind) 
        return individuals
        
            
    def assess (self):
        """
        assess population
        """
        self._cost=[]
        for i, ind in enumerate(self._individuals):
            self._cost.append(ind.assess(self.userRewardMethod))  
        self.rank()
        self.truncate()
        if (self.export): self.exportFrames()
    
    def rank (self):
        """
        sort individuals by cost
        """
        self._individuals = sorted(self._individuals, key=lambda self: self.cost, reverse=False)
        self._cost = sorted(self._cost, key=lambda self: self, reverse=False)
    
    def truncate (self):
        """
        truncate the population to nInd 
        """
        self._individuals = self._individuals[-self._nInd:]
        self._cost = self._cost[-self._nInd:]
    
    def exportFrames(self):
        """
        export individuals
        """
        for index, individuals, in enumerate(self._individuals):
            individuals.saveFrame(index, self._folder)
    
    def fitness(self, sp=2):
        """
        linear ranking fitness
        :param sp: selective pression
        :return fitness: fitness array
        """
        self._fitness = []
        for ind in range(len(self._individuals)):
            v = sp - (sp-1.) * 2. * (ind-1) / (len(self._individuals)-1.)
            self._fitness.append(v)
        return self._fitness
    
    def estocasticSearch (self):
        """
        estocastic search
        """
        newPopulation = self._initPopulation()
        self._individuals= self._individuals+newPopulation
        self.assess()
        self._best.append(self._individuals[-1].cost)
    
    def run(self, sp, pm, px):
        """
        run algortihm
        :param sp: selective pressure
        :param pm: mutation prob
        :param px: xover prob
        """
        self.fitness(sp)
        ix = sus(self._fitness)
        offspring=[self._individuals[i-1] for i in ix]
        #xover
        childs = self.xover(offspring, px)
        self._individuals= self._individuals+(childs)
        #mutation
        mutchilds = self.mutation(pm)
        self._individuals= self._individuals+(mutchilds)
        self.assess()
        #plot
        self._best.append(self._cost[-1])
        self._bestDetailedCost.append(self[-1].dtcost)
    
    def xover (self, offspring, px=.7):
        """
        crossover
        based on work of Carlos M. Fonseca and Cristina Viera
        :param offspring: selected population
        :param px: recombination probability
        :return childs: the recombined individuals not in population 
        """
        mpind = len (offspring)
        #selecte the individuals (based in probability)
        pool = [random() < px for i in range(mpind)]
        #get false vaues
        nSelected = [k for k,value in enumerate(pool) if value == True]
        #delete the false values from offsrpring
        offspring = [i for j, i in enumerate(offspring) if j not in nSelected]
        #from a offspring menber get a mate
        mate = [self._individuals[randint(0, len(self._individuals)-1)] for i in range(len (offspring))]
        childs=[]
        for i, ind in enumerate(offspring):
            midpoint = randint (1,len(ind)-1)
            child1=Individual("")
            child2=Individual("")
            child1._genotype = ind[:midpoint]+mate[i][midpoint:]
            child2._genotype = mate[i][:midpoint]+ind[midpoint:]
            childs.extend((child1, child2))
        childs = [child for child in childs if child not in self._individuals]
        return childs
           
    def mutation (self, pm=.3):
        """
        mutation
        based on work of Carlos M. Fonseca and Cristina Viera
        :param pm: mutation prob
        :return childs: mutated individuals
        :see: _mutatedIndividual
        """
        #selecte the individuals (based in probability)
        pool = [random() < pm for i in range(len(self._individuals))]
        #get false values
        nSelected = [k for k,value in enumerate(pool) if value == True]
        childs=[]
        for i in nSelected:
            mutype = round(uniform(0,6.4))
            self[i]._mutatedHistory.append(mutype)
            mt = self._mutateIndividual(mutype, self[i])
            childs.append(mt)
        childs = [child for child in childs if child not in self._individuals]
        return childs
            
    def _mutateIndividual(self, mutype, ind):
        """
        Choose the mutation to apply
        :param mutype: random value between 1 and 6
        :param ind: individual to mutate
        :return: mutation function
        """
        return {
            0:ind.independentMutation(),
            1:ind.valueMutation(), 
            2:ind.geneMutation(), 
            3:ind.swapMutation(), 
            4:ind.swapValueMutation(), 
            5:ind.fontMutation(),
            6:ind.widthMutation(),
        }[mutype]    
        
    def draw(self, lines, ceils, auxiliar=False, controls=150):
        """
        draw the population in grid
        :param lines: number of lines
        :param ceils: number of ceils
        :param auxiliar: see the auxiliar construct grid
        :param controls: controls nav height 
        :see: individual draw()
        """
        nInd = lines*ceils
        nInd = nInd if nInd < len (self._individuals) else len (self._individuals)
        lx = width/ceils
        ly = (height-controls)/lines
        current = PVector (lx/2,ly/2)
        counter=0
        for i in range(lines):
            for j in range(ceils):
                fill (245)
                rectMode (CENTER)
                ind = self._individuals[-counter]
                ind.auxiliar = auxiliar
                img = ind.draw()
                #rect (current.x, current.y, lx, ly)   
                imageMode(CENTER)
                image (img,current.x, current.y,img.width, img.height)
                current.x= current.x+lx 
                counter=counter+1
            current.x = lx/2
            current.y = current.y+ly 
    
    def exportResults(self, nGen, nRuns):
        """
        export run results
        :param nGen: generations number
        :param nRuns: run number
        """
        folder = self._folder+"/results/"
        try: 
            os.makedirs(folder)
        except OSError:
             if not os.path.isdir(folder):
                raise
        #detailhed cost of best individual
        patch = folder+"best_"+str(nGen)+"_"+str(nRuns)+"_"+str(self._nInd)+".txt"  
        _exportList(patch, self._best, nGen, nRuns)
        patch = folder+"detBest_"+str(nGen)+"_"+str(nRuns)+"_"+str(self._nInd)+".txt"
        _exportList(patch, self._bestDetailedCost, nGen, nRuns)
        
        """file= open(patch,"w+")
        for dvalue in self._bestDetailedCost:
            file.write(str(dvalue[-1]))
            file.write("\n")
        file.close()
        #cost of all population
        patch = "allpop_"+str(nGen)+"_"+str(nRuns)+"_"+str(self._nInd)+".txt" 
        for dvalue in self._bestDetailedCost:
            print 'ddd', dvalue
        file.write(str(dvalue))
            file.write("\n")
        file.close()
        #cost of the best undividual
        patch = "simplebest_"+str(nGen)+"_"+str(nRuns)+"_"+str(self._nInd)+".txt" 
        file= open(patch,"w+")
        for best in self._best:
            file.write(str(best))
            file.write("\n")
        file.close()"""
    
    def _getArea(self):
        """
        get best individual area
        :return area: best individual area
        """
        self._area=(posterGrid[0]-2) * (posterGrid[1]-2)
        return self._area
        
    def __getitem__(self, key):
        return self._individuals[key]
    
    def __len__(self):
        return len(self._individuals)
    
    def __repr__(self):
        return 'population with '+str(len(self._individuals))+' individuals' 
    
    __str__=__repr__
    
    
class Individual():
    posterGrid = (8,6)
    #postersize = (595,842)
    postersize = (198,280)
    _grid = [[False for x in range(posterGrid[0])] for y in range(posterGrid[1])]
    auxiliar = False
    
    def __init__(self, string):
        """
        :param string: poster content
        """
        self._genotype = []
        self._phenotype = createGraphics (self.postersize[0], self.postersize[1])
        self._defineGrid(self._phenotype)
        for i in range(len(string)):
            case = i if i==0 else round(random())
            gene = next(case, string[i])
            self._genotype.append(gene)
        #plot 
        self._mutatedHistory=[]
        self._costHistory=[]
        self._geneVisualHistory=[]

    def saveFrame(self, index, folder):
        """
        export the phenotype
        :param index: index of individual in list
        """
        filename = folder+"/frames/"+str(index)+"/"+str(hour())+"_"+str(minute())+"_"+str(second())+"_"+str(millis())+".png"
        self._phenotype.save(filename)
    
    def assess (self, userRewardMethod=True):
        """
        individual assessment
        """
        self.draw()
        comp = self._compositionEvaluation((self.posterGrid[0]*self.posterGrid[1]), self.posterGrid[1], self.posterGrid[0])
        vis= self._visualEvaluation()
        user = self._userEvaluation(userRewardMethod)
        self.cost = comp+vis+user
        self.cost = map(self.cost, 0, 3,0,1)
        self.dtcost = [(comp,user,vis),self.cost]
        self._costHistory.append(self.dtcost)
        #print self.cost
        #self.cost=0 if (self.cost <0) else self.cost
        return self.cost
    
    #Cost evaluation
    def _compositionEvaluation (self, targetArea, targetWidth, targetHeight):
        """
        poster composition assessment
        :param targetArea: Area of the best individual
        :param targetWidth: width of the best individual
        :param targetHeight: height of the best individual
        :return cpCost: composition assement value
        """
        dw = -abs(targetWidth-self.width())
        dw = map(dw,-targetWidth, 0, -1,0)
        dh = -abs(targetHeight-self.height())
        dh = map (dh, -targetHeight,0,-1,0)
        da = -abs(self.area()-targetArea)
        da = map (da, -targetArea,0,-1,0)
        cpCost = map (dw+dh+da, -3,0,0,1)
        return cpCost
    
    def _userEvaluation(self, rewardMethod=True, maxLineReward=.5):
        """
        Evaluation according to user criteria
        :param maxLineReward: reward by the same cap height in a line
        """
        global typefaces, fontratiox, fontratioy, serif
        self._userEvaluationValue = 0
        lineBasis=0
        for gene in self._genotype:
            usedFont = typefaces[gene[4]]
            fontRatio = usedFont.ratio
            #Line cap height reward
            lineGift=0
            if gene[1] == 1:
                lineBasis = fontRatio[1] if (rewardMethod) else gene[4]
            else:
                if (rewardMethod):
                    #useCap Height
                    lineGift = self._capHeight(fontRatio[1],lineBasis,maxLineReward)
                else:
                    #use same font rule
                    lineGift = self._sameFont(gene[4],lineBasis,maxLineReward)
            #Evaluation according to user criteria
            distx= -abs(fontRatio[0]- fontratiox) 
            disty= -abs(fontRatio[1]- fontratioy) 
            distf = 0 if (usedFont.serif == serif) else -1
            #distg = distx+disty+distf
            #distg = map(distg, -3,0,0,1)
            #print 'brute', distx, disty, distf, lineGift
            distg = distx+disty+distf+lineGift
            distg = map(distg, -3,maxLineReward,0,1)
            self._userEvaluationValue = self._userEvaluationValue+distg
            #print 'distg', distg
        self._userEvaluationValue = self._userEvaluationValue/(len(self._genotype))
        #print  self._userEvaluationValue
        return self._userEvaluationValue

    def _visualEvaluation(self):
        """
        poster design evaluation
        (If the text fits in the textboxes)
        :see: draw
        """
        sumCost = sum(self._visualCost)
        visualCost = map (sumCost, -len(self._visualCost),0,0,1)
        #visualCost = 0 if (visualCost<0) else visualCost
        return visualCost
    
    #user Assess Functions
    def _capHeight(self,fontRatio, saved,maxReward):
        """
        line evaluation by cap height
        :param fontRatio: typeface y ratio
        :param saved: saved line y ratio
        :param maxReward: reward value
        :return reward: line reward
        """
        reward = -abs(fontRatio - saved)
        reward = map (reward,-2,0,0,maxReward)
        return reward
    
    def _sameFont (self, saved, typefaceid, maxReward):
        """
        line evaluation by same font
        :saved: typeface id
        :typefaceid: save line typeface id
        :param maxReward: reward value
        :return reward: line reward
        """
        reward = 0
        if (typefaceid == saved):
            reward = maxReward
        return reward
    
    #visual Assess Functions
    def LinearVisAssess(self, pg, gene, maxdif=3):
        """
        Equal assessment measure whether the word does not fit in the box or the box is larger than the word
        :param pg: individual PGraphics
        :param gene: gene to evaluate
        :maxdif: Maximum difference in grid (-1 value)
        :return textboxWidth: textbox width evaluation value 
        """
        value = abs(pg.textWidth(gene[0])-gene[2]*self._gridRatio[0])
        textboxWidth = map (value,-(self._gridRatio[0]*maxdif), 0, -1,0)
        textboxWidth = round(textboxWidth,4)
        return textboxWidth  
    
    def nonLinearVisAssess(self, pg, gene, maxdif=1):
        """
        non-linear assessment measure, cut words have a worse evaluation than words in large boxes
        :param pg: individual PGraphics
        :param gene: gene to evaluate
        :maxdif: Maximum difference in grid (-1 value)
        :return textboxWidth: textbox width evaluation value 
        """
        twid = pg.textWidth(gene[0])+self._gridRatio[1]
        value = twid-gene[2]*self._gridRatio[1]
        value = -abs(value/10) if (value <=0.0) else -sq(value)*2
        textboxWidth = map (value,-(self._gridRatio[1]*maxdif), 0, -1,0)
        textboxWidth = round(textboxWidth,4)
        return textboxWidth
       
    def truncVisAssess(self, pg, gene, maxdif=2):
        """
        :param pg: individual PGraphics
        :param gene: gene to evaluate
        :maxdif: Maximum difference in grid (-1 value)
        :return textboxWidth: textbox width evaluation value 
        """
        pmargin = self._gridRatio[1]/2
        value = (pg.textWidth(gene[0])+pmargin)-gene[2]*self._gridRatio[1]
        value = 0 if (value <=0.0) else -sq(value)*2
        #value = 0 if (value>= -pmargin and value <=0.0) else value
        #if (value != 0):
        #value = -abs(sq(value)) if (value > 0.0) else -abs(value/2)
        textboxWidth = map (value,-(self._gridRatio[1]*maxdif), 0, -1,0)
        return textboxWidth 

    #mutation methods
    def independentMutation (self, ipm=.05):
        """
        only evaluates if words fits in textboxes
        gene a gene mutation
        :param ipm: gene mutation prob
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        pool = [[random() < ipm for i in range(len(mt[j])-1)] for j in range(len(mt))]
        nSelected = [[j for j, value in enumerate(pool[i]) if value == True] for i in range(len(pool))]
        for i, gene in enumerate(nSelected):
            if not gene == []:
                for genePosition in gene:
                    mt = _changeGene (mt, genePosition, i)
        return mt
    
    def valueMutation (self):
        """
        mutate a gene's value
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        #content gene not change > len(mt)-2 
        valuePosition, gene  = randint(0,len(mt[0])-2), randint(0,len(mt)-1) 
        mt = _changeGene (mt, valuePosition, gene)
        return mt
 
    def geneMutation (self):
        """
        mutate a gene 
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        pos = randint(0,len(mt)-1)
        for i in range(1,len(mt[pos])-1):
            mt = _changeGene (mt, i, pos)
        return mt    
        
    def swapMutation (self):
        """
        swap genes in genotype
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        pos, pos2 = randint(1,len(mt)-1), randint(1,len(mt)-1) 
        mt._genotype[pos][1:], mt._genotype[pos2][1:] = mt._genotype[pos2][1:], mt._genotype[pos][1:]
        return mt
    
    def swapValueMutation (self):
        """
        swap gene's values
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        gene, gene2 = randint(1,len(mt)-1), randint(1,len(mt)-1)
        pos = randint(1,len(mt[0])-2)
        mt._genotype[gene][pos], mt._genotype[gene2][pos] = mt._genotype[gene2][pos], mt._genotype[gene][pos] 
        if pos ==1 or pos==3:
            if mt._genotype[gene][3] == False:
                mt._genotype[gene][1] = 1
            else: 
                mt._genotype[gene][1] = 0
            
            if mt._genotype[gene2][3] == False:
                mt._genotype[gene2][1] = 1
            else:
                mt._genotype[gene2][1] = 0            
        return mt
    
    def fontMutation (self, ipm=.3):
        """
        mutate the font value
        :param ipm: gene mutation prob
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        pool = [random() < ipm for i in range(len(mt))]
        nSelected = [k for k,value in enumerate(pool) if value == True]
        for i in nSelected:
            _changeGene (mt, 3, i)
        return mt
    
    def widthMutation(self, ipm=.3):
        """
        increase/decrease the width of textbox
        :param ipm: gene mutation prob
        :return mt: mutated individual
        """
        mt = cp.deepcopy(self)
        pool = [random() < ipm for i in range(len(mt))]
        nSelected = [k for k,value in enumerate(pool) if value == True]
        for i in nSelected:
            _changeGene (mt, 1, i, True)
        return mt
    
    #composition evaluation auxiliar methods    
    def width(self):
        """
        calculates the individual's width
        :return max: individual's width
        """
        count = 0
        max = 0
        for gene in self._genotype:
            if (gene[1] == 0):
                count = 0
            count +=gene[2]
            if (count > max):
                max = count
        return max
    
    def height(self):
        """
        calculates the individual's height
        :return max: individual's height
        """
        max = 0
        for gene in self._genotype:
            if (gene[1] == 0):
                max +=gene[3]
        return max
    
    def area(self):
        """
        calculates the individual's area
        :return area: individual's area
        """
        area = 0
        height = 0
        for gene in self._genotype:
            if (gene[1] == 0): 
                height = gene[3]
            width = gene[2]
            area += width*height
        return area
    
    def draw(self):
        """
        display individual
        :see: display
        """
        self._phenotype.beginDraw()
        self._phenotype.background(255)
        if (self.auxiliar):
            self._displayGrid(self._phenotype)
        self._display(self._phenotype)
        self._phenotype.endDraw()
        return self._phenotype
    
    def _display(self, pg):
        """
        display phenotype
        :param pg: Individual PGraphics
        """
        self._visualCost = []
        current = PVector (0,0)
        currentHeight = 0
        pg.noStroke()
        self._geneVisualHistory =[]
        for gene in self._genotype:
            #font = loadFont('data/fonts/'+str(gene[4])+".vlw")
            font = typefaces[gene[4]].pfont
            if (gene[1] == 0):
                current.y+=currentHeight
                current.x=0
                currentHeight = gene[3]
            if (self.auxiliar):
                pg.fill(0,0,0,50)
                pg.stroke(0)
                pg.rect (current.x*self._gridRatio[1], current.y*self._gridRatio[0],gene[2]* self._gridRatio[1],currentHeight*self._gridRatio[0])
            #pg.textFont(font, currentHeight*self._gridRatio[0])
            pg.textFont(font, (currentHeight)*self._gridRatio[0])
            pg.fill(0)
            pg.textMode(SHAPE)
            pg.textAlign (CENTER, CENTER) 
            pg.text(gene[0].upper(), 
                    current.x*self._gridRatio[1], 
                    current.y*self._gridRatio[0],
                    gene[2]* self._gridRatio[1],
                    currentHeight*self._gridRatio[0])
            current.x= current.x+gene[2]
            #aesthetic evaluation
            value = self.truncVisAssess(pg, gene)
            #plot
            self._geneVisualHistory.append((gene[0], value, pg.textWidth(gene[0]), -gene[2]*self._gridRatio[1]))
            self._visualCost.append(value)
    
    #grid methods
    def _defineGrid (self, pg):
        """
        define individual grid
        :param pg: individual phenotype
        """
        self._gridRatio = (float(pg.height)/self.posterGrid[0], float(pg.width)/self.posterGrid[1])
        for i, line in enumerate(self._grid):
            for j, el in enumerate(self._grid[i]):
                self._grid[i][j] = PVector (i*self._gridRatio[1], j*self._gridRatio[0])
    
    def _displayGrid(self, pg):
        """
        display individual grid
        :param pg: individual phenotype
        """
        pg.fill(0)
        for i, line in enumerate(self._grid):
            for pos in self._grid[i]:
                pg.noStroke()
                pg.ellipse (pos.x, pos.y,2,2) 
                
    #global methods   
    def __deepcopy__(self, memodict={}):
        copyObject = Individual("")
        copyObject._genotype = cp.deepcopy(self._genotype)
        return copyObject
     
    def __repr__(self):
        #return str([gene[0] for gene in self._genotype])
        return str(self._genotype)
    
    def __len__(self):
        return len(self._genotype)
    
    def __getitem__ (self, key):
        return self._genotype[key]
    
    def __eq__(self, other):
        return self._genotype == other._genotype
    
    __str__=__repr__


#production rules
#maxHeight = 5

#define width, height and typeface from textbox
defineWidth = lambda word: round(len(word)*uniform(.5,2))
defineHeight = lambda : round(uniform(1,5))
defineTypeface = lambda : randint(1, len(typefaces)-1)

def addWord(word, case=1):
    """
    add new word to the line
    :param word: first word of the poster
    :return gene: list with genetic info [rect(pos/size), word, rule]
    """
    width= defineWidth(word)
    typeface = defineTypeface()
    return [word, case, width, False, typeface]

def addBreak(word):
    """
    make a break line and add word to new line. see addWord
    :param word: first word of the poster
    :return gene: list with genetic info [rect(pos/size), word, rule]
    """
    gene = addWord(word,0)
    gene[3] = defineHeight()
    return gene

def next(case, word):
    return {
        0:addBreak(word),
        1:addWord(word),
    }[case]
    

#auxiliar mutation methods
def _changeRule (individual, gene):
    """
    change gene rule
    :param individual: mutated genotype
    :param gene: gene index in genotype
    :return individual: mutated genotype
    """
    if (random() <.5):
        individual[gene][1] = 1
        individual[gene][3] = False
    else:
        individual[gene][1] = 0
        individual[gene][3] = defineHeight()
    return individual

def _changeGene (mt, gp, index, defined=False):
    """
    update gene value
    :param mt: mutated genotype
    :param gp: value position
    :param index: gene index in genotype
    :param defined: a new definition of gene value is not necessary
    :return mt: mutated genotype
    """
    if (gp == 0 and index != 0): #first gene the rule is always 1
       mt = _changeRule(mt,index)
    elif gp==1 and defined==True:
        mt[index][2] = mt[index][2]+randint(-2,2)
        mt[index][2] = 1 if (mt[index][2] <1) else mt[index][2]
    elif gp==1:
       mt[index][2] = defineWidth(mt[index][0]) 
    elif gp ==2:
        mt[index][1] = 0
        mt[index][3] = defineHeight()
    elif gp == 3:
        #mt[index][4] = defineTypeface()
        mt[index][4] = 25
    return mt

    
#selection methods
def sus(fitness, nsel=None):
    """
    Stochatic universal sampling
    based on work of Carlos M. Fonseca and Cristina Viera
    :param fitness: sorted population's fitness 
    :param Nsel: number of offspring to keep
    :return ix: pointers order
    """
    if nsel is None:
        nsel = len(fitness)
    cumfit = reduce(lambda c, x: c + [c[-1] + x], fitness, [0])[1:]
    cumfit = [i *nsel for i in cumfit]
    cumfit = [i /cumfit[-1] for i in cumfit]
    r = random()
    prt = [i+r for i in range(nsel)]
    ix = _sumNewAxis(prt, cumfit)
    shuffle(ix)
    return ix

#auxiliar methods
def _sumNewAxis(prt, cumfit):
    """
    sum a list in a new axis 
    add a dimension to the list
    :return sumlist: a list n+1 dimension
    """
    sumlist = []
    for n in prt:
        value = []
        for v in cumfit:
            value.append(1 if n >= v else 0)
        sumlist.append(sum(value))
    return sumlist

def _exportList(patch, listToExport, nGen, nRuns):
        """
        export list to txt
        :param patch: patch to txt
        :param listToExport: list 
        :param nGen: generations number
        :param nRuns: run number
        """
        file= open(patch,"w+")
        for value in listToExport:
            file.write(str(value))
            file.write("\n")
        file.close()