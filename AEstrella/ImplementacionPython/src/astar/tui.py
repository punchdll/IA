from __future__ import annotations


def run_tui():
    from .textual_app import launch_textual

    App = launch_textual()
    App().run()


def main():
    run_tui()


if __name__ == "__main__":
    main()
