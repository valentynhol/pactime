from tkinter import *
import time

x0=0
y0=50
z=20

mode=0
n=0
a=[]

dot=[]
dot_num=0
dot_score=0
final_score=0
pac_x=1
pac_y=1
pac_d=180
pac_dd=180
gameStartTime=0
pauseStartTime=0
pausesDuration=0
maxGameDuration=0

def mapInit():
     globals()['dot']=[]
     globals()['a'] =   [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
                         [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1],
                         [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                         [1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1],
                         [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
                         [1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1],
                         [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
                         [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
                         [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
                         [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                         [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                         [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
     
     globals()['dot'] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
      #Стінки              
     for r,row in enumerate(a, start=0):
          for e,element in enumerate(row, start=0):
               if globals()['a'][r][e] == 1:
                    x=e*globals()['z']
                    y=r*globals()['z']
                    field.create_rectangle([x+globals()['x0'],y+globals()['y0']],[x+globals()['z']+globals()['x0'],y+globals()['z']+globals()['y0']],fill='purple')
      #Точки              
     for r,row in enumerate(a, start=0):
          for e,element in enumerate(row, start=0):
               if globals()['a'][r][e] == 2:
                    x=e*globals()['z']
                    y=r*globals()['z']             
                    globals()['dot'][r][e] = field.create_rectangle([x+0.35*globals()['z']+globals()['x0'],y+0.35*globals()['z']+globals()['y0']],[x+0.55*globals()['z']+globals()['x0'],y+0.55*globals()['z']+globals()['y0']],fill='white')
                    globals()['dot_num']+=1

     globals()['gameStartTime'] = time.time()
     globals()['pauseStartTime'] = 0
     globals()['pausesDuration'] = 0
     globals()['maxGameDuration'] = 150


def mainCycle():
     time.sleep(0.03)
          
     if 0==globals()['mode']:
          x = globals()['pac_x']
          y = globals()['pac_y']
          a = globals()['a']
          dd = globals()['pac_dd']
          pac_rot = False
          zero = x%1 == 0 and y%1 == 0
          
          #Пам'ять
          if dd==0 and a[int(y)][int(x-1)] != 1:
               pac_rot = True
          elif dd==90 and a[int(y+1)][int(x)] != 1:
               pac_rot = True
          elif dd==180 and a[int(y)][int(x+1)] != 1:
               pac_rot = True
          elif dd==270 and a[int(y-1)][int(x)] != 1:
               pac_rot = True

          #З'їдання точок
          if zero and 2 == a[int(y)][int(x)]:
               field.delete(globals()['dot'][int(y)][int(x)])
               globals()['dot'][int(y)][int(x)] = 0
               a[int(y)][int(x)] = 0
               globals()['dot_score']+=1
               globals()['final_score']+=10
               globals()['dot_num']-=1
               score.config(text='Рахунок: '+str(globals()['final_score']))
               
          #Пересування
          if zero and pac_rot:
               globals()['pac_d'] = globals()['pac_dd']
               pac_rot = False
          d = globals()['pac_d']
               
          if d==0:
               if not zero or a[int(y)][int(x-1)] != 1:
                    x=round(x-0.1, 1)
          elif d==90:
               if not zero or a[int(y+1)][int(x)] != 1:
                    y=round(y+0.1, 1)
          elif d==180:
               if not zero or a[int(y)][int(x+1)] != 1:
                    x=round(x+0.1, 1)
          elif d==270:
               if not zero or a[int(y-1)][int(x)] != 1:
                    y=round(y-0.1, 1)

          #Рот
          globals()['n']+=1
          n = globals()['n']
          nn = n%10
          if nn<5:
              a = -280-nn*17
          else:
              a = -280-(9-nn)*17
              
          field.move(pac,(x-globals()['pac_x'])*globals()['z'],(y-globals()['pac_y'])*globals()['z'])
          field.itemconfig(pac,start=globals()['pac_d']-a/2,extent=a)

          globals()['pac_x'] = x
          globals()['pac_y'] = y
          
          #Таймер
          gameTime = globals()['maxGameDuration'] - (time.time() - globals()['gameStartTime'] - globals()['pausesDuration'])    

          if gameTime < 0:
               loseGame()
          elif 0 == globals()['dot_num']:
               winGame()
          else:     
               time_m = gameTime//60
               time_s = gameTime%60
               if 0==globals()['mode']:
                    field.itemconfig(time_l, text='Час: '+str(int(time_m))+':'+str(round(time_s,1)))


            

def stopGame():
     globals()['pauseStartTime'] = time.time()
     showModal()
     globals()['menu_1'] = field.create_text(275, 0.5*h, text='Меню,', fill='white')
     globals()['menu_2'] = field.create_text(275, 0.5*h+20, text='Натисни "Esc", щоб продовжити', fill='white')
     globals()['menu_3'] = field.create_text(275, 0.5*h+30, text='Натисни "Enter", щоб почати заново', fill='white')
     globals()['mode']=2

def continueGame():
     field.delete(globals()['menu_1'])
     field.delete(globals()['menu_2'])
     field.delete(globals()['menu_3'])
     hideModal()
     globals()['mode']=0
     globals()['pausesDuration']+=time.time()-globals()['pauseStartTime']
     globals()['pauseStartTime'] = 0
    
def winGame():
     showModal()
     final_win=field.create_text(275, 0.5*h, text='Ти виграв!!!', fill='white')
     final_score_=field.create_text(275, 0.5*h+20, text='Твій рахунок: '+str(globals()['final_score']), fill='white')
     globals()['mode']=2

def loseGame():
     showModal()
     final=field.create_text(275, 0.5*h+20, text='Час вийшов!!!', fill='white')
     globals()['mode']=2

def restartGame():
     for r,row in enumerate(globals()['a'], start=0):
          for e,element in enumerate(row, start=0):
               if globals()['a'][r][e] == 2:
                    field.delete(globals()['dot'][int(r)][int(e)])
                    
     mapInit()
     field.delete(globals()['pac'])
     field.delete(globals()['menu_1'])
     field.delete(globals()['menu_2'])
     field.delete(globals()['menu_3'])
     globals()['pac']=field.create_arc([z+globals()['x0'],z+globals()['y0']],[z*2+globals()['x0'],z*2+globals()['y0']],fill='yellow',start=45,extent=-270)
     globals()['time_']=150
     globals()['dot_num']=0
     globals()['dot_score']=0
     globals()['final_score']=0
     globals()['pac_x']=1
     globals()['pac_y']=1
     globals()['pac_d']=180
     globals()['pac_dd']=180
     globals()['mode']=0
     hideModal()


def startPause():
     globals()['pauseStartTime'] = time.time()
     showModal()
     globals()['pause_1'] = field.create_text(275, 0.5*h, text='Пауза,', fill='white')
     globals()['pause_2'] = field.create_text(275, 0.5*h+20, text='Натисни "Pause", щоб продовжити', fill='white')
     globals()['mode']=1
     
def stopPause():
     field.delete(globals()['pause_1'])
     field.delete(globals()['pause_2'])
     hideModal()
     globals()['mode']=0
     globals()['pausesDuration']+=time.time()-globals()['pauseStartTime']
     globals()['pauseStartTime'] = 0
     
def showModal():
     globals()['modal_bg'] = field.create_rectangle([100,190],[450,400],fill='black',outline='purple')
     
def hideModal():
     field.delete(globals()['modal_bg'])
     
def turn(event):
     if 0==globals()['mode']:
          key=event.keysym
          if key=='Left':
               globals()['pac_dd'] = 0
          if key=='Down':
               globals()['pac_dd'] = 90
          if key=='Right':
               globals()['pac_dd'] = 180
          if key=='Up':
               globals()['pac_dd'] = 270

     

def modeChange(event):
     key=event.keysym
     if 0==globals()['mode']:
          if key=='Pause':
               startPause()
          if key=='Escape':
               stopGame()
     elif 1==globals()['mode']:
          if key=='Pause':
               stopPause()
     elif 2==globals()['mode']:
          if key=='Return':
               restartGame()
          if key=='Escape':
               continueGame()
     
pacman=Tk()
h=28*z+x0
w=31*z+y0+25
pacman.title('Pacman')
pacman.geometry(str(h)+'x'+str(w))


field=Canvas(pacman, width=h, height=w,bg='black')
field.place(x=-1,y=0)
mapInit()

score=Label(text='Рахунок: 0', fg='white', bg='black', font='ArialBold '+str(int(0.3*y0)))
score.place(x=x0+40,y=0.25*y0)
time_l=field.create_text(w-x0-200, 0.5*y0, fill='white', font='ArialBold '+str(int(0.3*y0)))
pauseLabel=Label(text='"Pause" -- Пауза', bg='black', fg='white', font='ArialBold '+str(int(0.2*y0)))
pauseLabel.place(x=0.25*y0,y=w-0.45*y0)
pauseLabel=Label(text='Меню -- "Esc"', bg='black', fg='white', font='ArialBold '+str(int(0.2*y0)))
pauseLabel.place(x=h-2*y0,y=w-0.45*y0)

pac=field.create_arc([z+globals()['x0'],z+globals()['y0']],[z*2+globals()['x0'],z*2+globals()['y0']],fill='yellow',start=45,extent=-270)

pacman.bind('<KeyPress>',turn)
pacman.bind('<KeyRelease>',modeChange)


while True:
    pacman.update_idletasks()
    pacman.update()
    mainCycle()
