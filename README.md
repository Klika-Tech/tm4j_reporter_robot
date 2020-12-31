# Project summary
Package providing Robot Framework listener for TM4J Cloud integration.

# Install
## How to build
    python setup.py sdist
    
## How to install
    # PyPi
    pip install tm4j-reporter-robot
    # Git
    pip install git+ssh://git@github.com:Klika-Tech/tm4j_reporter_robot.git
    
# Usage
In order to use Robot Framework TM4J listener, it should be installed to the same PYTHONPATH as Robot Framework itself.
While running Robot Framework, pass `TM4JRobotListener` as value for `--listener` argument, along with access and project keys:
```bash
robot --listener tm4j_reporter_robot.TM4JRobotListener:<tm4j_access_key>:<tm4j_project_key>:<parallel_execution_flag>:<path_to_shared_test_cycle_key_file>:<tm4j_test_cycle_name> test.robot
```
| Param                                 | Mandatory | Description                                                                                                                                            | Type     | Example                           |
|---------------------------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-----------------------------------|
| tm4j_access_key                       | Yes       | API key to access TM4j. To get it see [Instruction](https://support.smartbear.com/tm4j-cloud/docs/api-and-test-automation/generating-access-keys.html) | str      |                                   |
| tm4j_project_key                      | Yes       | Jira / TM4J project prefix without trailing dash                                                                                                       | str      | QT                                |
| parallel_execution_flag               | No        | Flag to mark parallel execution. False by default                                                                                                      | boolean  | true                              |
| path_to_shared_test_cycle_key_file    | No        | Path to TM4J test cycle key shared file (used to handle parallel test execution). Deault value is `{os_tempdir}/TEST_CYCLE_KEY`                        | str      | /my_folder/my_test_cycle_key_file |
| tm4j_test_cycle_name                  | No        | TM4J test cycle name. If not passed, listener will create a new one test cycle with default name "Robot run YYYY-mm-DD HH-MM-SS"                       | str      | My test cycle                     |

**Example:** running without parallel exectution with custom test cycle name
```bash
robot --listener tm4j_reporter_robot.TM4JRobotListener:my_access_key:QT:::"My custom test cycle name" test.robot
```

**Example:** parallel execution with `pabot` and cleanup before run
```bash
rm -rf /my_user/temp/my_tc_key*
pabot --processes 4 --listener tm4j_reporter_robot.TM4JRobotListener:my_access_key:QT:true:/my_user/temp/my_tc_key:"My custom test cycle name" tests/
```

In order to listener reported test execution to TM4J, mark Robot test case with tag `TM4J:<tm4j_test_case_key>`:
```robot
My Robot Test Case
    [Tags]  Some tag 1  Some tag 2  TM4J:QT-001
    test code goes here
```

## Parallel execution
For parallel execution with e.g. `pabot`, you need to set parallel execution flag to `true`.<br>
Listener uses synchronization through shared file for test cycle key and lock file - so only one process \ thread will create TM4J test cycle for execution, write its key into a shared file, and all other processes \ threads read test cycle key from it.<br>
Unfortunately, Robot API doesn't have any methods that called before or after ALL executions, so you need to delete shared test cycle key file and lock file manually after run. The best way is to create some pre-execution script (similar to example above) that will do this cleanup for you.<br>
**IMPORTANT**: If you not delete those files, your next run will report test executions into previously created TM4J test cycle.

# Exceptions
## TM4JConfigurationException
Raised by listener if test is not tagged with TM4J test case key:
```bash
tm4j_reporter_api.tm4j_exceptions.tm4j_configuration_exceptions.TM4JConfigurationException: Test case key is not found in list of tags. Please mark robot test with tag 'TM4J:<test_case_key>'.
```

# TM4J test cycle description keyword
Library provides possibility to set TM4J test cycle description with special keyword `Set Tm4j Test Cycle Description`.

## Usage
Import library first, use keyword after:
```robot
*** Settings ***
Library  tm4j_reporter_robot.TM4JCycleDescriptor
Suite Setup  Setting Cycle Description


*** Keywords ***
Setting Cycle Description
    Set Tm4j Test Cycle Description  My test cycle description
```

Keyword is in global scope, so only one instance is created during the whole test execution and it is shared by all test cases and test suites.