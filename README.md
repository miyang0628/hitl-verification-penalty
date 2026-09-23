# hitl-verification-penalty

Replication data, analysis notebooks, and publication-ready figures for a study of
**bottleneck migration** and the **governance-induced verification penalty** in an
AI-assisted credit-rating human-in-the-loop (HITL) pipeline.

This repository accompanies a follow-up to earlier work on HITL review queues in which
explainable-AI support *reduced* reviewer service time. This study examines the opposite
regime: verification friction that a firm deliberately adopts to prevent rubber-stamping
raises service time, migrates the throughput bottleneck to human review, and turns
governance intensity into a staffing decision.

---

## Central idea

AI leverage does not cure the "cost disease" of knowledge work; it **migrates** it to the
human review-and-judgment stage, and the verification friction adopted to keep oversight
meaningful fixes that migration in place. Three results and a joint program formalise the
chain, all bridged by the verification cost `v_i(f)`:

1. **Delegation paradox** (Props 4.1–4.2) — when the verification cost `v_i` exceeds the
   gross AI time saving `g_i = tau_i`, delegating a task destroys value. Under convex error
   exposure `phi(x) = x^2` the optimal delegation is a smooth interior policy
   `x_i* = clip((g_i - v_i) / (2 e_i), 0, cap_i)`.
2. **Bottleneck migration** (Prop 4.3) — `dS_i/dx_i = v_i(f) - tau_i`; when `v_i(f) > tau_i`,
   delegation lengthens the review stage. With `g_i = tau_i` this is the same condition as
   the delegation paradox.
3. **Governance–capacity tradeoff** (Prop 4.4, Cor 4.5) — required staffing rises linearly in
   friction, `dc*/df = lambda * k`, with integer form `c*(f) = ceil(lambda * E[S(f)])`.
4. **Joint program** (Section 4.4) — choose delegation `x`, reviewers `c`, and friction `f`
   together. Friction makes delegation safe, so friction and delegation are complements; the
   optimal friction is set by the staffing staircase — the most friction the current
   reviewer team can absorb.

### Headline numbers (illustrative parameters)

| Quantity | Value |
|---|---|
| Delegation-loss tasks | T3, T6 (`tau_i - v_i = -1.0 h` each) |
| Optimal friction `f*` | **5.40** |
| Reviewers at `f*` | `c* = 2` (a third reviewer is needed beyond the plateau) |
| Optimal delegation `x*` | T1 = 1, T2 = 1, T5 = 0.5, T7 = 0.5 (cap); T3, T4, T6 kept human |
| Review load at `x*` | 5.2 h before friction, 6.7 h at `f*` (12.0 h pre-AI) |
| `f*` under ±50% weight changes | 5.40 in four of six cases; 8.60 (errors +50%) and 10.75 (hours −50%) with `c* = 3` |
| Seasonal ×3 peak | 95th-percentile wait ≈ 13.6 h |

---

## Repository structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── tasks.csv                        # Per-task times, verification cost, severity, constraints
│   └── queue_params.json                # Stage-6 queueing parameters (fixed scenario values)
├── notebooks/
│   ├── 01_data_integrity.ipynb          # Consistency checks; parameter reconciliation
│   ├── 02_theorem_verification.ipynb    # Symbolic checks of Props 4.1–4.4 and Cor 4.5
│   ├── 03_figures_tables.ipynb          # Core data figures (fig1–fig5) and Tables 1–2
│   ├── 04_simulation_verification.ipynb # Discrete-event check of M/G/1 (exact) and M/G/c (fig6)
│   ├── 05_revision_experiments.ipynb    # Interior delegation, joint program, migration, seasonality
│   └── 06_weight_sensitivity.ipynb      # Weight sensitivity of f* (fig10)
├── scripts/
│   └── make_cf3_causal_chain.py         # Redraws the CF3 causal-chain schematic
├── results/
│   ├── figures/                         # PNG + PDF, grayscale, 600 dpi, no captions
│   └── tables/                          # CSV + LaTeX + intermediate JSON results
└── docs/
    └── step1_data_integrity.md          # Data-integrity report (reconciliation and fixed estimates)
```

---

## Data

`data/tasks.csv` — seven review tasks (T1–T7) with `pre_ai_hours`, `post_ai_hours`,
`verification_hours`, `adoption_rate`, `error_severity` (1–5), `accountability_constraint`
(0/1), and `compression_type`.

| Symbol | Definition in the model |
|---|---|
| `tau_i` | `pre_ai_hours` — human task time; the AI draft replaces it, so `g_i = tau_i` |
| `v_i` | `verification_hours` — time to verify a full AI draft |
| `e_i` | `error_severity / 5` — error cost of a fully delegated task (hour-equivalents) |
| `cap_i` | 0.5 if `accountability_constraint == 1` (T3, T6, T7), else 1 |
| post-AI hours | Observed averages under current adoption; used only for residual-labour shares (Table 2) |

`data/queue_params.json` — Stage-6 bottleneck parameters. Type-level mean service times are
**estimated, scenario-based** values consistent with the reported mean service time and
client mix: `s_fast = 1.33 h`, `s_slow = 8.0 h`, prime share `p = 0.60`
(`E[S] = 4.0 h`, `C_S^2 = 0.67`). The `0.5 h / 12 h` values are min/max range endpoints,
not means. See `docs/step1_data_integrity.md` and `01_data_integrity.ipynb`.

### Joint-program parameters

| Parameter | Value | Meaning |
|---|---|---|
| `lambda` | 0.30 cases/h | Stylised single-team arrival rate |
| `k` | 0.6 | Friction sensitivity, `v_i(f) = v_i (1 + k f)` |
| `c_H` | 0.4 | Cost per reviewer |
| `w_h` | 0.25 | Weight on review hours `E[S]` |
| `w_e` | 5.0 | Weight on escaped-error cost (so `w_e * e_i = severity`) |
| grid | `x_i ∈ {0, .25, .5, .75, 1}`, `f ∈ [0, 12]` step 0.05 | Full enumeration |

Objective:
`Z(x, c, f) = c_H * c + w_h * E[S(x, f)] + w_e * sum_i e_i x_i^2 / (1 + f)`,
with `E[S(x, f)] = sum_i ((1 - x_i) tau_i + x_i v_i (1 + k f))`, subject to
`c > lambda * E[S]` and `x_i <= cap_i`.

---

## Figures

All figures are **grayscale**, **600 dpi**, saved as both **PNG and PDF**, without captions
(captions live in the manuscript).

### Data figures (Python-generated)

| File | Notebook | Manuscript | Content |
|---|---|---|---|
| `fig1_delegation_frontier`  | 03 | Fig 4  | Tasks on the (`g_i = tau_i`, `v_i`) plane; delegation-loss region shaded |
| `fig2_net_effect`           | 03 | Fig A1 | Per-task net effect `tau_i - v_i` |
| `fig3_governance_capacity`  | 03 | Fig 6  | Minimum reviewers vs friction `f` for three values of `k` |
| `fig4_optimal_friction`     | 03 | Fig A2 | Closed-form `f*` (Cor 4.5) over error-cost scale and `k` |
| `fig5_mgc_waiting`          | 03 | Fig A3 | M/G/c mean waiting time vs arrival rate at Stage 6 |
| `fig6_sim_verification`     | 04 | Fig A4 | M/G/1 exact P-K vs simulation; M/G/c simulation with 95% CI and KLB reference |
| `fig7_joint_optimum`        | 05 | Fig 7  | Joint-program cost envelope vs `f`, with optimal reviewer count `c*` |
| `fig8_nonlinear_delegation` | 05 | Fig 5  | Optimal delegation, linear vs convex exposure, with accountability caps |
| `fig9_seasonality`          | 05 | Fig 10 | Seasonal stress test: mean and 95th-percentile waiting time |
| `fig10_weight_sensitivity`  | 06 | Fig 8  | `f*` and `c*` under ±50% weight perturbations |

### Conceptual figures (schematic diagrams)

| File | Manuscript | Content |
|---|---|---|
| `CF4_two_failure_modes`     | Fig 1 | Verification effort as the common lever (rubber-stamp vs throughput failure) |
| `CF1_pipeline_diagram`      | Fig 2 | Eight-stage credit-rating pipeline; Stage 6 as the bottleneck |
| `CF3_causal_chain`          | Fig 3 | The results bridged by verification cost `v_i(f)` (`scripts/make_cf3_causal_chain.py`) |
| `CF2_bottleneck_migration`  | Fig 9 | Pre-AI distributed load vs post-AI concentration at review |
| `GA_graphical_abstract`     | —     | Graphical abstract (submitted separately) |

---

## Reproducing the results

```bash
# 1. Install dependencies
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt

# 2. Run the notebooks in order (regenerates everything under results/)
cd notebooks
for nb in 01_data_integrity 02_theorem_verification 03_figures_tables \
          04_simulation_verification 05_revision_experiments 06_weight_sensitivity; do
  jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 "$nb.ipynb"
done

# 3. (Optional) redraw the causal-chain schematic
cd ../scripts && python make_cf3_causal_chain.py
```

Notebook 04 runs 240 simulation replications and takes a few minutes; the others finish in
seconds. All simulations use fixed seeds (0–39), so results are reproducible exactly.

**Updating the estimates.** If observed type-level service times become available, edit
`data/queue_params.json` (`s_fast_prime_hours`, `s_slow_scarce_hours`, `client_mix`) and
re-run notebooks 04 and 05. If task-level data change, edit `data/tasks.csv` and re-run all
notebooks.

---

## Revision log

Changes relative to the previous version of this repository:

1. **Gross time saving.** `g_i = tau_i` because the AI draft replaces the human task. The
   previous `g_i = pre - post` charged verification twice, since observed post-AI time already
   contains the checking time (e.g. T3: post = `v` = 2.5 h). Net values are now `tau_i - v_i`
   (T3, T6 = −1.0 h each), which makes the delegation-paradox and migration conditions coincide.
2. **Error term of the joint program.** Escaped-error cost is `w_e * sum_i e_i x_i^2 / (1 + f)`:
   it grows with delegation, as in the task-level model. The previous `sum_i e_i (1 - x_i)` made
   retained human work the source of error, contradicting Prop 4.2.
3. **Friction channel.** Friction acts only on verification, `v_i(f) = v_i (1 + k f)`, as the
   model defines; the previous code multiplied the whole stage service time.
4. **Enumeration.** Full per-task enumeration over `{0, .25, .5, .75, 1}` with accountability
   caps (T3, T6, T7 at 0.5), replacing the three-group grid; `c` is the smallest stable integer.
5. **Error costs.** `e_i = severity / 5` is used consistently in the task-level and joint
   analyses, with `w_e = 5` in the joint program.
6. **Simulation.** All queueing checks and the seasonal stress test use the fixed scenario in
   `queue_params.json`; every check uses 40 replications × 20,000 jobs after a 2,000-job
   warm-up. M/G/1 results are reported with 95% confidence intervals (exact P-K value inside
   the interval at every load; relative error < 0.7%).
7. **Housekeeping.** Hard-coded external save paths removed; `scripts/` added.

---

## Requirements

Python 3.10+, with `numpy`, `pandas`, `matplotlib`, `seaborn`, `sympy`, `jupyter`, and
`nbformat`. Exact packages are listed in `requirements.txt`.

---

## Notes and limitations

- Parameters come from a single anonymised pipeline; task and firm identifiers are removed.
- Task coding was a single-coder check against written procedures and regulation; no
  independent double-coding or inter-rater statistic is reported.
- Type-level service-time means are estimated (scenario-based), not directly observed.
- Error costs are a linear scaling of a 1–5 severity rating, not measured losses.
- Multi-server results are reported with simulation confidence intervals; the KLB
  approximation is shown for reference only.
- The joint program is solved by full enumeration; `f*` is grid-resolved (step 0.05).
- Results are a worked, reproducible illustration of the model, not calibrated predictions.

---

## Citation

If you use this repository, please cite the accompanying paper. A `CITATION.cff` file will be
added on publication.

## License

Released under the MIT License. See `LICENSE`.
