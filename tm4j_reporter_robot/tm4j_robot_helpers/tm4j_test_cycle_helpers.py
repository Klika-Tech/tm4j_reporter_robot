import os

from filelock import FileLock
from tm4j_reporter_api.tm4j_api import tm4j_api

from tm4j_reporter_robot import library_variables


def get_tm4j_test_cycle_key(parallel_execution: bool, test_cycle_key_file_path: str, tm4j_test_cycle_name: str) -> str:
    """
    Helper method to handle TM4J test cycle creation.

    :param parallel_execution: flag to mark parallel execution
    :type parallel_execution: bool

    :param test_cycle_key_file_path: path to TM4J test cycle key shared file (used to handle parallel test execution)
    :type test_cycle_key_file_path: str

    :param tm4j_test_cycle_name: name for TM4J test cycle
    :type tm4j_test_cycle_name: str

    :return: TM4J test cycle key
    :rtype: str
    """
    def _create_test_cycle():
        return tm4j_api.create_test_cycle(
            test_cycle_name=tm4j_test_cycle_name, description=library_variables.TEST_CYCLE_DESCRIPTION
        )

    if not parallel_execution:
        tm4j_test_cycle_key = _create_test_cycle()

    # handling parallel execution - write access to file with test cycle key from one process only
    else:
        lock_file_path = f"{test_cycle_key_file_path}.lock"
        test_cycle_key_file_lock = FileLock(lock_file_path)

        # locking access to shared file with TM4J test cycle key
        with test_cycle_key_file_lock.acquire():
            # if file doesn't exist - creating TM4J test cycle trough TM4J API and writing its key to shared file
            if not os.path.exists(test_cycle_key_file_path):
                tm4j_test_cycle_key = _create_test_cycle()
                with open(test_cycle_key_file_path, "w") as f:
                    f.write(tm4j_test_cycle_key)
            # if file exists - reading TM4J test cycle key from it
            else:
                with open(test_cycle_key_file_path, "r") as f:
                    tm4j_test_cycle_key = f.read()

    return tm4j_test_cycle_key
