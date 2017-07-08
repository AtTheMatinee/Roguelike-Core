'''
config.py
'''
import libtcodpy
'''
====================
Constants
====================
'''
SCREEN_WIDTH = 80 #100 #80
SCREEN_HEIGHT = 60 #75 #60
FRAMERATE_LIMIT	= 480

MAP_WIDTH = 60 #80 #50
MAP_HEIGHT = 50 #60 #50

UI_PRIMARY_COLOR = libtcodpy.grey

HORIZONTAL_PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
HORIZONTAL_PANEL_Y = SCREEN_HEIGHT - HORIZONTAL_PANEL_HEIGHT

VIRTICAL_PANEL_WIDTH = SCREEN_WIDTH - MAP_WIDTH
VIRTICAL_PANEL_X = SCREEN_WIDTH - VIRTICAL_PANEL_WIDTH

HORIZONTAL_PANEL_WIDTH = SCREEN_WIDTH - VIRTICAL_PANEL_WIDTH
H_PANEL_BAR_WIDTH = 20

VIRTICAL_PANEL_HEIGHT = SCREEN_HEIGHT
V_PANEL_BAR_WIDTH = VIRTICAL_PANEL_WIDTH - 4

MSG_X = 2
MSG_WIDTH = HORIZONTAL_PANEL_WIDTH - 4
MSG_HEIGHT = HORIZONTAL_PANEL_HEIGHT - 2

LOGO = [
'----  ----      --    --              -----     ',
'==  ==  ==    ====    ==========    =========   ',
'xx  xx  xx    xxxx    xx      xx    xxx      xx ',
'XX  XX  XX    XXXX    XX    XX      XX          ',
'XX      XX    XXXX    XXXXXXX       XXX         ',
'XX  XX  XX    XXXX    XX    X       XXXXXXX     ',
'XX      XX     XXX    XX    XX      XX          ',
' x      xx     xxx    xx    xx      xxx      xx ',
'       ==        =         ==       =========   ',
'      --         -        --          -----     ',
'    --                  --                      '
]

if __name__ == '__main__':
	for line in LOGO:
		print line