"""
ghosty - Example Program
Run with: python -m ghosty
"""
from ghosty import ghosty


def main():
    print("=" * 50)
    print("  Welcome to Ghosty: Your Ghost Teammate Bot")
    print("=" * 50)
    print()

    # greet with no arguments (random message)
    print(ghosty.greet())
    print()

    # greet with arguments
    print(ghosty.greet(presence="active", intent="ask_about_teammate", teammate="Celia's section"))
    print()

    # Assign some tasks
    print(ghosty.assign("Fix login bug", 3, category="high"))
    print()
    print(ghosty.assign("Write documentation", 2, category="low"))
    print()
    print(ghosty.assign("Deploy to production", 8, category="critical"))
    print()

    # Check the full board
    print(ghosty.check_in())
    print()

    # Nudge a task
    print(ghosty.nudge("Fix login bug"))
    print()

    # Check a specific task after nudge
    print(ghosty.check_in("Fix login bug"))
    print()

    # Nudge until complete
    for _ in range(4):
        ghosty.nudge("Fix login bug")
    print(ghosty.nudge("Fix login bug"))
    print()

    # Clear completed tasks
    print(ghosty.clear_completed())
    print()

    # Check board after clearing
    print(ghosty.check_in())
    print()

    # Remove a task
    print(ghosty.remove_task("Write documentation"))
    print()

    # Ask for an excuse
    print(ghosty.excuse("my cat sat on my keyboard", seriousness="medium"))
    print()
    print(ghosty.excuse("the wifi stopped believing in me", seriousness="high"))
    print()


if __name__ == "__main__":
    main()
