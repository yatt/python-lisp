# coding: utf-8
# 多倍長整数とGCを実装しなくて済むのが楽。
# TODO: 末尾再帰の最適化の実装
# TODO: 継続の実装
# TODO: マクロの実装?
# TODO: readlineライブラリを用いた入力
# TODO: 変数はutf-8
# TODO: letrec

import os
import sys
import string
import operator
import time

"""
rule := sexp+
sexp := exp | ( sexp+ ) | [ sexp+ ] | ( exp . exp ) | '( exp )
exp := literal | sexp
literal := integer | float | string | label | boolean | nil
integer := [1-9][0-9]*
float := [0-9].[0-9]+
string := "[^"]*"
label := [a-zA-z+-*/%!=][a-zA-z+-*/%!=0-9]*
"""

class Label(str):
    def __init__(self, label):
        str.__init__(label)
    def __repr__(self):
        return str(self)

class Str(unicode):
    def __init__(self, st):
        unicode.__init__(st)
    def __repr__(self):
        return unicode.__repr__(self)

class Token(object):
    def __init__(self, tokentype, token):
        self.type = tokentype
        self.token = token
    def __repr__(self):
        #return "<'%s', type '%s'>" % (self.token, self.type)
        return "('%s', '%s')" % (self.token, self.type)
    def __eq__(self, t):
        # ユニットテストのために追加
        return self.type == t.type and self.token == t.token

class Lexer(object):
    tokentypes = ["openparen", "closeparen", "openbracket", "closebracket", "integer", "float", "string", "boolean", "label", "dot", "quote"]
    def topenparen(self):
        self.index += 1
        return Token("openparen", '(')
    def tcloseparen(self):
        self.index += 1
        return Token("closeparen", ')')
    def topenbracket(self):
        self.index += 1
        return Token("openbracket", '[')
    def tclosebracket(self):
        self.index += 1
        return Token("closebracket", ']')
    def tnumber(self):
        # integer,float両方をパース
        end = self.index
        isfloat = False
        sign = 1
        ch = self.input[end]
        if ch in "-+":
            end += 1
            ch = self.input[end]
        while True:
            if ch == '.':
                if isfloat:
                    raise Exception("invalid float literal")
                isfloat = True
            elif not ch.isdigit():
                break
            end += 1
            ch = self.input[end:end+1] # 空文字列でも正常に動作
        ttype = "float" if isfloat else "integer"
        castf = float   if isfloat else int
        t = Token(ttype, castf(self.input[self.index:end]))
        self.index = end
        return t
    def tstring(self):
        endindex = self.input.index('"', self.index+1)
        seg = self.input[self.index+1: endindex]
        lst = [ch for ch in seg]
        i = 0
        while i < len(lst):
            if lst[i] == '\\':
                lst[i] = {'n': '\n', 't': '\t', 'r': '\r'}[lst[i+1]]
                lst[i+1:] = lst[i+2:]
            i += 1
        seg = ''.join(lst)
        tok = Str(seg)
        t = Token("string", tok)
        self.index = endindex + 1
        return t
    def ttrue(self):
        self.index += 2
        return Token("boolean", "#t")
    def tfalse(self):
        self.index += 2
        return Token("boolean", "#f")
    def tlabel(self, firstIsSymbol=True):
        end = self.index
        table = string.letters + "_+-*/%!?=<>" + string.digits
        if not firstIsSymbol:
            table += string.digits
        ch = self.input[end:end+1]
        while ch in table:
            end += 1
            ch = self.input[end:end+1] # 空文字列でも動作
            if ch == '': break
        t = Token("label", Label(self.input[self.index: end]))
        self.index = end
        return t
    def tdot(self):
        self.index += 1
        return Token("dot", ".")
    def tquote(self):
        self.index += 1
        return Token("quote", "'")
    def tokenize(self, input):
        self.input = input
        self.index = 0
        while self.index != len(self.input):
            first = self.input[self.index]
            if first.isspace(): 
                self.index += 1
                continue
            if first == ';':
                lst = []
                while True:
                    if first in ['\n', ""]:
                        break
                    lst.append(first)
                    self.index += 1
                    first = self.input[self.index:self.index+1]
                #print "comment: '" + "".join(lst) + "'"
                continue
            elif first == '(': yield self.topenparen()
            elif first == ')': yield self.tcloseparen()
            elif first == '[': yield self.topenbracket()
            elif first == ']': yield self.tclosebracket()
            elif first in ['+', '-']:
                nextch = self.input[self.index+1:self.index+2]
                if nextch.isdigit():
                    yield self.tnumber()
                else:
                    yield self.tlabel()
            elif first in "_+-*/%!?=<>": yield self.tlabel(True)
            elif first.isdigit(): yield self.tnumber()
            elif first == '"': yield self.tstring()
            elif first == "'": yield self.tquote()
            elif first == '.': yield self.tdot()
            elif first == '#':
                mark  = self.input[self.index+1:self.index+2]
                if   mark == "t": yield self.ttrue()
                elif mark == "f": yield self.tfalse()
            elif first.isalpha():
                yield self.tlabel()
            else:
                raise Exception(u"invalid token")

class Cell(object):
    literalreprs = ["()", "#t", "#f"]
    # コンスセル
    def __init__(self, car, cdr=None, isLabel=False):
        self.car = car
        self.cdr = cdr
        self._isLabel = isLabel
    def cons(self, tree):
        self.cdr = tree
        return self
    def isNil(self):
        return self.car is None and self.cdr is None
    def isLabel(self):
        return self._isLabel
    def __repr__(self):
        return "(" + self.__repr1__() + ")"
    def xrepr(self, x):
        if x is None:  return "()"
        elif x is True:  return "#t"
        elif x is False: return "#f"
        else: return repr(x)
    def __repr1__(self):
        # print car
        lst = [self.xrepr(self.car)]
        add = lambda x: lst.append(x)
        if not (self.cdr is None):
            if not isinstance(self.cdr, Cell):
                add(".")
                add(self.xrepr(self.cdr))
            else:
                cell = self.cdr
                while True:
                    if cell is None:
                        break
                    if type(cell) in [int, float, Str]:
                        add(".")
                        add(repr(cell))
                        break
                    add(self.xrepr(cell.car))
                    cell = cell.cdr
        return " ".join(lst)
    def listitems(self):
        ref = self
        while ref != nil:
            yield ref.car
            ref = ref.cdr
    def zip(self, values):
        retval = nil
        for key,value in zip(self.listitems(), values.listitems()):
            retval = Cell(Cell(key, value), retval)
        return retval
    def append(self, cells):
        ref = self
        while ref.cdr != nil:
            ref = ref.cdr
        ref.cons(cells)
        return self

nil = None
true = True
false = False


class Parser(object):
    literal = ["integer", "float", "string", "label", "boolean"]
    class StopList(Exception): pass
    class Dot(Exception): pass
    def parse(self, tokenseq):
        self.seq = tokenseq
        t = self.seq.next()
        def raiseStopList(): raise Parser.StopList(t.type)
        def raiseDot(): raise Parser.Dot(t.type)
        tokentypes = {
            "openparen": lambda: self.exp(t.type),
            "openbracket": lambda: self.exp(t.type),
            "boolean": lambda: [true, false][["#t", "#f"].index(t.token)],
            "integer": lambda: t.token,
            "float":   lambda: t.token,
            "string":  lambda: t.token,
            "label":   lambda: t.token,
            "quote":   lambda: self.quote(),
            "dot": lambda: raiseDot(),
            "closeparen": lambda: raiseStopList(),
            "closebracket": lambda: raiseStopList(),
        }
        for ttype in tokentypes:
            if t.type == ttype:
                return tokentypes[ttype]()
        raise Exception("invalid syntax")
    def exp(self, starttype):
        if starttype == "openparen":    end = "closeparen"
        if starttype == "openbracket": end = "closebracket"
        c = Cell(None)
        ref = c
        try:
            x = self.parse(self.seq)
            ref.car = x
        except Parser.StopList, e:
            return nil

        try:
            x = self.parse(self.seq)
            y = Cell(x)
            ref.cons(y)
            ref = y
        except Parser.StopList, e:
            return c
        except Parser.Dot, e:
            # dot notation
            follow = self.parse(self.seq)
            ref.cons(follow)
            return c

        while True:
            try:
                x = self.parse(self.seq)
                y = Cell(x)
                ref.cons(y)
                ref = y
            except Parser.StopList, e:
                break
        return c
    def quote(self):
        return Cell(Label("quote"), Cell(self.parse(self.seq)))


class Evaluator(object):
    """
    builtin function:
        cons
        car
        cdr
        eq?
        lambda
        and
        or
        list
        display
        print
        newline
        load
        =
        <
        +,-,*,/
        eval-python-string
        exec-python-string
    special form:
        eval
        define
        quote
        if
        cond
        begin
        time : 時間測定
    """
    def __init__(self):
        # 変数格納
        self.environ = nil
        # 再帰呼び出し回数の上限
        self.recursionLimit = 700
        #self.recursionLimit = 10
        self.recursionDepth = 0
        self.builtins = {
            "cons": self.onCons,
            "car": self.onCar,
            "cdr": self.onCdr,
            "eq?": self.onEq,
            "apply": self.onApply,
            "list": self.onList,
            "display": self.onDisplay,
            "newline": self.onNewline,
            "print": self.onPrint,
            "load": self.onLoad,
            "=": self.onEqual,
            "<": self.onLs,
            "+": self.onAdd,
            "-": self.onSub,
            "*": self.onMul,
            "/": self.onDiv,
            "python-eval-string": self.onEvalPythonString,
            "python-exec-string": self.onExecPythonString,
        }
        self.specials = {
            "lambda": self.onLambda,
            "let": self.onLet,
            "and": self.onAnd,
            "or": self.onOr,
            "eval": self.onEval,
            "define": self.onDefine,
            "quote": self.onQuote,
            "if": self.onIf,
            "cond": self.onCond,
            "time": self.onTime,
            "begin": self.onBegin,
            "read-char": self.onReadChar,
        }
    def eval(self, tree):
        self.recursionDepth += 1
        if self.recursionDepth > self.recursionLimit:
            self.recursionDepth = 0
            raise Exception("maximum recursion limit exceeded (%d)" % self.recursionLimit)
        retval = None
        if type(tree) in [int, float, Str]:
            retval = tree
        elif tree in [None, True, False]: # nil, #t, #f
            retval = tree
        elif isinstance(tree, Label):
            label = tree
            if label in self.specials or label in self.builtins:
                retval = label
            else:
                try:
                    retval = self.lookup(label)
                except Exception,e:
                    raise e 
        else:
            fun = self.eval(tree.car)
            arg = tree.cdr
            if fun in self.specials:
                # special form
                retval = self.specials[fun](arg)
            else:
                # evaluate arguments
                if arg is nil:
                    evalarg = nil
                else:
                    evalarg = Cell(self.eval(arg.car))
                ref = evalarg
                if arg != nil and arg.cdr != nil:
                    for cell in arg.cdr.listitems():
                        c = Cell(self.eval(cell))
                        ref.cons(c)
                        ref = c
                arg = evalarg

                if fun in self.builtins:
                    # builtin function
                    retval = self.builtins[fun](arg)
                else:
                    # user-defined function
                    retval = self.onApply(Cell(fun, arg))
        self.recursionDepth -= 1
        return retval
    def bind(self, name, tree):
        self.environ = Cell(Cell(name, tree), self.environ)
    def lookup(self, name):
        if self.environ is nil:
            raise Exception("次の変数が見つかりません: " + name)
        for pair in self.environ.listitems():
            if name == pair.car:
                return pair.cdr
        raise Exception("次の変数が見つかりません: " + name)
    def onCons(self, arg): return Cell(arg.car, arg.cdr.car)
    def onCar(self, arg):  return arg.car.car
    def onCdr(self, arg): return arg.car.cdr
    def onAnd(self, arg):
        for cell in arg.listitems():
            result = self.eval(cell)
            if result is false:
                return false
        return true
    def onOr(self, arg):
        for cell in arg.listitems():
            result = self.eval(cell)
            if result is true:
                return true
        return false
    def onApply(self, arg):
        fun = arg.car
        param = arg.cdr
        if fun in self.specials:
            retval = self.specials[fun](arg)
        elif fun in self.builtins:
            retval = self.builtins[fun](arg.cdr)
        else:
            # lambda
            backup = self.environ
            if fun.cdr.car != nil: # if there are parameter to lambda
                # associate parameter to argument
                assoc = fun.cdr.car.zip(param)
                #print "onApply:",assoc,fun
                self.environ = assoc.append(self.environ)
            body = fun.cdr.cdr.car
            retval = self.eval(body)
            self.environ = backup
        return retval
    def onList(self, arg):
        if arg is nil:
            return nil
        elif arg.cdr is nil:
            return Cell(arg.car)
        else:
            tree = Cell(arg.car)
            ref = tree
            for cell in arg.cdr.listitems():
                x = Cell(cell)
                ref.cons(x)
                ref = x
            return tree
    def onDisplay(self, arg):
        sys.stdout.write(str(arg.car))
        return nil
    def onPrint(self, arg):
        sys.stdout.write(str(arg.car))
        print ""
        return nil
    def onNewline(self, arg):
        print ""
        return nil
    def relreduction(self, cells, op):
        if cells is nil or cells.cdr is nil:
            return true
        x = cells.car
        for cell in cells.cdr.listitems():
            if not op(x, cell):
                return false
        return true
    def onEq(self, arg):
        return self.relreduction(arg, operator.eq)
    def onEqual(self, arg):
        #print "onEqual:",arg,type(arg.car),type(arg.cdr.car)
        return self.relreduction(arg, operator.eq)
    def onLs(self, arg):
        return self.relreduction(arg, operator.lt)
    def onLoad(self, arg):
        filecontent = open(arg.car).read()
        tokenseq = Lexer().tokenize(filecontent)
        while True:
            try:
                tree = Parser().parse(tokenseq)
                self.eval(tree)
            except StopIteration, e:
                break
            except Exception, e:
                #print "error:",e
                print "load エラー:",e
    def reduction(self, cells, op, init):
        if cells is nil:
            return init
        acc = init
        for cell in cells.listitems():
            acc = op(acc, cell)
        return acc
    def onAdd(self, arg):
        return self.reduction(arg, operator.add, 0)
    def onSub(self, arg):
        return self.reduction(arg.cdr, operator.sub, arg.car)
    def onMul(self, arg):
        return self.reduction(arg, operator.mul, 1)
    def onDiv(self, arg):
        return self.reduction(arg.cdr, operator.div, arg.car)
    def onEvalPythonString(self, arg):
        expression = arg.car
        exp = eval(expression)
        return exp
    def onExecPythonString(self, arg):
        statement = arg.car
        exec statement
        return nil
    def onLambda(self, arg):
        return Cell(Label("lambda"), arg)
    def onLet(self, arg):
        # lambdaとパラメータ、引数のリストを構築してapply
        vars = arg.car
        body = arg.cdr.car
        params = nil
        arg = nil
        for cell in vars.listitems():
            params = Cell(cell.car, params)
            arg = Cell(self.eval(cell.cdr.car), arg)
        # e.g. (lambda (x y) (+ x y))
        fun = Cell(Label("lambda"), Cell(params, Cell(body, nil)))
        retval = self.onApply(Cell(fun, arg))
        return retval
    def onEval(self, arg):
        return self.eval(arg.car)
    def onDefine(self, arg):
        first = arg.car
        second = arg.cdr.car
        if type(first) == Label:
            # 変数
            name = first
            tree = self.eval(second)
            self.bind(name, tree)
            return name
        else:
            # 関数
            name = first.car
            funarg = first.cdr
            tree = Cell(second)
            fun  = Cell(Label("lambda"), Cell(first.cdr, tree))
            self.bind(name, fun)
            return name
    def onQuote(self, arg):
        return arg.car
    def onIf(self, arg):
        pred = self.eval(arg.car)
        if pred is true:
            branch = arg.cdr.car
        else:
            branch = arg.cdr.cdr.car
        #print "onIF: exec:",branch
        return self.eval(branch)
    def onCond(self, arg):
        for cell in arg.listitems():
            pred = cell.car
            body = cell.cdr.car
            result = self.eval(pred)
            if result is true:
                return self.eval(body)
    def onTime(self, arg):
        start = time.time()
        self.eval(arg.car)
        end   = time.time()
        return end - start
    def onBegin(self, arg):
        for cell in arg.listitems():
            retval = self.eval(cell)
        return retval
    def onReadChar(self, arg):
        return Str(sys.stdin.read(1))


class Reader(object):
    def read(self):
        return raw_input("pylisp> ")


def inputnormalize(inputs):
    f = lambda encode: unicode(inputs, encode).decode("utf-8")
    encodes = ["utf-8", "euc-jp", "iso-2202-jp", "sjis", "jis", "cp932"]
    for encode in encodes:
        try:
            return f(encode)
        except: pass
    raise Exception("inputnormalize: cannot normalize input")
    
class Lisp(object):
    def __init__(self, lexer=Lexer(), parser=Parser(), evaluator=Evaluator(), reader=Reader(), initfiles=[]):
        self.startup = [
            os.path.join(os.path.dirname(__file__), "./startup.scm"),
            ]
        self.lexer = lexer
        self.parser = parser
        self.evaluator = evaluator
        self.reader = reader
        for filepath in self.startup + initfiles:
            self.loadfile(filepath)
                
    def loop(self):
        while True:
            # read
            try:
                inputs = self.reader.read()
                inputs = inputnormalize(inputs)
            except KeyboardInterrupt, e:
                break
            # eval
            try:
                tokenseq = self.lexer.tokenize(inputs)
                tree = self.parser.parse(tokenseq)
                result = self.evaluator.eval(tree)
            except Exception, e:
                print e
                continue
                #break
            # print
            print result

    def loadfile(self, filepath):
        self.evaluator.onLoad(Cell(filepath))

def main():
    lisp = Lisp()
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
        lisp.loadfile(filepath)
    else:
        lisp.loop()

if __name__ == '__main__':
    main()
