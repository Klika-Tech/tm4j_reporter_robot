from datetime import datetime

from tm4j_reporter_api import tm4j_api

from tm4j_reporter_robot.tm4j_robot_helpers import tm4j_config_helpers


class TM4JRobotListener(object):
    def __init__(
        self,
        tm4j_access_key,
        tm4j_project_key,
        tm4j_test_cycle_name=f"Robot run {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ):
        self.tm4j_access_key = tm4j_access_key
        self.tm4j_project_key = tm4j_project_key
        self.tm4j_test_cycle_name = tm4j_test_cycle_name
        self.tm4j_test_cycle_key = None

    def end_test(self, name: str, attributes: dict) -> None:
        """
        Report test execution based on robot test attributes using TM4J Reporter API library.

        :param name: name of Robot Framework event
        :type name: str

        :param attributes: dictionary contains test case details
        :type attributes: dict

        :return: None
        :rtype: None
        """
        test_case_key = tm4j_config_helpers.get_tm4j_test_case_key(attributes)

        if not self.tm4j_test_cycle_key:
            tm4j_api.configure_tm4j_api(api_access_key=self.tm4j_access_key, project_key=self.tm4j_project_key)
            self.tm4j_test_cycle_key = tm4j_api.create_test_cycle(test_cycle_name=self.tm4j_test_cycle_name)

        tm4j_api.create_test_execution_result(
            test_cycle_key=self.tm4j_test_cycle_key,
            test_case_key=test_case_key,
            execution_status=attributes["status"],
            actual_end_date=datetime.utcfromtimestamp(attributes["endtime"]).strftime("%Y-%m-%d'T'%H:%M:%S'Z'"),
            execution_time=attributes["elapsedtime"],
            comment=attributes["message"],
        )

        return None
