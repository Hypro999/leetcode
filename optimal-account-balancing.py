"""
[HARD]
https://leetcode.com/problems/optimal-account-balancing/

You are given an array of transactions transactions where
transactions[i] = [from(i), to(i), amount(i)] indicates that the person with
ID = from(i) gave amount(i) $ to the person with ID = to(i).

Return the minimum number of transactions required to settle the debt.

Example:
Input: transactions = [[0,1,10],[1,0,1],[1,2,5],[2,0,5]]
Output: 1
Explanation:
    Person #0 gave person #1 $10.
    Person #1 gave person #0 $1.
    Person #1 gave person #2 $5.
    Person #2 gave person #0 $5.
Therefore, person #1 only need to give person #0 $4, and all debt is settled.
"""

import collections
import unittest


class Solution:

    def min_transfers(self, transactions: list[list[int]]) -> int:
        """
        The official LeetCode Editorial backtracking solution.

        Basic idea: This is a closed system where money can't be created nor destroyed.

        Think of this system as a pot that people put money into and take money from.
        At the end of the day everyone will either be net positive or net negative.

        Assume that instead of a pot you assign a person to be responsible for resolving
        debt. Everyone who owes money would give money to this person, and everyone
        owed money would take from this person. This means that in the WORST case, the
        answer would be n - 1 (everyone except the collector would give or take from the
        to the collector).

        If we wanted to find a way to minimize transactions, then things get a bit
        trickier. The idea behind the backtracking solution is that we could have a
        person owing money pay forward the entire amount they owe to a person owed
        money in a single transaction. Let's call this operation "pushing debt".

        Assume A --10--> B and A --5--> C. Converting this into the following series
        of transactions: A --15--> B and B --5--> C would yield the same number of
        transactions as if A had paid B and C separately. Thus the technique we're
        using above would not lead to an increase in the number of transactions (though
        it would be annoying in the real world if you didn't owe any money but still
        had to pay).

        Getting back to the solution, what you do is backtrack recursively, trying to
        push one person's debt onto someone else. When you push your debt to someone
        else, they should ideally be the opposite magnitude of the person pushing (i.e.
        if someone owes, push the debt to an owed) and the person being pushed to should
        not have 0 outstanding debt (otherwise we'd just be increasing the number of
        transactions performed for no reason - why not pay an ower/owned instead of
        getting someone clean involved? It's the difference between 1 transaction and
        2). Keep track of the minimum cost for each recursive call and return that at
        the end.

        Note: The Splitwise algorithm is different because Splitwise enforces a very
        sensible rule. At the end of debt simplification, no one should owe someone that
        they didn't already owe before. The solution for this problem is different and
        https://medium.com/@mithunmk93/algorithm-behind-splitwises-debt-simplification-feature-8ac485e97688
        does a good job of explaining it.
        """
        balance_map = collections.defaultdict(int)
        for a, b, amount in transactions:
            balance_map[a] += amount
            balance_map[b] -= amount

        balance_list = [amount for amount in balance_map.values() if amount]
        n = len(balance_list)

        def dfs(cur):
            while cur < n and not balance_list[cur]:
                cur += 1
            if cur == n:
                return 0
            cost = float("inf")
            for nxt in range(cur + 1, n):
                # If nxt is a valid recipient, do the following:
                # 1. add cur's balance to nxt.
                # 2. recursively call dfs(cur + 1).
                # 3. remove cur's balance from nxt.
                if balance_list[nxt] * balance_list[cur] < 0:
                    balance_list[nxt] += balance_list[cur]
                    cost = min(cost, 1 + dfs(cur + 1))
                    balance_list[nxt] -= balance_list[cur]
            return cost

        return dfs(0)


class SolutionTest(unittest.TestCase):

    def test_provided_first(self):
        transactions = [[0, 1, 10], [2, 0, 5]]
        solution = Solution().min_transfers(transactions)
        self.assertEqual(solution, 2)

    def test_provided_second(self):
        transactions = [[0, 1, 10], [1, 0, 1], [1, 2, 5], [2, 0, 5]]
        solution = Solution().min_transfers(transactions)
        self.assertEqual(solution, 1)

    def test_custom_first(self):
        transactions = [[0, 1, 5], [0, 3, 5], [1, 3, 5], [1, 4, 2], [1, 5, 3]]
        solution = Solution().min_transfers(transactions)
        self.assertEqual(solution, 3)

    def test_custom_second(self):
        transactions = [
            [0, 1, 5],
            [0, 3, 5],
            [1, 3, 5],
            [1, 4, 2],
            [1, 5, 3],
            [2, 0, 10],
        ]
        solution = Solution().min_transfers(transactions)
        self.assertEqual(solution, 3)


if __name__ == "__main__":
    unittest.main()
