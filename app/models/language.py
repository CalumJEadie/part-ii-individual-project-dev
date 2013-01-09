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
"""

import app.api.youtube

class Act():
    """
    Highest level container. Analagous to a program.
    """

    def __init__(self, scenes):
        self._scenes = scenes

class Scene(object):
    """
    Analagous to a basic block.
    """
    
    def __init__(self, title, comment, duration):
        """
        :type title: <:TextExpression
        :type comment: <:TextExpression
        :type duration: <:NumberExpression
        """
        self._title = title
        self._comment = comment
        self._duration = duration

class VideoScene(Scene):

    def __init__(self, title, comment, duration, offset, source):
        """
        :type title: <:TextExpression
        :type comment: <:TextExpression
        :type duration: <:NumberExpression
        :type offset: <:NumberExpression
        :type source: <:VideoExpression
        """
        super(VideoScene, self).__init__(title, comment, duration)
        self._offset = offset
        self._source = source

class ImageScene(Scene):

    def __init__(self, title, comment, duration, offset, source):
        """
        :type title: <:TextExpression
        :type comment: <:TextExpression
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
        :type title: <:TextExpression
        :type comment: <:TextExpression
        :type duration: <:NumberExpression
        :type text: <:TextExpression
        """
        super(TextScene, self).__init__(title, comment, duration)
        self._text = text

class Expression(object):
    """Base class for expressions."""
    pass

class TextExpression(Expression):
    """Base class for expressions that evaluate to type Text."""
    pass

class TextValue(TextExpression):

    def __init__(self,text):
        """
        :type text: string
        """
        self._text = text

class YoutubeVideoGetTitleOperation(TextExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        self._video_expr = video_expr

class YoutubeVideoGetDescriptionOperation(TextExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        self._video_expr = video_expr

class NumberExpression(Expression):
    """Base class for expressions that evaluate to type Number."""
    pass

class YoutubeVideoGetDurationOperation(NumberExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        self._video_expr = video_expr

class NumberValue(NumberExpression):

    def __init__(self,number):
        """
        :type number: int
        """
        self._number = number

class GetRandomNumberBetweenIntervalOperation(NumberExpression):

    def __init__(self,lower_number_expr,higher_number_expr):
        """
        :type lower_number_expr: <:NumberExpression
        :type higher_number_expr: <:NumberExpression
        """
        self._lower_number_expr = lower_number_expr
        self._higher_number_expr = higher_number_expr

class SubtractOperation(NumberExpression):

    def __init__(self,number_expr_1,number_expr_2):
        """
        :type number_expr_1: <:NumberExpression
        :type number_expr_2: <:NumberExpression
        """
        self._number_expr_1 = number_expr_1
        self._number_expr_2 = number_expr_2

class VideoExpression():
    """Base class for expressions that evaluate to type Video."""
    pass

class VideoValue(VideoExpression):

    def __init__(self,video):
        """
        :type video: Video
        """
        self._video = video

class VideoCollectionExpression():
    """Base class for expressions that evaluate to type VideoCollection."""
    pass

class YoutubeVideoGetRelatedOperation(VideoCollectionExpression):

    def __init__(self,video_expr):
        """
        :type video_expr: <:VideoExpression
        """
        self._video_expr = video_expr

class YoutubeSearchOperation(VideoCollectionExpression):

    def __init__(self,text_expr):
        """
        :type text_expr: <:TextExpression
        """
        self._text_expr = text_expr

class YoutubeVideoCollectionRandomOperation(VideoCollectionExpression):

    def __init__(self,video_collection_expr):
        """
        :type video_collection_expr: <:VideoCollectionExpression
        """
        self._video_collection_expr = video_collection_expr