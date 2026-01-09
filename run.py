#!/usr/bin/env python3
"""Pokreće CSV Visualizer aplikaciju."""

from csv_visualizer import __version__
from csv_visualizer.gui import Application


def main():
    """Entry point."""
    print(f"CSV Visualizer v{__version__}")
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
