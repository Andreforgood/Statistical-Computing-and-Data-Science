import os
import inspect
import termcolor
import time
import matplotlib.pyplot as plt
import numpy
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

def roc(y_test,y_prob):
    fpr, tpr, threshold = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.title('ROC Curve')
    plt.show()

def getObjectType(obj):
    if inspect.isabstract(object):  return "isabstract"
    if inspect.isasyncgen(object):  return "isasyncgen"
    if inspect.isasyncgenfunction(object):  return "isasyncgenfunction"
    if inspect.isawaitable(object):  return "isawaitable"
    if inspect.isbuiltin(object):  return "isbuiltin"
    if inspect.isclass(object):  return "isclass"
    if inspect.iscode(object):  return "iscode"
    if inspect.iscoroutine(object):  return "iscoroutine"
    if inspect.iscoroutinefunction(object):  return "iscoroutinefunction"
    if inspect.isdatadescriptor(object):  return "isdatadescriptor"
    if inspect.isframe(object):  return "isframe"
    if inspect.isfunction(object):  return "isfunction"
    if inspect.isgenerator(object):  return "isgenerator"
    if inspect.isgeneratorfunction(object):  return "isgeneratorfunction"
    if inspect.isgetsetdescriptor(object):  return "isgetsetdescriptor"
    if inspect.ismemberdescriptor(object):  return "ismemberdescriptor"
    if inspect.ismethod(object):  return "ismethod"
    if inspect.ismethoddescriptor(object):  return "ismethoddescriptor"
    if inspect.ismodule(object):  return "ismodule"
    if inspect.isroutine(object):  return "isroutine"
    if inspect.istraceback(object):  return "istraceback"
    return "unknown"

def peeksource(func):
    try:
        if callable(func): 
            lines=inspect.getsourcelines(func)[0]
            codes=[]
            for r in lines:
                r=r.rstrip('\n')
                r0=r.lstrip().rstrip()
                codes.append(r)
        else: 
            stype=str(type(func))
            if stype[:8]=="<class '":
                stype=stype[8:stype.rfind('.')]
                stype=stype.replace('.','\\')+'.py'
                print(termcolor.colored("<<<<<<<< "+stype+" >>>>>>>>", color='green'))
                print()
                fn=os.getcwd()+'\\'+stype
                if os.path.exists(fn):
                    with open(fn,'r') as fin:
                        codes=[line.rstrip('\n') for line in fin]
                else:
                    raise Exception('File not found') 
            else:
                raise Exception('Unrecognized object') 

        isQuoteBlock=False
        for r in codes:
            r0=r.lstrip().rstrip()
            if r0[0:1]=="#":
                print(termcolor.colored(r, color='red'))
            elif r0.count('"""')==1 or r0.count("'''")==1:
                print(termcolor.colored(r, color='red'))
                isQuoteBlock= not isQuoteBlock
            elif r0.count('"""')==2 or r0.count("'''")==2:
                print(termcolor.colored(r, color='red'))
                isQuoteBlock= False
            else:
                if isQuoteBlock: 
                    print(termcolor.colored(r, color='red'))
                else: 
                    print(termcolor.colored(r, color='grey'))
    except:
        print("The source file of type", getObjectType(func)[2:], "can not be located")
    finally:
        print(termcolor.colored("<<<<<<<< END >>>>>>>>", color='green'))
    
    
sprint=peeksource
    
def getTime(func):
    def wrapper(*args, **kwargs):
        t0=time.time()    
        func(*args, **kwargs)
        print('execution time:', time.time()-t0, "s")
    return wrapper

time_base=0
time_current=0

def initTime():
    global time_base, time_current
    time_current=time_base=time.time()

def showTime(label=''):
    global time_current, time_base
    if label!='': label='for '+label
    print('>> Execution time '+label+': %.4f s  Total elapse time %.4f s' 
          % (time.time()-time_current, time.time()-time_base ))
    time_current=time.time()

inittime=initTime
showtime=showTime


def prs(*args, **kwargs):
    #print("unnamed args:", args)
    #print("keyword args:", kwargs)
    for x in args:
        print('===', type(x), '===')
        print(x)
        print()

    for k in kwargs:
        x=kwargs[k]
        print('===', k, '===')
        print(x)
        print()

# Standardize features
def standardize(df, numeric_only=True):
    if numeric_only is True:
    # find non-boolean columns
        cols = df.loc[:, df.dtypes != 'uint8'].columns
    else:
        cols = df.columns
    for field in cols:
        mean, std = df[field].mean(), df[field].std()
        # account for constant columns
        if np.all(df[field] - mean != 0):
            df.loc[:, field] = (df[field] - mean) / std
    return df