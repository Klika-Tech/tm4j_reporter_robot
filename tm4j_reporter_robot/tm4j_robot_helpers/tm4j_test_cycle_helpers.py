import os

from filelock import FileLock
from tm4j_reporter_api.tm4j_api import tm4j_api

from tm4j_reporter_robot import library_variables


def get_tm4j_test_cycle_key(parallel_execution, test_cycle_key_file_name, tm4j_test_cycle_name):
    if not parallel_execution:
        tm4j_test_cycle_key = tm4j_api.create_test_cycle(
            test_cycle_name=tm4j_test_cycle_name, description=library_variables.TEST_CYCLE_DESCRIPTION
        )
    else:
        # handling parallel execution - write access to file with test cycle key from one process only
        lock_file_path = f"{test_cycle_key_file_name}.lock"
        test_cycle_key_file_lock = FileLock(lock_file_path)
        with test_cycle_key_file_lock:
            if not os.path.exists(test_cycle_key_file_name):
                tm4j_test_cycle_key = tm4j_api.create_test_cycle(
                    test_cycle_name=tm4j_test_cycle_name, description=library_variables.TEST_CYCLE_DESCRIPTION
                )
                with open(test_cycle_key_file_name, "w") as f:
                    f.write(tm4j_test_cycle_key)
            else:
                with open(test_cycle_key_file_name, "r") as f:
                    tm4j_test_cycle_key = f.read()

    return tm4j_test_cycle_key
