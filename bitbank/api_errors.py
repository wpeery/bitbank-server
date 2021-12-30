"""
Module for application specific api errors

These errors will be returned with http status code 200
"""
import dataclasses
from rest_framework import status
from rest_framework import response
import types

ENTITY_DOES_NOT_EXIST = 1000
UNABLE_TO_TRANSFER_FUNDS = 1010
NOT_ENOUGH_FUNDS = 1011


class UnknownApiErrorCode(Exception):
    """Error raised if the api error code is unknown"""


@dataclasses.dataclass
class ApiErrorData:
    """Class for holding onto data for a given api error"""

    error_code: int
    error_message: str


API_ERRORS = (
    ApiErrorData(
        error_code=ENTITY_DOES_NOT_EXIST, error_message="Entity does not exist"
    ),
    ApiErrorData(
        error_code=UNABLE_TO_TRANSFER_FUNDS, error_message="Unable to transfer funds"
    ),
    ApiErrorData(
        error_code=NOT_ENOUGH_FUNDS, error_message="Not enough funds in account"
    ),
)

# Read only mapping of error code to ApiErrorData
API_ERROR_MAPPING = types.MappingProxyType({e.error_code: e for e in API_ERRORS})


def api_error_response(error_code: int, details: str = None) -> response.Response:
    """
    Factory method for creating api error responses

    :param error_code: the error code to return
    :param details: any extra details that should be user visible

    :return: the api response
    :raises UnknownApiErrorCode: if the error_code is not defined
    """
    if error_code not in API_ERROR_MAPPING:
        raise UnknownApiErrorCode(f"Unknown api error_code: {error_code}")

    api_error = API_ERROR_MAPPING[error_code]
    data = {
        "error_code": api_error.error_code,
        "error": api_error.error_message,
    }
    if details:
        data["details"] = details
    return response.Response(status=status.HTTP_200_OK, data=data)
