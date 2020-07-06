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
   * [6. **kwargs and *args (mutable arguments passed to function)](#6-kwargs-and-args-mutable-arguments-passed-to-function)
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
## generator: retrun an iterator (generator iterator), call be "next()" to execute until it raises an exception
```python
use () to generate a generator object
g = ( x*x for x in range(100) )
```

## decorators: a function use function as input arguments to add addition feature without modify original function

#### function decorator
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

# II. Quiz #
### 1. sum
``` python
    sum(range(1,101))
```

### 2. change global var in function
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