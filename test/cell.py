# coding: utf-8
# Cellクラスのテスト

import sys
import os
sys.path += os.path.join(os.path.dirname(__file__), "../")

import lisp

def celltest():
    f = lambda x: lst.append(x)
    lst = [
     lisp.Cell(1),      # 1
     lisp.Cell(1.0),    # 1.0
     lisp.Cell("hello"),# "hello"
     lisp.nil,          # nil
     lisp.true,         # #t
     lisp.false,        # #f
     lisp.Cell(1, 2),   # (1 . 2)
     lisp.Cell(0, lisp.Cell(1, lisp.Cell(2, lisp.nil))) # (0 1 2)
    ]
    for n in lst:
        print n

    keys = lisp.Cell(lisp.Label("x"), lisp.Cell(lisp.Label("y"), lisp.nil))
    vals = lisp.Cell(1, lisp.Cell(10, lisp.nil))
    print keys
    print vals
    print keys.zip(vals)
    
if __name__ == '__main__':
    celltest()
