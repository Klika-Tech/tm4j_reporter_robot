# Copyright (C) 2020 Klika Tech, Inc. or its affiliates.  All Rights Reserved.
# Use of this source code is governed by an MIT-style license that can be found in the LICENSE file
# or at https://opensource.org/licenses/MIT.

import os
from datetime import datetime

from filelock import FileLock

from tm4j_reporter_api.tm4j_api import tm4j_api
from tm4j_reporter_api.tm4j_exceptions import tm4j_response_exceptions

from tm4j_reporter_robot import library_variables
from tm4j_reporter_robot.tm4j_robot_helpers import tm4j_config_helpers


LOCK = FileLock("./TEST_CYCLE_KEY.lock")


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

        Test cycle will be created after first test execution and the rest of test executions will be reported to it.

        File with test cycle key and file lock are used to handle parallel execution - the first one process will create
        test cycle and write test cycle key to file, from where the rest of processes will read it.

        :param name: name of Robot Framework event
        :type name: str

        :param attributes: dictionary contains test case details
        :type attributes: dict

        :return: None
        :rtype: None
        """
        test_case_key = tm4j_config_helpers.get_tm4j_test_case_key(attributes)

        tm4j_api.configure_tm4j_api(api_access_key=self.tm4j_access_key, project_key=self.tm4j_project_key)

        # handling parallel execution - write access to file with test cycle key from one process only
        if not os.path.exists("./TEST_CYCLE_KEY"):
            LOCK.acquire()
            with open("./TEST_CYCLE_KEY", "w") as f:
                self.tm4j_test_cycle_key = tm4j_api.create_test_cycle(
                    test_cycle_name=self.tm4j_test_cycle_name, description=library_variables.TEST_CYCLE_DESCRIPTION
                )
                f.write(self.tm4j_test_cycle_key)
        else:
            # loop in case file is created but still empty, for example while API call from another process is still
            # in progress and test cycle key is not written to file yet
            with open("./TEST_CYCLE_KEY", "r") as f:
                while not self.tm4j_test_cycle_key:
                    self.tm4j_test_cycle_key = f.read()

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

    @staticmethod
    def close() -> None:
        """
        Releasing file lock, removing test cycle key and lock files.

        :return: None
        :rtype: None
        """
        LOCK.release()
        os.remove("./TEST_CYCLE_KEY.lock")
        os.remove("./TEST_CYCLE_KEY")

        return None
