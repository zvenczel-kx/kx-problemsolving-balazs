import os

from storage_server.models.status_response import StatusResponse  # noqa: E501

instance_id: str = os.getenv('MY_INSTANCE_ID', 'no_id')


def data_get():  # noqa: E501
    """storageapi_api_data_get

    # noqa: E501


    :rtype: object
    """
    return {
        "instance_id": instance_id,
        "asdf": "fdsa",
        "bbb": "ddd",
        "alma": 121212
    }


def status_get():  # noqa: E501
    """storageapi_api_status_get

    # noqa: E501


    :rtype: StatusResponse
    """
    return StatusResponse("UP")
