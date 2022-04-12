class A():
    def __init__(self,num):
        self.count = -1
        self.maxnum = num

class B(A):
    def __init__(self,name):
        self.name = name
        super().__init__()

b = B('ivan')
print(b.maxnum)


