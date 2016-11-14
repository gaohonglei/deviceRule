def ToCheckFun(t):
    return lambda x:isinstance(x,t)
def fun(*args,**kwargs):
    ty=map(ToCheckFun,args)
    argv=dict((i,ToCheckFun(kwargs[i]))for i in kwargs)
    def dec(function):
        def _fun(*fun_x,**fun_y):
            if ty:
                x_list=[a for a in fun_x]
                x_list_it=iter(x_list)
                result=[]
                for t_check in ty:
                    r=t_check(x_list_it.next())
                    result.append(r)
                print "parm check result:",result
            if argv:
                y_dict=dict((i,fun_y[i]) for i in fun_y)
                result={}
                for k in argv.keys():
                    f=argv[k](y_dict.get(k))
                    result[k]=f
                print "parm check result:", result
            return function(*fun_x,**fun_y)
        return _fun
    return dec
@fun(int,int,c=int)
def fun1(a,b,c):
    return a,b,c

def binarySearch(l,k):
    length=len(l)
    low=0
    hight=length-1
    while(low<hight):
        mid=(low+hight)/2
        if l[mid]==k:
            return k
        else:
            if l[mid]<k:
                low=k+1
            else:
                hight=k-1
def qsort1(l,low,hight):
    while l<low:
        if l[low]>l[hight]:
            tmp=l[hight]
            l[hight]=l[low]
            l[low]=l[hight]
        else:
            pass

def qsort(seq):
    if seq==[]:
        return []
    else:
        pivot=seq[0]
        lesser=qsort([x for x in seq[1:] if x<pivot])
        greater=qsort([x for x in seq[1:] if x>=pivot])
        return lesser+[pivot]+greater

class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))

def lookup(root):
    stack = [root]
    while stack:
        current = stack.pop(0)
        print current.data
        if current.left:
            stack.append(current.left)
        if current.right:
            stack.append(current.right)

def deep(root):
    if not root:
        return
    print root.data
    deep(root.left)
    deep(root.right)
def preorder(tree):
    print(tree.data)
    if tree.left:
        preorder(tree.left)
    if tree.right:
        preorder(tree.right)
def lastorder(tree,a,k1,k2):
    if not tree:
        return
    if tree:
        if tree.data==k1:
            a.append(tree)
            lastorder(tree.right,a,k1,k2)
        else:
            lastorder(tree.left,a,k1,k2)
            lastorder(tree.right,a,k1,k2)
        print(tree.data)
def parents(tree,k1,k2):
    a=[]
    lastorder(tree,a,k1,k2)
def find(a,k):
    length=len(a)
    low=0
    hight=length-1
    while(low<=hight):
        mid=(low+hight)/2
        if(a[mid]<k):
            low=mid+1
        if(a[mid]>k):
            hight=mid-1
        if(a[mid]==k):
            return mid
    return -1
if __name__ == '__main__':
    #lookup(tree)
    #print(1111111111111111111111)
    #deep(tree)
   # preorder(tree)
   lastorder(tree)
    # a=[1,3,5,6,7,9,14,17,19]
    # print(find(a,20))




