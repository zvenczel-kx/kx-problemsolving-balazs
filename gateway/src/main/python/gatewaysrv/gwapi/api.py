import gwapi.storagemng


def data_get():  # noqa: E501
    """storageapi_api_data_get

    # noqa: E501


    :rtype: object
    """
    return gwapi.storagemng.get_data()


def status_get():  # noqa: E501
    """storageapi_api_status_get

    # noqa: E501


    :rtype: StatusResponse
    """
    return gwapi.storagemng.get_status()
