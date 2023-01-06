from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, follow_for_ms, FollowGyroAngleErrorTooFast, Motor,follow_for_forever
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sound import Sound
import random 
import time
from time import sleep
from threading import Thread

#DISTANCE = 1500
DISTANCE = 2000
motorA = Motor(OUTPUT_A)
motorB = Motor(OUTPUT_D)
tank = MoveTank(OUTPUT_A, OUTPUT_D)
gyro = GyroSensor(INPUT_4)
sensor_cor = ColorSensor(INPUT_1)
spkr = Sound()
sensor_proximidade = UltrasonicSensor (INPUT_2)
arm_motor = Motor(OUTPUT_C)


class notWhite(Exception):
    def __init__(self):
        self.str = "Linha nao branca"

    def __str__(self):
        return self.str

class Board:
    #INICIALIZADO COM A CLASS BOARD CONTENDO AS OUTRAS EV3ROBOT, ZOMBIES, PECAS
   
    def __init__(self):
        self.robot = ev3Robot(0,0) 
        self.firstZombie = None
        self.secondZombie = None
        self.mota = Mota(5,5)
        self.pecaA = None
        self.pecaB =  None
        self.municao =  None
        self.matouFirst = False
        self.matouSecond = False
        self.temPeca = False
        self.ganhar = False

        self.board= [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]]

    #PRINT DO BOARD
    def mostrarBoard(self): 
        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][0]) + "   " ,  end = "")
            else:
                print(str(self.board[x][0]))

        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][1]) + "   " ,  end = "")
            else:
                print(str(self.board[x][1]))
        
        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][2]) + "   " ,  end = "")
            else:
                print(str(self.board[x][2]))

        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][3]) + "   " ,  end = "")
            else:
                print(str(self.board[x][3]))

        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][4]) + "   " ,  end = "")
            else:
                print(str(self.board[x][4]))

        for x in range(0,6):
            if (x < 5):
                print(str(self.board[x][5]) + "   " ,  end = "")
            else:
                print(str(self.board[x][5]))

    #ATUALIZA O BOARD NOS TURNO    
    def atualizarBoard(self):
        for x in range(0,6):
            for y in range(0,6):
                self.board[x][y] = 0

        spkr.speak("Next Turn")

        self.cheiroZombie()
        if (hasattr(self, "municao")):
            if self.municao != None:
                self.board[self.municao.getX()][self.municao.getY()] = self.municao
                self.apanhouMunicao()

        
        if (hasattr(self, "municao")):
            if self.municao != None:
                self.board[self.municao.getX()][self.municao.getY()] = self.municao

        
        
            if (hasattr(self, "firstZombie")):
                if (self.firstZombie != None):
                    if(self.firstZombie.getStunned() < 2 or self.firstZombie.getStunned() > 0):
                        self.board[self.firstZombie.getX()][self.firstZombie.getY()] = self.firstZombie
                        if(self.firstZombie.getStunned() > 0):
                            newValue = self.firstZombie.getStunned() - 1
                            self.firstZombie.setStunned(newValue)
                        else:
                            self.firstZombie = None
                    else:
                        varDoMestre = self.firstZombie.getVisible()
                        varDoMestre = varDoMestre - 1
                        self.firstZombie.setVisible(varDoMestre)


       
            if(hasattr(self, "secondZombie")):
                if(self.secondZombie != None): 
                    if(self.secondZombie.getVisible() < 2 or self.secondZombie.getStunned() > 0):
                        self.board[self.secondZombie.getX()][self.secondZombie.getY()] = self.secondZombie
                        if(self.secondZombie.getStunned() > 0):
                            newValue = self.secondZombie.getStunned() - 1
                            self.secondZombie.setStunned(newValue)
                        else:
                            self.secondZombie = None
                    else:
                        varDoMestre = self.secondZombie.getVisible()
                        varDoMestre = varDoMestre - 1
                        self.secondZombie.setVisible(varDoMestre)

        if(hasattr(self, "pecaA")):
            if (self.pecaA != None):
                self.board[self.pecaA.getX()][self.pecaA.getY()] = self.pecaA

        if (hasattr(self, "pecaB")):
            if (self.pecaB != None):
                self.board[self.pecaB.getX()][self.pecaB.getY()] = self.pecaB
        self.apanhouPeca()
        self.board[self.robot.getX()][self.robot.getY()] = self.robot
        self.largarOBjeto()
        


    def largarOBjeto(self):# funcao onde verifica se este tem peca ou bala e se tiver e tiver nas coordenada 5,5 entao ganha 
        if(self.robot.getPecas()==1): #verifica se o robo tem peca
            if(self.robot.getX()==5 and self.robot.getY()==5):
                self.robot.mexerBraco(-90)
                newValue = self.mota.getPecas() + 1
                self.mota.setPecas(newValue) # irá adicionar um peca a mota
                print("Mota:" + str(self.mota.getPecas()))
                newValueRobot = self.robot.getPecas() - 1
                self.temPeca = False
                self.robot.setPecas(newValueRobot) # irá remover a peca que estava no robo
                if(self.mota.getPecas() == 2):
                    self.ganhar = True


    #ROBOT APANHOU A MUNICAO
    def apanhouMunicao(self):
        if ((self.robot.getX() == self.municao.getX()) and (self.robot.getY() == self.municao.getY())):
            balas  =  self.robot.getBalas()
            balas = balas + 1 
            self.robot.setBalas(balas)
            self.municao = None

    def atualizarTurno(self, nturno):
        self.atualizarBoard()
        self.mostrarBoard()
        print("Turno:"+ str(nturno))
        print("Pecas:"+ str(self.robot.getPecas()))
        sleep(5)
    #ROBOT APANHOU PECA
    def apanhouPeca(self):
        randomValuePecaA=random.randrange(2)

        
        if(self.robot.getPecas() == 0):
            if(hasattr(self, "pecaA")):
                if(self.pecaA != None):
                    if((self.robot.getX() == self.pecaA.getX()) and (self.robot.getY() == self.pecaA.getY())):
                        pecasAtuais = self.robot.getPecas()
                        pecasAtuais += 1
                        self.robot.setPecas(pecasAtuais)
                        self.robot.apanharOBjeto()
                        self.temPeca = True
                        self.pecaA = None
            if(hasattr(self, "pecaA")):
                if (self.pecaA != None):
                    if(self.pecaA == None):
                        if(self.robot.robotColorDetected() == 'RED'):
                            if(randomValuePecaA==0):
                                pecasAtuais=self.robot.getPecas()
                                pecasAtuais+=1
                                self.robot.setPecas(pecasAtuais)
                                self.robot.apanharOBjeto()

            #-------------------------------------------------------------------
            if(hasattr(self,"municao")): # caso não tenha apanahdo a municao com o reconhecimento 
                if(self.municao==None):
                    if(self.robot.robotColorDetected()== 'BLUE'):
                        municaoAtual=self.robot.getBalas()
                        municaoAtual+=1
                        self.robot.setBalas(municaoAtual)

            #-------------------------------------------------------------
            if (hasattr(self, "pecaB")):
                if (self.pecaB != None):    
                    if ((self.robot.getX() == self.pecaB.getX()) and (self.robot.getY() == self.pecaB.getY())):
                        pecasAtuais = self.robot.getPecas()
                        pecasAtuais += 1
                        self.robot.setPecas(pecasAtuais)
                        self.robot.apanharOBjeto()
                        self.temPeca = True
                        self.pecaB = None
            #-------------------------------------------------------------
            if (hasattr(self, "pecaB")):
                if(self.pecaB ==None):
                    if(self.robot.robotColorDetected() == 'RED'):
                        if(randomValuePecaA==1):
                            pecasAtuais=self.robot.getPecas()
                            pecasAtuais+=1
                            self.robot.setPecas(pecasAtuais)
                            self.robot.apanharOBjeto()

    #FUNCOES POR TESTAR
    def achouBala(self, x, y):
        self.municao = pecas(x,y,True)
        self.board[x][y] = self.municao


    def detetarGanhar(self):
        if(self.mota.getPecas() == 2):
            self.ganhar = True
            spkr.speak('isso win ate parece facil')
            #spkr.play_file('win.wav')
            return True
            

    def detetarPerder(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if(self.robot.getX() == self.firstZombie.getX() and self.robot.getY() == self.firstZombie.getY() and self.firstZombie.getStunned() == 0): 
                    spkr.speak('Perdeste seu pato')
                    return True
            
        if (hasattr(self, "secondZombie")): 
            if(self.secondZombie != None):
                if (self.robot.getX() == self.secondZombie.getX() and self.robot.getY() == self.secondZombie.getY() and self.secondZombie.getStunned() == 0):
                    spkr.speak('Perdeste seu pato')
                    return True 
            
        return False

    def aoLadoFirst(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if((self.robot.getX() - 1) == self.firstZombie.getX() or (self.robot.getX() + 1) == self.firstZombie.getX() or (self.robot.getY() - 1) == self.firstZombie.getY() or 
                    (self.robot.getY() + 1) == self.firstZombie.getY()):
                    return True
                else:
                    return False
            else:
                    return False
    def aoLadoSec(self):
        if (hasattr(self, "secondZombie")):
            if(self.secondZombie != None):
                if((self.robot.getX() - 1) == self.secondZombie.getX() or (self.robot.getX() + 1) == self.secondZombie.getX() or 
                    (self.robot.getY() - 1) == self.secondZombie.getY() or (self.robot.getY() + 1) == self.secondZombie.getY()):
                    return True
                else:
                    return False
            else:
                    return False
    
    def aoLado2DireitaFirst(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if(((self.robot.getX() - 2) == self.firstZombie.getX()) or ((self.robot.getX() - 1) == self.firstZombie.getX() and (self.robot.getY() - 1) == self.firstZombie.getY()) or ((self.robot.getX() - 1) == self.firstZombie.getX() and (self.robot.getY() + 1) == self.firstZombie.getY())):
                    return True
                else:
                    return False
            else:
                return False
    def aoLado2DireitaSec(self):
        if (hasattr(self, "secondZombie")):
            if(self.secondZombie != None):
                if(((self.robot.getX() - 2) == self.secondZombie.getX()) or ((self.robot.getX() - 1) == self.secondZombie.getX() and (self.robot.getY() - 1) == self.secondZombie.getY()) or ((self.robot.getX() - 1) == self.secondZombie.getX() and (self.robot.getY() + 1) == self.secondZombie.getY())):
                    return True
                else:
                    return False
            else:
                return False
    
    def aoLado2EsquerdaFirst(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if(((self.robot.getX() + 2) == self.firstZombie.getX()) or ((self.robot.getX() + 1) == self.firstZombie.getX() and (self.robot.getY() - 1) == self.firstZombie.getY()) or ((self.robot.getX() + 1) == self.firstZombie.getX() and (self.robot.getY() + 1) == self.firstZombie.getY())):
                    return True
                else:
                    print("deu False")
                    return False
            else:
                print("deu False 2")
                return False
    def aoLado2EsquerdaSec(self):
        if (hasattr(self, "secondZombie")):
            if(self.secondZombie != None):
                if(((self.robot.getX() + 2) == self.secondZombie.getX()) or ((self.robot.getX() + 1) == self.secondZombie.getX() and (self.robot.getY() - 1) == self.secondZombie.getY()) or ((self.robot.getX() + 1) == self.secondZombie.getX() and (self.robot.getY() + 1) == self.secondZombie.getY())):
                    return True
                else:
                    print("deu False 1")
                    return False
            else:
                print("deu False 2")
                return False
    
    def aoLado2FrenteFirst(self):
        if (hasattr(self, "firstZombie")):
            print("print 1")
            if(self.firstZombie != None):
                print("print 2")
                print(str(self.firstZombie.getY()))
                print(str(self.firstZombie.getX()))
                print(str(self.robot.getX()))
                print(str(self.robot.getY()))
                if(((self.robot.getY() + 2) == self.firstZombie.getY()) or ((self.robot.getX() + 1) == self.firstZombie.getX() and (self.robot.getY() + 1) == self.firstZombie.getY()) or ((self.robot.getX() - 1) == self.firstZombie.getX() and (self.robot.getY() + 1) == self.firstZombie.getY())):
                    print("print 3")
                    return True
                else:
                    print("print 4")
                    return False
            else:
                return False
    def aoLado2FrenteSec(self):
        print("print secondzombie")
        if (hasattr(self, "secondZombie")):
            print("tem second hasattr")
            if(self.secondZombie != None):
                print("tem second zombie dif de noen")
                if(((self.robot.getY() + 2) == self.secondZombie.getY()) or ((self.robot.getX() + 1) == self.secondZombie.getX() and (self.robot.getY() + 1) == self.secondZombie.getY()) or ((self.robot.getX() - 1) == self.secondZombie.getX() and (self.robot.getY() + 1) == self.secondZombie.getY())):
                    print("print 5")
                    return True
                else:
                    print("print 6")
                    return False
            else:   
                return False
    
    def aoLado2AtrasFirst(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if(((self.robot.getY() - 2) == self.firstZombie.getY()) or ((self.robot.getX() + 1) == self.firstZombie.getX() and (self.robot.getY() - 1) == self.firstZombie.getY()) or ((self.robot.getX() - 1) == self.firstZombie.getX() and (self.robot.getY() - 1) == self.firstZombie.getY())):
                    return True
                else:
                    return False
            else:
                return False
    def aoLado2AtrasSec(self):
        if (hasattr(self, "secondZombie")):
            if(self.secondZombie != None):
                if(((self.robot.getY() - 2) == self.secondZombie.getY()) or ((self.robot.getX() + 1) == self.secondZombie.getX() and (self.robot.getY() - 1) == self.secondZombie.getY()) or ((self.robot.getX() - 1) == self.secondZombie.getX() and (self.robot.getY() - 1) == self.secondZombie.getY())):
                    return True
                else:
                    return False
            else:
                return False

    def detetouAlgo3(self):
        anguloGyto = gyro.angle
        xRobot = self.robot.getX()
        yRobot = self.robot.getY()
        flagDoMestre = False
        #0 0º
        #1 90º
        #2 -90º
        #3 180º
        possibilidade = [0,1,2,3]
        if(xRobot == 0 and yRobot == 0):
            possibilidade.remove(3)
            possibilidade.remove(1)
        elif(xRobot == 5 and yRobot == 5):
            possibilidade.remove(0)
            possibilidade.remove(2)
        elif(xRobot == 5 and yRobot == 0):
            possibilidade.remove(3)
            possibilidade.remove(2)
        elif(xRobot == 0 and yRobot == 5):
            possibilidade.remove(0)
            possibilidade.remove(1)
        elif(xRobot == 0):
            possibilidade.remove(1)
        elif(yRobot == 0):
            possibilidade.remove(3)
        elif(xRobot == 5):
            possibilidade.remove(2)
        elif(yRobot == 5):
            possibilidade.remove(0)
        
            
        for possible in possibilidade:
            if possible == 0:
                destinyAngle = -(anguloGyto - 0)   
                tank.turn_degrees(
                    speed=SpeedPercent(30),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                )
                anguloGyto = gyro.angle
                time.sleep(2)
                distanciaAlgo = self.robot.obterDistancia()
                print(anguloGyto)
                print(distanciaAlgo)
                if(distanciaAlgo >= 0 and distanciaAlgo < 10):
                    print("detetou diag")
                    encontrouAlgoX = self.robot.getX() - 1
                    encontrouAlgoY = self.robot.getY() + 1 
                    if (self.firstZombie == None and self.matouFirst == False):
                        if (hasattr(self, "firstZombie")):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie diagonal")
                            self.firstZombie.setVisible(1)
                    elif (self.secondZombie == None and self.matouSecond == False):
                            if(hasattr(self, "secondZombie")):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie diagonal")
                                self.secondZombie.setVisible(1)
                    time.sleep(2)
                if(distanciaAlgo > 10 and distanciaAlgo < 35):
                    print("detetou")
                    encontrouAlgoX = self.robot.getX() 
                    encontrouAlgoY = self.robot.getY() + 1 
                    if (self.firstZombie == None and self.matouFirst == False):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(2)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(2)
                        flagDoMestre = False
                if(distanciaAlgo > 40 and distanciaAlgo < 65 and self.robot.getY() < 4):
                    spkr.speak("2 houses")
                    encontrouAlgoX = self.robot.getX()
                    encontrouAlgoY = self.robot.getY() + 2 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(1)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(1)
                        flagDoMestre = False
                    
                if(self.robot.robotColorDetected()=="Red"):
                    encontrouAlgoX = self.robot.getX() 
                    encontrouAlgoY = self.robot.getY() + 1
                    if(self.pecaA==None):
                        if(hasattr(self,"pecaA")):
                            self.pecaA=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")
                    elif(self.pecaB==None):
                        if(hasattr(self,"pecaB")):    
                            self.pecaB=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")


                if(self.robot.robotColorDetected()=="Green"):
                    encontrouAlgoX = self.robot.getX() 
                    encontrouAlgoY = self.robot.getY() + 1
                    if(hasattr(self,"municao")):
                        if(self.municao==None):
                            self.municao=pecas(encontrouAlgoX,encontrouAlgoY,True,False)
                            spkr.speak("I found a ammunition")
            if possible == 1:
                destinyAngle = -(anguloGyto  -(90))   
                tank.turn_degrees(
                speed=SpeedPercent(30),
                target_angle=destinyAngle,
                brake=True,
                error_margin=1,
                sleep_time=0.02
                )
                anguloGyto = gyro.angle
                time.sleep(2)
                distanciaAlgo = self.robot.obterDistancia()
                print(anguloGyto)
                print(distanciaAlgo)
                if(distanciaAlgo >=0 and distanciaAlgo < 10):
                    print("detetou diag")
                    encontrouAlgoX = self.robot.getX() - 1
                    encontrouAlgoY = self.robot.getY() - 1 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if (hasattr(self, "firstZombie")):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie diagonal")
                            self.firstZombie.setVisible(1)
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(hasattr(self, "secondZombie")):
                            self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                            spkr.speak("Achei Zombie diagonal")
                            self.secondZombie.setVisible(1)
                    time.sleep(2)
                if(distanciaAlgo > 10 and distanciaAlgo < 35):
                    print("detetou")
                    encontrouAlgoX = self.robot.getX() -1
                    encontrouAlgoY = self.robot.getY() 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(2)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(2)
                        flagDoMestre = False
                if(distanciaAlgo > 40 and distanciaAlgo < 65 and self.robot.getX() > 1):
                    print("detetou 2")
                    spkr.speak("2 houses")
                    encontrouAlgoX = self.robot.getX() -2
                    encontrouAlgoY = self.robot.getY()  
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(1)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(1)
                        flagDoMestre = False

                if(self.robot.robotColorDetected()=="Red"):
                    encontrouAlgoX = self.robot.getX() -1
                    encontrouAlgoY = self.robot.getY()
                    if(self.pecaA==None):
                        if(hasattr(self,"pecaA")):
                            self.pecaA=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")
                    elif(self.pecaB==None):
                        if(hasattr(self,"pecaB")):
                            self.pecaB=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")


                if(self.robot.robotColorDetected()=="Green"):
                    encontrouAlgoX = self.robot.getX() -1
                    encontrouAlgoY = self.robot.getY()
                    if(hasattr(self,"municao")):
                        if(self.municao==None):
                            self.municao=pecas(encontrouAlgoX,encontrouAlgoY,True,False)
                            spkr.speak("I found a ammunition")
            if possible == 2:
                destinyAngle = -(anguloGyto  + 90)   
                tank.turn_degrees(
                    speed=SpeedPercent(30),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                )
                anguloGyto = gyro.angle
                time.sleep(2)
                distanciaAlgo = self.robot.obterDistancia()
                print(anguloGyto)
                print(distanciaAlgo)
                if(distanciaAlgo >= 0 and distanciaAlgo < 10):
                    print("detetou diag")
                    encontrouAlgoX = self.robot.getX() + 1
                    encontrouAlgoY = self.robot.getY() + 1 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if (hasattr(self, "firstZombie")):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie diagonal")
                            self.firstZombie.setVisible(1)
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(hasattr(self, "secondZombie")):
                            self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                            spkr.speak("Achei Zombie diagonal")
                            self.secondZombie.setVisible(1)
                    time.sleep(2)
                if(distanciaAlgo > 10 and distanciaAlgo < 35):
                    print("detetou")
                    encontrouAlgoX = self.robot.getX() + 1
                    encontrouAlgoY = self.robot.getY() 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(2)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(2)
                        flagDoMestre = False

                if(distanciaAlgo > 40 and distanciaAlgo < 65 and self.robot.getX() < 4):
                    print("detetou 2")
                    spkr.speak("2 houses")
                    encontrouAlgoX = self.robot.getX() + 2
                    encontrouAlgoY = self.robot.getY()  
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(1)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(1)
                        flagDoMestre = False
                    
                if(self.robot.robotColorDetected()=="Red"):
                    encontrouAlgoX = self.robot.getX() +1
                    encontrouAlgoY = self.robot.getY()
                    if(self.pecaA==None):
                        if(hasattr(self,"pecaA")):     
                            self.pecaA=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")
                    elif(self.pecaB==None):
                        if(hasattr(self,"pecaB")):
                            self.pecaB=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")


                if(self.robot.robotColorDetected()=="Green"):
                    encontrouAlgoX = self.robot.getX() +1
                    encontrouAlgoY = self.robot.getY()
                    if(hasattr(self,"municao")):
                        if(self.municao==None):
                            self.municao=pecas(encontrouAlgoX,encontrouAlgoY,True,False)
                            spkr.speak("I found a ammunition")
            if possible == 3:
                destinyAngle = -(anguloGyto  - 180)   
                tank.turn_degrees(
                    speed=SpeedPercent(30),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                )
                anguloGyto = gyro.angle
                time.sleep(2)
                distanciaAlgo = self.robot.obterDistancia()
                print(anguloGyto)
                print(distanciaAlgo)
                if(distanciaAlgo >= 0 and distanciaAlgo < 10):
                    print("detetou diag")
                    encontrouAlgoX = self.robot.getX() + 1
                    encontrouAlgoY = self.robot.getY() - 1 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if (hasattr(self, "firstZombie")):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie diagonal")
                            self.firstZombie.setVisible(1)
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(hasattr(self, "secondZombie")):
                            self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                            spkr.speak("Achei Zombie diagonal")
                            self.secondZombie.setVisible(1)
                    time.sleep(2)
                if(distanciaAlgo > 10 and distanciaAlgo < 35):
                    print("detetou")
                    encontrouAlgoX = self.robot.getX()
                    encontrouAlgoY = self.robot.getY() -1 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(2)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(2)
                        flagDoMestre = False
                if(distanciaAlgo > 40 and distanciaAlgo < 65 and self.robot.getY() > 1):
                    print("detetou 2")
                    spkr.speak("2 houses")
                    encontrouAlgoX = self.robot.getX()
                    encontrouAlgoY = self.robot.getY() -2 
                    if (self.firstZombie == None and self.matouFirst == False and hasattr(self, "firstZombie")):
                        if(self.secondZombie != None):
                            if(self.secondZombie.getX() == encontrouAlgoX and self.secondZombie.getY() == encontrouAlgoY and self.secondZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if (hasattr(self, "firstZombie") and flagDoMestre == False):
                            self.firstZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "A")
                            spkr.speak("Achei Zombie")
                            self.firstZombie.setVisible(1)
                        flagDoMestre = False
                    elif (self.secondZombie == None and self.matouSecond == False and hasattr(self, "secondZombie")):
                        if(self.firstZombie != None):
                            if(self.firstZombie.getX() == encontrouAlgoX and self.firstZombie.getY() == encontrouAlgoY and self.firstZombie.getStunned() > 0):
                                print("zombie na mesma casa")
                                flagDoMestre = True
                        if(hasattr(self, "secondZombie") and flagDoMestre == False):
                                self.secondZombie = Zombie(encontrouAlgoX,encontrouAlgoY, "B")
                                spkr.speak("Achei Zombie")
                                self.secondZombie.setVisible(1)
                        flagDoMestre = False

                if(self.robot.robotColorDetected()=="Red"):
                    encontrouAlgoX = self.robot.getX() 
                    encontrouAlgoY = self.robot.getY()-1
                    if(self.pecaA==None):
                        if(hasattr(self,"pecaA")):  
                            self.pecaA=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece") 
                    elif(self.pecaB==None):
                        if(hasattr(self,"pecaB")):
                            self.pecaB=pecas(encontrouAlgoX,encontrouAlgoY,False,True)
                            spkr.speak("I found a piece")


                if(self.robot.robotColorDetected()=="Green"):
                    encontrouAlgoX = self.robot.getX() 
                    encontrouAlgoY = self.robot.getY()-1
                    if(hasattr(self,"municao")):
                        if(self.municao==None):
                            self.municao=pecas(encontrouAlgoX,encontrouAlgoY,True,False)
                            spkr.speak("I found a ammunition")
                    

            self.zombieApanhouPeca()
            time.sleep(1)

    def zombieApanhouPeca(self):
        if (hasattr(self, "pecaA")):
            if (self.pecaA != None):
                if (hasattr(self, "firstZombie")):
                    if(self.firstZombie != None):
                        if ((self.firstZombie.getX() == self.pecaA.getX()) and (self.firstZombie.getY() == self.pecaA.getY())):
                            pecasAtuais = self.firstZombie.getPecas()
                            self.firstZombie.setPecas(pecasAtuais + 1)
                            self.pecaA = None

            if (hasattr(self, "pecaA")):
                if (self.pecaA != None):
                    if (hasattr(self, "secondZombie")):
                        if(self.secondZombie != None):
                            if ((self.secondZombie.getX() == self.pecaA.getX()) and (self.secondZombie.getY() == self.pecaA.getY())):
                                pecasAtuais = self.secondZombie.getPecas()
                                self.secondZombie.setPecas(pecasAtuais + 1)
                                self.pecaA = None

            if (hasattr(self, "pecaB")):
                if (self.pecaB != None):
                    if (hasattr(self, "firstZombie")):
                        if(self.firstZombie != None):
                            if ((self.firstZombie.getX() == self.pecaB.getX()) and (self.firstZombie.getY() == self.pecaB.getY())):
                                pecasAtuais = self.firstZombie.getPecas()
                                self.firstZombie.setPecas(pecasAtuais + 1)
                                self.pecaB = None

            if (hasattr(self, "pecaB")):
                if (self.pecaB != None):
                    if (hasattr(self, "secondZombie")):
                        if(self.secondZombie != None):
                            if ((self.secondZombie.getX() == self.pecaB.getX()) and (self.secondZombie.getY() == self.pecaB.getY())):
                                pecasAtuais = self.secondZombie.getPecas()
                                self.secondZombie.setPecas(pecasAtuais + 1)
                                self.pecaB = None
    
    def cheiroZombie(self):
        if (hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                firstX = self.firstZombie.getX()
                firstY = self.firstZombie.getY()
                posicaoX1 = firstX + 1
                posicaoX2 = firstX - 1
                posicaoY1 = firstY + 1
                posicaoY2 = firstY - 1

                posicaoX3 = firstX + 2
                posicaoX4 = firstX - 2
                posicaoY3 = firstY + 2
                posicaoY4 = firstY - 2


                if (firstY != 5):
                    self.board[firstX][posicaoY1] = 1
                if (firstY != 5 and firstX != 5):
                    self.board[posicaoX1][posicaoY1] = 2
                if (firstY != 0):
                    self.board[firstX][posicaoY2] = 1
                if (firstY != 0 and firstX != 5):
                    self.board[posicaoX1][posicaoY2] = 2
                if (firstX != 5):
                    self.board[posicaoX1][firstY] = 1
                if (firstY != 0 and firstX != 0):
                    self.board[posicaoX2][posicaoY2] = 2
                if (firstX != 0):
                    self.board[posicaoX2][firstY] = 1
                if (firstY != 5 and firstX != 0):
                    self.board[posicaoX2][posicaoY1] = 2

                if (firstY < 4):
                    self.board[firstX][posicaoY3] = 2
                if (firstY > 1):
                    self.board[firstX][posicaoY4] = 2
                if (firstX < 4):
                    self.board[posicaoX3][firstY] = 2
                if (firstX > 1):
                    self.board[posicaoX4][firstY] = 2


                


        if (hasattr(self, "secondZombie")):
            if(self.secondZombie != None):
                firstX = self.secondZombie.getX()
                firstY = self.secondZombie.getY()
                posicaoX1 = firstX + 1
                posicaoX2 = firstX - 1
                posicaoY1 = firstY + 1
                posicaoY2 = firstY - 1

                posicaoX3 = firstX + 2
                posicaoX4 = firstX - 2
                posicaoY3 = firstY + 2
                posicaoY4 = firstY - 2

                if (firstY != 5):
                    self.board[firstX][posicaoY1] = 1
                if (firstY != 5 and firstX != 5):
                    self.board[posicaoX1][posicaoY1] = 2
                if (firstY != 0):
                    self.board[firstX][posicaoY2] = 1
                if (firstY != 0 and firstX != 5):
                    self.board[posicaoX1][posicaoY2] = 2
                if (firstX != 5):
                    self.board[posicaoX1][firstY] = 1
                if (firstY != 0 and firstX != 0):
                    self.board[posicaoX2][posicaoY2] = 2
                if (firstX != 0):
                    self.board[posicaoX2][firstY] = 1
                if (firstY != 5 and firstX != 0):
                    self.board[posicaoX2][posicaoY1] = 2

                if (firstY < 4):
                    self.board[firstX][posicaoY3] = 2
                if (firstY > 1):
                    self.board[firstX][posicaoY4] = 2
                if (firstX < 4):
                    self.board[posicaoX3][firstY] = 2
                if (firstX > 1):
                    self.board[posicaoX4][firstY] = 2

    def efetuarAtaque(self):
        if(hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if ((self.robot.getX() - 1 == self.firstZombie.getX() and self.robot.getY() == self.firstZombie.getY()) 
                or (self.robot.getX() + 1 == self.firstZombie.getX() and self.robot.getY() == self.firstZombie.getY()) 
                or (self.robot.getY() - 1 == self.firstZombie.getY() and self.robot.getX() == self.firstZombie.getX()) 
                or (self.robot.getY() + 1 == self.firstZombie.getY() and self.robot.getX() == self.firstZombie.getX())):
                    spkr.speak("Ataquei")
                    self.firstZombie.setStunned(1)
                    if (self.firstZombie.getPecas() == 1):
                        self.firstZombie.setPecas(0)
                        self.robot.setPecas(1)
                        self.robot.mexerBraco(90)
                        self.temPeca = True
        if(hasattr(self,"secondZombie")):
            if(self.secondZombie != None):
                if ((self.robot.getX() - 1 == self.secondZombie.getX() and self.robot.getY() == self.secondZombie.getY()) 
                or (self.robot.getX() + 1 == self.secondZombie.getX() and self.robot.getY() == self.secondZombie.getY()) 
                or (self.robot.getY() - 1 == self.secondZombie.getY() and self.robot.getX() == self.secondZombie.getX()) 
                or (self.robot.getY() + 1 == self.secondZombie.getY() and self.robot.getX() == self.secondZombie.getX())):
                    spkr.speak("Ataquei") # som para efetuar ataque com a mao
                    self.secondZombie.setStunned(1)
                    if (self.secondZombie.getPecas() == 1):
                            self.secondZombie.setPecas(0)
                            self.robot.setPecas(1)
                            self.robot.mexerBraco(90)
                            self.temPeca = True
            
    def efetuarPistola(self):
        if(hasattr(self, "firstZombie")):
            if(self.firstZombie != None):
                if ((self.robot.getX() - 1 == self.firstZombie.getX() and self.robot.getY() == self.firstZombie.getY()) 
                or (self.robot.getX() + 1 == self.firstZombie.getX() and self.robot.getY() == self.firstZombie.getY()) 
                or (self.robot.getY() - 1 == self.firstZombie.getY() and self.robot.getX() == self.firstZombie.getX()) 
                or (self.robot.getY() + 1 == self.firstZombie.getY() and self.robot.getX() == self.firstZombie.getX())):
                    if (self.robot.getBalas() == 1):
                        spkr.speak("Bang") # som para efetuar ataque com a pistola
                        if (self.firstZombie.getPecas() == 1):
                            newPecas = self.robot.getPecas() + 1
                            self.robot.setPecas(newPecas)
                            self.robot.mexerBraco(90)
                            self.temPeca = True
                        self.matouFirst = True
                        self.firstZombie = None
                        self.robot.setBalas(0)
        if(hasattr(self,"secondZombie")):
            if(self.secondZombie != None):
                if ((self.robot.getX() - 1 == self.secondZombie.getX() and self.robot.getY() == self.secondZombie.getY()) 
                or (self.robot.getX() + 1 == self.secondZombie.getX() and self.robot.getY() == self.secondZombie.getY()) 
                or (self.robot.getY() - 1 == self.secondZombie.getY() and self.robot.getX() == self.secondZombie.getX()) 
                or (self.robot.getY() + 1 == self.secondZombie.getY() and self.robot.getX() == self.secondZombie.getX())):
                    if (self.robot.getBalas() == 1):    
                        spkr.speak("Bang") # som para efetuar ataque com a pistola
                        if (self.secondZombie.getPecas() == 1):
                            newPecas = self.robot.getPecas() + 1
                            self.robot.setPecas(newPecas)
                            self.robot.mexerBraco(90)
                            self.temPeca = True
                        self.matouSecond = True
                        self.secondZombie = None
                        self.robot.setBalas(0)




class ev3Robot:
    def __init__ (self,x,y):
        self.x = x
        self.y = y
        self.balas = 0
        self.pecas = 0
        self.zombieDetetado = 0
        self.pecaDetetada = 0


    def __str__(self):
        return 'R'
    
    def getX(self):
        return self.x
    
    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y
    
    def getY(self):
        return self.y
    
    def getBalas(self):
        return self.balas

    def setBalas(self,balas):
        self.balas = balas

    def getPecas(self):
        return self.pecas

    def setPecas(self, pecas):
        self.pecas = pecas

    def calibrarGyro(self) :
        tank.gyro.calibrate()

    def tankGyro(self):
        tank.gyro = GyroSensor(INPUT_4)
    
    def robotColorDetected(self):
        sensor_cor.MODE_COL_COLOR
        return sensor_cor.color_name


    #MOSTAR POSICAO DO ROBOT NO MOMENTO
    def mostrarPosicao(self):
        return "X:" + str(self.x) + "\n" + "Y:" + str(self.y)
    


    def andarFrente(self):
        newY = self.y + 1
        if (self.verificaPosicao(self.x, newY)):
            self.y = self.y + 1  
            anguloGyto = gyro.angle
            destinyAngle = -(anguloGyto - 0)
            tank.turn_degrees(
                    speed=SpeedPercent(40),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                )       
            try:
                tank.follow_gyro_angle(
                        kp=14.3, ki=0.01, kd=3.2,
                        speed=SpeedPercent(-40),
                        target_angle=0,
                        sleep_time=0.1,
                        follow_for=follow_for_ms,
                        ms=DISTANCE
                )              
                tank._run_command
            except FollowGyroAngleErrorTooFast:
                tank.stop()
        else: 
            print("Nao e possivel")

    
    def andarAtras(self):
        newY = self.y - 1
        if (self.verificaPosicao(self.x, newY)):
            self.y = self.y - 1
            anguloGyto = gyro.angle
            destinyAngle = -(anguloGyto  - 180)
            tank.turn_degrees(
                    speed=SpeedPercent(40),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                    )  

            try:
                tank.follow_gyro_angle(
                    kp=14.3, ki=0.01, kd=3.2,
                    speed=SpeedPercent(-40),
                    target_angle=180,
                    follow_for=follow_for_ms,
                    ms=DISTANCE        
                )
            except FollowGyroAngleErrorTooFast:
                tank.stop()
                raise     
        else: 
            print("Nao e possivel")

    def andarEsquerda(self):
        #VERIFICA
        newX = self.x + 1
        if (self.verificaPosicao(newX, self.y)):
        
            self.x = self.x + 1
            anguloGyto = gyro.angle
            destinyAngle = -(anguloGyto - (-90))
            tank.turn_degrees(
                    speed=SpeedPercent(40),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                ) 

            try:
                tank.follow_gyro_angle(
                    kp=14.3, ki=0.01, kd=3.2,
                    speed=SpeedPercent(-40),
                    target_angle=-90,
                    follow_for=follow_for_ms,
                    ms=DISTANCE + 200      
                )
            except FollowGyroAngleErrorTooFast:
                raise 


        else:
            print("Nao e possivel")

    def andarDireita(self):
        newX = self.x - 1
        if(self.verificaPosicao(newX, self.y)):
            self.x = self.x - 1

            anguloGyto = gyro.angle
            destinyAngle = -(anguloGyto - (90))
            tank.turn_degrees(
                    speed=SpeedPercent(40),
                    target_angle=destinyAngle,
                    brake=True,
                    error_margin=1,
                    sleep_time=0.02
                ) 
        

        try:
            tank.follow_gyro_angle(
                kp=14.3, ki=0.01, kd=3.2,
                speed=SpeedPercent(-40),
                target_angle=90,
                follow_for=follow_for_ms,
                ms=DISTANCE        
            )
        except FollowGyroAngleErrorTooFast:
                raise   

        else:
            print("Nao e possivel")

    def randomMovimento(self):
        xRobot = self.getX()
        yRobot = self.getY()
        possibilidade = [0,1,2,3]

        if(xRobot == 0):
            possibilidade.remove(3)
        if(yRobot == 0):
            possibilidade.remove(1)
        if(xRobot == 5):
            possibilidade.remove(2)
        if(yRobot == 5):
            possibilidade.remove(0)

        random.shuffle(possibilidade)
        generatedNumber = possibilidade.pop()

        if(generatedNumber == 0):
            self.andarFrente()
               
        if(generatedNumber == 1):
            self.andarAtras()
               
        if(generatedNumber == 2):
            self.andarEsquerda()
    
        if(generatedNumber == 3):
            self.andarDireita()

    def verificaPosicao(self, x , y):
        if (x >= 0 and x <= 5 and y <= 5 and y >= 0):
            return True
        else: 
            return False
    
    def apanharOBjeto(self): ## apanhar objeto quando foi apanhado no registo 
            self.mexerBraco(90)

    def obterDistancia(self):
        sensor_proximidade.MODE_US_SI_CM
        return sensor_proximidade.distance_centimeters
    
    def getGyroPos(self):
        return gyro.angle
    
    def resetGyroAngle(self,valor):
        gyro.reset_angle(valor)
    
    def getAnguloBraco(self):
        return arm_motor.angle()
    
    def mexerBraco(self, valor):
        arm_motor.on_for_degrees(SpeedPercent(30),valor,True,True)
    
    def inverterPolaridade(self):
        motorA.POLARITY_INVERSED
        motorB.POLARITY_INVERSED

class Mota:
    def __init__ (self,x,y):
        self.x = x
        self.y = y
        self.pecas = 0
    def __str__(self):
        return 'M'

    def getX(self):
        return self.x
    
    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y
    
    def getY(self):
        return self.y

    def getPecas(self):
        return self.pecas

    def setPecas(self, pecas):
        self.pecas = pecas

    #MOSTAR POSICAO DA MOTA NO MOMENTO
    def mostrarPosicao(self):
        return "X:" + str(self.x) + "\n" + "Y:" + str(self.y)


class Zombie(ev3Robot):
    def __init__(self, x, y,name):
        super().__init__(x,y)
        self.pecas = 0
        self.name = name
        self.isStunned = 0
        self.stunnedfor = 0
        self.isVisible = 0
        self.maxVisible = 1
        self.alarme = False

    def __str__(self):
        return self.name

    def setStunned(self, isStunned):
        self.isStunned = isStunned

    def setStunnedfor(self, stunnedFor):
        self.stunnedfor = stunnedFor

    def getStunned(self):
        return self.isStunned

    def getStunnedfor(self):
        return self.stunnedfor

    def getPecas(self):
        return self.pecas

    def setPecas(self, pecas):
        self.pecas = pecas

    def andarFrente(self):
        newY = self.y + 1
        if (self.verificaPosicao(self.x, newY)):
            self.y = newY
            print(str(newY))
        else: 
            print("Não é possivel")
            
    def andarAtras(self):
        newY = self.y - 1
        if (self.verificaPosicao(self.x, newY)):
            self.y = newY
            print(str(newY))
        else: 
            print("Não é possivel")

    def andarEsquerda(self):
        #VERIFICA
        newX = self.x + 1
        if (self.verificaPosicao(newX, self.y)):
            self.x = newX
            print(str(newX))
        else:
            print("Não é possivel")

    def andarDireita(self):
        newX = self.x - 1
        if(self.verificaPosicao(newX, self.y)):
            self.x = newX
            print(str(newX))
        else:
            print("Não é possivel")
    
    def setVisible(self, value):
        self.isVisible = value

    def getVisible(self):
        return self.isVisible

    def  getmaxVisible(self):
        return self.maxVisible 
    


class pecas:
    def __init__(self,x,y,isMunicao, isPeca):
        self.x = x
        self.y = y
        self.isMunicao = isMunicao
        self.isPeca = isPeca
    
    def __str__(self):
        if(self.isMunicao):
            return "M"
        else:
            return "P"

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y
    
    def getisPeca(self):
        return self.isPeca

    def setisPeca(self, isPeca):
        self.isPeca = isPeca

    def getisMunicao(self):
        return self.isMunicao

    def setisMunicao(self, isMunicao):
        self.isMunicaou = isMunicao
        
    def __init__(self,x,y,isMunicao, isPeca):
        self.x = x
        self.y = y
        self.isMunicao = isMunicao
        self.isPeca = isPeca
    
    def __str__(self):
        if(self.isMunicao):
            return "M"
        else:
            return "P"

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y
    
    def getisPeca(self):
        return self.isPeca

    def setisPeca(self, isPeca):
        self.isPeca = isPeca

    def getisMunicao(self):
        return self.isMunicao

    def setisMunicao(self, isMunicao):
        self.isMunicaou = isMunicao
