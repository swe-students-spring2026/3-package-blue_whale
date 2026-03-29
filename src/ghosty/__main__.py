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

    # TODO: greet() - waiting for Mumu

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

    # TODO: nudge()

    # Check a specific task after nudge
    print(ghosty.check_in("Fix login bug"))
    print()

    # Ask for an excuse
    print(ghosty.excuse("my cat sat on my keyboard", seriousness="medium"))
    print()
    print(ghosty.excuse("the wifi stopped believing in me", seriousness="high"))
    print()


if __name__ == "__main__":
    main()
