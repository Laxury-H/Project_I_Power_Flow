# Project I power flow
Development of a Python-Based Program for Steady-State Power Flow Analysis Using the Newton–Raphson Method

Educational technical package. Supervisor approval of scope and formatting remains necessary. Personal fields remain placeholders. AI-assisted implementation and drafting must be reviewed, understood and disclosed according to the applicable course policy; no claim of unaided authorship is made.

## Start here
Vietnamese step-by-step setup and demo guide: `START_HERE_VI.md`. Optional Windows helpers: `setup_windows.cmd` and `run_windows.cmd` (not executed on Windows here).

## Install and run
Python 3.12 recommended. From this directory:
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
python -m pytest -q --junitxml=results/tests.xml
python verify_pypower.py
python -m streamlit run app.py
```
PYPOWER is used only by the comparison script, never by the main solver. `results/environment.txt` records the numerical generation environment. `results/test_environment.txt` records test dependencies. Package ranges support installation; environment records identify the actual run. Reproduction is numerical to stated tolerances, not byte-identical plots across platforms.

## Input contract
All CSV powers and impedances use one common base, 100 MVA for supplied cases. Voltage magnitudes are pu, CSV angles are degrees, internal angles are radians. Bus IDs may be noncontiguous integers. Bus columns: bus,type,pg_pu,qg_pu,pd_pu,qd_pu,vm_pu,va_deg. Line columns: from_bus,to_bus,r_pu,x_pu. Additional columns are rejected to avoid silently ignoring unsupported taps or charging.

Slack pg and qg fields and PV qg fields are finite placeholders, ignored as constraints and recovered from the solution. PQ vm and all non-slack va fields are initial guesses. Net injection is generation minus demand. Demand is nonnegative, R >= 0 and X > 0. One connected island and exactly one Slack bus are required. Parallel lines are supported through additive admittances. No switching of PV to PQ at reactive limits.

For your own CSVs use the UI or:
```python
from src.data_models import read_csv
from src.newton_raphson import solve
from src.branch_flows import output_tables
buses, lines = read_csv('my_buses.csv', 'my_lines.csv')
solution = solve(buses, lines)
if solution.converged:
    bus_results, branch_results = output_tables(buses, lines, solution, base_mva=100)
```

## Reproduce the study
`main.py` overwrites generated numerical tables and plots under results and figures. Both pd and qd scale together to 80%, 100% and 120%; all scheduled generation and controlled voltage setpoints remain fixed. Each case starts independently from its CSV voltage guess. Results JSON is the common data source for the report and deck. History row 0 is the initial mismatch; the iteration count is the number of completed updates.

The three-bus inputs come from the supplied task. The five-bus system is synthetic, developed for this project, not an IEEE or MATPOWER benchmark. No real grid is represented.

## Files
- src: reusable solver, Jacobian, validation and branch flows
- data: editable input CSVs
- tests: numerical, input validation, failure-path and Streamlit tests
- results: actual tables, JUnit test evidence and PYPOWER comparison
- report: editable English report and corresponding PDF
- slides: editable English deck with speaker notes
- docs: Vietnamese math/code guides, bilingual defense Q&A, script, study plan and checklist
- figures: exact generated diagrams and result plots

## Tested scope and limitations
See results/tests.xml and results/pypower_comparison.csv. Streamlit AppTest covers example selection and solve buttons for both networks. Browser display, CSV upload/download interaction and a user-machine installation require local review. Dense Newton has no damping or continuation and may fail away from the tested operating points. Failure to converge is not proof that no physical solution exists. No thermal ratings, voltage compliance criteria, machine reactive capability or dynamic stability assessment is implemented.

## Interface follow-up
Results persist on unchanged-input reruns, including download-button reruns. Changing inputs invalidates stored results before the next solve. The displayed convergence chart uses log10 mismatch; downloaded CSV retains the original pu residual. AppTest also verifies state retention, input invalidation, 120% loading and the zero-update failure path.

   PYTHON = 3.12
    OPENTRADE = 5.15.2  
    PYPOWER = 5.15.2 
    Streamlit = 1.36.0
    Pandas = 2.2.2
    Numpy = 1.26.4
    Matplotlib = 3.9.1