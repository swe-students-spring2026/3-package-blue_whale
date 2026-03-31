"""
ghosty.py - The Ghost Teammate Bot
A bot that simulates a teammate who does absolutely nothing.
"""

import random

_task_board = {}


def greet(presence=None, intent=None, teammate=None, blocker=None):
    """Return a Ghosty greeting from the greeter's perspective."""
    valid_presence = ["reappearing", "active"]
    valid_intents = [
        "catch_up",
        "ask_about_teammate",
        "promise_progress",
        "encourage",
        "question_minor_detail",
    ]

    if presence is None and intent is None and teammate is None and blocker is None:
        return random.choice([
            "Hey! Just catching up on the thread now. What did I miss?",
            "Morning! How is your part coming along? Looking great so far!",
            "Just grabbing coffee and then diving deep into my task. Update soon.",
            "Love the direction this is going. Keep it up, team!",
        ])

    if presence is None:
        presence = "active"
    if intent is None:
        intent = "encourage"

    if presence not in valid_presence:
        raise ValueError(f"Presence must be one of {valid_presence}")
    if intent not in valid_intents:
        raise ValueError(f"Intent must be one of {valid_intents}")

    if teammate is not None and (not isinstance(teammate, str) or len(teammate.strip()) == 0):
        raise ValueError("Teammate must be a non-empty string when provided.")
    if blocker is not None and (not isinstance(blocker, str) or len(blocker.strip()) == 0):
        raise ValueError("Blocker must be a non-empty string when provided.")

    opener = (
        "Ghosty says: Sorry for the radio silence."
        if presence == "reappearing"
        else "Ghosty says: Morning team!"
    )

    teammate_name = teammate.strip() if isinstance(teammate, str) else "your part"

    if intent == "catch_up":
        follow_up = "Just catching up on the thread now, what did I miss?"
    elif intent == "ask_about_teammate":
        follow_up = f"How is {teammate_name} coming along? Looking great so far!"
    elif intent == "promise_progress":
        if blocker is not None:
            follow_up = f"Currently fighting with {blocker}, will post when I clear it."
        else:
            follow_up = "Just grabbing coffee and then diving deep into my task. Update soon."
    elif intent == "question_minor_detail":
        follow_up = "Do we think we should tweak that minor detail before we ship?"
    else:
        follow_up = "Love the direction this is going. Keep it up, team!"

    return f"{opener} {follow_up}"

def assign(task_name, hours, category="medium"):

    if not isinstance(task_name, str) or len(task_name.strip()) == 0:
        raise ValueError("Task name must be a non-empty string.")
    if not isinstance(hours, (int, float)) or hours <= 0:
        raise ValueError("Hours must be a positive number.")
    
    valid_categories = ["low", "medium", "high", "critical"]

    if category not in valid_categories:
        raise ValueError(f"Category must be one of {valid_categories}")
    
    _task_board[task_name] = {
        "hours": hours,
        "category": category,
        "progress": 0,      
        "nudged": False
    }
    
    return (
        f"Task '{task_name}' (Priority: {category}, {hours}hrs) assigned to Ghosty.\n"
        f"Ghosty has been notified... just kidding, Ghosty doesn't check Slack."
    )


def nudge(task_name):
    """Nudge Ghosty on a task; progress increases a little each time."""
    if not isinstance(task_name, str) or len(task_name.strip()) == 0:
        raise ValueError("Task name must be a non-empty string.")

    if task_name not in _task_board:
        raise KeyError(f"Task '{task_name}' not found on the board.")

    task = _task_board[task_name]
    task["nudged"] = True

    previous_progress = task["progress"]
    task["progress"] = min(100, previous_progress + 20)

    if task["progress"] == 100:
        return (
            f"Ghosty was nudged about '{task_name}'.\n"
            "Miraculously, the task is now complete (100%)."
        )

    return (
        f"Ghosty was nudged about '{task_name}'.\n"
        f"Progress moved from {previous_progress}% to {task['progress']}%."
    )


def remove_task(task_name):
    """Remove a single task from the board."""
    if not isinstance(task_name, str) or len(task_name.strip()) == 0:
        raise ValueError("Task name must be a non-empty string.")

    if task_name not in _task_board:
        raise KeyError(f"Task '{task_name}' not found on the board.")

    del _task_board[task_name]
    return f"Task '{task_name}' was removed from Ghosty's board."


def clear_completed():
    """Remove all tasks that have reached 100% progress."""
    completed_tasks = [name for name, task in _task_board.items() if task["progress"] >= 100]

    for name in completed_tasks:
        del _task_board[name]

    return f"Cleared {len(completed_tasks)} completed task(s)."


def check_in(task_name=None, include_completed=False):
    if task_name is not None:
        if task_name not in _task_board:
            raise KeyError(f"Task '{task_name}' not found on the board.")
        
        task = _task_board[task_name]
        remaining = task["hours"] * (1 - task["progress"] / 100)
        return (
            f"Task: {task_name}\n"
            f"   Category : {task['category']}\n"
            f"   Progress : {task['progress']}%\n"
            f"   Remaining: {remaining:.1f} hrs\n"
            f"   Status   : {'Nudged' if task['nudged'] else 'Ghosty hasnt started yet'}"
        )
    
    if len(_task_board) == 0:
        return "No tasks assigned yet. Ghosty is 'working on it'."
    
    board_items = [
        (name, task)
        for name, task in _task_board.items()
        if include_completed or task["progress"] < 100
    ]

    if len(board_items) == 0:
        return "No active tasks on the board. Use include_completed=True to view finished tasks."

    
    lines = ["Ghosty's Task Board\n"]
    lines.append(f"{'Task':<20} {'Category':<15} {'Progress':<10} {'Remaining':<10}")
    lines.append("-" * 55)
    
    for name, task in board_items:
        remaining = task["hours"] * (1 - task["progress"] / 100)
        lines.append(
            f"{name:<20} {task['category']:<15} {task['progress']:<10}% {remaining:<10.1f}hrs"
        )
    
    return "\n".join(lines)

def excuse(reason, seriousness="medium"):
    """Return a playful excuse message."""
    if not isinstance(reason,str) or len(reason.strip())==0:
        raise ValueError("Reason must be a non-empty string.")
    
    valid_levels = ["low","medium", "high"]

    if seriousness not in valid_levels:
        raise ValueError(f"Seriousness must be one of {valid_levels}")
    
    reason = reason.strip()

    if seriousness == "high":
        return(
            f"Ghosty's excuse:\n"
            f"{reason}\n"
            "This was clearly a critical situation.\n"
            "Expecting productivity would be unrealistic."
        )
    elif seriousness == "medium":
        return(
            f"Ghosty's excuse:\n"
            f"{reason}\n"
            "Ghosty planned to start working... emotionally"
        )
    else:
        return(
            f"Ghosty's excuse:\n"
            f"{reason}\n"
            "Ghosty apologizes and promises absolutely nothing."
        )

