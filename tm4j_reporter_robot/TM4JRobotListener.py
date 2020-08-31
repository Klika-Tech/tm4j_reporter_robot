# Copyright (C) 2020 Klika Tech, Inc. or its affiliates.  All Rights Reserved.
# Use of this source code is governed by an MIT-style license that can be found in the LICENSE file
# or at https://opensource.org/licenses/MIT.

from datetime import datetime

from tm4j_reporter_api.tm4j_api import tm4j_api
from tm4j_reporter_api.tm4j_exceptions import tm4j_response_exceptions

from tm4j_reporter_robot.tm4j_robot_helpers import tm4j_config_helpers


class TM4JRobotListener(object):
    ROBOT_LISTENER_API_VERSION = 2

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

        try:
            tm4j_api.create_test_execution_result(
                test_cycle_key=self.tm4j_test_cycle_key,
                test_case_key=test_case_key,
                execution_status=attributes["status"],
                actual_end_date=datetime.strptime(attributes["endtime"], "%Y%m%d %H:%M:%S.%f").strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                execution_time=attributes["elapsedtime"],
                comment=attributes["message"],
            )
        except tm4j_response_exceptions.TM4JResponseException as e:
            print(f"Sorry, test execution reporting for {test_case_key} didn't go well because of: {e.message}")

        return None
