# linear-algebra

Linear algebra experiments in Python: interactive visualizations with a topic home menu. Dependencies and the environment are managed with [uv](https://docs.astral.sh/uv/).

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package and virtualenv manager)
- Python 3.13 (pinned in `.python-version`)

## Install

From the repository root:

```bash
uv sync
```

This creates `.venv` and installs dependencies (numpy, plotly, dash).

## Run

**Main app** — home menu and all topics:

```bash
uv run python app.py
```

http://127.0.0.1:8050 — pick a topic on the home screen.

Current topics:

- **Vector projection onto a plane** (`/proekcia`) — step-by-step walkthrough of  
  `proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂`  
  (steps 0–6, sliders, 3D plot).
- **Dot product** (`/skalyarnoe`) — definition, coordinate formula, angle,  
  orthogonality, projection, properties (steps 0–6, presets and sliders for **a**, **b**).
- **Matrix rank** (`/rang`) — columns, span, independence, Gaussian elimination,  
  `rank(A) = rank(Aᵀ)`, dimension and systems `Ax = b` (steps 0–7, matrix presets).

Stop: `Ctrl+C`.

On the 3D plot: drag to rotate, scroll to zoom, Shift+drag to pan. The camera view is preserved when you change steps.

## New topic

1. Add an entry in `topics/__init__.py` (card on the home page).
2. Create `pages/topic_name/` with `__init__.py` (`dash.register_page`, layout, callbacks) and visualization modules alongside it.
3. Import the package in `app.py`.

## Your own scripts

```bash
uv run python path/to/your_script.py
```

Add a dependency:

```bash
uv add <package>
```
