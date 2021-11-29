"""RollUp Module"""

from collections import defaultdict
import logging

from rollup.helpers.bom_api import QuickReleaseBoMAPI

_LOGGER = logging.getLogger(__name__)


class RollUp:
        self.parts_grouped_by_parent = {}
        self.number_of_parts_required = defaultdict(int)

        self.quick_release_bom_api = QuickReleaseBoMAPI()

    def run(self) -> None:
        parts_data = (self.quick_release_bom_api.get_bill_of_material().json()
                      .get('data', []))

        if parts_data:
            self.parts_grouped_by_parent = self.group_by_parent(parts_data)

            # Pass in hard coded info initially to get the recursion started
            self.calc_parts_required('parents', 1)

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

