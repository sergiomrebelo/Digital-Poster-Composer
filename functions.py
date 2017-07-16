add_library('controlP5')
import os as os
import csv as csv

#text string load
def loadt(patch="textfile.txt"):
    """
    input text in the system
    :param patch: the patch to txt with content
    :return: a list with text splited in words
    """
    if os.path.exists(patch):
        try:
            with open(patch, 'r') as file:
                string=file.readlines()
                st = ""
                for s in string:
                    st = st+s
                return st.split(" ")
        except:
            exit()
    elif IOError:
        print 'could not read the file:', patch
        exit() 
            

#typeface load
def loadf(patch):
    """
    load typefaces
    :param patch: the patch to typefaces
    :return: a list with typefaces in the system
    """
    fonts=[]
    if os.path.exists(patch):
        with open(patch, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                fontinst = Typeface (int(row[0]),row[1],(float(row[3]),float(row[4])),int(row[5]), row[2])
                fonts.append(fontinst)
    elif IOError:
        print 'could not read the file:', patch
        exit()
    return fonts

class Typeface:
    """
    creates a typeface instance 
    """
    def __init__ (self, i, name, ratio, serif, weight="regular"):
        self.id = i
        self._name=name
        self.ratio=ratio
        self.serif=serif
        self._weight= weight
        #self.pfont = createFont(self._name+"-"+self._weight, 100)
        typefacePatch = self._name
        if (self._weight != ""):
            typefacePatch+="-"+self._weight
        self.pfont = createFont(typefacePatch, 100)
    
    def __repr__(self):
        return self._name+" ("+self._weight+")"
    
    __str__ = __repr__



    