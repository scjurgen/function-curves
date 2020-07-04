import math
import re
import subprocess

with open('response.plot', "r") as f:
    plotTemplate = f.read()

indexhtml = '<head></head><body>'

class Curve:
    def __init__(self):
        self.funcPairs = []
        self.results = []


    def createCrossPlot(self, name: str, funcMath1: str, funcMath2: str):
        global indexhtml
        print(name)
        func1 = re.sub(r'([a-z]{2,})', "math.\\1", funcMath1)
        func1 = re.sub(r'x', '{x}', func1)
        if funcMath2 is not None:
            func2 = re.sub(r'([a-z]{2,})', "math.\\1", funcMath2)
            func2 = re.sub(r'x', '{x}', func2)
            title = "x={}\\ny={}".format(funcMath1, funcMath2)
            basic = 0
        else:
            func2 = None
            title = funcMath1
            basic = 1
        deltaIntegral = 0
        lastValue = 0
        integral = 0.0
        with open("curve.csv", "w") as fOut:

            for i in range(0, 101):
                x = i / 100.0
                result = eval(func1.format(x=x))
                if funcMath2 is not None:
                    result = eval(func2.format(x=result))
                integral += result
                deltaIntegral += result-lastValue
                lastValue = result
                fOut.write("{}\t{}\n".format(x, result))
        filename = "images/{}.png".format(name.replace("^", "_"))

        with open("temp.plot", "w") as fTmpl:
            fTmpl.write(plotTemplate.format(filename=filename, title=title))
        subprocess.call("gnuplot temp.plot", shell=True)
        self.results.append([integral, deltaIntegral, filename, basic])

    def addfunction(self, name: str, func: str):
        self.funcPairs.append([name, func])

    def runAll(self):
        for name, func in self.funcPairs:
            self.createCrossPlot(name, func, None)
        for name1, func1 in self.funcPairs:
            for name2, func2 in self.funcPairs:
                self.createCrossPlot(name1 + name2, func1, func2)
        self.results.sort(key=lambda x: (x[3], x[0], x[1], x[2]), reverse=True)
        indexhtml = ""
        for item in self.results:
            indexhtml += '<img src="{}" />\n'.format(item[2])

        with open('index.html', "w") as fHtml:
            fHtml.write(indexhtml)


curve = Curve()

curve.addfunction("x", "x")
curve.addfunction("x1", "1-x")
curve.addfunction("sin2", "sin(x*pi/2)")
curve.addfunction("cos1", "(-cos(x*pi)+1)/2")

curve.addfunction("x^3", "pow(x-0.5,3)*(pow(2,(3-1)))+0.5")
curve.addfunction("x^5", "pow(x-0.5,5)*(pow(2,(5-1)))+0.5")
curve.addfunction("x^11", "pow(x-0.5,11)*(pow(2,(11-1)))+0.5")
curve.addfunction("sqr", "x*x")
curve.addfunction("cube", "x*x*x")
curve.addfunction("sigmoid1", "(atan(x*2-1)-atan(-1))/atan(1)/2")
curve.addfunction("sigmoid5", "(atan(x*10-5)-atan(-5))/atan(5)/2")
curve.addfunction("atan1", "atan(x)/atan(1)")
curve.addfunction("atan2", "atan(x*2)/atan(2)")
curve.addfunction("atan10", "atan(x*10)/atan(10)")
curve.addfunction("atan100", "atan(x*100)/atan(100)")
curve.addfunction("log", "log(x+1)/log(2)")
curve.addfunction("tan1", "tan(x)/tan(1)")
curve.addfunction("tan1.3", "tan(x*1.3)/tan(1.3)")
curve.addfunction("tan1.5", "tan(x*1.5)/tan(1.5)")
curve.addfunction("asin2", "asin(x*2-1)/pi+0.5")
curve.addfunction("quarter", "sqrt(1-(x-1)*(x-1))")
curve.addfunction("sqrtdivx3", "sqrt(1-pow(-x+1,3.0))")
curve.addfunction("sqrtdivx11", "sqrt(1-pow(-x+1,11.0))")
curve.addfunction("triangle2", "(asin(-cos(x*pi*2))/pi*2+1)/2")
curve.addfunction("trianglerev", "(asin(cos(x*pi*2))/pi*2+1)/2")
curve.addfunction("triangle3", "(asin(-cos(x*pi*3))/pi*2+1)/2")

curve.runAll()
