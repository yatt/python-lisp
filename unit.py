# coding: utf-8
# unit test
import unittest
import lisp

class Lexer_test(unittest.TestCase):
    def setUp(self):
        self.lexer = lisp.Lexer()
    def compare(self, instr, toks):
        x = list(self.lexer.tokenize(instr))
        y = [lisp.Token(*pair) for pair in toks]
        #for n in zip(x,y): print n
        #print ""
        #print ""
        self.assertEqual(x, y)
    def testIntegerConstant(self):
        # 1
        self.compare("1", [("integer", 1)])
    def testFloatConstant(self):
        # 1.0
        self.compare("1.0", [("float", 1.0)])
    def testFloatConstant2(self):
        # 0.1
        self.compare("0.1", [("float", 0.1)])
    def testStringConstant(self):
        # "hello" 
        self.compare('"hello"', [("string", "hello")])
    def testLabelConstant(self):
        # x10
        self.compare("x10", [("label", "x10")])
    def testTrueConstant(self):
        # #t
        self.compare('#t', [("boolean", "#t")])
    def testFalseConstant(self):
        # #f
        self.compare('#f', [("boolean", "#f")])
    def testFuncConstant(self):
        # +
        self.compare('+', [("label", "+")])
    def testSexpr(self):
        # (+ 1 (+ 2 3))
        toks = [("openparen", "("),
                ("label", "+"),
                ("integer", 1),
                ("openparen", "("),
                ("label", "+"),
                ("integer", 2),
                ("integer", 3),
                ("closeparen", ")"),
                ("closeparen", ")"),
                ]
        self.compare("(+ 1 (+ 2 3))", toks)
    def testVariousTypeValues(self):
        #  \t \n  \r (add "string" #t #f literal 1 1.2 + * ) 
        toks = [("openparen", "("),
                ("label", "add"),
                ("string", "string"),
                ("boolean", "#t"),
                ("boolean", "#f"),
                ("label", "literal"),
                ("integer", 1),
                ("float", 1.2),
                ("label", "+"),
                ("label", "*"),
                ("closeparen", ")"),
                ]
        self.compare(' \t \n  \r (add "string" #t #f literal 1 1.2 + * )', toks)
    def testBrancket(self):
        # (if [= 3 3] [+ 1 2] [* 1 2])
        toks = [("openparen", "("),
                ("label", "if"),
                ("openbracket", "["),
                ("label", "="),
                ("integer", 3),
                ("integer", 3),
                ("closebracket", "]"),
                ("openbracket", "["),
                ("label", "+"),
                ("integer", 1),
                ("integer", 2),
                ("closebracket", "]"),
                ("openbracket", "["),
                ("label", "*"),
                ("integer", 1),
                ("integer", 2),
                ("closebracket", "]"),
                ("closeparen", ")"),
                ]
        self.compare("(if [= 3 3] [+ 1 2] [* 1 2])", toks)
    def testComment(self):
        # 2.3 ; hoge
        toks = [("float", 2.3)]
        self.compare("2.3 ; hoge", toks)
    def testUtf8String(self):
        # 日本語
        toks = [("string", u"日本語")]
        self.compare('"日本語"', toks)

class Cell_test(unittest.TestCase):
    pass

class Parser_test(unittest.TestCase):
    pass

class Evaluator_test(unittest.TestCase):
    pass

class Lisp_test(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
