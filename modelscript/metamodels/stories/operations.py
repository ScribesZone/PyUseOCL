# coding=utf-8
"""
Meta elements for modeling operations

The structure of this package is the following::

    Step
    <|-- OperationStep
        <|-- UpdateStep
            <|-- ObjectCreationStep
            <|-- ObjectDeletionStep
            <|-- SlotStep
            <|-- LinkCreationStep
            <|-- LinkDeletionStep
            <|-- LinkObjectCreationStep
        <|-- ConsultStep
            <|-- CheckStep
            <|-- ReadStep

"""
from abc import ABCMeta

from typing import Optional, Text

from modelscript.metamodels.textblocks import TextBlock
from modelscript.metamodels.classes.classes import (
    PlainClass)
from modelscript.metamodels.classes.assocclasses import (
    AssociationClass)
from modelscript.metamodels.classes.associations import (
    PlainAssociation,
    Association)
from modelscript.metamodels.classes.types import SimpleValue
from modelscript.base.grammars import AST

from modelscript.metamodels.stories import Step

META_CLASSES=[
    'OperationStep',
    'UpdateStep',
    'ObjectCreationStep',
    'ObjectDeletionStep',
    'SlotStep',
    'LinkCreationStep',
    'LinkDeletionStep',
    'LinkObjectCreationStep',
    'LinkObjectDeletionStep',
    'ConsultStep',
    'CheckStep',
    'ReadStep',
]
__all__=META_CLASSES

#--------------------------------------------------------------
#   Abstract classes
#--------------------------------------------------------------

class OperationStep(Step):
    __metaclass__ = ABCMeta

    def __init__(self,
        parent,
        astNode=None,
        lineNo=None,
        description=None):
        #type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(OperationStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

    @property
    def hasOperations(self):
        return True


class UpdateOperationStep(OperationStep):
    __metaclass__ = ABCMeta


    def __init__(self,
                    parent, isAction, 
                    astNode=None, lineNo=None,
                    description=None):
        # type: (Step, bool, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(UpdateOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.isAction=isAction
        #type: bool


class ConsultOperationStep(OperationStep):
    __metaclass__ = ABCMeta


    def __init__(self,
                    parent,
                    astNode=None, lineNo=None,
                    description=None):
        # type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ConsultOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


#--------------------------------------------------------------
#   Update operations
#--------------------------------------------------------------

class ObjectCreationStep(UpdateOperationStep):
    """
    Creation of an object. The class is known.
    """
    def __init__(self,
                 parent, isAction,
                 objectName, class_,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, PlainClass,  Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ObjectCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        assert isinstance(class_, PlainClass)

        self.objectName=objectName
        #type: Text

        self.class_=class_
        #type: PlainClass


class SlotStep(UpdateOperationStep):
    """
    Assignment like "o"."a"=v. The names of the object
    and the attribute are known but not the attribute/object.
    """
    def __init__(self,
                 parent, isAction,
                 objectName, attributeName, value,
                 isUpdate=None,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Text, 'BasicValue', Optional[bool], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(SlotStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName=objectName
        #type: Text

        self.attributeName=attributeName
        #type: Text

        self.simpleValue=value
        #type: SimpleValue

        self.isUpdate=isUpdate
        #type: Optional[bool]
        # Indicates if this is an initialization or an isUpdate
        # this indication could be given in the syntax (or not).


class ObjectDeletionStep(UpdateOperationStep):
    """
    Deletion of a regular object OR of a link object.
    Only the name of the object is known.
    No indication about the class/association class.
    """
    def __init__(self,
                 parent,
                 objectName,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, Text, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ObjectDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName=objectName
        #type: Text


class LinkCreationStep(UpdateOperationStep):
    """
    Creation of a link like "(o1, R, o2)" where R is a
    PlainAssociation. The name of the plain association is known.
    Names of objects are known but not the objects themselves.
    """
    def __init__(self,
                 parent, isAction,
                 sourceObjectName, targetObjectName, association,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Text, PlainAssociation, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None

        super(LinkCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName=sourceObjectName
        #type:Text

        self.targetObjectName=targetObjectName
        #type:Text

        self.association=association
        # type: PlainAssociation


class LinkDeletionStep(UpdateOperationStep):
    """
    Deletion of a link like "o1" R "o2": the name of association
    is known. Names of objects are known but not the objects.
    """
    def __init__(self,
                 parent,
                 sourceObjectName, targetObjectName, association,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, Text, Text, Association, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(LinkDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName=sourceObjectName
        #type:Text

        self.targetObjectName=targetObjectName
        #type:Text

        self.association=association
        # type: PlainAssociation


class LinkObjectCreationStep(UpdateOperationStep):
    """
    Creation of a link object like "x : AC (o1, o2).
    The name AC of the association class is known.
    Names of objects are known but not the objects.
    """
    def __init__(self,
                 parent, isAction,
                 linkObjectName,
                 sourceObjectName, targetObjectName, associationClass,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Text, Association, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None

        super(LinkObjectCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        assert isinstance(associationClass, AssociationClass)
        self.linkObjectName=linkObjectName
        #type:Text

        self.sourceObjectName=sourceObjectName
        #type:Text

        self.targetObjectName=targetObjectName
        #type:Text

        self.associationClass=associationClass
        # type: AssociationClass



#--------------------------------------------------------------
#   Consult operations
#--------------------------------------------------------------

class CheckStep(ConsultOperationStep):

    def __init__(self,
                 parent, number, position=None, astNode=None):
        super(CheckStep, self).__init__(
            parent=parent,
            astNode=astNode)

        self.number=number
        #type: int
        """
        The index of the CheckStep in the story.
        It is computed be StoryFiller.story().
        This number is used to give a unique label to each CheckStep.
        """

        self.position=position
        #type: Optional['before','after']
        """ 
        Indicates if the check statement is explicit (None)
        or implicit 'before' or 'after' a block. These implicit
        checks step are automatically added by the parser.
        """

    @property
    def isImplicit(self):
        return self.position is not None

    @property
    def label(self):
        # property label might not be necessary
        return self.subjectLabel

    @property
    def subjectLabel(self):
        """
        Label like
        * "A.3.2" if the check is explicit
        * or "A.2.before_1" if the check is before step 1
        """
        parent_label=self.parent.subjectLabel
        nth_label=self.parent.steps.index(self)+1
        if self.isImplicit:
            return '%s.%s_%s' % (
                parent_label,
                self.position,
                nth_label)
        else:
            return '%s.%s' % (
                parent_label,
                nth_label)



class ReadStep(ConsultOperationStep):
    def __init__(self,
                 parent,
                 astNode=None, lineNo=None, description=None):
        super(ReadStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        #TODO:4 implement ReadStep
        pass