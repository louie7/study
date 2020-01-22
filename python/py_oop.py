#!/usr/bin/python

import sys
import os
import re

## leetcode
class Solution(object):
    '''two eles added in list which equal target'''
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        s_num = sorted(nums)
        i = 0
        j = len(nums) - 1
        while i < j :
            if s_num[i] + s_num[j] == target: 
                print "{}, {}".format(s_num[i], s_num[j])
                if s_num[i] == s_num[j]:
                    return [nums.index(s_num[i]), nums.index(s_num[j], nums.index(s_num[i]) + 1)]
                else:
                    return [nums.index(s_num[i]), nums.index(s_num[j])]

            if s_num[i] + s_num[j] > target: 
                j -= 1
            else: 
                i += 1


    def twoSum_1(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        idx = 0
        n_set = set(nums)
        for i in nums:
            sub = target -i
            if sub in n_set and sub in nums[idx + 1:]:
                if i == target - i:
                    print '[{},{}]'.format(idx, nums.index(target-i, idx + 1))
                    return [idx, nums.index(target-i, idx + 1)]
                else:
                    print '[{},{}]'.format(idx, nums.index(target-i))
                    return [idx, nums.index(target-i)]
            idx += 1

class Sort(object):
    ''' sort '''
    def bubble_sort(self, nums):
        ''' stable O(n2) '''
        print "Before sort", nums, "\n",
        for i in range(len(nums) - 1):
            for j in range(len(nums) - i - 1):
                if nums[j] > nums[j + 1]:
                    # print ("switch {} -> {} ({} to {})".format(j, j+1, nums[j], nums[j+1]))
                    nums[j], nums[j + 1] = nums[j + 1], nums[j] 
        print "After sort", nums, "\n",
        return nums

    def merge_sort(self, nums):
        ''' stable O(nlogn); most used external sort; need O(n) space '''
        def merge(left, right):
            result = []

    def quicksort(self, nums, outputs):
        ''' instable O(nlogn) '''
        pass



def MergeSort(left, right):
    i, j = 0, 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    print("i:{} j:{} result: {}: left:{} right:{}".format(i, j, result, left[i:],right[j:]))
    result += left[i:] ##i or j already arrived the end of the list
    result += right[j:]

    print("results: ==> {}".format(result))
    return result


def SortByMerge(arr, size):
    if size <= 1:
        print("call SortByMerge return {} size {}".format(arr, size))
        return arr

    i = int(size/2)
    # print("call SortByMerge arr[:i] {} size: {}".format(arr[:i], i))
    left = SortByMerge(arr[:i], i)
    # print("call SortByMerge arr[i:] {} size: {}".format(arr[i:], i))
    right = SortByMerge(arr[i:], size - i)
    # print("call MergeSort {} {}".format(left, right))
    return MergeSort(left, right)


def mergeSort(nums):
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result = result + left[i:] + right[j:]
        return result

    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2
    left = mergeSort(nums[:mid])
    right = mergeSort(nums[mid:])
    return merge(left, right)

def get_uniq_intersection_set(arr1, arr2):
    '''get uniq intersection set of two arrays'''
    s = set(arr1)
    intersection_set = s.intersection(set(arr2))

    print "uniq common cells of {} and {} is {}".format(arr1, arr2, intersection_set)
    return intersection_set



def get_intersection_set(arr1, arr2):
    '''get intersection set of two arrays, contain duplicate'''
    r = {}
    for e in arr1:
        if e in r:
            r[e] += 1
        else:
            r[e] = 1

    results = []
    for e in arr2:
        if e in r and r[e] > 0:
            results.append(e)
            r[e] -= 1

    print "common cells of {} and {} is {}".format(arr1, arr2, results)
    return results


class Node:
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None

class DoubleLinkList(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head == None

    def length(self):
        cur = self._head
        count = 0
        while cur != None:
            count += 1
            cur = cur.next
        return count

    def travel(self):
        cur = self._head
        print ("walk the linklist from {}".format(cur.item))
        while cur != None:
            print("{} ".format(cur.item))
            cur = cur.next
        print("END")

    def add(self, item):
        node = Node(item)
        if self.is_empty():
            self._head = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node

    def append(self, item):
        node = Node(item)
        if self.is_empty():
            self._head = node
        else:
            cur = self._head
            while cur.next != None:
                cur = cur.next
            cur.next = node
            node.prev = cur

    def search(self):
        cur = self._head
        while cur != None:
            if cur.item == item:
                return true
            else:
                cur = cur.next
        return false

    def insert(self, pos, item):
        if pos <= 0 or pos > self.length() + 1:
            print 'Error input for pos', pos
        elif pos == 1:
            self.add(item)
        elif pos == self.length() + 1:
            self.append(item)
        else:
            node = Node(item)
            cur = self._head
            count = 1
            while count < (pos -1):
                count += 1
                cur = cur.next

            node.prev = cur
            node.next = cur.next

            cur.next.prev = node
            cur.next = node

    def remove(self, item):
        if self.is_empty():
            print 'list is empty'
            return
        else:
            cur = self._head
            if cur.item == item:
                if cur.next == None:
                    self._head = None
                else:
                    cur.next.prev = None
                    self._head = cur.next
                return

        while cur != None:
            if cur.item == item:
                cur.prev.next = cur.next
                cur.next.prev = cur.prev
                break
            cur = cur.next

def run_Linklist():
    '''node link list operation'''
    d_list = DoubleLinkList()
    d_list.add('a')
    d_list.append('b')
    d_list.travel()

    d_list.insert(2, 'd')
    d_list.insert(2, 'c')
    d_list.insert('c', 3)
    d_list.travel()

    d_list.append('e')
    d_list.travel()
    d_list.remove('d')
    d_list.travel()




def orderedbox(num, boxlist):
    general = re.compile(r"(?:\w+\s+\w+)+")
    old = re.compile(r"(?:[a-z]+\s+[a-z])+")
    new = re.compile(r"(?:\d+\s+\d+)+")
    result = []
    old_l = []
    new_l = []
    for s in boxlist:
        if re.search(old, s):
            old_l.append(s)
        if re.search(new, s):
            new_l.append(s)
    result = sorted(old_l)
    result.extend(sorted(new_l))
    print "result: {}".format(result)
    return result
    # l = sorted(s, key=lambda x: (re.search(old,x), re.search(new,x)))
    # print l,
    
    

if __name__ == '__main__':
    boxlist = ['ykc 82 01', 'eo first qpx', '09z cat hamster', '06f 12 25 6', 'az0 first qpx',
                '236 cat dog rabbit snake']
    orderedbox(6, boxlist)
    # ltcode = Solution()
    # ltcode.twoSum([3,3], 6) 
    # ltcode.twoSum([2,5,7,11], 9) 
    # ltcode.twoSum([-1,-2,-3,-4,-5], -8) 

    # nums = [7, 5, 2, 4, 3, 5, 6, 1]
    # st = Sort()
    # st.bubble_sort(nums)

    # arr = [12, 11, 5, 13, 5, 7, 6]
    # ## print(SortByMerge(arr, len(arr)))
    # ## print(mergeSort(arr))

    # get_uniq_intersection_set(arr, nums)
    # get_intersection_set(arr, nums)

    ## run_Linklist()

