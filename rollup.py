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

    xlsx_file_name = sys.argv[1] if len(sys.argv) > 1 else 'output.xlsx'

    roll_up = RollUp(xlsx_file_name)
    roll_up.run()

if __name__ == "__main__":
    main()
