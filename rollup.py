"""Roll Up entry point script"""

import logging
import sys

from rollup.roll_up import RollUp

def main() -> None:
    """Roll Up entry point method"""

    logging.basicConfig(
        filename='roll_up.error.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
    )

    roll_up.run()

if __name__ == "__main__":
    main()
