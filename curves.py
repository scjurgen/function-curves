import math
import re
import subprocess

# from math import *
import sys

with open('response.plot', "r") as f:
    plotTemplate = f.read()
with open('response_multi.plot', "r") as f:
    plotTemplateMulti = f.read()
indexhtml = '<head></head><body>'


def mathDict():
    d = {
        "pow": math.pow, "cos": math.cos, "sin": math.sin, "asin": math.asin, "acos": math.acos, "pi": math.pi,
        "tan": math.tan, "tanh": math.tanh, "atan": math.atan, "sqrt": math.sqrt, "log": math.log,
        "log10": math.log10, "exp": math.exp, "cosh": math.cosh, "acosh": math.acosh,
        "erf": math.erf
    }
    return d


def similarList(l: list, s: list) -> bool:
    for i in range(len(l)):
        if l[i] is None:
            return False
        if s[i] is None:
            return False
        if math.fabs(l[i] - s[i]) > 0.0001:
            return False
    return True


class Curve:
    def __init__(self):
        self.funcPairs = []
        self.results = []

    def createCrossPlot(self, name: str, funcMath1: str, funcMath2: str, precondition1: str, precondition2: str):
        global indexhtml
        print(name)
        func1 = funcMath1
        preCon1Str = ""
        preCon2Str = ""
        if precondition1 != "":
            preCon1Str = "a={}\\n".format(precondition1)
        if precondition2 != "":
            preCon2Str = "a={}\\n".format(precondition2)
        if funcMath2 is not None:
            func2 = funcMath2
            title = "{}nx={}\\n{}y={}".format(preCon1Str, funcMath1, preCon2Str, funcMath2)
            basic = 0
        else:
            func2 = None
            title = "{}y={}".format(preCon1Str, funcMath1)
            basic = 1

        deltaIntegral = 0
        lastValue = 0
        integral = 0.0
        startPoints = []
        with open("curve.csv", "w") as fOut:
            for i in range(-100, 101):

                x = i / 100.0
                y = None
                try:
                    if precondition1 is not None:
                        if precondition1 != "":
                            aFactor = eval(precondition1)
                        else:
                            aFactor = 1
                    y = eval(func1, mathDict(), {"a": aFactor, "x": x})
                    if funcMath2 is not None:
                        if precondition2 is not None:
                            if precondition2 != "":
                                aFactor = eval(precondition2)
                            else:
                                aFactor = 1
                        y = eval(func2, mathDict(), {"a": aFactor, "x": y})
                    integral += y
                    deltaIntegral += y - lastValue
                    lastValue = y
                    fOut.write("{}\t{}\n".format(x, y))
                except Exception as e:
                    print(e)
                if i in [-100, 0, 100]:
                    startPoints.append(y)

        niceRange = similarList(startPoints, [-1, 0, 1]) or similarList(startPoints, [1, 0, -1])
        goodRange = similarList(startPoints[1:], [0, 1]) or similarList(startPoints[1:], [1, 0])
        color = '#009900'
        if niceRange:
            color = '#990000'
        elif goodRange:
            color = '#000099'
        filename = "images/{}.png".format(name.replace("^", "_"))
        with open("temp.plot", "w") as fTmpl:
            fTmpl.write(plotTemplate.format(filename=filename, title=title, color=color))
        subprocess.call("gnuplot temp.plot", shell=True)
        self.results.append([integral, deltaIntegral, filename, basic, niceRange, goodRange])

    def addfunction(self, includeCross: str, name: str, func: str, precondition: str):
        self.funcPairs.append([name, func, precondition, includeCross])

    def runAll(self):
        for name, func, precondition1, cross1 in self.funcPairs:
            self.createCrossPlot(name, func, None, precondition1, None)
        for name1, func1, precondition1, cross1 in self.funcPairs:
            if cross1 == "#":
                for name2, func2, precondition2, cross2 in self.funcPairs:
                    if cross2 == "#":
                        self.createCrossPlot(name1 + name2, func1, func2, precondition1, precondition2)

        self.results.sort(key=lambda x: (x[3], x[0], x[1], x[2]), reverse=True)
        indexhtml = ""
        for item in self.results:
            indexhtml += '<img src="{}" alt="{}" />\n'.format(item[2], item[2])

        with open('index.html', "w") as fHtml:
            fHtml.write(indexhtml)


class ParamtricCurve:
    def __init__(self):
        self.funcPairs = []
        self.results = []

    def done(self):
        indexhtml = ""
        for image in self.results:
            indexhtml += '<img src="{}" alt="{}" />\n'.format(image,image)

        with open('index_parametric.html', "w") as fHtml:
            fHtml.write(indexhtml)

    def createPlot(self, name: str, funcMath1: str, min:int, param_a: list):
        global indexhtml
        func1 = funcMath1
        func2 = None
        title = "y={}".format(funcMath1)
        basic = 1

        with open("curve.csv", "w") as fOut:
            for i in range(min*100, 101):
                x = i / 100.0
                fOut.write("{}".format(x))
                y = None
                for a in param_a:
                    try:
                        y = eval(func1, mathDict(), {"a": a, "x": x})
                        fOut.write("\t{}".format(y))
                    except Exception as e:
                        print("f={} x={} a={} :  {}".format(funcMath1, x,a,e))
                fOut.write("\n")
        plot = "'curve.csv' using 1:{idx} smooth mcspline  title \"{title}\""
        plotAdd = ""
        i = 1
        for a in param_a:
            if i != 1:
                plotAdd += ","
            plotAdd += plot.format(idx=i + 1, title=str(a))

            i += 1
        filename = "images/parametric_{}.png".format(name.replace("^", "_"))
        self.results.append(filename)
        with open("temp.plot", "w") as fTmpl:
            fTmpl.write(plotTemplateMulti.format(minrange=min-0.1, filename=filename, title=title, plot=plotAdd))
        subprocess.call("gnuplot temp.plot", shell=True)


pcurve = ParamtricCurve()
oddIntParams = [1, 3, 5, 7, 9, 11, 13]
atanValues = [ 0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000]
expos = []
for i in range(-10, 10):
    if i != 0:
        expos.append(math.pow(2, i))

pcurve.createPlot("atan_n", "atan(x*a)/atan(a)", -1, atanValues)
pcurve.createPlot("erf", "erf(x*a)", -1, [0.1, 0.5, 1,1.5, 2, 3, 4, 5, 7, 9, 11, 13])
pcurve.createPlot("x^n", "pow(x-0.5,a)*(pow(2,(a-1)))+0.5", 0, oddIntParams)
pcurve.createPlot("x^n-1_1", "pow(x,a)", -1,  [1, 3, 5, 7, 9, 11, 13])
pcurve.createPlot("tanh", "tanh(x*a)/tanh(a)", -1,  [1, 2, 3, 5, 7, 9, 11, 13])
pcurve.createPlot("sigmoid_n", "(atan(x*2*a-a)-atan(-a))/atan(a)/2", 0,  [0.5, 1, 2, 3, 5, 7, 9, 11, 13])
pcurve.createPlot("log0_1", "log(abs(x*a)+1)/log(a+1)", 0,  [0.1, 0.5, 1, 2, 10, 50, 100, 1000, 10000])
pcurve.createPlot("exp", "(pow(a,x-1)-pow(a,-1))*a/(a-1)", 0,  expos)
pcurve.createPlot("exp2", "(pow(a,sin(x*pi/2)-1)-pow(a,-1))*a/(a-1)", 0,  expos)

pcurve.done()


sys.exit(0)

curve = Curve()

curve.addfunction("", "x", "x", "")
curve.addfunction("", "x1", "1-x", "")
curve.addfunction("", "sin2", "sin(x*pi/2)", "")
curve.addfunction("", "cos1", "(-cos(x*pi)+1)/2", "")

curve.addfunction("#", "x^3", "pow(x-0.5,a)*(pow(2,(a-1)))+0.5", "3")

curve.addfunction("", "x^5", "pow(x-0.5,a)*(pow(2,(a-1)))+0.5", "5")
curve.addfunction("", "x^11", "pow(x-0.5,a)*(pow(2,(a-1)))+0.5", "11")
curve.addfunction("#", "sqr", "x*x", "")
curve.addfunction("#", "cube", "x*x*x", "")
curve.addfunction("#", "sigmoid1", "(atan(x*2*a-a)-atan(-a))/atan(a)/2", "1")
curve.addfunction("", "sigmoid5", "(atan(x*2*a-a)-atan(-a))/atan(a)/2", "5")
curve.addfunction("", "atan1", "atan(x*a)/atan(a)", "1")
curve.addfunction("#", "atan2", "atan(x*a)/atan(a)", "2")
curve.addfunction("", "atan10", "atan(x*a)/atan(a)", "10")
curve.addfunction("", "atan100", "atan(x*a)/atan(a)", "100")
curve.addfunction("#", "log", "log(x+1)/log(2)", "")
curve.addfunction("", "tan1", "tan(x*a)/tan(a)", "1")
curve.addfunction("", "tan1.3", "tan(x*a)/tan(a)", "1.3")
curve.addfunction("#", "tan1.5", "tan(x*a)/tan(a)", "1.5")
curve.addfunction("", "asin2", "asin(x*2-1)/pi+0.5", "")
curve.addfunction("", "halfcircle", "sqrt(1-x*x)", "")
curve.addfunction("", "quarter", "sqrt(1-(x-1)*(x-1))", "")
curve.addfunction("", "sqrtdivx3", "sqrt(1-pow(-x+1,a))", "3")
curve.addfunction("", "sqrtdivx11", "sqrt(1-pow(-x+1,a))", "11")
curve.addfunction("", "triangle2", "(asin(-cos(x*pi*a))/pi*2+1)/2", "2")
curve.addfunction("", "trianglerev", "(asin(cos(x*pi*a))/pi*2+1)/2", "2")
curve.addfunction("", "triangle3", "(asin(-cos(x*pi*a))/pi*2+1)/2", "3")

curve.runAll()
