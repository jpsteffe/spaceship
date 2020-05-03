import pygame, sys, random, math
from pygame.locals import *

pygame.init()
mainClock=pygame.time.Clock()

width=600
height=600
window=pygame.display.set_mode((width, height))
pygame.display.set_caption('Game_Test')

black=(0,0,0)
white=(255,255,255)
green=(0,255,0)
red=(255,0,0)

menu=pygame.image.load('mainmenu.png').convert()
pausebg=pygame.image.load('pausebg.png').convert()
font=pygame.font.SysFont(None,36)
font2=pygame.font.SysFont(None,20)


def pause():
    while True:

        window.blit(pausebg,(window.get_rect().centerx-100,window.get_rect().centery-150))
        
        resume=pygame.Rect(window.get_rect().centerx-50,window.get_rect().centery-40,96,23)
        quitgame=pygame.Rect(window.get_rect().centerx-60,window.get_rect().centery+5,125,25)
        quitprogram=pygame.Rect(window.get_rect().centerx-30,window.get_rect().centery+55,55,23)


        
        if resume.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,resume,2)
        if quitgame.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,quitgame,2)
        if quitprogram.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,quitprogram,2)
            
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                return False

            if event.type==MOUSEBUTTONUP:
                if resume.collidepoint(event.pos):
                    return False
                
                if quitgame.collidepoint(event.pos):
                    return True
                
                if quitprogram.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def mainmenu():
    while True:

        window.blit(menu,(0,0))
        
        play=pygame.Rect(window.get_rect().centerx-55,window.get_rect().centery-90,125,55)
        options=pygame.Rect(window.get_rect().centerx-75,window.get_rect().centery-20,167,55)
        highscores=pygame.Rect(window.get_rect().centerx-110,window.get_rect().centery+45,250,55)
        quitprogram=pygame.Rect(window.get_rect().centerx-45,window.get_rect().centery+105,105,45)


        
        if play.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,play,2)
        if options.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,options,2)
        if highscores.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,highscores,2)
        if quitprogram.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,red,quitprogram,2)
            
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                return False

            if event.type==MOUSEBUTTONUP:
                if play.collidepoint(event.pos):
                    game()
                
                if options.collidepoint(event.pos):
                    return True

                if highscores.collidepoint(event.pos):
                    return True
                
                if quitprogram.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

        

def game():
    
    score=0
    
    background=pygame.image.load('stars.gif').convert()
    background=pygame.transform.scale(background,(width,height))
    
    bombpic=pygame.image.load('bomb.jpg').convert()
    bombpic=pygame.transform.scale(bombpic,(20,20))
    bombpic.set_colorkey(white)
    
    playerpic=pygame.image.load('spaceship.png').convert()
    playerpic=pygame.transform.scale(playerpic,(30,30))
    playerpic.set_colorkey(white)
    
    rockpic=pygame.image.load('rock.png').convert()
    rockpic.set_colorkey(white)

    explosion=pygame.image.load('explosion.jpg')
    explosion=pygame.transform.scale(explosion,(60,60))
    explosion.set_colorkey(white)
    
    rockcounter=0
    newrock=40
    rocknumber=5
    player=pygame.Rect(window.get_rect().centerx,window.get_rect().centery,30,30)
    speed=6

    rocks=[]
    for i in range(rocknumber):
        rocksize = random.randint(20,40)
        rockx=random.randint(-rocksize,width)
        rocky=random.randint(-rocksize,0)
        rocks.append({'rect':pygame.Rect(rockx,rocky,rocksize,rocksize),'xspeed':math.cos(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'yspeed':math.sin(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'pic':pygame.transform.scale(rockpic,(rocksize,rocksize))})

    moveleft=False
    moveright=False
    moveup=False
    movedown=False
    bombs=[]

    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_LEFT or event.key==ord('a'):
                    moveright=False
                    moveleft=True
                if event.key==K_UP or event.key==ord('w'):
                    movedown=False
                    moveup=True
                if event.key==K_DOWN or event.key==ord('s'):
                    moveup=False
                    movedown=True
                if event.key==K_RIGHT or event.key==ord('d'):
                    moveright=True
                    moveleft=False
                if event.key==K_ESCAPE:
                    if pause():
                        return
            if event.type==KEYUP:
                if event.key==K_LEFT or event.key==ord('a'):
                    moveleft=False
                if event.key==K_RIGHT or event.key==ord('d'):
                    moveright=False
                if event.key==K_UP or event.key==ord('w'):
                    moveup=False
                if event.key==K_DOWN or event.key==ord('s'):
                    movedown=False
            if event.type==MOUSEBUTTONUP:
                if len(bombs)<5:
                    mousex,mousey=pygame.mouse.get_pos()
                    bombs.append({'rect':pygame.Rect(player.centerx,player.centery,15,15),'xspeed':-math.cos(math.atan2(player.centery-mousey,player.centerx-mousex)),'yspeed':-math.sin(math.atan2(player.centery-mousey,player.centerx-mousex)),'pic':bombpic})

        window.fill(black)
        window.blit(background,(0,0))
                
        if moveleft and player.left > speed:
            player.left -= speed
        if moveup and player.top > speed:
            player.top -= speed
        if movedown and player.bottom < height-speed:
            player.bottom += speed
        if moveright and player.right < width-speed:
            player.right += speed

        for i in bombs:
            if i['rect'].bottom > -25 and i['rect'].top < height+25 and i['rect'].left < width+25 and i['rect'].right > -25:
                i['rect'].centerx += i['xspeed']*speed
                i['rect'].centery += i['yspeed']*speed
                
            if  i['rect'].bottom <= -25 or i['rect'].top >= height+25 or i['rect'].left >= width+25 or i['rect'].right <= -25:
                bombs.remove(i)
                
            window.blit(i['pic'], i['rect'])   

        for i in rocks:
            if i['rect'].bottom > -50 and i['rect'].top < height+50 and i['rect'].left < width+50 and i['rect'].right > -50:
                i['rect'].centerx += i['xspeed']*speed
                i['rect'].centery += i['yspeed']*speed
            
            if player.colliderect(i['rect']):                                               #make a death menu
                while True:
                    text=font.render('Game Over',True,red,black)
                    scoretext=font.render('Your Score: '+str(score),True,red,black)
                    scorerect=scoretext.get_rect()
                    textRect=text.get_rect()
                    textRect.centerx=window.get_rect().centerx
                    textRect.centery=window.get_rect().centery
                    scorerect.top=textRect.bottom+4
                    scorerect.left=textRect.left
                    window.blit(scoretext,scorerect)
                    window.blit(text,textRect)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if (event.type==KEYUP and event.key==K_ESCAPE) or event.type==QUIT:
                            pygame.quit()
                            sys.exit()
                
            if  i['rect'].bottom <= -50 or i['rect'].top >= height+50 or i['rect'].left >= width+50 or i['rect'].right <= -50:
                score += 1
                rocksize = random.randint(20,40)
                rockx=random.randint(-rocksize,width)
                rocky=random.randint(-rocksize,0)
                rocks.append({'rect':pygame.Rect(rockx,rocky,rocksize,rocksize),'xspeed':math.cos(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'yspeed':math.sin(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'pic':pygame.transform.scale(rockpic,(rocksize,rocksize))})
                rocks.remove(i)
            window.blit(i['pic'], i['rect'])

            for bomb in bombs:
                if bomb['rect'].colliderect(i['rect']):
                    window.blit(explosion,i['rect'])
                    rocks.remove(i)
                    bombs.remove(bomb)
                    pygame.display.update()
                    pygame.time.delay(10)

                    
            
        window.blit(font2.render(str(score),True,red,black),(350,25))
        mousex,mousey=pygame.mouse.get_pos()
        playerpicrotated=pygame.transform.rotate(playerpic,-math.degrees(math.atan2(player.centery-mousey,player.centerx-mousex))+45)
        window.blit(playerpicrotated, player)

        if score % 51 == 1:                                         #make so it progresses smoothly
            rocksize = random.randint(20,40)
            rockx=random.randint(-rocksize,width)
            rocky=random.randint(-rocksize,0)
            rocks.append({'rect':pygame.Rect(rockx,rocky,rocksize,rocksize),'xspeed':math.cos(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'yspeed':math.sin(math.atan2(player.centery-rocky,math.fabs(rockx-player.centerx))),'pic':pygame.transform.scale(rockpic,(rocksize,rocksize))})
                    
        pygame.display.update()
        mainClock.tick(40)

mainmenu()
pygame.quit()
sys.exit()
