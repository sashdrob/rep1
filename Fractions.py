from random import randint
from fractions import Fraction
class My_Fraction:
    def __init__(self,num,den):
        self.num=num
        self.den=den
    def __mul__(self,other):
        if type(other)==int:
            return Fraction(self.num * other,self.den)
        else:
            return Fraction(self.num*other.num,self.den*other.den)
    def __truediv__(self, other):
        if type(other)==int:
            return Fraction(self.num,self.den*other)
        else:
            return Fraction(self.num*other.den,self.den*other.num)
    def __str__(self):
        return str(Fraction(self.num,self.den))
    @staticmethod
    def rf(start,end):
        return My_Fraction(randint(start,end),randint(1,end))