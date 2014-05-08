import unittest
from trpy.translate import tokenize, translate

class TestLexer(unittest.TestCase):

    def test_iter(self):
        s = """
a = [1,2,3]

her bir, a icin x
    yazdir x
"""
        tokens = list(tokenize(s))
        code = translate(tokens)
        print code
        assert code == """
a = [1,2,3]

for x in  a:
    print x
"""

    def test_while(self):
        s = """
c = 1
durum, c < 10 iken
    yazdir c
    c += 1
"""
        tokens = list(tokenize(s))
        code = translate(tokens)
        assert code == """
c = 1
while c < 10:
    print c
    c += 1
"""

    def test_conditions(self):
        s = """
eger, x > 10 ve x < 20 ise
   yazdir "10 ile 20 arasinda"
   eger, y < 10 ise
        yazdir m, 20
ya da, x > 30 veya y < 10
    yazdir "x 10 dan buyuk"
ya da,
    yazdir "x 10 dan kucuk"
"""
        tokens = list(tokenize(s))
        code = translate(tokens)
        assert code == """
if x > 10 and x < 20:
   print "10 ile 20 arasinda"
   if y < 10:
        print m, 20
elif x > 30 or y < 10:
    print "x 10 dan buyuk"
else:
    print "x 10 dan kucuk"
"""

    def test_functions(self):
        s = """
x(a, b)->
    <- a * b

x(a, b)->
    y(a, b)->
        <- a, b
    <- a, b

f->
    <- bar
"""
        tokens = list(tokenize(s))
        code = translate(tokens)
        assert code == """
def x(a, b):
    return a * b

def x(a, b):
    def y(a, b):
        return a, b
    return a, b

def f():
    return bar
"""




if __name__ == '__main__':
    unittest.main()
