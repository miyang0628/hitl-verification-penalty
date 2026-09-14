# hitl-verification-penalty

Replication data, analysis notebooks, and publication-ready figures for a study of
**bottleneck migration** and the **governance-induced verification penalty** in an
AI-assisted credit-rating human-in-the-loop (HITL) pipeline.

This repository is a companion to earlier work on XAI-assisted HITL queues. Where that
work modelled how *reducing* verification effort restores stability, this study examines
the opposite regime: how verification friction a firm adopts to prevent rubber-stamping
migrates the throughput bottleneck downstream and makes additional staffing unavoidable.

---

## Central idea

AI leverage does not cure the "cost disease" of knowledge work; it **migrates** it to the
human review-and-judgment stage, and the verification friction adopted to keep oversight
meaningful fixes that migration in place. Three propositions plus a joint program formalise
the chain, all bridged by the verification cost `v_i(f)`:

1. **Delegation (Becker) paradox** — when verification cost `v_i` exceeds AI time saving
   `g_i`, delegating a task reduces net value; under convex error exposure the optimum is a
   smooth interior policy, not a binary choice.
2. **Bottleneck migration** — when `v_i(f) > tau_i`, upstream automation shifts the binding
   constraint onto the human review stage rather than relieving it.
3. **Governance-capacity tradeoff** — required staffing rises in verification friction
   (`dc*/df = lambda*k`; integer form `c*(f) = ceil(lambda * E[S(f)])`), with an interior
   optimal friction that trades error-cost reduction against staffing cost.

---

## Repository structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── tasks.csv                 # Per-task pre/post-AI times, verification cost, severity, constraints
│   └── queue_params.json         # Bottleneck-stage (Stage 6) queueing parameters
├── notebooks/
│   ├── 01_data_integrity.ipynb        # Consistency checks; parameter reconciliation
│   ├── 02_theorem_verification.ipynb  # Symbolic checks of the propositions and corollary
│   ├── 03_figures_tables.ipynb        # Generates the core data figures and tables
│   ├── 04_simulation_verification.ipynb # Discrete-event check of the coupled M/G/c queue
│   ├── 05_revision_experiments.ipynb  # Interior delegation, joint optimum, seasonality
│   └── 06_weight_sensitivity.ipynb    # Weight-sensitivity of the interior optimal friction
├── results/
│   ├── figures/                  # PNG + PDF, grayscale, 600 dpi, no captions
│   └── tables/                   # CSV + LaTeX + intermediate JSON results
└── docs/
    └── step1_data_integrity.md   # Data-integrity report (reconciliation and fixed estimates)
```

---

## Data

`data/tasks.csv` — seven review tasks (T1-T7) with, for each task:
`pre_ai_hours`, `post_ai_hours`, `verification_hours`, `adoption_rate`,
`error_severity` (1-5), `accountability_constraint` (0/1), and `compression_type`.

- **Delegation-loss (Becker) tasks:** T3, T6 — here `v_i > g_i` (net saving is negative).
- **Accountability-constrained tasks:** T3, T6, T7 — human sign-off is legally required.

`data/queue_params.json` — Stage-6 bottleneck parameters. Type-level mean service times
(`s_fast`, `s_slow`) are **estimated, scenario-based** values chosen to be internally
consistent with the reported mean service time and client mix; the `0.5 h / 12 h` figures
are min/max range endpoints, not means. See `docs/step1_data_integrity.md` and
`01_data_integrity.ipynb` for the reconciliation. Because further observation is not
currently feasible, these values are fixed and declared as scenario assumptions.

---

## Figures

All figures are **grayscale**, **600 dpi**, saved as both **PNG and PDF**, without captions
(captions live in the manuscript).

### Data figures (Python-generated)

| File | Content |
|---|---|
| `fig1_delegation_frontier`  | Delegation frontier on the (`g_i`, `v_i`) plane; delegation-loss region shaded |
| `fig2_net_effect`           | Per-task net effect of delegation (`g_i - v_i`) |
| `fig3_governance_capacity`  | Governance-capacity tradeoff: minimum reviewers vs friction `f` |
| `fig4_optimal_friction`     | Optimal-friction surface `f*` over error-cost scale and service-time sensitivity |
| `fig5_mgc_waiting`          | M/G/c mean waiting time vs arrival rate at the Stage-6 bottleneck |
| `fig6_sim_verification`     | Simulation vs analytical (M/G/1 exact; M/G/c) |
| `fig7_joint_optimum`        | Joint program: total cost vs friction, interior optimum `f*` |
| `fig8_nonlinear_delegation` | Optimal delegation under linear vs convex error exposure |
| `fig9_seasonality`          | Seasonal stress test: mean and 95th-percentile waiting time |
| `fig10_weight_sensitivity`  | Sensitivity of the interior `f*` to objective-weight perturbations |

### Conceptual figures (schematic diagrams)

| File | Content |
|---|---|
| `CF1_pipeline_diagram`      | Eight-stage credit-rating pipeline; Stage 6 as the bottleneck |
| `CF2_bottleneck_migration`  | Pre-AI distributed load vs post-AI concentration at review |
| `CF3_causal_chain`          | The three results bridged by verification cost `v_i(f)` |
| `CF4_two_failure_modes`     | Verification effort as the common lever (rubber-stamp vs throughput) |
| `GA_graphical_abstract`     | Graphical abstract (submitted separately, not in the body) |

---

## Reproducing the results

```bash
# 1. Install dependencies
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt

# 2. Run the notebooks in order (regenerates everything under results/)
jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_integrity.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_theorem_verification.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_figures_tables.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_simulation_verification.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/05_revision_experiments.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/06_weight_sensitivity.ipynb
```

Or open the notebooks interactively with `jupyter lab` / `jupyter notebook` and run all cells.

**Updating the estimates.** If observed type-level service times become available later,
edit the four values in `data/queue_params.json` (`s_fast`, `s_slow`, and the client mix)
and re-run `03_figures_tables.ipynb`; all dependent figures and tables regenerate.

---

## Requirements

Python 3.10+, with `numpy`, `pandas`, `matplotlib`, `seaborn`, `sympy`, and `jupyter`.
Exact packages are listed in `requirements.txt`.

---

## Notes and limitations

- Parameters come from a single anonymised pipeline; task/firm identifiers are removed.
- Task coding was a single-coder check against written procedures and regulation; no
  independent double-coding or inter-rater statistic is reported.
- Type-level service-time means are estimated (scenario-based), not directly observed.
- Multi-server results are reported with simulation confidence intervals; the KLB
  approximation is shown for reference only.
- The joint program is solved by grid enumeration; the interior `f*` is grid-resolved and
  robust to +/-50% weight perturbations (see `06_weight_sensitivity.ipynb`).
- Results are a worked, reproducible illustration of the model, not calibrated predictions.

---

## Citation

If you use this repository, please cite the accompanying paper. A `CITATION.cff` file will
be added on publication.

## License

Released under the MIT License. See `LICENSE`.
