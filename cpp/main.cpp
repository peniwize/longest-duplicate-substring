/*!
    \file "main.cpp"

    Author: Matt Ervin <matt@impsoftware.org>
    Formatting: 4 spaces/tab (spaces only; no tabs), 120 columns.
    Doc-tool: Doxygen (http://www.doxygen.com/)

    https://leetcode.com/problems/longest-duplicate-substring/
    https://github.com/peniwize/longest-duplicate-substring.git
*/

//!\sa https://github.com/doctest/doctest/blob/master/doc/markdown/main.md
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "utils.hpp"

/*
    Given a string s, consider all duplicated substrings: (contiguous) 
    substrings of s that occur 2 or more times. The occurrences may overlap.

    Return any duplicated substring that has the longest possible length.
    If s does not have a duplicated substring, the answer is "".

    Constraints:

        * 2 <= s.length <= 3 * 104
        * s consists of lowercase English letters.
*/

/*
    Time = O(?)

    Space = O(?)
*/
class Solution {
public:
    string longestDupSubstring(string s) {

//
//!\todo TODO: >>> Under Construction <<<
//
return {};

    }
};
// {----------------(120 columns)---------------> Module Code Delimiter <---------------(120 columns)----------------}

namespace doctest {
    const char* testName() noexcept { return doctest::detail::g_cs->currentTest->m_name; }
} // namespace doctest {

TEST_CASE("Case 1")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"banana"};
    auto const expected = string{"ana"};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 2")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"abcd"};
    auto const expected = string{""};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 100")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"ababa"};
    auto const expected = string{"aba"};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 101")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"abcdefg"};
    auto const expected = string{""};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 102")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"thequickbrownfoxjumpsoverthelazydogthequickbrownfoxjumpsoverthelazydog"};
    auto const expected = string{"thequickbrownfoxjumpsoverthelazydog"};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

TEST_CASE("Case 103")
{
    cerr << doctest::testName() << '\n';
    auto const s = string{"abcabcxabcdabcabcabcd"};
    auto const expected = string{"abcabc"};
    auto solution = Solution{};
    { // New scope.
        auto const start = std::chrono::steady_clock::now();
        auto const result = solution.longestDupSubstring(s);
        CHECK(expected == result);
        cerr << "Elapsed time: " << elapsed_time_t{start} << '\n';
    }
    cerr << "\n";
}

/*
    End of "main.cpp"
*/
