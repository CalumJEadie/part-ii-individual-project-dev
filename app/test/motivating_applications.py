"""
Motivating applications.

1.  Smart music player - plays related songs or switchs to different types of
    music depending on user interaction.
"""

from app.models.language import *




curr_video = VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0") # PSY - GANGNAM STYLE

smart_music_player = Act("",
    [

    TextScene(
        title = "Show video title",
        comment = "",
        duration = NumberValue(2),
        text = YoutubeVideoGetTitle(curr_video),
        pre_commands = CommandSequence([]),
        post_commands = CommandSequence([])
    ),

    TextScene(
        title = "Show video description",
        comment = "",
        duration = NumberValue(2),
        text = YoutubeVideoGetDescription(curr_video),
        pre_commands = CommandSequence([]),
        post_commands = CommandSequence([])
    ),

    VideoScene(
        title = "Play video",
        comment = "",
        duration = GetVariableExpression(Type.NUMBER, "clip_duration"),
        pre_commands = CommandSequence([
            SetVariableStatement("clip_duration", NumberValue(1)),
            SetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
            SetVariableStatement("clip_offset",
                GetRandomNumberBetweenInterval(
                    NumberValue(0),
                    Subtract(
                        GetVariableExpression(Type.NUMBER, "video_duration"),
                        GetVariableExpression(Type.NUMBER, "clip_duration")
                    )
                )
            )
        ]),
        post_commands = CommandSequence([]),
        offset = GetVariableExpression(Type.NUMBER, "clip_offset"),
        source = GetVariableExpression(Type.VIDEO, "curr_video")
    )

])