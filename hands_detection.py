import cv2
import mediapipe as mp
from hands_functions import *
from programs import programas, atualiza_status_processos
import subprocess
# import os

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands()
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUCAO_X)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUCAO_Y)


while True:
    sucesso, img = camera.read()
    img = cv2.flip(img, 1)
    img, todas_maos = encontra_coordenadas_maos(maos, mp_maos, mp_desenho, img)

    if len(todas_maos) > 1:
        if todas_maos[0]['lado'] == 'Right':
            right_hand = todas_maos[0]
            left_hand = todas_maos[1]
        else:
            right_hand = todas_maos[1]
            left_hand = todas_maos[0]

        info_right = dedos_levantados(right_hand) # [0]: porque neste caso uma só mão foi levantada
        info_left = dedos_levantados(left_hand)

        programas = atualiza_status_processos(programas)

        for i,p in programas.items():
            if p['status'] == False and info_right == p['activation'] and info_left == [True]*5:
                p['status'] = True # Sinal de programa ativo
                # Cria um processo filho e retorna o controle ao Python imediatamente
                p['processo'] = subprocess.Popen([p['bin']])
                # os.startfile('/usr/bin/gedit') -> No windows | os.system('comando') funciona no Linux,
                # mas trava a execução do vídeo (não cria um processo em segundo plano)

            if p['status'] == True and info_right == p['activation'] and info_left == [False]*5:
                p['status'] = False
                # os.startfile('/usr/bin/gedit') -> No windows | os.system('comando') funciona no Linux, mas trava a execução do vídeo (não cria um processo em segundo plano)
                if p['processo'] is not None:
                    p['processo'].kill()  # Força o fechamento do processo
                    p['processo'].wait()  # Aguarda o encerramento processo
                    p['processo'] = None


    # Exibe a imagem (frame) capturada pela câmera
    cv2.imshow("Imagem", img)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break