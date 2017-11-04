# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.base.printers import (
    AbstractPrinter,
    SourcePrinter
)

from modelscribes.metamodels.usecases import (
    UsecaseModel,
    METAMODEL
)



class UsecaseModelPrinter(AbstractPrinter):  # check

    def __init__(self, usecaseModel, displayLineNos=True):
        #type: (UsecaseModel, bool) -> None
        super(UsecaseModelPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.usecaseModel=usecaseModel

    def do(self):
        super(UsecaseModelPrinter, self).do()
        self._usecaseModel(self.usecaseModel)
        return self.output

    def _usecaseModel(self, usecaseModel):
        self.outLine(
            'usecase model',
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1  )

        self.doActorsUsecases(usecaseModel)


        for actor in usecaseModel.actorNamed.values():
            self.actor(actor)

        if usecaseModel.system is None:
            self.outLine('-- NO SYSTEM DEFINED !')
        else:
            self.outLine(
                'system %s ' % usecaseModel.system.name,
                lineNo=usecaseModel.system.lineNo,
                linesBefore=1,
                linesAfter=1)

            for usecase in usecaseModel.system.usecases:
                self.usecase(usecase)



    def actor(self, actor):
        self.outLine(
            'actor %s' % actor.name,
            lineNo=actor.lineNo
        )

    def usecase(self, usecase):
        self.outLine(
           'usecase %s' % usecase.name,
            lineNo=usecase.lineNo
        )

    def doActorsUsecases(self, usecaseModel):
        for a in usecaseModel.actors:
            if len(a.usecases)>=1:
                for u in a.usecases:
                    self.outLine('%s %s' % (a.name, u.name))
            else:
                self.outLine('-- %s DO_NOTHING' % a.name)
        if usecaseModel.system is None:
            self.outLine('-- NO SYSTEM DEFINED !')
            for u in usecaseModel.system.usecases:
                if len(u.actors)==0:
                    self.outLine('-- NOBODY %s' % u.name)
                    self.outLine('')
            self.outLine('')



class UsecaseSourcePrinter(SourcePrinter):

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True,
                 ):
        super(UsecaseSourcePrinter, self).__init__(
            theSource=theSource,
            summary=summary,
            displayLineNos=displayLineNos)

    def do(self):
        self.output=''
        if self.theSource.isValid:
            p=UsecaseModelPrinter(
                usecaseModel=self.theSource.model,
                displayLineNos=self.displayLineNos,
            ).do()
            self.out(p)
        else:
            self._issues()
        return self.output

METAMODEL.registerModelPrinter(UsecaseModelPrinter)
METAMODEL.registerSourcePrinter(UsecaseSourcePrinter)

