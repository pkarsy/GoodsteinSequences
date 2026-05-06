
#!/usr/bin/env python3
import sys

def int_to_hereditary(n,b):
    '''
    Converts an integer to a hereditary representation of a number
    '''
    if n<b:
        return n
    res = []
    exp = 0
    while n != 0:
        n, r = n//b, n%b
        if r > 0:
            if exp==0:
                res.insert(0,r)
            else:
                res.insert( 0, (r,int_to_hereditary(exp,b)) )
        exp += 1
    if len(res)==1:
        return res[0]
    else:
        return res


def hereditary_validate(h, b, canBeList=True):
    '''
    Mainly for debugging, raises an exception if h is not a valid hereditary representation.
    '''
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
            print("debug", h[0], type(h[0]))
            raise Exception(f"The multiplier {h[0]} must be int")
        elif h[0] >= b:
            raise Exception(f"In tuple {h}, the multiplier({h[0]}) must be < {b}")
        elif h[0]<1:
            raise Exception(f"In tuple {h}, the multiplier({h[0]}) must be > 0")
        elif type(h[1])==int and (h[1]<1 or h[1]>=b):
            raise Exception(f"Invalid exponent {h[1]}, must be >0 and <{b}")
        else:
            hereditary_validate( h[1], b )
    elif canBeList and type(h)==list:
        for e in h:
            hereditary_validate(e, b, canBeList=False)
    else:
        raise Exception(f"{h} has invalid type, {type(h)}")

def hereditary_is_zero(h):
    return h == 0

def hereditary_to_int(h, b):
    if type(h)==int:
        return h
    elif type(h)==tuple:
        return h[0]*( b**hereditary_to_int(h[1], b) )
    elif type(h)==list:
        sum=0
        for e in h:
            sum += hereditary_to_int(e, b)
        return sum


def hereditary_to_string(h, b,root=True,showBase=True):
    #hereditary_validate(h, b1)
    if type(h)==int:
        return str(h)
    elif type(h)==tuple:
        if showBase:
            exp=str(b)
        else:
            exp='B'
        exponent_her = hereditary_to_string( h[1], b, False)
        if exponent_her!="1":
            exp += "^"+exponent_her
        if h[0]==1:
            return exp
        else:
            return str(h[0])+"*"+exp
    elif type(h)==list:
        t=[]
        for e in h:
            t.append( hereditary_to_string( e, b, root=False) )
        if root:
            return "+".join(t)
        else:
            return "("+"+".join(t)+")"


def constant(h):
    #hereditary_validate(h, b)
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
        raise Exception(f"hereditary_constant({h}: Unknown error")


def hereditary_sub_one(h, b):
    '''
    Removes 1 from a hereditary represented number.
    Does not increase the base, this is a job of the calling function BEFORE the call
    Tries to do the correct way. Without decomposing the whole representation to int
    This is crucial as even seemingly "innocent" herediaty represented numbers
    like 8^8^8 can have a huge number of digits. If the rightmost element is constant
    removes 1, otherwise goes to the least significant power and decomposes it.
    '''
    # hereditary_validate( h, b )
    if type(h)==int:
        if h>0:
            return h-1
        else:
            raise Exception(f'Cannot remove from 0')
    elif type(h)==tuple:
        # a tuple represents a power B^(int,tuple,list)
        if h[0]==1: # the coefficient is 1
            if h[1]==1: # the exponent is 1, n = 1*B^1 -> B
                return b-1
            else:
                # the exponent is > 1 : result = B^e -1  -> Β*B^(e-1) -1 
                # -> (Β-1)*Β^(e-1)+B^(e-1)-1
                newexp = hereditary_sub_one(h[1],b)
                bpow = (1, newexp)
                bpowminus = hereditary_sub_one(bpow,b)
                if type(bpowminus)==int or type(bpowminus)==tuple:
                    return [(b-1, newexp), bpowminus ]
                elif type(bpowminus)==list:
                    return [(b-1, newexp)] + bpowminus
                else:
                    raise Exception(f'Unknown error')
        else:
            pass
            # c*B^e -1 -> (c-1)*B^e + (B^e -1)
            bpow = (1, h[1])
            bpowminus = hereditary_sub_one(bpow,b)
    else:
        raise Exception(f'The list element must be int or tuple')



def hereditary_sub(h, b, n):
    # hereditary_validate(h, b)
    if type(n)!=int or n<1:
        raise Exception("The subtractor must be an int >= 1")
    if type(h)==int:
        if h<n:
            raise Exception("n > number")
        return h-n
    elif type(h)==tuple:
        if n!=1:
            raise Exception("Cannot do the subtraction, only 1 allowed, with no constant")
        decomp = hereditary_to_int(h, b+1) - 1
        return int_to_hereditary(decomp, b+1)
    elif type(h)==list:
        if type(h[-1])==int:
            if h[-1] < n:
                raise Exception("Cannot subtract more than the constant element")
            elif h[-1] == n:
                h = h[0:-1]
                if len(h)==1:
                    h=h[0]
                return h
            else:
                h1 = h[-1]
                h=h[0:-1]
                h.append(h1-n)
                return h
        else:
            if n==1:
                decomb = hereditary_to_int(h[-1], b+1) - 1
                decomb = int_to_hereditary(decomb,b+1)
                h = h[0:-1]
                if type(decomb)==int or type(decomb)==tuple:
                    h.append(decomb)
                else:
                    h=h+decomb
                return h
            else:
                raise Exception("Cannot do the subtraction, only 1 allowed, with no constant")

def hereditary_trivial_steps(h, b):
    trivialSteps = constant(h)
    if trivialSteps == 0:
        return h
    else:
        return hereditary_sub(h, b,trivialSteps)


class Goodstein:

    def __init__(self, n, b):
        self.__value__ = int_to_hereditary(n,b)
        self.__base__ = b
        self.__initial_value__ = self.__value__
        self.__initial_base__ = self.__base__
    
    def reset(self):
        '''
        Resets the value to the creation time value
        '''
        self.__value__ = self.__initial_value__
        self.__base__ = self.__initial_base__

    def validate(self):
        '''
        Checks if the value is in valid hereditary representation.
        '''
        hereditary_validate(self.__value__, self.__base__)
    
    def is_zero(self):
        '''
        Checks if the value is 0.
        '''
        return self.__value__ == 0
    
    def base(self):
        '''
        Returns the current base.
        '''
        return self.__base__
    
    def value(self):
        return self.__value__

    def __int__(self):
        '''
        Decomposes the hereditary representation to the equal integer value.
        Note that for most representations this operation cannot be done due
        to the sheer size of the numbers
        '''
        return hereditary_to_int(self.__value__, self.__base__)
    
    def __eq__(self, other):
        
        return self.base()==other.base() and str(self) == str(other)
    
    def constant(self):
        return constant(self.__value__)
    
    def step(self,n=1):
        self.__value__ = hereditary_sub(self.__value__, self.__base__, n)
        self.__base__ += n
    
    def trivial_steps(self):
        self.__value__ = hereditary_trivial_steps(self.__value__, self.__base__)
    
    def __str__(self):
        return hereditary_to_string(self.__value__, self.__base__)
    
    def run(self, skip=True, showVal=False, showStep=False, maxBase=1_000_000_000):
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
                print(f"Base={self.base()} : {self} - {int(self)}")
            else:
                print(f"Base={self.base()} : {self}")
            if self.is_zero():
                break
            if self.base()>maxBase:
                print(f"[Limit reached: base {self.base()} exceeds max base {maxBase}. Increase with -b.]")
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate a Goodstein sequence")
    parser.add_argument("initial_value", type=int,
                        help="starting value of the sequence")
    parser.add_argument("initial_base", type=int,
                        help="starting base (e.g. 2)")
    parser.add_argument("-b", "--max-base", type=int, default=1_000_000_000,
                        help="stop when the base exceeds this limit (default: 1_000_000_000)")
    args = parser.parse_args()
    g = Goodstein(args.initial_value, args.initial_base)
    g.run(maxBase=args.max_base)
