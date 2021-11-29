"""RollUp Module"""

from rollup.helpers.bom_api import QuickReleaseBoMAPI

class RollUp:
    def __init__(self) -> None:
        self.quick_release_bom_api = QuickReleaseBoMAPI()

    def run(self) -> None:
        parts_data = (self.quick_release_bom_api.get_bill_of_material().json()
                      .get('data', []))
