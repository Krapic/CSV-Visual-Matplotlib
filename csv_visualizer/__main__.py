"""Entry point za pokretanje aplikacije."""

from .gui import Application


def main():
    """Pokreće aplikaciju."""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
