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
robot --listener tm4j_reporter_robot.TM4JRobotListener:<tm4j_access_key>:<tm4j_project_key>:<tm4j_test_cycle_name> test.robot
```
| Param                | Mandatory | Description                                                                                                                                            | Type | Example       |
|----------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|------|---------------|
| tm4j_access_key      | Yes       | API key to access TM4j. To get it see [Instruction](https://support.smartbear.com/tm4j-cloud/docs/api-and-test-automation/generating-access-keys.html) | str  |               |
| tm4j_project_key     | Yes       | Jira / TM4J project prefix without trailing dash                                                                                                       | str  | QT            |
| tm4j_test_cycle_name | No        | TM4J test cycle name. If not passed, listener will create a new one test cycle with default name "Robot run YYYY-mm-DD HH-MM-SS"                       | str  | My test cycle |

In order to listener reported test execution to TM4J, mark Robot test case with tag `TM4J:<tm4j_test_case_key>`:
```robot
My Robot Test Case
    [Tags]  Some tag 1  Some tag 2  TM4J:QT-001
    test code goes here
```

# Exceptions
## TM4JConfigurationException
Raised by listener if test is not tagged with TM4J test case key:
```bash
tm4j_reporter_api.tm4j_exceptions.tm4j_configuration_exceptions.TM4JConfigurationException: Test case key is not found in list of tags. Please mark robot test with tag 'TM4J:<test_case_key>'.
```
