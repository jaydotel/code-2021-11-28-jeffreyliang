"""Roll Up entry point script"""

import logging
import sys

from rollup.roll_up import RollUp

def main() -> None:
    """Roll Up entry point method"""

    roll_up = RollUp()
    roll_up.run()

if __name__ == "__main__":
    main()
