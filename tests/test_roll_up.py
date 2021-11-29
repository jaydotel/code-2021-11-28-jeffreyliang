"""Unit tests for Roll Up"""

from unittest import TestCase
from unittest.mock import patch

from rollup.roll_up import RollUp


class RollUpTestCase(TestCase):
    """Unit tests for Roll Up"""

    @classmethod
    def setUpClass(cls):
        cls.roll_up = RollUp('test_output.xlsx')

    @patch('rollup.roll_up.RollUp.output_to_xlsx')
    @patch('rollup.helpers.bom_api.QuickReleaseBoMAPI.get_part_number')
    @patch('rollup.helpers.bom_api.QuickReleaseBoMAPI.get_bill_of_material')
    def test_total_number_parts_required_calculated_successfully(
        self,
        mock_get_bill_of_material,
        mock_get_part_number,
        mock_output_to_xlsx):
        """Test to check if total number of parts required has been calculated
        successfully"""

        mock_output_to_xlsx.return_value = None

        mock_get_bill_of_material.return_value.json.return_value = {
            'data': [
                {
                    'id': 0,
                    'parent_part_id': None,
                    'part_id': 1766,
                    'quantity': 2
                },
                {
                    'id': 1,
                    'parent_part_id': 1766,
                    'part_id': 307,
                    'quantity': 3
                },
                {
                    'id': 2,
                    'parent_part_id': 1766,
                    'part_id': 4866,
                    'quantity': 1
                },
                {
                    'id': 3,
                    'parent_part_id': 4866,
                    'part_id': 4522,
                    'quantity': 5
                },
                {
                    'id': 4,
                    'parent_part_id': 4522,
                    'part_id': 3970,
                    'quantity': 5
                }
            ]
        }

        mock_get_part_number.return_value.json.side_effect = [
            {
                'id': 1766,
                'part_number': '24-68536-Z'
            },
            {
                'id': 307,
                'part_number': '24-62992-H'
            },
            {
                'id': 4866,
                'part_number': '24-66602-S'
            },
            {
                'id': 4522,
                'part_number': '24-94110-C'
            },
            {
                'id': 3970,
                'part_number': '24-21487-V'
            }
        ]

        expected_number_of_parts_required = {
            "24-68536-Z": 2,
            "24-62992-H": 6,
            "24-66602-S": 2,
            "24-94110-C": 10,
            "24-21487-V": 50
        }

        self.roll_up.run()

        self.assertDictEqual(
            expected_number_of_parts_required,
            dict(self.roll_up.number_of_parts_required)
        )
