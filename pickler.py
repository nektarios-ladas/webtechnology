import pickle

def dumpObject(obj,filename):
    pickle.dump( obj, open( filename, "wb" ) )

def loadObject(filename):
    obj=pickle.load(open(filename,"rb"))
    return obj

def test():
    favorite_color = { "lion": "yellow", "kitty": "red" }
    dumpObject(favorite_color,"d:/webtechnology/test_pickle.p")
    obj=loadObject("d:/webtechnology/test_pickle.p")
    print(obj)


test()
