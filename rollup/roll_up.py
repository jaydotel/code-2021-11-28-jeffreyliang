"""RollUp Module"""

from collections import defaultdict
import logging

from xlsxwriter import Workbook

from rollup.helpers.bom_api import QuickReleaseBoMAPI

_LOGGER = logging.getLogger(__name__)


class RollUp:
    """Contains the functionality to perform a quantity rollup calculation given
    part numbers and how they are grouped into assemblies.

    Each part is treated similar to a node in a tree data structure where each
    part/node may have a parent part and children parts.
    """

    def __init__(self, xlsx_file_name: str) -> None:
        self.xlsx_file_name = xlsx_file_name

        self.parts_grouped_by_parent = {}
        self.number_of_parts_required = defaultdict(int)

        self.quick_release_bom_api = QuickReleaseBoMAPI()

    def run(self) -> None:
        """Runs the bulk of RollUp's functionality

        1. Calls BoM API to get the parts data
        2. Groups the data by parent
        3. Calculates total parts required while calling BoM API to get the
        `part_number` for each part
        4. Outputs to xlsx
        """
        parts_data = (self.quick_release_bom_api.get_bill_of_material().json()
                      .get('data', []))

        if parts_data:
            self.parts_grouped_by_parent = self.group_by_parent(parts_data)

            # Pass in hard coded info initially to get the recursion started
            self.calc_parts_required('parents', 1)

            self.output_to_xlsx()
        else:
            _LOGGER(f'No data returned from BoM. {parts_data=}')

    @staticmethod
    def group_by_parent(parts: dict) -> dict:
        """Groups parts by parent for easier processing

        Args:
            parts (dict): Parts data retrieved from BoM API

        Returns:
            (dict): Parts grouped by parent
                (list): All children parts
                    (dict): children part_id and quantity needed
        """

        parts_grouped_by_parent = defaultdict(list)

        for part in parts:
            # BoM endpoint returns parent of root node as "null". Change this
            # to parent so it's accessible
            if part.get('parent_part_id'):
                parent_part_id = part.get('parent_part_id')
            else:
                parent_part_id = 'parents'

            parts_grouped_by_parent[parent_part_id].append({
                'part_id': part.get('part_id'),
                'quantity': part.get('quantity')
            })

        return parts_grouped_by_parent

    def calc_parts_required(self, parent_part_id: int, parent_total_parts_required: int) -> dict:
        """Calculates total number of parts required for all parts

        Args:
            parent_part_id (int): Part ID of parent, required to find children
            of a part
            parent_total_parts_required (int): Total parts required for parent,
            needed for calculating total parts required for children parts

        Returns:
            dict: Total parts required for each part, categorised by part_id
        """

        for part in self.parts_grouped_by_parent.get(parent_part_id, []):
            part_id = part.get('part_id')
            part_quantity = part.get('quantity')

            total_parts_required = parent_total_parts_required * part_quantity

            part_number = (self.quick_release_bom_api.get_part_number(part_id)
                           .json().get('part_number', part_id))

            # Sum total parts required (for this part) in case it's
            # required somewhere else
            self.number_of_parts_required[part_number] =+ total_parts_required

            # Calculate total parts required this part's children (if any)
            self.calc_parts_required(part_id, total_parts_required)

    def output_to_xlsx(self) -> None:
        """Outputs total parts required categorised by `part_number` to a .xlsx
        file in the project's root dir

        File name can be defined as a second argument in command line. Default
        name will be 'output.xlsx'
        """

        workbook = Workbook(self.xlsx_file_name)
        worksheet = workbook.add_worksheet()

        # Add Part Number column
        worksheet.write_column(0, 0, tuple(self.number_of_parts_required.keys()))

        # Add Total Parts Required Column
        worksheet.write_column(0, 1, tuple(self.number_of_parts_required.values()))

        workbook.close()
