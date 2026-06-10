Performance notes
=================

Overview
--------
This document describes profiling and small optimizations applied to backlog planning.

Optimizations applied
---------------------
- Precompute item scores once in select_plan to avoid repeated score computations when sorting.
- Use set lookups for dependency checks (O(1) per dep) instead of nested searches.

Profiling
---------
A profiling script is provided at script/profile_backlog.py. Run:

    python script/profile_backlog.py src/IS2_T3_C5_IA/IS2_T3_C5_IA/sample_backlog.json

It runs several iterations and writes profile_stats.txt with the top cumulative-time callers.

Results
-------
A sample profiling run was executed and results are saved as src/IS2_T3_C5_IA/IS2_T3_C5_IA/profile_stats.txt in the repository. The main hotspots were plan selection and score computation; precomputing scores reduced repeated work during sorting.

Next steps
----------
- For larger backlogs (thousands+ items), consider using a heap-based selection or solving as a knapsack with dependencies.
- Add microbenchmarks and CI-based performance regression checks if needed.
