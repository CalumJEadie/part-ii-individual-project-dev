"""
Models for the language.

Notes on notation:
- Using <:A to mean any subtype of A

Based on review of ideas from Semantics of Programming Languages,
Compiler Construction and Optimising Compilers.

Using Text and Number rather than familiar types like String, Integer and Float
to emphasis that these are abstractions over these types designed for purposes
of an education programming language.

Classes representing method invocations are named using module, class and
method.

To minimise implementation and make output close to normal Python for education
purposes Python's variable system is used directly.

Hence the language is dynamically typed.

Function class based on Scala's anonymous functions.
"""

import app.api.youtube

def partition_on_last_newline(text):
    """
    Splits text into lines up to last line and the last line.

    >>> print partition_on_last_newline("a")
    ('', 'a')
    >>> print partition_on_last_newline("a\\nb")
    ('a', 'b')
    >>> print partition_on_last_newline("a\\nb\\nc")
    ('a\\nb', 'c')
    """
    before,sep,after = text.rpartition("\n")
    return before,after

def get_fresh_variable_name():
    get_fresh_variable_name.count += 1
    return "tmp_%s" % get_fresh_variable_name.count
get_fresh_variable_name.count = 0

class LanguageComponent(object):
    """Base class for all components of the language."""
    
    def translate(self):
        """
        Returns a translation of language component in linear Python code.

        Indentation, blankspace and other details depend on the particular type
        of language component.

        :return: Linear Python code.
        :rtype: string
        """
        raise NotImplementedError



class Expression(LanguageComponent):
    """Base class for all expressions in the language."""
    pass

class Operator2(Expression):
    """Asbtract class for a 2-ary infix operator application"""

    def __init__(self, operator_name, operand1, operand2):
        self._operator_name = operator_name
        self._operand1 = operand1
        self._operand2 = operand2

    def translate(self):
        code = ""
        operand1_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand1_var_name,self._operand1).translate()
        operand2_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand2_var_name,self._operand2).translate()
        code += "%s %s %s" % (operand1_var_name, self._operator_name,
            operand2_var_name)
        return code

class Function1(Expression):
    """Abstract class for a 1-ary function application."""

    def __init__(self, function_name, operand1):
        self._function_name = function_name
        self._operand1 = operand1

    def translate(self):
        code = ""
        operand1_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand1_var_name,self._operand1).translate()
        code += "%s(%s)" % (self._function_name, operand1_var_name)
        return code

class Function2(Expression):
    """Abstract class for a 2-ary function application."""

    def __init__(self, function_name, operand1, operand2):
        self._function_name = function_name
        self._operand1 = operand1
        self._operand2 = operand2

    def translate(self):
        code = ""
        operand1_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand1_var_name,self._operand1).translate()
        operand2_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand2_var_name,self._operand2).translate()
        code += "%s(%s, %s)" % (self._function_name, operand1_var_name, 
            operand2_var_name)
        return code

class Function3(Expression):
    """Abstract class for a 3-ary function application."""

    def __init__(self, function_name, operand1, operand2, operand3):
        self._function_name = function_name
        self._operand1 = operand1
        self._operand2 = operand2
        self._operand3 = operand3

    def translate(self):
        code = ""
        operand1_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand1_var_name,self._operand1).translate()
        operand2_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand2_var_name,self._operand2).translate()
        operand3_var_name = get_fresh_variable_name()
        code += SetVariableStatement(operand3_var_name,self._operand3).translate()
        code += "%s(%s, %s, %s)" % (self._function_name, operand1_var_name, 
            operand2_var_name, operand3_var_name)
        return code

class InstanceMethod0(Expression):
    """Abstrat class for a 0-ary instance method application."""

    def __init__(self, instance_expr, method_name):
        """
        :type instance_expr: <:Expression
        :type method_name: string
        """
        self._instance_expr = instance_expr
        self._method_name = method_name

    def translate(self):
        code = ""
        instance_var_name = get_fresh_variable_name()
        code += SetVariableStatement(instance_var_name,self._instance_expr).translate()
        code += "%s.%s()" % (instance_var_name, self._method_name)
        return code

class Act(LanguageComponent):
    """
    Highest level container. Analagous to a program.
    """

    def __init__(self, scenes):
        self._scenes = scenes

    def translate(self):
        code = ""
        for scene in self._scenes:
            code += scene.translate()

class Scene(LanguageComponent):
    """
    Analagous to a basic block.
    """
    
    def __init__(self, title, comment, duration):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        """
        self._title = title
        self._comment = comment
        self._duration = duration

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        code = ""
        code += CommentStatement(self._title).translate()
        if self._comment != "":
            code += CommentStatement("").translate()
            code += CommentStatement(self._comment).translate()
        return code

class VideoScene(Scene,Function3):

    def __init__(self, title, comment, duration, offset, source):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        """
        super(VideoScene, self).__init__(title, comment, duration)
        Function3.__init__(self, "videoplayer", source, offset, duration)

    def translate(self):
        code = super(VideoScene, self).translate()
        code += Function3.translate(self)
        return code

class ImageScene(Scene):

    def __init__(self, title, comment, duration, offset, source):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        """
        super(ImageScene, self).__init__(title, comment, duration)
        self._offset = offset
        self._source = source

class TextScene(Scene):

    def __init__(self, title, comment, duration, text):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type text: <:TextExpression
        """
        super(TextScene, self).__init__(title, comment, duration)
        self._text = text

    def translate(self):
        code = super(TextScene, self).translate()
        text_var_name = get_fresh_variable_name()
        code += SetVariableStatement(text_var_name,self._text).translate()
        code += "display(%s,duration)" % text_var_name
        return code

class Statement(LanguageComponent):

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        raise NotImplementedError

class CommentStatement(Statement):

    def __init__(self, text):
        self._text = text

    def translate(self):
        return "# %s\n" % self._text

class SetVariableStatement(Statement):

    def __init__(self, name, value):
        """
        :type name: string
        :type value: <: TextExpression | NumberExpression | VideoExpression | VideoCollectionExpression
        """
        self._name = name
        self._value = value

    def translate(self):
        value_code = self._value.translate()
        up_to, last = partition_on_last_newline(value_code)
        code = up_to
        code += "%s = %s\n" % (self._name,last)
        return code

class GetVariableExpression(LanguageComponent):

    def __init__(self, name):
        """
        :type name: string
        """

    def translate(self):
        return self._name

class TextExpression(Expression):
    """Base class for expressions that evaluate to type Text."""
    pass

class TextValue(TextExpression):

    def __init__(self,text):
        """
        :type text: string
        """
        self._text = text

    def translate(self):
        return "'%s'" % self._text

class YoutubeVideoGetTitle(TextExpression):

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        self._video = video

    def translate(self):
        code = ""
        video_var_name = get_fresh_variable_name()
        code += SetVariableStatement(video_var_name,self._video).translate()
        code += "\n%s.title()" % video_var_name
        return code

class YoutubeVideoGetDescription(InstanceMethod0, TextExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        super(YoutubeVideoGetDescription, self).__init__(video_expr, "description")

class NumberExpression(Expression):
    """Base class for expressions that evaluate to type Number."""
    pass

class YoutubeVideoGetDuration(InstanceMethod0, NumberExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        super(YoutubeVideoGetDuration, self).__init__(video_expr, "duration")

class NumberValue(NumberExpression):

    def __init__(self,number):
        """
        :type number: int
        """
        self._number = number

    def translate(self):
        return str(self._number)

class GetRandomNumberBetweenInterval(Function2, NumberExpression):

    def __init__(self,lower_number_expr,higher_number_expr):
        """
        :type lower_number_expr: <:NumberExpression
        :type higher_number_expr: <:NumberExpression
        """
        super(GetRandomNumberBetweenInterval, self).__init__(
            "random.uniform",
            lower_number_expr,
            higher_number_expr
        )

class Add(Operator2):

    def __init__(self,op1,op2):
        super(Add,self).__init__("+", op1, op2)

class Subtract(Operator2):

    def __init__(self,op1,op2):
        super(Subtract,self).__init__("-", op1, op2)

class Multiply(Operator2):

    def __init__(self,op1,op2):
        super(Multiply,self).__init__("*", op1, op2)

class VideoExpression():
    """Base class for expressions that evaluate to type Video."""
    pass

class VideoValue(VideoExpression):

    def __init__(self,video):
        """
        :type video: Video
        """
        self._video = video

    def translate(self):
        return "Video('%s')" % self._video

class VideoCollectionExpression():
    """Base class for expressions that evaluate to type VideoCollection."""
    pass

    def __init__(self,video_collection):
        """
        :type video_collection: VideoCollection
        """
        self._video_collection = video_collection

    def translate(self):
        return "VideoCollection('%s')" % self._video_collection

class YoutubeVideoGetRelated(InstanceMethod0, VideoCollectionExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        super(YoutubeVideoGetRelated, self).__init__(video_expr, "related")

class YoutubeSearch(Function1, VideoCollectionExpression):

    def __init__(self,text_expr):
        """
        :type text_expr: <:TextExpression
        """
        super(YoutubeSearch, self).__init__(text_expr, "youtube.search")

class YoutubeVideoCollectionRandom(InstanceMethod0, VideoCollectionExpression):

    def __init__(self,video_collection_expr):
        """
        :type video_collection_expr: <:VideoCollectionExpression
        """
        super(YoutubeVideoCollectionRandom, self).__init__(video_collection_expr, "random")