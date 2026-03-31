# Python Package Exercise

> ## Ghosty: Your Ghost Teammate Bot

![Build Status](https://github.com/swe-students-spring2026/3-package-blue_whale/actions/workflows/build.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/ghosty-teammate.svg)](https://pypi.org/project/ghosty-teammate/)

**PyPI Project Page:** https://pypi.org/project/ghosty-teammate/

Ghosty is a Python package that simulates a ghost teammate — the kind who gets assigned tasks, never does anything, and always has an excuse. Install it, assign Ghosty some work, and watch absolutely nothing happen.

---

## Installation

```bash
pip install ghosty-teammate
```

---

## Usage

### `greet(presence=None, intent=None, teammate=None, blocker=None)`

Ghosty greets the team. All parameters are optional — calling with no arguments returns a random message.

- `presence` (str): `"active"` or `"reappearing"` — affects the opening tone
- `intent` (str): one of `"catch_up"`, `"ask_about_teammate"`, `"promise_progress"`, `"encourage"`, `"question_minor_detail"`
- `teammate` (str): name to mention when intent is `"ask_about_teammate"`
- `blocker` (str): blocker to mention when intent is `"promise_progress"`

```python
from ghosty import ghosty

ghosty.greet()
ghosty.greet(presence="active", intent="ask_about_teammate", teammate="Alice")
ghosty.greet(presence="reappearing", intent="promise_progress", blocker="a merge conflict")
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

### `check_in(task_name=None, include_completed=False)`

View the task board. Pass a task name to see details on a specific task, or leave it empty to see everything.

- `task_name` (str): Optional — name of a specific task to view
- `include_completed` (bool): Whether to show completed tasks. Default: `False`

```python
ghosty.check_in()                              # view all active tasks
ghosty.check_in("Fix login bug")               # view one task
ghosty.check_in(include_completed=True)        # include completed tasks
```

### `nudge(task_name, scold=False, tired=False)`

Nudge Ghosty on a specific task. Each regular nudge increases progress by 20%; with scolding, the progress is increased by 30%; with tiredness, it increases 10% only. If it possible that Ghosty would get slack once the progress is over 60%. It would also become angry if you nudge and scold it more than 3 times, or nudge and scold it when it is tired. Without a nudge, nothing will ever happen.

- `task_name` (str): Name of the task to nudge
- `scold` (bool): Whether or not if you want to push and scold Ghosty for work
- `tired` (bool): Whether or not if Ghosty is tired

```python
ghosty.nudge("Fix login bug")
```

### `IAmSorry(task_name)

A function that lets you say sorry to Ghosty. If ghosty is angry, it wuld get back to work after you say sorry. If it is not angry, it would consider you a weirdo.

- `task_name` (str): Name of the task

```python
ghosty.IAmSorry("Fix login bug")
```

### `excuse(reason, seriousness="medium")`

Ask Ghosty to justify why no progress has been made.

- `reason` (str): The excuse text
- `seriousness` (str): How serious the excuse is — `"low"`, `"medium"`, or `"high"`. Default: `"medium"`

```python
ghosty.excuse("my cat sat on my keyboard", seriousness="medium")
ghosty.excuse("the wifi stopped believing in me", seriousness="high")
```

### `remove_task(task_name)`

Remove a specific task from the board.

- `task_name` (str): Name of the task to remove

```python
ghosty.remove_task("Fix login bug")
```

### `clear_completed()`

Remove all tasks that have reached 100% progress.

```python
ghosty.clear_completed()
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

## Configuration

This project does not use any secret configuration files such as `.env` or similar files. No additional configuration is required to run or contribute to this project.

---

## Team

- [Celia Liang](https://github.com/liangchuxin)
- [Mumu Li](https://github.com/n3xta)
- [Xiongfeng Li](https://github.com/DaobaRoger12)
- [Meili Liang](https://github.com/ml8397)
- [Hanxi Li](https://github.com/hanxili435)
