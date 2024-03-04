
s = '()'

mapping = {
           '(':')',
           '{':'}', 
           '[':']' }

stack = []

def isValid(s):
    
    for br in s:

        if br not in mapping:
            top_element = stack.pop()
            if mapping.get(top_element) != br:
                return False
        else:
            stack.append(br)
    return True

# a = isValid(s)
# print(a)

def _ten_to1():          
    c = 1
    for i in range(1, 20):
        if i > 10:
            print(i - 2 * c)
            c += 1
        else:
            print(i)
# _ten_to1()
            


###      [1, 2, 3, 6, 9, 8, 7, 4, 5]
matrix = [[1,2,3],[4,5,6],[7,8,9]]




def spiralOrder (matrix):
    result = []
    while matrix:
        result += matrix.pop(0)

        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())

        if matrix:
            result += matrix.pop()[::-1]
        if matrix and matrix[0]:
            for row in matrix[::-1]:
                result.append(row.pop())
    return result


# print(spiralOrder(matrix))



def best_buy(arr):

    min_ = arr[0]
    max_ = 0

    for price in arr:

        min_ = min(price, min_ )

        max_ = max( max_, price - min_ )

    return max_

# print(best_buy([7,1,5,3,6,4]))
# print(best_buy([7,6,4,3,1]))


def maxProfit(prices):
    profit = 0
    for i in range(1,len(prices)):

        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit

# print(maxProfit([7,1,5,3,6,4]))


def length_of_longest_substring(s):

    char_index = {}
    max_length = start = 0

    for i, character in enumerate(s):
        print('char index', char_index)

        if character in char_index and char_index[character] >= start:
            start = char_index[character]+1 
        
        char_index[character] = i
        max_length  = max(max_length, i - start + 1 )



# s = "abcabcbb"
# print(length_of_longest_substring(s)) 