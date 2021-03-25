Table of Contents
=================
* [I. Lessons](#i-lessons)
   * [generator: retrun an iterator (generator iterator), call be "next()" to execute until it raises an exception](#generator-retrun-an-iterator-generator-iterator-call-be-next-to-execute-until-it-raises-an-exception)
   * [decorators: a function use function as input arguments to add addition feature without modify original function](#decorators-a-function-use-function-as-input-arguments-to-add-addition-feature-without-modify-original-function)
         * [function decorator](#function-decorator)
* [II. Snippet](#ii-Snippet)
* [III. Quiz](#iii-quiz)
   * [1. sum](#1-sum)
   * [2. change global var in function](#2-change-global-var-in-function)
   * [3. del key and merge dicts](#3-del-key-and-merge-dicts)
   * [4. GIL](#4-gil)
   * [5. remove duplicated items in list](#5-remove-duplicated-items-in-list)
   * [6. \*\*kwargs and \*args (mutable arguments passed to function)](#6-kwargs-and-args-mutable-arguments-passed-to-function)
   * [8. __new__ and __init__](#8-__new__-and-__init__)
   * [9. map(...): map(function, sequence[, sequence, ...]) -&gt; list](#9-map-mapfunction-sequence-sequence----list)
   * [10. filter(...): filter(function or None, sequence) -&gt; list, tuple, or string](#10-filter-filterfunction-or-none-sequence---list-tuple-or-string)
   * [11. mutable and immutable type](#11-mutable-and-immutable-type)
   * [12. sort list by removing redundant char](#12-sort-list-by-removing-redundant-char)
   * [13. sort dict key](#13-sort-dict-key)
   * [14. timestamp](#14-timestamp)
   * [15. statistic lib: pyecharts, matplotlib](#15-statistic-lib-pyecharts-matplotlib)
   * [16. list operation](#16-list-operation)
      * [a. extend list](#a-extend-list)


# I. Lessons #
## 1.1 generator: retrun an iterator (generator iterator), call be "next()" to execute until it raises an exception
```python
use () to generate a generator object
g = ( x*x for x in range(100) )
```

## 1.2 decorators: a function use function as input arguments to add addition feature without modify original function

### function decorator
```python
import time
def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print(end_time - start_time)

    return wrapper

@decorator
def func():
    time.sleep(1)

func()
```

## 1.3 re
> re.escape to escape meta character use (?:aaa|bbb) to group re match

## 1.4 SET operations
s.update(t) s |= t return set s with elements added from t 
s.intersection_update(t) s &= t return set s keeping only elements also found in t s.
difference_update(t) s -= t return set s after removing elements found in t s.
symmetric_difference_update(t) s ^= t return set s with elements from s or t but not both s.add(x) add element x to set s 
s.remove(x) remove x from set s, raises KeyError if not present s.discard(x) removes x from set s if present 
s.pop() remove and return an arbitrary element from s; raises KeyError if empty s.clear() remove all elements from set s
```python
use SET to do one loop to find the pair whose summary is 6
(use space to exchange time)
    s1 = set([1, 3, 2, 5, 4])
    s = frozenset([1, 3, 2, 5, 4])
    r = []
    for i in s:
       s1.discard(i)
       t = 6 - i
       if t in s1:
           r.append([i, t])
           s1.discard(t)
```

## 1.5 sorted instance
```python
    >>> l
    ['Chr1-10.txt', 'Chr1-1.txt', 'Chr1-2.txt', 'Chr1-14.txt', 'Chr1-3.txt', 'Chr1-20.txt', 'Chr1-5.txt']
    >>> sorted(l, key = lambda d: int(d.split('-')[-1].split('.')[0]))
    ['Chr1-1.txt', 'Chr1-2.txt', 'Chr1-3.txt', 'Chr1-5.txt', 'Chr1-10.txt', 'Chr1-14.txt', 'Chr1-20.txt']
    >>> l
    ['Chr1-10.txt', 'Chr1-1.txt', 'Chr1-2.txt', 'Chr1-14.txt', 'Chr1-3.txt', 'Chr1-20.txt', 'Chr1-5.txt']
listrt
    >>> print (l.sort.__doc__)
    L.sort(cmp=None, key=None, reverse=False) -- stable sort *IN PLACE*;
    cmp(x, y) -> -1, 0, 1
    >>> l = [('b',2),('a',1),('c',3)]
    >>> l.sort(key=lambda x:x[1])
    >>> l
    [('a', 1), ('b', 2), ('c', 3)]

    ## dictrted
    >>> d = {'banana':3, 'apple':4, 'pear':1, 'orange':2}
    >>> import collections
    >>> collections.OrderedDict(sorted(d.items(),key = lambda t:t[0]))
    OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])
    >>> collections.OrderedDict(sorted(d.items(),key = lambda t:t[1]))
    OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])

```

# II. Snippet #
## 2.1 check python script syntax
``` python
    python -m <py_script>.py  #python 2
    python -m py_compile  <py_script>.py  #python 3
```

## 2.2 install python package on OSX
``` python
[luyi@mbp700] ~/louie7 %
python3.8 -m pip install html-table
```

# III. Quiz #
## 1. sum
``` python
    sum(range(1,101))
```

## 2. change global var in function
```python
g_v = 5
def fn():
    global g_v
    g_v = 7
fn()
```

### 3. del key and merge dicts
```python
dic = {"name": "aa", "age": 18}
del dic['age']
dic2 = {"name": "ls"}
dic.update(dic2)
```

### 4. GIL


### 5. remove duplicated items in list
```python
l = [1, 2, 3, 5, 7, 3, 2, 1]
[x for x in set(l)]
```

### 6. \*\*kwargs and \*args (mutable arguments passed to function)
```python
def demo(**args_v):
    for k,v in args_v.items():
        print k,v
```



### 8. \_\_new\_\_ and \_\_init\_\_
+ \_\_init\_\_ initial method, immediately call by the object is created, could pass arguments
+ \_\_new\_\_ need at least one argument cls (current classs)
    - must have return value, return instance object (call \_\_init\_\_ automatically)

```python
class A(object):
    def __init__(self):
        print ("this is init method", self)

    def __new__(cls):
        print ("this is cls id", id(cls))
        print ("this is new method", object.__new__(cls))
        return object.__new__(cls)

A()
print ("this is A ID, id(A))
```

### 9. map(...): map(function, sequence[, sequence, ...]) -> list
```python
list = [1, 2, 3, 4, 5]
[x for x in map(lambda x: x**2, list) if x > 10]
[ x * x for x in [1,2,3,4,5] if x * x > 10 ]
```

### 10. filter(...): filter(function or None, sequence) -> list, tuple, or string
```python
list = [1, 2, 3, 4, 5]
[x for x in list if x % 2 != 0]
filter(lambda x: x % 2 != 0, list]
```

### 11. mutable and immutable type
- immutable: int, string, tuple
    + only one object in mem for same value, value could be changed
- mutable: list, dcit
    + value could be changed (append, etc), only change the value, would not create new object
    + same value for different objects, they are different objects in mem


### 12. sort list by removing redundant char
```python
# sorted(...)
#   sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
a = 'ajldjlajfdljfddd'
''.join(sorted([x for x in set(a)]))
```

### 13. sort dict key
> D.items() -> list of D's (key, value) pairs, as 2-tuples
```python
d = {'name': 'aa', 'age': 18, 'city': 'sh'}
new_d ={}
for i in sorted(d.items(), key=lambda i:i[0]):
    print("{} ==> {}".format(i[0],i[1]))
    new_d[i[0]]=i[1]
```


### 14. timestamp
```python
>>> import datetime
>>> datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
'2019-04-23 08:52:12'
```

### 15. statistic lib: pyecharts, matplotlib
- https://github.com/pyecharts/pyecharts


### 16. list operation
#### a. extend list
```python
l = [[1, 2], [3, 4], [5, 6]]
[x for i in l for x in i]
```
