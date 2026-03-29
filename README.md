# Python Package Exercise

> ## Ghosty: Your Ghost Teammate Bot

![Build Status](https://github.com/swe-students-spring2026/3-package-blue_whale/actions/workflows/event-logger.yml/badge.svg)

**PyPI:** _coming soon_

Ghosty is a Python package that simulates a ghost teammate — the kind who gets assigned tasks, never does anything, and always has an excuse. Install it, assign Ghosty some work, and watch absolutely nothing happen.

---

## Installation

```bash
pip install ghosty
```

---

## Usage

### `greet()`

Ghosty greets you (or doesn't, depending on the mood).

```python
from ghosty import ghosty

ghosty.greet()
```

### `assign(task_name, hours, category="medium")`

Assign Ghosty a task. It will be logged to the task board and promptly ignored.

- `task_name` (str): Name of the task
- `hours` (int/float): Estimated hours
- `category` (str): Priority level — `"low"`, `"medium"`, `"high"`, or `"critical"`. Default: `"medium"`

```python
ghosty.assign("Fix login bug", 3, category="high")
ghosty.assign("Write documentation", 2, category="low")
```

### `check_in(task_name=None)`

View the task board. Pass a task name to see details on a specific task, or leave it empty to see everything.

```python
ghosty.check_in()                  # view all tasks
ghosty.check_in("Fix login bug")   # view one task
```

### `nudge()`

Nudge Ghosty to actually do something. Without a nudge, nothing will ever happen.

```python
ghosty.nudge("Fix login bug")
```

### `excuse(reason, seriousness="medium")`

Ask Ghosty to justify why no progress has been made.

- `reason` (str): The excuse text
- `seriousness` (str): How serious the excuse is — `"low"`, `"medium"`, or `"high"`. Default: `"medium"`

```python
ghosty.excuse("my cat sat on my keyboard", seriousness="medium")
ghosty.excuse("the wifi stopped believing in me", seriousness="high")
```

---

## Example Program

See [`src/ghosty/__main__.py`](./src/ghosty/__main__.py) for a complete example using all functions.

Run it with:

```bash
python -m ghosty
```

---

## Contributing

### Setup

```bash
git clone https://github.com/swe-students-spring2026/3-package-blue_whale.git
cd 3-package-blue_whale
pipenv install --dev
pipenv shell
```

### Running Tests

```bash
pipenv run pytest
```

### Building the Package

```bash
pipenv run python -m build
```

---

## Team

- [Celia Liang](https://github.com/liangchuxin)
- [Mumu Li](https://github.com/n3xta)
- [Xiongfeng Li](https://github.com/DaobaRoger12)
- [Meili Liang](https://github.com/ml8397)
- [Hanxi Li](https://github.com/hanxili435)
