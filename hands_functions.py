import cv2

RESOLUCAO_X = 1280
RESOLUCAO_Y = 720

def encontra_coordenadas_maos(maos, mp_maos, mp_desenho, img, lado_invertido = False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = maos.process(img_rgb)
    todas_maos = []

    # MULTI_HAND_LANDMARKS: retorna as coordenadas dos pontos, normalizadas entre 0 e 1 com base na proporção da imagem
    if resultado.multi_hand_landmarks:
        # itera sobre cada mão
        for lado_mao, marcacoes_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_mao = {}
            coordenadas = []
            # marcacoes_maos.landmark: array de tuplas (x,y,z) dos 21 pontos da mão
            for marcacao in marcacoes_maos.landmark: # Landmark: um ponto de referência da mão
                coord_x, coord_y, coord_z = int(marcacao.x * RESOLUCAO_X), int(marcacao.y * RESOLUCAO_Y), int(marcacao.z * RESOLUCAO_Y)
                coordenadas.append((coord_x, coord_y, coord_z))

            info_mao['coordenadas'] = coordenadas
            if lado_invertido:
                if lado_mao.classification[0].label == 'Left':
                    info_mao['lado'] = 'Right'
                else:
                    info_mao['lado'] = 'Left'
            else:
                info_mao['lado'] = lado_mao.classification[0].label

            todas_maos.append(info_mao)
            mp_desenho.draw_landmarks(img,
                                    marcacoes_maos,
                                    mp_maos.HAND_CONNECTIONS)

    return img, todas_maos



def dedos_levantados(mao):
    dedos = []

    # Trata o caso do polegar na mão Direita
    if mao['lado'] == 'Right':
        # Mão aberta com palma para frente: 4 >> 3 >> 2 >> 1 >> 0
        if mao['coordenadas'][4][0] < mao['coordenadas'][3][0]:
            dedos.append(True) # Polegar levantado
        else:
            dedos.append(False)

    # Trata o caso do polegar na mão Esquerda
    else:
        if mao['coordenadas'][4][0] > mao['coordenadas'][3][0]:
            dedos.append(True)
        else:
            dedos.append(False)

    # Trata os demais dedos, independente da mão
    for ponta_dedo in [8,12,16,20]:
        # [1]: coordenada y, começando do canto superior esquerdo. Sentido positivo: de cima para baixo
        if mao['coordenadas'][ponta_dedo][1] < mao['coordenadas'][ponta_dedo-2][1]:
            dedos.append(True) # Dedo levantado
        else:
            dedos.append(False) # Dedo abaixado
    return dedos