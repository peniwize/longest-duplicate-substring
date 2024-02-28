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
    This is the baseline brute force implementation that confirms that all
    tests work and are solved correctly.  This is intuitive logic that 
    searches for each sub-string in the provided string.  A sub-string is
    composed of [1, n-1] characters, where 'n' is the number of characters
    in 's'.  For example, the following 21 sub-strings are produced from 
    the string "banana":

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
    This brute force implementation uses pointers (indexes) rather than
    copying, which is faster, and it searches for sub-strings from longest
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
        cache = set()
        result = str()

        for i in range(len(s)):
            if len(s) - i > len(result): # Ignore smaller sub-strings.
                for j in range(len(s), i, -1):
                    ss = s[i:j]
                    if ss in cache:
                        if len(result) < len(ss):
                            result = ss
                            break # Ignore smaller sub-strings.
                    else:
                        cache.add(ss)

        return result

"""
    TODO: Describe how this works.  Illustrate 2D matrix.
          Point out that only 1/2 of the matrix is actually populated.
          Explain that the matrix can NOT contain sub-string lengths
          that propagate to matrix[0][0] because this breaks for 
          the last test (review test data for specific reason).

          Note that only 1/2 of the matrix memory could be used if the
          address of each element were explicitly calculated within a
          1D array.

          Tracking both x and y of the lcs is not necessary if the 
          lcs length is tracked and only one coordinate.  This also 
          eliminates the need for an entire 2D table since onlt the last 
          two rows are needed.  The algorithm could allocate two and leap
          frog them (to reuse the oldest) with each iteration.
    
    Time = O(?)

    Space = O(?)
"""
class Solution3_DP:
    def longestDupSubstring(self, s: str) -> str:
        result = []
        slen = len(s)
        
        # Calculate sub-string lengths in matrix.
        lcsCoords = (-1, -1)
        m = [[0] * (slen + 1) for _ in range(slen + 1)] # 2D matrix.
        for y in range(slen - 1, -1, -1):
            for x in range(y, -1, -1):
                if s[y] == s[x] and y != x:
                    m[y][x] = 1 + m[y + 1][x + 1]
                    lcsx, lcsy = lcsCoords
                    if m[y][x] > m[lcsy][lcsx]:
                        lcsCoords = (x, y)
                else:
                    #m[y][x] = max(m[y][x + 1], m[y + 1][x])
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

        if (-1, -1) != lcsCoords:
            # Extract longest sub-string from matrix.
            x, y = lcsCoords
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
