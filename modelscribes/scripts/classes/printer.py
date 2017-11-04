# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscribes.use.use.printer import (
    UseSourcePrinter,
    UseModelPrinter
)
from modelscribes.metamodels.classes import METAMODEL



class ClassModelPrinter(UseModelPrinter):
    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=True):
        super(ClassModelPrinter, self).__init__(
            theModel=theModel,
            summary=summary,
            displayLineNos=displayLineNos)

class ClassSourcePrinter(UseSourcePrinter):
    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True):
        super(UseSourcePrinter, self).__init__(
            theSource=theSource,
            summary=summary,
            displayLineNos=displayLineNos)

METAMODEL.registerModelPrinter(ClassModelPrinter)
METAMODEL.registerSourcePrinter(ClassSourcePrinter)
