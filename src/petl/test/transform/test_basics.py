from __future__ import absolute_import, print_function, division
# N.B., do not import unicode_literals in tests


from petl.testutils import ieq
from petl.util import expr, empty, coalesce
from petl.transform.basics import cut, cat, addfield, rowslice, head, tail, \
    cutout, skipcomments, annex, addrownumbers, addcolumn, \
    addfieldusingcontext, movefield


def test_cut():
    
    table = (('foo', 'bar', 'baz'),
             ('A', 1, 2),
             ('B', '2', '3.4'),
             (u'B', u'3', u'7.8', True),
             ('D', 'xyz', 9.0),
             ('E', None))

    cut1 = cut(table, 'foo')
    expectation = (('foo',),
                   ('A',),
                   ('B',),
                   (u'B',),
                   ('D',),
                   ('E',))
    ieq(expectation, cut1)
    
    cut2 = cut(table, 'foo', 'baz')
    expectation = (('foo', 'baz'),
                   ('A', 2),
                   ('B', '3.4'),
                   (u'B', u'7.8'),
                   ('D', 9.0),
                   ('E', None))
    ieq(expectation, cut2)
    
    cut3 = cut(table, 0, 2)
    expectation = (('foo', 'baz'),
                   ('A', 2),
                   ('B', '3.4'),
                   (u'B', u'7.8'),
                   ('D', 9.0),
                   ('E', None))
    ieq(expectation, cut3)
    
    cut4 = cut(table, 'bar', 0)
    expectation = (('bar', 'foo'),
                   (1, 'A'),
                   ('2', 'B'),
                   (u'3', u'B'),
                   ('xyz', 'D'),
                   (None, 'E'))
    ieq(expectation, cut4)

    cut5 = cut(table, ('foo', 'baz'))
    expectation = (('foo', 'baz'),
                   ('A', 2),
                   ('B', '3.4'),
                   (u'B', u'7.8'),
                   ('D', 9.0),
                   ('E', None))
    ieq(expectation, cut5)


def test_cut_empty():
    table = (('foo', 'bar'),)
    expect = (('bar',),)
    actual = cut(table, 'bar')
    ieq(expect, actual)
        

def test_cutout():
    
    table = (('foo', 'bar', 'baz'),
             ('A', 1, 2),
             ('B', '2', '3.4'),
             (u'B', u'3', u'7.8', True),
             ('D', 'xyz', 9.0),
             ('E', None))

    cut1 = cutout(table, 'bar', 'baz')
    expectation = (('foo',),
                   ('A',),
                   ('B',),
                   (u'B',),
                   ('D',),
                   ('E',))
    ieq(expectation, cut1)
    
    cut2 = cutout(table, 'bar')
    expectation = (('foo', 'baz'),
                   ('A', 2),
                   ('B', '3.4'),
                   (u'B', u'7.8'),
                   ('D', 9.0),
                   ('E', None))
    ieq(expectation, cut2)
    
    cut3 = cutout(table, 1)
    expectation = (('foo', 'baz'),
                   ('A', 2),
                   ('B', '3.4'),
                   (u'B', u'7.8'),
                   ('D', 9.0),
                   ('E', None))
    ieq(expectation, cut3)
    

def test_cat():
    
    table1 = (('foo', 'bar'),
              (1, 'A'),
              (2, 'B'))

    table2 = (('bar', 'baz'),
              ('C', True),
              ('D', False))
    
    cat1 = cat(table1, table2, missing=None)
    expectation = (('foo', 'bar', 'baz'),
                   (1, 'A', None),
                   (2, 'B', None),
                   (None, 'C', True),
                   (None, 'D', False))
    ieq(expectation, cat1)

    # how does cat cope with uneven rows?
    
    table3 = (('foo', 'bar', 'baz'),
              ('A', 1, 2),
              ('B', '2', '3.4'),
              (u'B', u'3', u'7.8', True),
              ('D', 'xyz', 9.0),
              ('E', None))

    cat3 = cat(table3, missing=None)
    expectation = (('foo', 'bar', 'baz'),
                   ('A', 1, 2),
                   ('B', '2', '3.4'),
                   (u'B', u'3', u'7.8'),
                   ('D', 'xyz', 9.0),
                   ('E', None, None))
    ieq(expectation, cat3)
    
    # cat more than two tables?
    cat4 = cat(table1, table2, table3)
    expectation = (('foo', 'bar', 'baz'),
                   (1, 'A', None),
                   (2, 'B', None),
                   (None, 'C', True),
                   (None, 'D', False),
                   ('A', 1, 2),
                   ('B', '2', '3.4'),
                   (u'B', u'3', u'7.8'),
                   ('D', 'xyz', 9.0),
                   ('E', None, None))
    ieq(expectation, cat4)
    

def test_cat_with_header():

    table1 = (('bar', 'foo'),
              ('A', 1),
              ('B', 2))

    table2 = (('bar', 'baz'),
              ('C', True),
              ('D', False))

    actual = cat(table1, header=['A', 'foo', 'B', 'bar', 'C'])
    expect = (('A', 'foo', 'B', 'bar', 'C'),
              (None, 1, None, 'A', None),
              (None, 2, None, 'B', None))
    ieq(expect, actual)
    ieq(expect, actual)

    actual = cat(table1, table2, header=['A', 'foo', 'B', 'bar', 'C'])
    expect = (('A', 'foo', 'B', 'bar', 'C'),
              (None, 1, None, 'A', None),
              (None, 2, None, 'B', None),
              (None, None, None, 'C', None),
              (None, None, None, 'D', None))
    ieq(expect, actual)
    ieq(expect, actual)


def test_cat_empty():
    table1 = (('foo', 'bar'),
              (1, 'A'),
              (2, 'B'))
    table2 = (('bar', 'baz'),)
    expect = (('foo', 'bar', 'baz'),
              (1, 'A', None),
              (2, 'B', None))
    actual = cat(table1, table2)
    ieq(expect, actual)


def test_addfield():
    table = (('foo', 'bar'),
             ('M', 12),
             ('F', 34),
             ('-', 56))
    
    result = addfield(table, 'baz', 42)
    expectation = (('foo', 'bar', 'baz'),
                   ('M', 12, 42),
                   ('F', 34, 42),
                   ('-', 56, 42))
    ieq(expectation, result)
    ieq(expectation, result)

    result = addfield(table, 'baz', lambda rec: rec['bar'] * 2)
    expectation = (('foo', 'bar', 'baz'),
                   ('M', 12, 24),
                   ('F', 34, 68),
                   ('-', 56, 112))
    ieq(expectation, result)
    ieq(expectation, result)

    result = addfield(table, 'baz', expr('{bar} * 2'))
    expectation = (('foo', 'bar', 'baz'),
                   ('M', 12, 24),
                   ('F', 34, 68),
                   ('-', 56, 112))
    ieq(expectation, result)
    ieq(expectation, result)

    result = addfield(table, 'baz', 42, index=0)
    expectation = (('baz', 'foo', 'bar'),
                   (42, 'M', 12),
                   (42, 'F', 34),
                   (42, '-', 56))
    ieq(expectation, result)
    ieq(expectation, result)
    

def test_addfield_empty():
    table = (('foo', 'bar'),)
    expect = (('foo', 'bar', 'baz'),)
    actual = addfield(table, 'baz', 42)
    ieq(expect, actual)
    ieq(expect, actual)


def test_addfield_coalesce():
    table = (('foo', 'bar', 'baz', 'quux'),
             ('M', 12, 23, 44),
             ('F', None, 23, 11),
             ('-', None, None, 42))
    
    result = addfield(table, 'spong', coalesce('bar', 'baz', 'quux'))
    expect = (('foo', 'bar', 'baz', 'quux', 'spong'),
              ('M', 12, 23, 44, 12),
              ('F', None, 23, 11, 23),
              ('-', None, None, 42, 42))
    ieq(expect, result)
    ieq(expect, result)

    result = addfield(table, 'spong', coalesce(1, 2, 3))
    expect = (('foo', 'bar', 'baz', 'quux', 'spong'),
              ('M', 12, 23, 44, 12),
              ('F', None, 23, 11, 23),
              ('-', None, None, 42, 42))
    ieq(expect, result)
    ieq(expect, result)


def test_addfield_uneven_rows():
    table = (('foo', 'bar'),
             ('M',),
             ('F', 34),
             ('-', 56, 'spong'))
    result = addfield(table, 'baz', 42)
    expectation = (('foo', 'bar', 'baz'),
                   ('M', None, 42),
                   ('F', 34, 42),
                   ('-', 56, 42))
    ieq(expectation, result)
    ieq(expectation, result)


def test_rowslice():
    """Test the rowslice function."""
    
    table = (('foo', 'bar', 'baz'),
             ('A', 1, 2),
             ('B', '2', '3.4'),
             (u'B', u'3', u'7.8', True),
             ('D', 'xyz', 9.0),
             ('E', None))

    result = rowslice(table, 2)
    expectation = (('foo', 'bar', 'baz'),
                   ('A', 1, 2),
                   ('B', '2', '3.4'))
    ieq(expectation, result)

    result = rowslice(table, 1, 2)
    expectation = (('foo', 'bar', 'baz'),
                   ('B', '2', '3.4'))
    ieq(expectation, result)

    result = rowslice(table, 1, 5, 2)
    expectation = (('foo', 'bar', 'baz'),
                   ('B', '2', '3.4'),
                   ('D', 'xyz', 9.0))
    ieq(expectation, result)


def test_rowslice_empty():
    table = (('foo', 'bar'),)
    expect = (('foo', 'bar'),)
    actual = rowslice(table, 1, 2)
    ieq(expect, actual)
        

def test_head():
    """Test the head function."""
    
    table1 = (('foo', 'bar'),
              ('a', 1),
              ('b', 2),
              ('c', 5),
              ('d', 7),
              ('f', 42),
              ('f', 3),
              ('h', 90),
              ('k', 12),
              ('l', 77),
              ('q', 2))
    
    table2 = head(table1, 4)
    expect = (('foo', 'bar'),
              ('a', 1),
              ('b', 2),
              ('c', 5),
              ('d', 7))
    ieq(expect, table2)


def test_tail():
    """Test the tail function."""
    
    table1 = (('foo', 'bar'),
              ('a', 1),
              ('b', 2),
              ('c', 5),
              ('d', 7),
              ('f', 42),
              ('f', 3),
              ('h', 90),
              ('k', 12),
              ('l', 77),
              ('q', 2))
    
    table2 = tail(table1, 4)
    expect = (('foo', 'bar'),
              ('h', 90),
              ('k', 12),
              ('l', 77),
              ('q', 2))
    ieq(expect, table2)
    

def test_tail_empty():
    table = (('foo', 'bar'),)
    expect = (('foo', 'bar'),)
    actual = tail(table)
    ieq(expect, actual)
        
    
def test_skipcomments():

    table1 = (('##aaa', 'bbb', 'ccc'),
              ('##mmm',),
              ('#foo', 'bar'),
              ('##nnn', 1),
              ('a', 1),
              ('b', 2))
    table2 = skipcomments(table1, '##')
    expect2 = (('#foo', 'bar'),
               ('a', 1),
               ('b', 2))
    ieq(expect2, table2)
    ieq(expect2, table2)  # can iterate twice?
    
    
def test_skipcomments_empty():

    table1 = (('##aaa', 'bbb', 'ccc'),
              ('##mmm',),
              ('#foo', 'bar'),
              ('##nnn', 1))
    table2 = skipcomments(table1, '##')
    expect2 = (('#foo', 'bar'),)
    ieq(expect2, table2)
    
    
def test_annex():

    table1 = (('foo', 'bar'),
              ('A', 9),
              ('C', 2),
              ('F', 1))
    table2 = (('foo', 'baz'),
              ('B', 3),
              ('D', 10))
    expect = (('foo', 'bar', 'foo', 'baz'),
              ('A', 9, 'B', 3),
              ('C', 2, 'D', 10),
              ('F', 1, None, None))
    actual = annex(table1, table2)
    ieq(expect, actual)
    ieq(expect, actual)

    expect21 = (('foo', 'baz', 'foo', 'bar'),
                ('B', 3, 'A', 9),
                ('D', 10, 'C', 2),
                (None, None, 'F', 1))
    actual21 = annex(table2, table1)
    ieq(expect21, actual21)
    ieq(expect21, actual21)


def test_annex_uneven_rows():

    table1 = (('foo', 'bar'),
              ('A', 9, True),
              ('C', 2),
              ('F',))
    table2 = (('foo', 'baz'),
              ('B', 3),
              ('D', 10))
    expect = (('foo', 'bar', 'foo', 'baz'),
              ('A', 9, 'B', 3),
              ('C', 2, 'D', 10),
              ('F', None, None, None))
    actual = annex(table1, table2)
    ieq(expect, actual)
    ieq(expect, actual)


def test_addrownumbers():

    table1 = (('foo', 'bar'),
              ('A', 9),
              ('C', 2),
              ('F', 1))

    expect = (('row', 'foo', 'bar'),
              (1, 'A', 9),
              (2, 'C', 2),
              (3, 'F', 1))
    actual = addrownumbers(table1)
    ieq(expect, actual)
    ieq(expect, actual)
    
    
def test_addcolumn():
    
    table1 = (('foo', 'bar'),
              ('A', 1),
              ('B', 2))
    
    col = [True, False]
    
    expect2 = (('foo', 'bar', 'baz'),
               ('A', 1, True),
               ('B', 2, False))
    table2 = addcolumn(table1, 'baz', col)
    ieq(expect2, table2)
    ieq(expect2, table2)

    # test short column
    table3 = (('foo', 'bar'),
              ('A', 1),
              ('B', 2),
              ('C', 2))
    expect4 = (('foo', 'bar', 'baz'),
               ('A', 1, True),
               ('B', 2, False),
               ('C', 2, None))
    table4 = addcolumn(table3, 'baz', col)
    ieq(expect4, table4)
    
    # test short table
    col = [True, False, False]
    expect5 = (('foo', 'bar', 'baz'),
               ('A', 1, True),
               ('B', 2, False),
               (None, None, False))
    table5 = addcolumn(table1, 'baz', col)
    ieq(expect5, table5)


def test_empty_addcolumn():

    table1 = empty()
    table2 = addcolumn(table1, 'foo', ['A', 'B'])
    table3 = addcolumn(table2, 'bar', [1, 2])
    expect = (('foo', 'bar'),
              ('A', 1),
              ('B', 2))
    ieq(expect, table3)
    ieq(expect, table3)


def test_addfieldusingcontext():

    table1 = (('foo', 'bar'),
              ('A', 1),
              ('B', 4),
              ('C', 5),
              ('D', 9))

    expect = (('foo', 'bar', 'baz', 'quux'),
              ('A', 1, None, 3),
              ('B', 4, 3, 1),
              ('C', 5, 1, 4),
              ('D', 9, 4, None))

    def upstream(prv, cur, nxt):
        if prv is None:
            return None
        else:
            return cur.bar - prv.bar

    def downstream(prv, cur, nxt):
        if nxt is None:
            return None
        else:
            return nxt.bar - cur.bar

    table2 = addfieldusingcontext(table1, 'baz', upstream)
    table3 = addfieldusingcontext(table2, 'quux', downstream)
    ieq(expect, table3)
    ieq(expect, table3)


def test_movefield():

    table1 = (('foo', 'bar', 'baz'),
              (1, 'A', True),
              (2, 'B', False))

    expect = (('bar', 'foo', 'baz'),
              ('A', 1, True),
              ('B', 2, False))

    actual = movefield(table1, 'bar', 0)
    ieq(expect, actual)
    ieq(expect, actual)

    actual = movefield(table1, 'foo', 1)
    ieq(expect, actual)
    ieq(expect, actual)
