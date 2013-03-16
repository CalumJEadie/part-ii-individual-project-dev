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

import collections
import logging
import re
import collections

import app.api.youtube
import app.api.videoplayer
from app.api.videoplayer import Speed

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Type():
    """Type enum."""
    TEXT, NUMBER, VIDEO, VIDEO_COLLECTION = range(4)

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

# def get_fresh_variable_name():
#     get_fresh_variable_name.count += 1
#     return "tmp_%s" % get_fresh_variable_name.count
# get_fresh_variable_name.count = 0

class VariableNameGenerator(object):
    """
    Use Singleton design pattern.

    >>> g1 = VariableNameGenerator.get_instance()
    >>> g1.reset()
    >>> g1.generate()
    'store_a'
    >>> g1.generate()
    'store_b'
    >>> g2 = VariableNameGenerator.get_instance()
    >>> g2.generate()
    'store_c'
    >>> g2.reset()
    >>> g2.generate()
    'store_a'
    """

    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instantiation already exists!")
        self._count = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VariableNameGenerator()
        return cls._instance

    def generate(self):
        """
        Generate a variable name. Use alphabetical characters to make variable unique.
        Start with one character and increase length as count increases.

        Supports up to 26**2 identifiers. Splits identifier into base 26.

        store_ id1 id0
        """ 
        # assert self._count <= 26**2
        assert self._count <= 26*2

        # id1_count = self._count / 26
        # id0_count = self._count % 26

        # # ord("a") = 97
        # id1 = '' if id1_count == 0 else chr(97 + id1_count)
        # id0 = chr(97 + id0_count)
        if self._count < 26:
            id1 = ""
            id0 = chr(97 + self._count)
        else:
            id1 = "a"
            id0 = chr(97 + self._count - 26)

        self._count += 1

        return "store_%s%s" % (id1, id0)

    def reset(self):
        self._count = 0

def get_fresh_variable_name():
    generator = VariableNameGenerator.get_instance()
    return generator.generate()

def translate_function_0(function_name):
    """Generates code for 0-ary function application."""
    return "%s()" % (function_name)

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

def translate_function_4(function_name, operand1, operand2, operand3, operand4):
    """Generates code for 4-ary function application."""
    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name,operand1).translate()
    operand2_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand2_var_name,operand2).translate()
    operand3_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand3_var_name,operand3).translate()
    operand4_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand4_var_name,operand4).translate()
    code += "%s(%s, %s, %s, %s)" % (function_name, operand1_var_name, 
        operand2_var_name, operand3_var_name, operand4_var_name)
    return 

def translate_function_5(function_name, operand1, operand2, operand3, operand4, operand5):
    """Generates code for 5-ary function application."""
    code = ""
    operand1_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand1_var_name,operand1).translate()
    operand2_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand2_var_name,operand2).translate()
    operand3_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand3_var_name,operand3).translate()
    operand4_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand4_var_name,operand4).translate()
    operand5_var_name = get_fresh_variable_name()
    code += SetVariableStatement(operand5_var_name,operand5).translate()
    code += "%s(%s, %s, %s, %s, %s)" % (function_name, operand1_var_name, 
        operand2_var_name, operand3_var_name, operand4_var_name, operand5_var_name)
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
    :type name: string
    :type body: string

    >>> generate_function("f", "pass")
    'def f():\\n    pass'
    """
    return """def %s():
%s""" % (name, indent(body))

def generate_if(condition, true_body, false_body):
    """
    :type condition: string
    :type true_body: string
    :type false_body: string

    >>> generate_if("True", "pass", "pass")
    'if True:\\n    pass\\nelse:\\n    pass'
    """
    return """if %s:
%s
else:
%s""" % (condition, indent(true_body), indent(false_body))

def generate_while(condition, body):
    """
    :type condition: string
    :type body: string

    >>> generate_while("True", "pass")
    'while True:\\n    pass'
    """
    return """while %s:
%s""" % (condition, indent(body))

def generate_safe_identifier(text):
    """
    Create safe identifier name from arbitrary text.

    Satisfies definition of identifiers at
    http://docs.python.org/2/reference/lexical_analysis.html#identifiers

    `identifier ::=  (letter|"_") (letter | digit | "_")*`

    >>> generate_safe_identifier("Example Text Scene")
    'example_text_scene'

    >>> generate_safe_identifier("Example  Text  Scene!!!")
    'example__text__scene___'

    >>> generate_safe_identifier("current video")
    'current_video'

    >>> generate_safe_identifier("111")
    '_11'
    """
    text = text.lower().replace(" ", "_")
    # Make sure starts with (letter|"_")
    text = re.sub(r'^([^a-z_])', "_", text)
    # Make sure rest of identifier is made up of (letter | digit | "_")
    return re.sub(r'[^a-z0-9_]', "_", text)

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

    def get_live_variables(self, type):
        """
        Returns list of variable names for variable that are live on entrance
        to the language component.

        Analysis will **overestimate** for safety and returns variables that
        **may be** live.

        :type type: Type enum
        :rtype: string set
        """
        # Implement naive recursive strategy.
        # This assumes all variables are defined in leaves and that leaves
        # implement the base case.
        live_variables = set()
        for child in self._children:
           live_variables |= child.get_live_variables(type)
        return live_variables

    def get_all_live_variables(self):
        """
        :rtype: string set
        """
        return self.get_live_variables(Type.NUMBER) | \
            self.get_live_variables(Type.TEXT) | \
            self.get_live_variables(Type.VIDEO) | \
            self.get_live_variables(Type.VIDEO_COLLECTION)

    def get_all_live_variables_sorted_type_name(self):
        """
        Returns all live variables sorted by type then name.
        """
        return sorted(self.get_live_variables(Type.NUMBER)) + \
            sorted(self.get_live_variables(Type.TEXT)) + \
            sorted(self.get_live_variables(Type.VIDEO)) + \
            sorted(self.get_live_variables(Type.VIDEO_COLLECTION))

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

class SceneSequence(LanguageComponent):
    """
    Represents a linear sequence of scenes.
    """

    scenes = property(lambda self: self._children)

    def __init__(self, scenes):
        super(SceneSequence, self).__init__(scenes)

    def translate(self):
        code = ""
        # Handle empty scene collection
        if len(self._children) > 0:
            for scene in self._children:
                code += scene.translate() + "\n"
        else:
            code += "pass\n"
        return code

class Act(SceneSequence):
    """
    Highest level container. Analagous to a program.

    Responsible for translating entire program. Uses recursive translation strategy
    where each component responsible for it's own translation subject to some
    basic rules about new lines and indentation.
    """

    title = property(lambda self: self._title)

    def __init__(self, title, scenes):
        super(Act, self).__init__(scenes)
        self._title = title

    def translate(self):

        # Handle empty act
        if len(self._children) > 0:

            # Reset variable name generator
            VariableNameGenerator.get_instance().reset()

            code = ""

            # functions = collections.OrderedDict()
            # function_num = 1

            # Define sensible default values in case for variable in case user
            # does not initalise them.

            # Sort so that undeterministic order changing due from use of set doesn't
            # distract the user.
            
            live_number_variables = sorted(self.get_live_variables(Type.NUMBER))
            live_text_variables = sorted(self.get_live_variables(Type.TEXT))
            live_video_variables = sorted(self.get_live_variables(Type.VIDEO))
            live_video_collection_variables = sorted(self.get_live_variables(Type.VIDEO_COLLECTION))

            global_var_defn = ""
            for variable in live_number_variables:
                global_var_defn += SetVariableStatement(variable, NumberValue(0)).translate()
            for variable in live_text_variables:
                global_var_defn += SetVariableStatement(variable, TextValue("")).translate()
            for variable in live_video_variables:
                global_var_defn += SetVariableStatement(variable, VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")).translate()
            for variable in live_video_collection_variables:
                global_var_defn += SetVariableStatement(variable, VideoCollectionValue([])).translate()

            # for scene in self._children:
            #     name = "scene_%s" % function_num
            #     function = generate_function(name, scene.translate())
            #     functions[name] = function
            #     function_num += 1

            # generate_function_call = lambda name: "%s()" % name

            # main_function_body = '\n'.join(map(generate_function_call, functions.keys()))
            # main_function = generate_function("main", main_function_body)

            if global_var_defn != "":
                code += global_var_defn + "\n"
            # code += main_function + "\n\n"
            # code += "\n".join(functions.values())
            # code += "\n" + generate_function_call("main")
            
            code += super(Act, self).translate()

        else:

            code = super(Act, self).translate()

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

        ## In Python module/global scope is read-only shadow within the local function/
        ## method scope so can access variables but not change them. Need to be able
        ## to change the variables do declare any variables that might be changed as
        ## global.
        ## See: http://stereochro.me/ideas/global-in-python
        # live_variables = self.get_all_live_variables_sorted_type_name()
        # if len(live_variables) > 0:
        #     code += "\n"
        #     for variable in live_variables:
        #         code += "global %s\n" % generate_safe_identifier(variable)

        if len(self._pre_commands) > 0:
            code += "\n"
            code += CommentStatement("Pre commands.").translate()
            code += self._pre_commands.translate()
        else:
            code += "\n"

        return code

    def translate_content(self):
        raise NotImplementedError

    def translate_after_content(self):
        if len(self._post_commands) > 0:
            code = "\n"
            code += CommentStatement("Post commands.").translate()
            code += self._post_commands.translate()
        else:
            code = "\n"
        return code

class SpeedValue(LanguageComponent):

    value = property(lambda self: self._value)

    def __init__(self, value):
        """
        :type value: app.api.videoplayer.Speed
        """
        assert value in (Speed.Slow, Speed.Normal,
            Speed.Fast, Speed.VFast)
        super(SpeedValue, self).__init__()
        self._value = value

    def translate(self):
        return {
            Speed.Slow : "Speed.Slow",
            Speed.Normal : "Speed.Normal",
            Speed.Fast : "Speed.Fast",
            Speed.VFast : "Speed.VFast"
        }[self._value]

class VideoScene(Scene):

    offset = property(lambda self: self._offset)
    source = property(lambda self: self._source)
    volume = property(lambda self: self._volume)
    speed = property(lambda self: self._speed)

    def __init__(self, title, comment, duration, pre_commands, post_commands, offset, source, volume=None, speed=None):
        """
        :type title: string
        :type comment: string
        :type duration: <:NumberExpression
        :type pre_commands: CommandSequence
        :type post_commands: CommandSequence
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        :type volume: <:NumberExpression
        :type speed: SpeedValue
        """
        super(VideoScene, self).__init__(title, comment, duration, pre_commands, post_commands)
        self._children.extend([offset, source, volume, speed])
        self._offset = offset
        self._source = source
        self._volume = volume if volume is not None else NumberValue(0)
        self._speed = speed if speed is not None else SpeedValue(Speed.Normal)

    def translate_content(self):
        return translate_function_5("videoplayer.play", self._source, self._offset, self._duration, self._volume, self._speed) + "\n"

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

class IfScene(LanguageComponent):
    """
    Conditionaly executes one of two acts based on boolean condition.

    'Hard wire' boolean condition to be generated by ask_yes_no. Can generalise later.
    """

    title = property(lambda self: self._title)
    comment = property(lambda self: self._comment)
    question = property(lambda self: self._question)
    true_scene_sequence = property(lambda self: self._true_scene_sequence)
    false_scene_sequence = property(lambda self: self._false_scene_sequence)

    def __init__(self, title, comment, question, true_scene_sequence, false_scene_sequence):
        """
        :type title: string
        :type comment: string
        :type question: <:TextExpression
        :type true_scene_sequence: SceneSequence
        :type false_scene_sequence: SceneSequence
        """
        super(IfScene, self).__init__([question, true_scene_sequence, false_scene_sequence])
        self._title = title
        self._comment = comment
        self._question = question
        self._true_scene_sequence = true_scene_sequence
        self._false_scene_sequence = false_scene_sequence

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        code = CommentStatement(self._title).translate()

        if self._comment != "":
            code += CommentStatement("").translate()
            code += CommentStatement(self._comment).translate()

        code += "\n"

        # Need to break up condition code as may span many lines when evaluating
        # question value.
        condition_code = translate_function_1("ask_yes_no", self._question)
        up_to, last = partition_on_last_newline(condition_code)
        if up_to != "":
            code += up_to + "\n"
        code += generate_if(
            last,
            self._true_scene_sequence.translate(),
            self._false_scene_sequence.translate()
        )
        code += "\n"

        return code

class WhileScene(LanguageComponent):
    """
    Conditionaly repeatedly execute a scene seeuqnce based on a boolean condition.

    'Hard wire' boolean condition to be generated by ask_yes_no. Can generalise later.
    """

    title = property(lambda self: self._title)
    comment = property(lambda self: self._comment)
    question = property(lambda self: self._question)
    scene_sequence = property(lambda self: self._scene_sequence)

    def __init__(self, title, comment, question, scene_sequence):
        """
        :type title: string
        :type comment: string
        :type question: <:TextExpression
        :type scene_sequence: SceneSequence
        """
        super(WhileScene, self).__init__([question, scene_sequence])
        self._title = title
        self._comment = comment
        self._question = question
        self._scene_sequence = scene_sequence

    def translate(self):
        """
        Preconditions:
        - Will follow a new line.
        Postconditions:
        - Will end in a new line.
        """
        code = CommentStatement(self._title).translate()

        if self._comment != "":
            code += CommentStatement("").translate()
            code += CommentStatement(self._comment).translate()

        code += "\n"

        # Need to break up condition code as may span many lines when evaluating
        # question value.
        condition_code = translate_function_1("ask_yes_no", self._question)
        up_to, last = partition_on_last_newline(condition_code)
        if up_to != "":
            code += up_to + "\n"
        code += generate_while(
            last,
            self._scene_sequence.translate()
        )
        code += "\n"

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
        """
        >>> SetVariableStatement("number 1", NumberValue(10)).translate()
        'number_1 = 10\\n'
        """
        value_code = self._value.translate()
        up_to, last = partition_on_last_newline(value_code)
        code = up_to
        if up_to != "":
            code += "\n"
        code += "%s = %s\n" % (generate_safe_identifier(self._name),last)
        return code

    # Do not need to implement `get_live_variables` as do not have typed variables
    # and is not used for **user** variables.

class TypedSetVariableStatement(SetVariableStatement):
    """
    Adds type enforcement to SetVariableStatement with a type property.
    """

    type = property(lambda self: self._type)

    def __init__(self, type, name, value):
        """
        :type type: Type enum
        :type name: string
        :type value: <: TextExpression | NumberExpression | VideoExpression | VideoCollectionExpression
        """
        super(TypedSetVariableStatement, self).__init__(name, value)
        self._type = type

    def get_live_variables(self, type):
        """
        Base case. Need include variables dereferenced to know what is changed and
        hence what to make global. May need to change from use of "live" to a different
        term to describe this kind of analysis.
        """
        if type == self._type:
            return set([self._name])
        else:
            return set([])

class NumberSetVariableStatement(TypedSetVariableStatement):
    
    def __init__(self, name, value):
        super(NumberSetVariableStatement, self).__init__(Type.NUMBER, name, value)

class TextSetVariableStatement(TypedSetVariableStatement):
    
    def __init__(self, name, value):
        super(TextSetVariableStatement, self).__init__(Type.TEXT, name, value)

class VideoSetVariableStatement(TypedSetVariableStatement):
    
    def __init__(self, name, value):
        super(VideoSetVariableStatement, self).__init__(Type.VIDEO, name, value)

class VideoCollectionSetVariableStatement(TypedSetVariableStatement):
    
    def __init__(self, name, value):
        super(VideoCollectionSetVariableStatement, self).__init__(Type.VIDEO_COLLECTION, name, value)

class GetVariableExpression(LanguageComponent):

    type = property(lambda self: self._type)
    name = property(lambda self: self._name)

    def __init__(self, type, name):
        """
        :type type: Type enum
        :type name: string
        """
        self._name = name
        self._type = type

    def translate(self):
        return generate_safe_identifier(self._name)

    def get_live_variables(self, type):
        """Base case."""
        if type == self._type:
            return set([self._name])
        else:
            return set([])

class NumberGetVariableExpression(GetVariableExpression):
    
    def __init__(self, name):
        super(NumberGetVariableExpression, self).__init__(Type.NUMBER, name)

class TextGetVariableExpression(GetVariableExpression):
    
    def __init__(self, name):
        super(TextGetVariableExpression, self).__init__(Type.TEXT, name)

class VideoGetVariableExpression(GetVariableExpression):
    
    def __init__(self, name):
        super(VideoGetVariableExpression, self).__init__(Type.VIDEO, name)

class VideoCollectionGetVariableExpression(GetVariableExpression):
    
    def __init__(self, name):
        super(VideoCollectionGetVariableExpression, self).__init__(Type.VIDEO_COLLECTION, name)

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

class YoutubeVideoRandomComment(TextExpression):

    video = property(lambda self: self._video)

    def __init__(self,video):
        """
        :type video: <:VideoExpression
        """
        super(YoutubeVideoRandomComment, self).__init__([video])
        self._video = video

    def translate(self):
        return translate_instance_method_0(self._video, "random_comment")

class NumberExpression(Expression):
    """Base class for expressions that evaluate to type Number."""
    pass

class YoutubeVideoGetDuration(NumberExpression):

    video = property(lambda self: self._video)

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

    op1 = property(lambda self: self._lower_number_expr)
    op2 = property(lambda self: self._higher_number_expr)

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
        return "youtube.VideoCollection.from_web_urls(%s)" % self._web_urls

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

    query = property(lambda self: self._text_expr)

    def __init__(self,text_expr):
        """
        :type text_expr: <:TextExpression
        """
        super(YoutubeSearch,self).__init__([text_expr])
        self._text_expr = text_expr

    def translate(self):
        return translate_function_1("youtube.search", self._text_expr)

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

class YoutubeTopRated(VideoCollectionExpression):
    
    def translate(self):
        return translate_function_0("youtube.top_rated")

class YoutubeMostViewed(VideoCollectionExpression):
    
    def translate(self):
        return translate_function_0("youtube.most_viewed")

class YoutubeRecentlyFeatured(VideoCollectionExpression):

    def translate(self):
        return translate_function_0("youtube.recently_featured")

class YoutubeMostRecent(VideoCollectionExpression):
    
    def translate(self):
        return translate_function_0("youtube.most_recent")