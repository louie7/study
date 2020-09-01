#!/usr/local/bin/python3

import sys
import os
import re

from enum import Enum, unique

## enum constant usage
# @unique to assume no duplicate
@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

## OOP learning
class Province:
    # static var, Only keep one in mem
    country = 'China'

    def __init__(self, name):
    #every obj has one
        self.name = name

    # class method, call by class, at least one cls parameter
    @classmethod
    def class_func(cls):
        print ('class_func call')

    # static method, call by class, no default parameter
    @staticmethod
    def static_func():
        print ('static_func call')


class Person(object):
    '''person'''

    ## XXX limit the instance could added attribution with __slots__
    ## *only* work for current class (no impact sub-class)
    __slots__ = ('__name', '_age')
    #__slots__ = ('score', '_age')


    def __init__(self, name, age):
        ## make __name attribute private 
        self.__name = name
        self._age = age

    def __str__(self):
        return "Person object, Name: %s" % self.__name

    ## use @property to make method to attribution call 
    ## without setter, they culd not be set as attribute
    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    #
    def play(self):
        print('%s is playing.' % self.__name)

    def watch(self):
        if self._age >= 18:
            print('%s is watching Movie' % self.__name)
        else:
            print('%s is watching Batman' % self.__name)


class Student(Person):
    ''' student '''
    #__slots__ = ('score', 'grade')

    def __init__(self, name, age, grade):
        super(Student, self).__init__(name,age)
        self._grade = grade

    ## XXX make method become attribution call
    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self,grade):
        if not isinstance(grade, int):
            raise ValueError("grade must be integer!")
        if grade > 6 or grade < 1:
            raise ValueError("grade must between 1 to 6!")

        self._grade = grade

    @grade.deleter
    def grade(self, grade):
        del self._grade

    def study(self, course):
        print('%s: %s is studying %s' % (self._grade,self.name,course))

    def set_score(self, score):
        self.score = score


class Teacher(Person):
    '''teacher'''

    def __init__(self, name, age, title):
        super(Teacher, self).__init__(name, age)
        self._title = title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def teach(self, course):
        print('%s%s is teaching %s.' % (self.name, self._title, course))


# public member could be accessed by: obj, class internal, derived class
# private member ONLY could be accessed by: class internal


class Goods(object):
    '''static field to create attribute'''

    def __init__(self):
        self.original_price = 100
        self.discount = 0.8

    def get_price(self):
        new_price = self.original_price * self.discount
        return new_price

    def set_price(self, value):
        self.original_price = value

    def del_price(self, value):
        del self.original_price

    PRICE = property(get_price, set_price, del_price, 'price attribute description')


def main_oop():
    obj = Province('Hebei')
    print (obj.name)
    
    print (Province.country)
    Province.static_func()
    Province.class_func()

    print ("\n=================")
    people = Person('Lee', 15)
    print (people)
    stu = Student('Jack', 15, 'grade 3')
    print (stu)     ## call __str__
    # print (stu.__name)    # ==> __name is private attribute
    # stu.grade = 'grade 6' # ==> fail for grade setter 
    print (stu.name) ## call __str__
    print (stu._age)
    stu.study('math')
    ## stu.name = 'zzz'  ==> can't set attribute
    stu.set_score(100)
    print ("score: {} {}".format(stu.score, stu.name))
    stu.watch()
    #del stu.grade

    print ("\n=================")
    t = Teacher('Ma', 28, 'huang')
    t.teach('Python design')
    t.watch()


    print ("\n=================")
    obj = Goods()
    obj.PRICE
    obj.PRICE = 200
    #del obj.PRICE(200)


if __name__ == '__main__':

    main_oop()

    ## open to extend
    ## no open to modify

    ## isinstance(), 
    ## dir() to get object all attribution

    ## getattr(), setattr(), hasattr()

    ## MixIn


    ## class special members: __doc__, __module__, __class__, __init__, __del__, __call__, __dict__, __str__, __slots__
    
    ## user defined class, __iter__, __next__ to implement 'for ... in'
    ## __getitem__ to implement index operation of list
    ## instance call directly __call__
