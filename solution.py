# Start of "solution.py".

from collections import deque
import copy
import inspect
import time
from typing import List
from typing import Optional
from typing import Set

"""
    Given a string s, consider all duplicated substrings: (contiguous) 
    substrings of s that occur 2 or more times. The occurrences may overlap.

    Return any duplicated substring that has the longest possible length.
    If s does not have a duplicated substring, the answer is "".

    https://leetcode.com/problems/longest-duplicate-substring/
    https://github.com/peniwize/longest-duplicate-substring.git

    Constraints:

        * 2 <= s.length <= 3 * 104
        * s consists of lowercase English letters.

    Constraints:

        * The input must be a binary string of length 32
"""

"""
    This is the baseline brute force implementation that confirms that the
    problem is understood and all tests pass.  This is intuitive logic that 
    searches for each sub-string in the provided string.  A sub-string is
    composed of [1, n-1] characters, where 'n' is the number of characters
    in 's'.  For example, the following 21 sub-strings exist within the 
    string "banana":

     1: b
     2: ba
     3: ban
     4: bana
     5: banan
     6: banana
     7: a
     8: an
     9: ana
    10: anan
    11: anana
    12: n
    13: na
    14: nan
    15: nana
    16: a
    17: an
    18: ana
    19: n
    20: na
    21: a

    Note that "banana" is technically a valid sub-string, however it is not 
    used because, for this problem, a sub-string has fewer characters than 
    the provided string.  If it could have the same number of characters then
    the answer would always be the provided string.

    This implementation simply calculates every sub-string and stores them in
    a set.  If the sub-string being added to the set is already present and it
    is longer than the previously present and added sub-string then it becomes
    the new longest sub-string (result).

    Time = O(n*(n-1)/2) => O(n*n/2) => O(n**2)

    Space = O(n*(n-1)/2) => O(n*n/2) => O(n**2)
            One cache entry for each sub-string.
"""
class Solution1_BruteForce:
    def longestDupSubstring(self, s: str) -> str:
        cache = set()
        subStr = []
        lds = str()
        #ln = 0

        for i in range(len(s)):
            subStr = s[i]
            ss = ''.join(subStr)
            
            #ln += 1
            #print("{:02d}: {}".format(ln, ss))

            if ss in cache:
                if len(lds) < len(ss):
                    lds = ss
            else:
                cache.add(ss)
            
            for j in range (i + 1, len(s)):
                subStr += s[j]
                ss = ''.join(subStr)

                #ln += 1
                #print("{:02d}: {}".format(ln, ss))

                if ss in cache:
                    if len(lds) < len(ss):
                        lds = ss
                else:
                    cache.add(ss)

        return lds

"""
    This optimized brute force implementation uses pointers (indexes) rather 
    than copying, which is faster, and it searches for sub-strings from longest
    to shortest, which prevents shorter sub-strings from being pointlessly
    produced and evaluated after any [inherently longer] sub-string match 
    is found.

    This implementation runs roughly twice as fast as 'Solution1_BruteForce'.

    Time = O(n*(n-1)/2) => O(n*n/2) => O(n**2)
           Worst case complexity when there are NO duplicate sub-strings.

    Space = O(n*(n-1)/2) => O(n*n/2) => O(n**2)
            One cache entry for each sub-string.
"""
class Solution2_BruteForce:
    def longestDupSubstring(self, s: str) -> str:
        slen = len(s)
        cache = set()
        result = str()

        for i in range(slen):
            if slen - i > len(result): # Ignore smaller sub-strings.
                for j in range(slen, i, -1):
                    ss = s[i:j]
                    if ss in cache:
                        if len(result) < len(ss):
                            result = ss
                            break # Ignore smaller sub-strings.
                    else:
                        cache.add(ss)

        return result

"""
    Bottom up DP solution.
    The following 21 sub-strings exist within the example string "banana":

     1: b
     2: ba
     3: ban
     4: bana
     5: banan
     6: banana

     7: a
     8: an
     9: ana
    10: anan
    11: anana

    12: n
    13: na
    14: nan
    15: nana

    16: a
    17: an
    18: ana

    19: n
    20: na

    21: a

    Notice: 
        * The set of all sub-strings is composed of sub-strings with lengths 
          in the range [1, n], where 'n' is the length of the input text 's'.
        * Each character in 's' creates a sub-string of length 1.
        * Each sub-string of length 2 is composed of each sub-string of length
          1 PLUS the following character; each sub-string of length 3 is 
          composed of each sub-string of length 2 PLUS the following character;
          and so on up to sub-strings of length n-1.
        * Each sub-string builds upon the sub-strings it contains, which is a
          RECURRENCE RELATION.
    
    DYNAMIC PROGRAMMING can be used to solve this recurrence relation problem.
    This solution uses a 2D grid (a matrix) to detect sub-strings.  The grid
    axes are both the input text 's'.  Each cell in the grid contains an 
    integer whose value describes the length of the sub-string that starts 
    with the input text character that corresponds to the cell.  This is the 
    grid for the example input text "banana":

           0      1      2      3      4      5      6
           b      a      n      a      n      a
        +------+------+------+------+------+------+------+
        | diag |      |      |      |      |      |      |
    0 b |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
        |      |      |      |      |      |      |      |
        +------+------+------+------+------+------+------+
        |      | diag |      |      |      |      |      |
    1 a |  0   |  0   |  0   |  3 = |  0   |  1 = |  0   |
        |      |      |      | 1+ 2↘|      | 1+ 0↘|      |
        +------+------+------+------+------+------+------+
        |      |      | diag |      |      |      |      |
    2 n |  0   |  0   |  0   |  0   |  2 = |  0   |  0   |
        |      |      |      |      | 1+ 1↘|      |      |
        +------+------+------+------+------+------+------+
        |      |      |      | diag |      |      |      |
    3 a |  0   |  3 = |  0   |  0   |  0   |  1 = |  0   |
        |      | 1+ 2↘|      |      |      | 1+ 0↘|      |
        +------+------+------+------+------+------+------+
        |      |      |      |      | diag |      |      |
    4 n |  0   |  0   |  2 = |  0   |  0   |  0   |  0   |
        |      |      | 1+ 1↘|      |      |      |      |
        +------+------+------+------+------+------+------+
        |      |      |      |      |      | diag |      |
    5 a |  0   |  1 = |  0   |  1 = |  0   |  0   |  0   |
        |      | 1+ 0↘|      | 1+ 0↘|      |      |      |
        +------+------+------+------+------+------+------+
        |      |      |      |      |      |      | diag |
    6   |  0   |  0   |  0   |  0   |  0   |  0   |  0   |
        |      |      |      |      |      |      |      |
        +------+------+------+------+------+------+------+

    Notice:
        * There are n+1 rows and n+1 columns.
        * The cells in the last row and the last column of each row are all 0.
        * All cells on the diagnal from the upper left (0, 0) to the 
          lower right (6, 6) are ZERO.  This diagnal represents the sub-string
          composed of ALL characters in the input text 's'.  Since, for this
          problem, sub-strings can NOT be composed of ALL characters in 's', 
          i.e. they must have a length in the range [1, n-1], all cells on 
          this diagnal are always / forced to zero.
        * The value in a cell is zero when the characters at X and Y in the 
          input text 's' do NOT match.  Cells with a value of zero (0) 
          indicate that there are no matching sub-strings starting with the 
          characters at indexes (X, Y) in the input text 's'.
        * The value in a cell is one (1) PLUS the value in the adjacent south-
          east cell, i.e. the cell one down and one to the right, when the 
          characters at X and Y in the input text 's' DO match.  This is 
          because sub-strings are composed of ADJACENT characters in 's' and 
          adjacent characters in 's' land on diagnals.
        * The sub-string patterns (cell values) north-east of the diagnal are 
          the mirror image of the sub-string patterns (cell values) south-east 
          of the diagnal.  Therefore, only half of the grid must be processed.

    Processing begins in the lower right corner (6, 6) and proceedes right to 
    left, bottom to top.  This results in all sub-problems being solved before
    the super-problems whose results depends on them.  NOTE: since this is
    tabluation, it's valid to begin in the top left corner (1, 1) and proceed
    to the bottom right corner (6, 6), however to do so requires all the cells
    of the top row and left column to be zero instead of the bottom row and 
    right column.  Also, non-zero cell values would be 1 plus the value in the 
    cell to the north-west rather than the south-east.

    The algorithm tracks the largest cell value.  If there are multiple cells
    with the same value then the algorithm will track only one of them, since
    only one sub-string is produced as a result.

    WARNING: If you should ever need only to determine the length of the 
             longest duplicate sub-string, rather than the sub-string itself, 
             then you may be tempted to replace the 0 cells with the max value 
             of the adjacent cells to the right and down, however this will 
             NOT work for inputs like: "abcabcxabcdabcabcabcd"

    NOTE: The following algorithm could track the only one coordinate (either 
          X or Y) and the sub-string size rather than tracking (X, Y).  This 
          would also mean that only [the last] two rows would be needed to 
          calculate everything rather than the entire grid.
          Experiment with this in the next implementation.
    
    Time = O(n*n/2+n) => O(n**2)
           n*n/2: Visiting 1/2 of matrix.
           +n: Extract result from matrix.

    Space = O(n**2)
            Matrix size.
"""
class Solution3_DP:
    def longestDupSubstring(self, s: str) -> str:
        result = []
        slen = len(s)
        
        # Calculate sub-string lengths in matrix.
        ldsCoords = (-1, -1)
        m = [[0] * (slen + 1) for _ in range(slen + 1)] # 2D matrix.
        for y in range(slen - 1, -1, -1):
            for x in range(y, -1, -1):
                if s[y] == s[x] and y != x:
                    m[y][x] = 1 + m[y + 1][x + 1]
                    ldsx, ldsy = ldsCoords
                    if m[y][x] > m[ldsy][ldsx]:
                        ldsCoords = (x, y)
                else:
                    m[y][x] = 0
        
        # # Report the matrix (for debugging).
        # print(" ", end=str())
        # for x in range(slen):
        #     print(f"  {s[x]:}", end=str())
        # print("")
        # for y in range(slen + 1):
        #     if slen > y:
        #         print(f"{s[y]} ", end=str())
        #     else:
        #         print(f"  ", end=str())
        #     for x in range(slen + 1):
        #         print(f"{m[y][x]:2} ", end=str())
        #     print("")

        if (-1, -1) != ldsCoords:
            # Extract longest sub-string from matrix.
            x, y = ldsCoords
            for _ in range(m[y][x]):
                result.append(s[x])
                x += 1
                y += 1
        
        return ''.join(result)

def test1(solution): 
    s = "banana"
    expected = "ana"
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test2(solution): 
    s = "abcd"
    expected = ""
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test100(solution): 
    s = "ababa"
    expected = "aba"
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test101(solution): 
    s = "abcdefg"
    expected = ""
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test102(solution): 
    s = "thequickbrownfoxjumpsoverthelazydogthequickbrownfoxjumpsoverthelazydog"
    expected = "thequickbrownfoxjumpsoverthelazydog"
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

def test103(solution): 
    s = "abcabcxabcdabcabcabcd"
    expected = "abcabc"
    startTime = time.time()
    result = solution.longestDupSubstring(s)
    endTime = time.time()
    print("{}:{}({:.6f} sec) result = {}".format(inspect.currentframe().f_code.co_name, type(solution), endTime - startTime, result))
    assert(expected == result)

if "__main__" == __name__:
    test1(Solution1_BruteForce())
    test1(Solution2_BruteForce())
    test1(Solution3_DP())

    test2(Solution1_BruteForce())
    test2(Solution2_BruteForce())
    test2(Solution3_DP())

    test100(Solution1_BruteForce())
    test100(Solution2_BruteForce())
    test100(Solution3_DP())

    test101(Solution1_BruteForce())
    test101(Solution2_BruteForce())
    test101(Solution3_DP())

    test102(Solution1_BruteForce())
    test102(Solution2_BruteForce())
    test102(Solution3_DP())

    test103(Solution1_BruteForce())
    test103(Solution2_BruteForce())
    test103(Solution3_DP())

# End of "solution.py".
