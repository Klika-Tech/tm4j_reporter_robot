from typing import Tuple

from robot.libraries.BuiltIn import BuiltIn
from tm4j_reporter_api import tm4j_configuration_exceptions


def get_tm4j_configuration_keys() -> Tuple[str, str]:
    """
    Get TM4J configuration keys from Robot Framework variables.

    :raise TM4JConfigurationException: if any of TM4J access or project key is not defined

    :return: tuple of two strings - TM4J access key, TM4J project key
    :rtype: tuple
    """
    tm4j_access_key = BuiltIn().get_variable_value("${TM4J_ACCESS_KEY}")
    tm4j_project_key = BuiltIn().get_variable_value("${TM4J_PROJECT_KEY}")

    if not tm4j_access_key:
        raise tm4j_configuration_exceptions.TM4JConfigurationException(
            "TM4J access key is not specified. Please pass TM4J access key as robot variable."
        )

    if not tm4j_project_key:
        raise tm4j_configuration_exceptions.TM4JConfigurationException(
            "TM4J project key is not specified. Please pass TM4J project key as robot variable."
        )

    return tm4j_access_key, tm4j_project_key


def get_tm4j_test_case_key(test_attributes: dict) -> str:
    """
    Get TM4J test case key from Robot Framework test tags.

    :param test_attributes: dictionary contains test case details
    :type test_attributes: dict

    :raise TM4JConfigurationException: if tag starting from TM4J is not found

    :return: TM4J test case key
    :rtype: str
    """
    test_case_key = None
    for tag in test_attributes["tags"]:
        if tag.startswith("TM4J"):
            test_case_key = tag.split(":")[1]
            break

    if not test_case_key:
        raise tm4j_configuration_exceptions.TM4JConfigurationException(
            "Test case key is not found in list of tags. Please mark robot test with tag 'TM4J: <test_case_key>'."
        )

    return test_case_key
