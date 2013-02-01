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
import collections
import logging
import show
import re
import collections

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class LanguageException(Exception):
    """Base class for exceptions."""
    pass

class TypeError(LanguageException):
    """
    Raised when an operation could not be performed due to an inappropriate type.
    """
    pass

class GapError(LanguageException):
    """
    Raised when an operation could not be performed due to a gap in the 
    synax tree.
    """
    pass

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

def translate_function_1(function_name, operand1):
    """Generates code for 1-ary function application."""
    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name,operand1).translate()
    code += "%s(%s)" % (function_name, operand1_var_name)
    return code

def translate_function_2(function_name, operand1, operand2):
    """Generates code for 2-ary function application."""
    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name,operand1).translate()
    operand2_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand2_var_name,operand2).translate()
    code += "%s(%s, %s)" % (function_name, operand1_var_name, 
        operand2_var_name)
    return code

def translate_function_3(function_name, operand1, operand2, operand3):
    """Generates code for 3-ary function application."""
    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name,operand1).translate()
    operand2_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand2_var_name,operand2).translate()
    operand3_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand3_var_name,operand3).translate()
    code += "%s(%s, %s, %s)" % (function_name, operand1_var_name, 
        operand2_var_name, operand3_var_name)
    return code

def translate_operator_2(operator_name, operand1, operand2):
    """Generates code for 2-ary infix operator application."""

    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name, operand1).translate()
    operand2_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand2_var_name, operand2).translate()
    code += "(%s %s %s)" % (operand1_var_name,  operator_name,
        operand2_var_name)
    return code

def translate_instance_method_0(instance_expr, method_name):
    """Generates code for 0-ary instance method application."""
    code = ""
    instance_var_name = get_fresh_variable_name()
    code += SetVariableStatement(instance_var_name,instance_expr).translate()
    code += "%s.%s()" % (instance_var_name, method_name)
    return code

def indent(code):
    """
    Indent each non empty line by 4 spaces.
    """
    def indent_line(line):
        if line == "":
            return ""
        else:
            return "    " + line
    return '\n'.join(map(indent_line, code.splitlines()))

def generate_function(name, body):
    """
    >>> generate_function("f", "pass")
    'def f():\\n    pass'
    """
    return """def %s():
%s""" % (name, indent(body))

def generate_function_name(text):
    """
    Creates safe function name from arbitrary text.

    Satisfies definition of identifiers at
    http://docs.python.org/2/reference/lexical_analysis.html#identifiers

    >>> generate_function_name("Example Text Scene")
    'example_text_scene'

    >>> generate_function_name("Example  Text  Scene!!!")
    'example__text__scene___'
    """
    text = text.lower().replace(" ", "_")
    return re.sub(r'[^a-z_]', "_", text)

class LanguageComponent(object):
    """Base class for all components of the language."""

    def __init__(self, children=[]):
        self._children = children
    
    def translate(self):
        """
        Returns a translation of language component in linear Python code.

        Indentation, blankspace and other details depend on the particular type
        of language component.

        :return: Linear Python code.
        :rtype: string
        """
        raise NotImplementedError

    def get_live_variables(self):
        """
        Returns list of variable names for variable that are live on entrance
        to the language component.

        Analysis will **overestimate** for safety and returns variables that
        **may be** live.

        :rtype: string set
        """
        # Implement naive recursive strategy.
        # This assumes all variables are defined in leaves and that leaves
        # implement the base case.
        live_variables = set()
        for child in self._children:
           live_variables |= child.get_live_variables()
        return live_variables

class Gap(LanguageComponent):
    """
    Base class for gaps, components to represent an incomplete part of the syntax
    tree.
    """
    
    def translate(self):
        raise GapError()

class NumberGap(Gap):
    pass

class TextGap(Gap):
    pass

class VideoGap(Gap):
    pass

class VideoCollectionGap(Gap):
    pass

class Expression(LanguageComponent):
    """Base class for all expressions in the language."""
    pass

class CommandSequence(LanguageComponent, collections.Sequence):
    """
    Implement collections.Sequence abstract class using delegation-composition
    so only expose neccessary features in interface.
    """

    def __init__(self, commands=[]):
        """
        :type commands: Statement iterable
        """
        super(CommandSequence, self).__init__(commands)

    def __getitem__(self,key):
        return self._children.__getitem__(key)

    def __len__(self):
        return self._children.__len__()

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        code = ""
        for command in self._children:
            code += command.translate()
        code += "\n"
        return code

class Act(LanguageComponent):
    """
    Highest level container. Analagous to a program.
    """

    scenes = property(lambda self: self._children)

    def __init__(self, scenes):
        super(Act, self).__init__(scenes)

    def translate(self):
        # code = ""
        # for scene in self._children:
        #     code += "\n" + scene.translate()
        # return code
         
        functions = collections.OrderedDict()
        function_num = 1

        for scene in self._children:
            name = "scene_%s" % function_num
            function = generate_function(name, scene.translate())
            functions[name] = function
            function_num += 1

        generate_function_call = lambda name: "%s()" % name

        main_function_body = '\n'.join(map(generate_function_call, functions.keys()))
        main_function = generate_function("main", main_function_body)

        code = main_function + "\n\n"
        code += "\n".join(functions.values())
        code += "\n\n" + generate_function_call("main")

        return code

class Scene(LanguageComponent):
    """
    Analagous to a basic block.
    """

    title = property(lambda self: self._title)
    comment = property(lambda self: self._comment)
    duration = property(lambda self: self._duration)
    pre_commands = property(lambda self: self._pre_commands)
    post_commands = property(lambda self: self._post_commands)
    
    def __init__(self, title, comment, duration, pre_commands=CommandSequence([]), post_commands=CommandSequence([])):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type pre_commands: CommandSequence
        :type post_commands: CommandSequence
        """
        super(Scene, self).__init__([duration, pre_commands, post_commands])
        self._title = title
        self._comment = comment
        self._duration = duration
        self._pre_commands = pre_commands
        self._post_commands = post_commands

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        code = self.translate_before_content()
        code += CommentStatement("Scene content.").translate()
        code += self.translate_content()
        code += self.translate_after_content()
        return code

    def translate_before_content(self):
        code = CommentStatement(self._title).translate()
        if self._comment != "":
            code += CommentStatement("").translate()
            code += CommentStatement(self._comment).translate()
        code += CommentStatement("Pre commands.").translate()
        code += self._pre_commands.translate()
        return code

    def translate_content(self):
        raise NotImplementedError

    def translate_after_content(self):
        code = CommentStatement("Post commands.").translate()
        code += self._post_commands.translate()
        return code

class VideoScene(Scene):

    offset = property(lambda self: self._offset)
    source = property(lambda self: self._source)

    def __init__(self, title, comment, duration, pre_commands, post_commands, offset, source):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type pre_commands: CommandSequence
        :type post_commands: CommandSequence
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        """
        super(VideoScene, self).__init__(title, comment, duration, pre_commands, post_commands)
        self._children.extend([offset, source])
        self._offset = offset
        self._source = source

    def translate_content(self):
        return translate_function_3("videoplayer.play", self._source, self._offset, self._duration) + "\n"

class ImageScene(Scene):

    def __init__(self, title, comment, duration, offset, source):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        """
        raise NotImplementedError

class TextScene(Scene):

    text = property(lambda self: self._text)

    def __init__(self, title, comment, duration, pre_commands, post_commands, text):
        """
        :type title: string
        :type comment: string
        :type pre_commands: CommandSequence
        :type post_commands: CommandSequence
        :type duration: <:NumberExpression
        :type text: <:TextExpression
        """
        super(TextScene, self).__init__(title, comment, duration, pre_commands, post_commands)
        self._children.append(text)
        self._text = text

    def translate_content(self):
        return translate_function_2("display", self._text, self._duration) + "\n"

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
        """
        :type text: string
        """
        self._text = text

    def translate(self):
        return "# %s\n" % self._text

class SetVariableStatement(Statement):

    name = property(lambda self: self._name)
    value = property(lambda self: self._value)

    def __init__(self, name, value):
        """
        :type name: string
        :type value: <: TextExpression | NumberExpression | VideoExpression | VideoCollectionExpression
        """
        super(SetVariableStatement, self).__init__([value])
        self._name = name
        self._value = value

    def translate(self):
        value_code = self._value.translate()
        up_to, last = partition_on_last_newline(value_code)
        code = up_to
        if up_to != "":
            code += "\n"
        code += "%s = %s\n" % (self._name,last)
        return code

    # def get_live_variables(self):
    #     """
    #     Later may want to implement a better estimate by taking into account
    #     variables being dereferenced by setting to a new value.
    #     """
    #     return []

class GetVariableExpression(LanguageComponent):

    name = property(lambda self: self._name)

    def __init__(self, name):
        """
        :type name: string
        """
        self._name = name

    def translate(self):
        return self._name

    def get_live_variables(self):
        """Base case."""
        return set([self._name])

class TextExpression(Expression):
    """Base class for expressions that evaluate to type Text."""
    pass

class TextValue(TextExpression):

    def __init__(self,text):
        """
        :type text: string
        """
        super(TextValue, self).__init__()
        self._text = text

    def translate(self):
        return "'%s'" % self._text

    @property
    def value(self):
        return self._text

class YoutubeVideoGetTitle(TextExpression):

    video = property(lambda self: self._video)

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        super(YoutubeVideoGetTitle, self).__init__([video])
        self._video = video

    def translate(self):
        return translate_instance_method_0(self._video, "title")

class YoutubeVideoGetDescription(TextExpression):

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        super(YoutubeVideoGetDescription, self).__init__([video])
        self._video = video

    def translate(self):
        return translate_instance_method_0(self._video, "description")

class NumberExpression(Expression):
    """Base class for expressions that evaluate to type Number."""
    pass

class YoutubeVideoGetDuration(NumberExpression):

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        super(YoutubeVideoGetDuration, self).__init__([video])
        self._video = video

    def translate(self):
        return translate_instance_method_0(self._video, "duration")

class NumberValue(NumberExpression):

    def __init__(self,number):
        """
        :type number: int
        """
        super(NumberValue, self).__init__()
        self._number = number

    def translate(self):
        return str(self._number)

    def __repr__(self):
        return "NumberValue(%s)" % self._number

    @property
    def value(self):
        return str(self._number)

class GetRandomNumberBetweenInterval(NumberExpression):

    def __init__(self,lower_number_expr,higher_number_expr):
        """
        :type lower_number_expr: <:NumberExpression
        :type higher_number_expr: <:NumberExpression
        """
        super(GetRandomNumberBetweenInterval, self).__init__([
            lower_number_expr,
            higher_number_expr
        ])
        self._lower_number_expr = lower_number_expr
        self._higher_number_expr = higher_number_expr

    def translate(self):
        return translate_function_2("random.uniform", self._lower_number_expr, self._higher_number_expr)


class Add(NumberExpression):

    op1 = property(lambda self: self._op1)
    op2 = property(lambda self: self._op2)

    def __init__(self, op1, op2):
        super(Add,self).__init__([op1, op2])
        self._op1 = op1
        self._op2 = op2

    def translate(self):
        return translate_operator_2("+", self._op1, self._op2)

    def __repr__(self):
        return "Add(%s,%s)" % (self._op1, self._op2)

class Subtract(NumberExpression):

    op1 = property(lambda self: self._op1)
    op2 = property(lambda self: self._op2)

    def __init__(self,op1,op2):
        super(Subtract,self).__init__([op1, op2])
        self._op1 = op1
        self._op2 = op2

    def translate(self):
        return translate_operator_2("-", self._op1, self._op2)

    def __repr__(self):
        return "Subtract(%s,%s)" % (self._op1, self._op2)

class Multiply(NumberExpression):

    op1 = property(lambda self: self._op1)
    op2 = property(lambda self: self._op2)

    def __init__(self,op1,op2):
        super(Multiply,self).__init__([op1, op2])
        self._op1 = op1
        self._op2 = op2

    def translate(self):
        return translate_operator_2("*", self._op1, self._op2)

    def __repr__(self):
        return "Multiply(%s,%s)" % (self._op1, self._op2)

class VideoExpression(Expression):
    """Base class for expressions that evaluate to type Video."""
    pass

class VideoValue(VideoExpression):

    def __init__(self, web_url):
        """
        :type web_url: string
        """
        super(VideoValue, self).__init__()
        self._web_url = web_url

    def translate(self):
        return "youtube.Video.from_web_url('%s')" % self._web_url

    @property
    def value(self):
        return self._web_url

class VideoCollectionExpression(Expression):
    """Base class for expressions that evaluate to type VideoCollection."""
    pass

class VideoCollectionValue(VideoCollectionExpression):

    def __init__(self,web_urls):
        """
        :type web_urls: string
        """
        super(VideoCollectionValue, self).__init__()
        self._web_urls = web_urls

    def translate(self):
        return "youtube.VideoCollection.from_web_urls('%s')" % self._web_urls

class YoutubeVideoGetRelated(VideoCollectionExpression):

    video = property(lambda self: self._video)

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        super(YoutubeVideoGetRelated,self).__init__([video])
        self._video = video

    def translate(self):
        return translate_instance_method_0(self._video, "related")

class YoutubeSearch(VideoCollectionExpression):

    def __init__(self,text_expr):
        """
        :type text_expr: <:TextExpression
        """
        super(YoutubeSearch,self).__init__([text_expr])
        self._text_expr = text_expr

    def translate(self):
        return translate_function_2("youtube.search", self._text_expr)

class YoutubeVideoCollectionRandom(VideoExpression):

    video_collection = property(lambda self: self._video_collection_expr)

    def __init__(self,video_collection_expr):
        """
        :type video_collection_expr: <:VideoCollectionExpression
        """
        super(YoutubeVideoCollectionRandom,self).__init__([video_collection_expr])
        self._video_collection_expr = video_collection_expr

    def translate(self):
        return translate_instance_method_0(self._video_collection_expr, "random")