ROUTE A: complete Lean source project

Main theorem: PaperRoute.induced_matching_packing20
Toolchain: leanprover/lean4:v4.35.0-rc4
mathlib commit: 49fd9dee36e7bbf345fe7981d2de6aeeb591f75b

The local Library is a documented fork: 39 files only rename the namespace; six supporting files are refactored. The manuscript-level theorems, exact identities and unified load proof are supplied separately. This is not a claim of an unrelated mathematical strategy.

The project includes all project-specific source dependencies, the pinned Lake
manifest, independent semantic/sharpness checks, and an executable dependency audit.
It does not include Lean binaries, mathlib source/binary caches, or .lake.
An initial reproduction therefore needs network access to fetch the pinned
dependencies (or an existing cache). No dependency on the other route is required.

WINDOWS REPRODUCTION
1. Install the exact Lean version above (for example using elan).
2. Open PowerShell in this extracted directory.
3. Run: .\reproduce.ps1 -FetchCache
   If Lean is not on PATH: .\reproduce.ps1 -LeanBin 'C:\path\to\lean\bin' -FetchCache
   With dependencies already available, omit -FetchCache.
The script verifies source hashes, builds the default library, checks supplemental
proofs, audits actual proof dependencies, and checks all crosswalk declarations.
It stops on any failed command and writes reproduction-logs.

The source-manifest.json hashes exclude themselves and reproduction logs.
The package contains no admitted mathematical lemma. The accepted dependency
axioms are propext, Classical.choice and Quot.sound.

See the paired English PDF, the Chinese ROUTE_COMPARISON report and
proof_crosswalk.csv in the full delivery for the mathematical correspondence.
