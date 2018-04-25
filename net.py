class Test:
    def __init__(self):
        print("constructed!")


def function(typ):
    a = typ()


function(Test)



