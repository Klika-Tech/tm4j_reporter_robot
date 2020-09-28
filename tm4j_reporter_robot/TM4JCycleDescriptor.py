# Copyright (C) 2020 Klika Tech, Inc. or its affiliates.  All Rights Reserved.
# Use of this source code is governed by an MIT-style license that can be found in the LICENSE file
# or at https://opensource.org/licenses/MIT.

from tm4j_reporter_robot import library_variables


def set_tm4j_test_cycle_description(description: str) -> None:
    """
    Setting TM4J test cycle description.

    :param description: TM4J test cycle description
    :type description: str

    :return: None
    :rtype: None
    """
    print(f"Setting TM4J test cycle description to {description}")
    library_variables.TEST_CYCLE_DESCRIPTION = description
    return None
