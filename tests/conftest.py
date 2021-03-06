#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""pytest configuration file"""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "unit: Run only unit tests",
    )
    config.addinivalue_line(
        "markers",
        "integration: Run only integration tests",
    )
    config.addinivalue_line(
        "markers",
        "acceptance: Run only acceptance tests",
    )
