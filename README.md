## Example

The proof-of-concept is executed by running `python3 gen-and-test.py`. This will use the dataset in dummy.py to find a definition for the term in gen-and-test.py by repeatedly generating and testing new rules. By default, this looks for a definition of `Island` and will find that, in the dataset, countries with less than two neighbours are considered islands.

This particular example highlights how IDP can use aggregates to count the amount of elements that fit a particular expression, and use that number as part of a larger expression. This expressiveness means that we can search and find interesting rules that involve the amount of elements which fit a particular predicate.

```
(some output omitted)
[82] Testing ! a: Island(a) <- #{b : Neighbour(b, a)} < 4.
[83] Testing ! a: Island(a) <- #{b : Neighbour(b, a)} < 2.
[84] Testing ! a: Island(a) <- ? b d e: Neighbour(b, b) & Neighbour(d, e).
[85] Testing ! a: Island(a) <- ? b d: Neighbour(b, b) & Island(d).
[86] Testing ! a: Island(a) <- #{b : Neighbour(b, b)} < 3.
[87] Testing ! a: Island(a) <- #{b : Neighbour(b, b)} < 3.
Potential rule found: (75 % coverage)
[83] ! a: ApproxIsland(a) <- #{b : Neighbour(b, a)} < 2.
*********
```

There is a different example available in gen-and-test-family.py. This demonstrates how inductive definitions can be used and discovered. It does not use aggregates, but it does involve more complicated First-Order Logic, as well as inductive definitions. The code in this file is largely the same as gen-and-test.py, with the exception of different configuration in the beginning of the file, and a different dataset. It sets options to disable aggregates (for performance reasons) as well as enable inductive defitions. Using data_family.py as a datasource, it tries to find a definition for `Ancestor`, which inductively uses `Ancestor` itself. Because this rule is somewhat more complicated, it takes significantly longer to find.

```
[3536] Testing ! a b: Ancestor(a, b) <- ? c d: Parent(c, d) & Ancestor(a, a) | Parent(a, b) & Parent(a, b).
[3538] Testing ! a b: Ancestor(a, b) <- ? f: Parent(b, b) & Ancestor(a, f) | Parent(a, b).
[3540] Testing ! a b: Ancestor(a, b) <- ? d: Parent(b, d) & Ancestor(a, d) | Parent(a, b).
[3547] Testing ! a b: Ancestor(a, b) <- ? d f: Parent(b, d) & Ancestor(a, f) | Parent(a, b) & Parent(a, b).
[3549] Testing ! a b: Ancestor(a, b) <- ? c: Parent(c, b) & Ancestor(a, c) | Parent(a, b).
Potential rule found: (100 % coverage)
[3549] ! a b: ApproxAncestor(a, b) <- ? c: Parent(c, b) & ApproxAncestor(a, c) | Parent(a, b).
*********
```
