#!/usr/bin/env python3

from time import sleep

#from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
#from ev3dev2.sensor import INPUT_1
#from ev3dev2.led import Leds
import test
import random

board = test.Board()
robotController = board.robot 
zombieAController = board.firstZombie
zombieBController = board.secondZombie
pecaAController = board.pecaA
pecaBController = board.pecaB
municaoController = board.municao
arrayComOsLugares=[]
arrayComTodasAsPosicoes=[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),
(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),
(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]

robotController.tankGyro()
robotController.calibrarGyro()
robotController.inverterPolaridade()

# Write your program here.

def sigarCaminho(nturno,robotX, robotY, destinyX, destinyY):
    while(robotY < destinyY):
        board.detetouAlgo3()
        if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
            if(robotController.getBalas() > 0):
                board.efetuarPistola()
            else:
                board.efetuarAtaque()
        if(board.aoLado2FrenteFirst() == False and board.aoLado2FrenteSec() == False):
            robotController.andarFrente()
            robotY = robotY + 1
        nturno += 1
        board.atualizarTurno(nturno)
        print(str(robotY))
        if(robotY == destinyY and robotX == destinyX): 
            if(robotController.getX() < 5 and robotController.getY() < 5):
                board.detetouAlgo3()
                if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
                if(board.aoLado2AtrasFirst() == False and board.aoLado2AtrasSec() == False):
                    robotController.andarAtras()
                nturno += 1
                board.atualizarTurno(nturno)
    while(robotX < destinyX):
        board.detetouAlgo3()
        if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
            if(robotController.getBalas() > 0):
                board.efetuarPistola()
            else:
                board.efetuarAtaque()
        if(board.aoLado2EsquerdaFirst() == False and board.aoLado2EsquerdaSec() == False):
            robotController.andarEsquerda()
            robotX = robotX + 1
        nturno += 1
        board.atualizarTurno(nturno)
        print(str(robotX))
        if(robotY == destinyY and robotX == destinyX):
            if(robotController.getX() < 5 and robotController.getY() < 5):
                board.detetouAlgo3()
                if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
                if(board.aoLado2DireitaFirst() == False and board.aoLado2DireitaSec() == False):
                    robotController.andarDireita()
                nturno += 1
                board.atualizarTurno(nturno)
    while (robotX > destinyX):
        board.detetouAlgo3()
        if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
            if(robotController.getBalas() > 0):
                board.efetuarPistola()
            else:
                board.efetuarAtaque()
        if(board.aoLado2DireitaFirst() == False and board.aoLado2DireitaSec() == False):
            robotController.andarDireita()
            robotX = robotX - 1
        nturno += 1
        board.atualizarTurno(nturno)  
        print(str(robotX))
        if(robotY == destinyY and robotX == destinyX): 
            if(robotController.getX() < 5 and robotController.getY() < 5):
                board.detetouAlgo3()
                if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
                    board.detetouAlgo3()
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
                if(board.aoLado2EsquerdaFirst() == False and board.aoLado2EsquerdaSec() == False):
                    robotController.andarEsquerda() 
                nturno += 1
                board.atualizarTurno(nturno)
    while(robotY > destinyY):
        board.detetouAlgo3()
        if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
            if(robotController.getBalas() > 0):
                board.efetuarPistola()
            else:
                board.efetuarAtaque()
        if(board.aoLado2AtrasFirst() == False and board.aoLado2AtrasSec() == False):
            robotController.andarAtras()
            robotY = robotY - 1
        nturno += 1
        board.atualizarTurno(nturno) 
        print(str(robotY))
        if(robotY == destinyY and robotX == destinyX):
            if(robotController.getX() < 5 and robotController.getY() < 5):
                board.detetouAlgo3()
                if(board.aoLadoFirst() == True or board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
                if(board.aoLado2FrenteFirst() == False and board.aoLado2FrenteSec() == False):
                    robotController.andarFrente()
                nturno += 1
                board.atualizarTurno(nturno)


def menuPrincipal():
    print("Introduza a opcao")
    print("1 - Menu Robot")
    print("2 - Menu ZombieA")
    print("3 - Menu ZombieB")
    print("4 - Turno")
    print("5 - Jogar Random")
    print("6 - Jogar Inteligente")
    print("0 - Sair")
    

def menuRobot():
    optionRobot = True
    while optionRobot:
        print("Introduza a opcao")
        print("1 - Balas")
        print("2 - Pecas")
        print("3 - Posicao")
        print("0 - Sair")
        optionRobot = input()
        if optionRobot == "1":
            print("Balas: " + str(robotController.getBalas()))

        if optionRobot == "2":
            print("Pecas:" + str(robotController.getPecas()))

        if optionRobot == "3":
            print(robotController.mostrarPosicao())

        if optionRobot == "0":
            optionRobot = False

def menuZombieA():
    optionZombiaA = True
    while optionZombiaA:
        print("Introduza a opcao")
        print("1 - Pecas")
        print("2 - Posicao")
        print("0 - Sair")
        optionZombiaA = input()
        if optionZombiaA == "1":
            print("Pecas:" + str(zombieAController.getPecas()))

        if optionZombiaA == "2":
            print(zombieAController.mostrarPosicao())

        if optionZombiaA == "0":
            optionZombiaA = False


def menuZombieB():
    optionZombiaB = True
    while optionZombiaB:
        print("Introduza a opcao")
        print("1 - PecasB")
        print("2 - PosicaoB")
        print("0 - Sair")
        optionZombiaB = input()
        if optionZombiaB == "1":
            print("Pecas:" + str(zombieBController.getPecas()))

        if optionZombiaB == "2":
            print(zombieBController.mostrarPosicao())

        if optionZombiaB == "0":
            optionZombiaB = False

def Menuturno():
    optTurno = True
    while optTurno:
        print("Introduza a opcao")
        print("1 - Andar frente")
        print("2 - Andar Atras")
        print("3 - L a Esquerda")
        print("4 - L a direita")
        print("5 - L esquerda atras")
        print("6 - L direita atras")
        print("7 - Andar esquerda")
        print("8 - Andar direita ")
        print("9 - Detetar Cor")
        print("10 - Tocou Braco")
        print("11 - Obter distancia objeto")
        print ("12 - Obtem angulo")
        print ("13 - Resetar valor do angulo")
        print("14 - Angulo do braco")
        print("15 - MexerBraco baixo")
        print("16 - MexerBraco cima")
        print("17 - Binoculos")
        print("18 - Apanha o objeto ao tocar")
        print("19 - Fazer scan e detetar algo")
        print("20 - Efetuar ataque do robo")
        print("21 - Efetuar ataque de pistola do robo")
        print("0 - Sair")
        optTurno = input()
        if optTurno == "1":
            robotController.andarFrente()
            coordendasRoboX=robotController.getX()
            coordendasRoboY=robotController.getY()

            arrayComOsLugares.append((coordendasRoboX,coordendasRoboY))
            print(arrayComOsLugares)

        elif optTurno == "2":
            robotController.andarAtras()

        elif optTurno == "3":
            robotController.andarFrente()
            robotController.andarEsquerda()

        elif optTurno == "4":
            robotController.andarFrente()
            robotController.andarDireita()

        elif optTurno == "5":
            robotController.andarAtras()
            robotController.andarEsquerda()

        elif optTurno == "6":
            robotController.andarAtras()
            robotController.andarDireita()

        elif optTurno == "7":
            robotController.andarEsquerda()

        elif optTurno == "8":
            robotController.andarDireita()

        elif optTurno == "9":
            print("Cor" + str(robotController.robotColorDetected()))
        
        elif optTurno == "10":
            print("Tocou no braco " + str(robotController.sensorToqueBraco()))
        
        elif optTurno == "11":
            print("Distancia: " + str(robotController.obterDistancia()))

        elif optTurno == "12":
            print("Angulo gyro: " + str(robotController.getGyroPos()))
        
        elif optTurno == "13":
            robotController.resetGyroAngle(0)
        
        elif optTurno == "14":
            print("Angulo do braco: " + str(robotController.getAnguloBraco()))

        elif optTurno == "15":
            robotController.mexerBraco(-90)

        elif optTurno == "16":
            robotController.mexerBraco(90)

        elif optTurno == "17":
            board.detetouAlgo()
        
        elif optTurno == "18":
            robotController.apanharOBjeto()
        
        elif optTurno == "19":
            board.detetouAlgo3()

        elif optTurno == "20":
            board.efetuarAtaque()

        elif optTurno == "21":
            board.efetuarPistola()

        elif optTurno == "0":
            optTurno = False

        if (optTurno != False):
            board.atualizarBoard()
            board.mostrarBoard()

def JogarInteligente():
    #Primeira Jogada
    global nturno
    optJogar= True
    finalPercurso = False
    robotController.andarEsquerda()
    nturno = 0
    nturno += 1
    board.atualizarTurno(nturno)
    #fim primeira jogada
    while(optJogar):
        #VERIFICA GANHOU
        if(board.detetarGanhar()):
            print("--------------VITORIA----------------------")
            optJogar = False

        #VERIFICA PERDEU
        if(board.detetarPerder()):
            print("--------------PERDEU-----------------------")
            optJogar = False

        #verificação que chegou ao fim do percurso
        if((robotController.getX() == 5 and robotController.getY() == 4 and robotController.getPecas() == 0) or (robotController.getX() == 5 and robotController.getY() == 5 and robotController.getPecas() == 0)):
            finalPercurso = True
            print(str(finalPercurso))
        #verificação que chegou ao inicio do percurso depois de ter chegado do inicio
        if(robotController.getX() == 1 and robotController.getY() == 0 and robotController.getPecas() == 0 and finalPercurso == True):
            finalPercurso = False
            print(str(finalPercurso))
        #Verificação que tem uma peça para entregar
        while(board.temPeca == True and board.ganhar == False):
            print("a entregar")
            sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=5,
                destinyY=5   
            )
        #fim da verificação da peça
        
        #percurso 1 (inicial) para o fim
        while(robotController.getX()==1 and robotController.getY()<5 and finalPercurso == False and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):    
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2FrenteSec() == False and board.aoLado2FrenteFirst() == False):
                robotController.andarFrente()
            nturno += 1
            board.atualizarTurno(nturno)
        #percurso 2 (final) para o início
        while(robotController.getX()==1 and robotController.getY() > 0 and finalPercurso == True and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):    
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2AtrasFirst() == False and board.aoLado2AtrasSec() == False):
                robotController.andarAtras()
            nturno += 1
            board.atualizarTurno(nturno)
        #percurso 1 (inicial) para o fim
        while(robotController.getX()==3 and robotController.getY() > 0 and finalPercurso == False and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2AtrasFirst() == False and board.aoLado2AtrasSec() == False):
                robotController.andarAtras()
            nturno += 1
            board.atualizarTurno(nturno)
        #percurso 2 (final) para o início
        while(robotController.getX()==3 and robotController.getY() < 5 and finalPercurso == True and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2FrenteFirst() == False and board.aoLado2FrenteSec() == False):
                robotController.andarFrente()
            nturno += 1
            board.atualizarTurno(nturno)
        #percurso 1 (inicial) para o fim
        while(robotController.getX()==5 and robotController.getY() < 4 and finalPercurso == False and board.temPeca == False and board.ganhar == False):    
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2FrenteFirst() == False and board.aoLado2FrenteSec() == False):
                robotController.andarFrente()
            nturno += 1
            board.atualizarTurno(nturno)
        #percurso 2 (final) para o início
        while(robotController.getX()==5 and robotController.getY() > 0 and finalPercurso == True and board.temPeca == False and board.ganhar == False):    
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY()
                    )
                    print("Municao: "+ str(robotController.getBalas()))
                    break
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
                break
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
                break
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2AtrasFirst() == False and board.aoLado2AtrasSec() == False):
                robotController.andarAtras()
            nturno += 1
            board.atualizarTurno(nturno)
        #ação inicial, tem um if para verificar se chegou ao fim ou não
        #se não chegou ao fim
        if((finalPercurso == False and robotController.getY() == 0) or (finalPercurso == False and robotController.getY() == 5) and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY(),
                    )
                    print("Municao: "+ str(robotController.getBalas()))
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2EsquerdaFirst() == False and board.aoLado2EsquerdaSec() == False):
                robotController.andarEsquerda()
            nturno += 1
            board.atualizarTurno(nturno)
        #se vem do fim
        elif((finalPercurso == True and robotController.getY() == 0 and robotController.getX() > 1) or (finalPercurso == True and robotController.getY() == 5 and robotController.getX() > 1) and board.temPeca == False and board.ganhar == False):
            if(hasattr(board, "municao")):
                if(board.municao != None):
                    sigarCaminho(nturno,
                    robotX=robotController.getX(),
                    robotY=robotController.getY(),
                    destinyX=board.municao.getX(),
                    destinyY=board.municao.getY(),
                    )
                    print("Municao: "+ str(robotController.getBalas()))
            if(board.pecaA != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaA.getX(),
                destinyY=board.pecaA.getY()
                )
            if(board.pecaB != None):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=board.pecaB.getX(),
                destinyY=board.pecaB.getY()
                )
            board.detetouAlgo3()
            if (hasattr(board, "firstZombie")):
                if(board.firstZombie != None and board.aoLadoFirst() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if (hasattr(board, "secondZombie")):
                if(board.secondZombie != None and board.aoLadoSec() == True):
                    if(robotController.getBalas() > 0):
                        board.efetuarPistola()
                    else:
                        board.efetuarAtaque()
            if(board.pecaA == None and board.municao == None and board.pecaB == None and board.aoLado2DireitaFirst() == False and board.aoLado2DireitaSec() == False):
                robotController.andarDireita()
            nturno += 1
            board.atualizarTurno(nturno)


def MenuJogar():
    optJogar= True
    nturno=0
    while(optJogar):

        movimentosDisponiveis = 2

        if (robotController.getPecas() == 1):
            while(movimentosDisponiveis > 0):
                sigarCaminho(nturno,
                robotX=robotController.getX(),
                robotY=robotController.getY(),
                destinyX=5,
                destinyY=5   
                )
                movimentosDisponiveis -= 1 



        if (hasattr(board, "pecaA")) or (hasattr(board, "pecaB")):
            if (board.pecaA == None and board.pecaB == None):
                #MODO EXPLORACAO
                print("Modo exploracao")
                if(movimentosDisponiveis > 0):
                    if (board.efetuarAtaque()):
                        movimentosDisponiveis -= 1
                    board.detetouAlgo3()
                    movimentosDisponiveis -= 1
                    while(movimentosDisponiveis > 0):
                        
                        robotController.randomMovimento()
                        movimentosDisponiveis -= 1
                    
            else:
                print("Busca peca")
                if(movimentosDisponiveis > 0):

                    if(hasattr(board, "pecaB")):
                        if(board.pecaB != None):
                            while(movimentosDisponiveis > 0):
                                sigarCaminho(nturno,
                                    robotX=robotController.getX(),
                                    robotY=robotController.getY(),
                                    destinyX=pecaBController.getX(),
                                    destinyY=pecaBController.getY()
                                )
                                movimentosDisponiveis -= 1

                    if(hasattr(board, "pecaA")): 
                        if(board.pecaA != None):   
                            while(movimentosDisponiveis > 0):
                                sigarCaminho(nturno,
                                robotX=robotController.getX(),
                                robotY=robotController.getY(),
                                destinyX=pecaAController.getX(),
                                destinyY=pecaAController.getY()
                                )
                                movimentosDisponiveis -= 1  


                

                
        #VERIFICA GANHOU
        if(board.detetarGanhar()):
            print("--------------VITORIA----------------------")
            optJogar=False

        #VERIFICA PERDEU
        if(board.detetarPerder()):
            print("--------------PERDEU-----------------------")
            optJogar = False


        board.atualizarBoard()
        board.mostrarBoard()
        print("Turno:"+ str(nturno))
        nturno += 1
        sleep(5)
            
            
option = True

while (option):
    menuPrincipal()
    option = input()

    if option == "1":
        menuRobot()
    elif option == "2":
        menuZombieA()
    elif option == "3":
        menuZombieB()
    elif option == "4":
        Menuturno()
    elif option == "5":
        MenuJogar()
    elif option == "6":
        JogarInteligente()
    elif option == "0":
        option = False

'''s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    # do your stuff
s.enter(30, 1, do_something, (s,))
s.run()'''
