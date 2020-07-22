from datetime import datetime

from tm4j_reporter_api import tm4j_api

from tm4j_reporter_robot.tm4j_robot_helpers import tm4j_config_helpers


TM4J_TEST_CYCLE_KEY = None


def end_test(name: str, attributes: dict) -> None:
    """
    Report test execution based on robot test attributes using TM4J Reporter API library.

    :param name: name of Robot Framework event
    :type name: str

    :param attributes: dictionary contains test case details
    :type attributes: dict

    :return: None
    :rtype: None
    """
    global TM4J_TEST_CYCLE_KEY

    tm4j_access_key, tm4j_project_key = tm4j_config_helpers.get_tm4j_configuration_keys()
    test_case_key = tm4j_config_helpers.get_tm4j_test_case_key(attributes)

    if not TM4J_TEST_CYCLE_KEY:
        tm4j_api.configure_tm4j_api(api_access_key=tm4j_access_key, project_key=tm4j_project_key)
        TM4J_TEST_CYCLE_KEY = tm4j_api.create_test_cycle(test_cycle_name="My TM4J test cycle")

    tm4j_api.create_test_execution_result(
        test_cycle_key=TM4J_TEST_CYCLE_KEY,
        test_case_key=test_case_key,
        execution_status=attributes["status"],
        actual_end_date=datetime.utcfromtimestamp(attributes["endtime"]).strftime("%Y-%m-%d'T'%H:%M:%S'Z'"),
        execution_time=attributes["elapsedtime"],
        comment=attributes["message"],
    )

    return None
