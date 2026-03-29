"""
ghosty.py - The Ghost Teammate Bot
A bot that simulates a teammate who does absolutely nothing.
"""

_task_board = {}

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


def check_in(task_name=None):
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
    
    
    lines = ["Ghosty's Task Board\n"]
    lines.append(f"{'Task':<20} {'Category':<15} {'Progress':<10} {'Remaining':<10}")
    lines.append("-" * 55)
    
    for name, task in _task_board.items():
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

