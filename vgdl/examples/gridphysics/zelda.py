'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''

zelda_level = """
wwwwwwwwwwwww
wA       w  w
w  w        w
w   w   w +ww
www w1  wwwww
w       w G w
w 1        ww
w     1    ww
wwwwwwwwwwwww
"""

        
zelda_game = """
BasicGame
  SpriteSet         
    goal  > Immovable color=GREEN
    key   > Immovable color=ORANGE
    sword > Flicker limit=5 singleton=True
    movable > 
      avatar  > ShootAvatar   stype=sword 
        nokey   >
        withkey > color=ORANGE
      monster > RandomNPC cooldown=4 
  LevelMapping
    G > goal
    + > key        
    A > nokey
    1 > monster            
  InteractionSet
    movable wall  > stepBack
    nokey goal    > stepBack
    goal withkey  > killSprite        
    monster sword > killSprite        
    avatar monster> killSprite
    key  avatar   > killSprite
    nokey key     > transformTo stype=withkey                
  TerminationSet
    SpriteCounter stype=goal   win=True
    SpriteCounter stype=avatar win=False
"""


if __name__ == "__main__":
    from vgdl.core import VGDLParser
    VGDLParser.playGame(zelda_game, zelda_level)    