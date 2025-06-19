

def hereditary(n,b):
    if n<b:
        return (n,b)
    res = []
    exp = 0
    while n != 0:
        n, r = n//b, n%b
        if r > 0:
            if exp==0:
                res.insert(0,r)
            else:
                res.insert( 0, (r,hereditary(exp,b)[0]) )
        exp += 1
    if len(res)==1:
        return (res[0],b)
    else:
        return (res,b)


def validate(hb, canBeList=True): #(h,b)
    if type(hb)!=tuple or len(hb)!=2:
        raise Exception(f"Expected tuple (her_repr, base)")
    h, b = hb[0], hb[1]
    if type(b) != int or b<2:
        raise Exception("The base must be an integer >= 2")
    elif type(h)==int:
        if h>=b:
            raise Exception(f"The constant {h} must be < {b}")
        if not canBeList and h<1:
            raise Exception(f"The constant {h} must be >0")
        if h<0:
            raise Exception(f"The constant {h} must be >=0")
    elif type(h)==tuple:
        if len(h)!=2:
            raise Exception(f"The tuple {h} must have 2 elements")
        elif type(h[0])!=int:
            raise Exception(f"The multiplier {h[0]} must be int")
        elif h[0] >= b:
            raise Exception(f"In tuple {h}, the multiplier({h[0]}) must be < {b}")
        elif h[0]<1:
            raise Exception(f"In tuple {h}, the multiplier({h[0]}) must be > 0")
        elif type(h[1])==int and (h[1]<1 or h[1]>=b):
            raise Exception(f"Invalid exponent {h[1]}, must be >0 and <{b}")
        else:
            validate( (h[1], b) )
    elif canBeList and type(h)==list:
        for e in h:
            validate((e, b), canBeList=False)
    else:
        raise Exception(f"{h} has invalid type, {type(h)}")

def is_zero(hb):
    if type(hb)==tuple and hb[0]==0:
        return True
    else:
        return False

def to_int(hb):
    h,b = hb[0],hb[1]
    if type(h)==int:
        return h
    elif type(h)==tuple:
        return h[0]*(b**to_int((h[1],b)))
    elif type(h)==list:
        sum=0
        for e in h:
            sum+=to_int((e,b))
        return sum


def to_string(hb,root=True,showBase=True):
    #hereditary_validate(hb)
    h, b = hb[0], hb[1]
    if type(h)==int:
        return str(h)
    elif type(h)==tuple:
        exp=str(b)
        exponent_her = to_string( (h[1],b), False)
        if exponent_her!="1":
            exp += "^"+exponent_her
        if h[0]==1:
            return exp
        else:
            return str(h[0])+"*"+exp
    elif type(h)==list:
        t=[]
        for e in h:
            t.append( to_string( (e,b), root=False) )
        if root:
            return "+".join(t)
        else:
            return "("+"+".join(t)+")"


def constant(hb):
    #hereditary_validate(hb)
    h, b = hb[0], hb[1]
    if type(h)==int:
        return h
    elif type(h)==list:
        last=h[-1]
        if type(last)==int:
            return last
        else:
            return 0
    elif type(h)==tuple:
        return 0
    else:
        raise Exception(f"hereditary_constant({h}, {b}: Unknown error")


def step(hb, n):
    validate(hb)
    h,b=hb[0],hb[1]
    if n==-1:
        n=constant(hb)
    if type(n)!=int or n<1:
        raise Exception("The subtractor must be an int >= 1")
    if type(h)==int:
        if h<n:
            raise Exception("n > number")
        return (h-n, b+n)
    elif type(h)==tuple:
        if n!=1:
            raise Exception("Cannot do the subtstraction, only 1 allowed, with no constant")
        decomp = to_int((h,b+1)) - 1
        return hereditary(decomp,b+1)
    elif type(h)==list:
        if type(h[-1])==int:
            if h[-1] < n:
                raise Exception("Cannot subtract more than the constant element")
            elif h[-1] == n:
                h = h[0:-1]
                if len(h)==1:
                    h=h[0]
                return(h, b+n)
            else:
                h1 = h[-1]
                h=h[0:-1]
                h.append(h1-n)
                return (h,b+n)
        else:
            if n==1:
                decomb = to_int((h[-1],b+1)) - 1
                decomb = hereditary(decomb,b+1)[0]
                h = h[0:-1]
                if type(decomb)==int or type(decomb)==tuple:
                    h.append(decomb)
                else:
                    h=h+decomb
                return (h,b+1)
            else:
                raise Exception("Cannot do the subtstraction, only 1 allowed, with no constant")

def trivial_steps(hb):
    trivialSteps = constant(hb)
    if trivialSteps == 0:
        return hb
    else:
        return step(hb,trivialSteps)


class Goodstein:

    def __init__(self,n,b):
        self.hb = hereditary(n,b)
        self.__initial_value = self.hb
    
    def reset(self):
        self.hb = self.__initial_value

    def validate(self):
        validate(self.hb)
    
    def is_zero(self):
        return is_zero(self.hb)
    
    def base(self):
        return self.hb[1]
    
    def to_int(self):
        return to_int(self.hb)
    
    def to_string(self):
        return to_string(self.hb)
    
    def constant(self):
        return constant(self.hb)
    
    def step(self,n):
        self.hb = step(self.hb, n)
    
    def trivial_steps(self):
        self.hb = trivial_steps(self.hb)
    
    def print(self):
        print( to_string(self.hb) )
    
    def run(self,skip=True,showVal=False,showStep=False,maxBase=1_000_000_000):
        def showstp(c):
            if self.constant()==0:
                print('[Decomposing]')
            if not showStep:
                if c>1:
                    print("...")
                return
            fmt=f"We replace base {self.base()} with {self.base()+c} and we remove {c}"
            if c==1:
                print(fmt)
            else:
                print ("[Multiple steps]:",fmt)
        while True:

            if showVal:
                print(f"Base={self.base()} : {self.to_string()} - {self.to_int()}")
            else:
                print(f"Base={self.base()} : {self.to_string()}")
            if self.is_zero():
                break
            c = self.constant()
            if c+4 > self.base():
                showstp(1)
                self.step(1)
            elif c>5:
                showstp(c-3)
                self.step(c-3)
            else:
                showstp(1)
                self.step(1)
