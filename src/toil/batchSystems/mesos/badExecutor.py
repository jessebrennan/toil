#!/usr/bin/env python

# Copyright (C) 2015 UCSC Computational Genomics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import itertools
import logging

from toil.batchSystems.mesos.executor import MesosExecutor, main

log = logging.getLogger(__name__)


class BadMesosExecutor(MesosExecutor):
    i = itertools.count()

    # FIXME: The overridden method does not exist (#234)

    def _callCommand(self, command, taskID):
        if self.i.next() % 2 == 0:
            result = super(BadMesosExecutor, self)._callCommand(command, taskID)
            if result != 0:
                log.debug("Command {} actually failed with {}".format(command, result))
            return result
        else:
            log.debug("Mimic failure of command: {}".format(command))
            return 1


if __name__ == "__main__":
    main(executorClass=BadMesosExecutor)
