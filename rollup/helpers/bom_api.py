"""Quick Release Bill of Materials API Module"""

import logging

import requests
from requests import get, Response

_LOGGER = logging.getLogger(__name__)


class QuickReleaseBoMAPI:
    """Handles requests to BoM (Bill of Materials) API"""

    _REQUEST_TIMEOUT = 10
    _BOM_API_HOST = 'https://interviewbom.herokuapp.com'

    def get_bill_of_material(self) -> Response:
        """GETs bill of materials data

        Returns:
            (Response): JSON response with `id`, `parent_part_id`, `part_id` and
            `quantity`
        """
        return self._get_request(f'{self._BOM_API_HOST}/bom/')

    def get_part_number(self, part_id: int) -> Response:
        """GETs the part number for a part with a particular part id

        Args:
            part_id (int): The part unique identifier

        Returns:
            (Response): JSON response with `id` (part_id) and `part_number`
        """

        return self._get_request(f'{self._BOM_API_HOST}/part/{part_id}')

    def _get_request(self, path: str) -> Response:

        try:
            response = get(path, timeout=self._REQUEST_TIMEOUT)

            # Raise an error if the response status code is not 2XX or 404
            if not response.status_code == requests.codes.ok:
                if response.status_code == requests.codes.not_found:
                    _LOGGER.critical(
                        f'Critical error sending GET request to BoM API.'
                        f'{path=} {response.status_code=} {response.text=}'
                    )
                response.raise_for_status()

            return response
        except Exception as exception:
            _LOGGER.critical(
                f'Critical error sending GET request to BoM API. {path=} {exception=}',
            )
            raise exception
