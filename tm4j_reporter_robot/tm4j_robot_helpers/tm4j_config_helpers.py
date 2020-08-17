from tm4j_reporter_api import tm4j_configuration_exceptions


def get_tm4j_test_case_key(test_attributes: dict) -> str:
    """
    Get TM4J test case key from Robot Framework test tags.

    :param test_attributes: dictionary contains test case details
    :type test_attributes: dict

    :raise TM4JConfigurationException: if tag starting from TM4J is not found

    :return: TM4J test case key
    :rtype: str
    """
    for tag in test_attributes["tags"]:
        if tag.startswith("TM4J"):
            test_case_key = tag.split(":")[1]
            break
    else:
        raise tm4j_configuration_exceptions.TM4JConfigurationException(
            "Test case key is not found in list of tags. Please mark robot test with tag 'TM4J:<test_case_key>'."
        )

    return test_case_key