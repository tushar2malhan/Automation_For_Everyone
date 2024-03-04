def solution(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 2

    ways = [0] * (n + 1)
    ways[1] = 1
    ways[2] = 2

    for i in range(3, n + 1):
        print( i-1,  i -2, '\t' ,ways[i] ,'\t', ways[i-1], ways[i-2])
        ways[i] = ways[i - 1] + ways[i - 2]
        print('ways [i] ', ways[i])

    return ways[n]

# Test cases
# print(solution(5)) 


import numpy as np

a = np.array([[0, 1, 2], [3, 4, 5]])
b = a.ravel()
# print(ord('x'))

def c():
    s = 'xobin'
    # char_set = [False] * 128
    # for i in range(0, len(s)):
    #     val = ord(s[i])
    #     print(val)
    #     if char_set[val]:
    #         return False
    #     char_set[val] = True
    # return True
s = '0'
# c()
# print(s)

# a = 8;b = 51; c = 2
# c = (a^c)^(a)
# b = b mod 4
# print a+b+C



# print(1)

###    0 1 2 3 4 5 6 7 8
arr = [1,2,3,5,6,7,8,9,12]
target = 12
def binary_search(arr, target):

    start_index = 0
    end_index   = len(arr)  - 1

    while start_index <= end_index:
        mid_element = (start_index + end_index) // 2
       
        print('array\t', arr[:mid_element], 'mid_element ', mid_element-1)
        if arr[mid_element] == target:
            print(1)
            return True
        
        elif arr[mid_element] > target:
            end_index = mid_element - 1
        else:
            start_index = mid_element + 1
    print(0)
    return False

# binary_search(arr, target)


class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        hash_map = {}
        vowels = ['a', 'e', 'i', 'o','u']

        for char in s:
            if char in vowels :
                if char in hash_map:
                    hash_map[char] += 1
                
            
        
s = "abciiidef"; k = 3

ok = Solution()
ok.maxVowels(s, k)