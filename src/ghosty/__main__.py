"""
ghosty - Example Program
Run with: python -m ghosty
"""
try:
    from . import ghosty
except ImportError:
    import ghosty


def main():
    print("=" * 50)
    print("  Welcome to Ghosty: Your Ghost Teammate Bot")
    print("=" * 50)
    print()

    print(ghosty.greet())
    print()
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

    # Nudge with different styles
    print(ghosty.nudge("Fix login bug"))
    print(ghosty.nudge("Fix login bug", scold=True))
    print(ghosty.nudge("Write documentation", scold=True, tired=True))
    print(ghosty.IAmSorry("Write documentation"))
    print(ghosty.nudge("Write documentation", scold=False, tired=True))
    print()

    # Check a specific task after nudge
    print(ghosty.check_in("Fix login bug"))
    print()

    # Nudge Fix login bug to completion (already at 50%, need 3 more regular nudges)
    for _ in range(3):
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
