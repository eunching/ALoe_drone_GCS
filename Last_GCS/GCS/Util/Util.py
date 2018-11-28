# -*- coding: utf-8 -*-

import os
import sys

########################################################
# WIDGET - SIZE
########################################################

# 윈도우 전체 사이즈(가로 * 세로)
WIN_WIDTH = 1600
WIN_HEIGHT = 1025

# 상단 사이즈 (세로)
LOGO_HEIGHT = 71

# 하단 전체 사이즈 (세로)
CONTENTS_HEIGHT = 954

# 하단 Control Widget 사이즈 (가로)
CONTROL_WIDTH = 430

# 하단 Control -> Button Module Widget 사이즈 (세로)
CONTROL_HEIGHT = 270

# 하단 Control -> Drone Module Widget 사이즈 (세로)
DRONE_HEIGHT = 190

# 하단 Control -> WayPoint Module Widget 사이즈 (세로)
WAYPOINT_HEIGHT = 394

# 하단 Map Widget 사이즈 (가로)
MAP_WIDTH = 1190

# 하단 Status Widget 사이즈 (가로)
STATUS_WIDTH = 250

# 하단 Status -> Flight Module Widget 사이즈 (세로)
FLIGHT_HEIGHT = 370

# 하단 Status -> GPS Module Widget 사이즈 (세로)
GPS_HEIGHT = 290

# 하단 Status -> Status text Module Widget 사이즈 (세로)
STATUS_TEXT_HEIGHT = 175

# 하단 Status -> Text Module Widget 사이즈 (세로)
TEXT_HEIGHT = 290

# 하단 로그 너비
TEXT_WIDTH = 396


########################################################
# WIDGET - COLOR
########################################################

TOP_WIDGET_COLOR = "background-color:rgb(89, 190, 186)"
CONTROL_WIDGET_COLOR = "background-color:rgb(89, 190, 186)"
MAP_WIDGET_COLOR = "background-color:rgb(85, 194, 110)"
STATUS_WIDGET_COLOR = "background-color:rgb(85, 94, 110)"
GPS_WIDGET_COLOR = "background-color:rgb(85, 94, 110)"
WAYPOINT_WIDGET_COLOR = "background-color:rgb(89, 190, 186)"
DRONE_WIDGET_COLOR = "background-color:rgb(89, 178, 186) "
BACKGROUNG_WIDGET_COLOR = "background-color:rgb(108,91,123) "


########################################################
# 파일 패스(os 버전별 패스 설정)
########################################################

if sys.platform.startswith('win'):
    PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\Util", "")
    HTML_PATH = PATH + "\\Html\\"
    IMG_PATH = PATH + "\\Images\\"
    HUD_HTML_PATH = PATH + "\\Html\\www\\"
else:
    PATH = os.path.dirname(os.path.abspath(__file__)).replace("/Util", "")
    HTML_PATH = PATH + "/Html/"
    IMG_PATH = PATH + "/Images/"
    HUD_HTML_PATH = PATH + "/Html/www/"

########################################################
# QLabel FONT - COLOR
########################################################
FONT_WHITE = "QLabel {color : white; border: none;}"
TEXT_WHITE = "QTextEdit{ background-color : white; border: none;}"
LABEL_BLACK = "QLabel {background-color : black; border: none;}"

# #######################################################
# 글씨 스타일
# #######################################################
FONT_STYLE = 'font-size : 12pt; font-family : HY그래픽M;'