# Directed two-linkage → Cycle factor containing an even cycle

Category: Complexity open

## Source

The source gives a digraph and two designated terminal pairs. Its outputs are two vertex-disjoint directed paths joining the respective pairs, or NO-SOLUTION.

## Target

The source asks for two vertex-disjoint directed paths between prescribed terminal pairs. The target is a loopless digraph and asks for a spanning directed cycle factor containing at least one even cycle; directed two-cycles are allowed.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This addresses the complexity difference between parity conditions imposed on some cycles and on all cycles of a factor.

## Difficulty

A parity modification must prevent unintended even cycles without destroying the linkage correspondence.

## Literature context

Requiring at least one even cycle is different from requiring every cycle to have a specified parity; those classifications cannot be substituted for this predicate.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Odd and Even Harder Problems on Cycle-Factors](https://arxiv.org/html/2510.18393v1): Horsch, Kiraly, Mendoza-Cadena, Pap, Szabo and Yamaguchi, Odd and Even Harder Problems on Cycle-Factors, arXiv:2510.18393v1 (2025), Section 3.4 and Section 6, explicitly leave the target open. Theorem 3.5 proves hardness for a factor containing an odd cycle from directed two-linkage. The all-odd and all-even variants are also hard, but have different quantifiers. Ordinary directed cycle-factor existence is polynomial by bipartite matching.
- [arXiv version record](https://arxiv.org/abs/2510.18393): On 2026-09-16 checked the arXiv version record and searched "cycle-factor" "even cycle" complexity 2026, "Odd and Even Harder" cycle factors, "exists even" "cycle-factor" complexity, "cycle factor" "at least one even" 2026, and "2510.18393" algorithm complexity. No later resolution was identified. Coverage is bounded, especially for equivalent algebraic formulations; this is evidence of openness within the search, not an exhaustive certificate.

Fixed from board record `website/questions/exists-even-directed-cycle-factor.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
