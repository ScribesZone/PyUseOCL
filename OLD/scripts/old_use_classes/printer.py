# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinterConfig,
    ModelSourcePrinter
)
from modelscripts.metamodels.classes import (
    METAMODEL,
    ClassModel
)
from modelscripts.use.use.printer import (
    UseModelPrinter
)


class ClassModelPrinter(UseModelPrinter):
    def __init__(self,
                 theModel,
                 config=None):
        #type: (ClassModel, Optional[ModelPrinterConfig]) -> None
        super(ClassModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

METAMODEL.registerModelPrinter(ClassModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
