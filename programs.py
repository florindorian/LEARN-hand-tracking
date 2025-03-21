# Definição dos programas que serão abertos e fechados
programas = {
    'bloco_notas': {
        'status': False,
        'processo': None,
        'bin': '/usr/bin/gedit',
        'activation': [False, True, False, False, False]
    },
    'calc': {
        'status': False,
        'processo': None,
        'bin': '/usr/bin/gnome-calculator',
        'activation': [False, True, True, False, False]
    }
}

def atualiza_status_processos(programas: dict):
    for i,p in programas.items():
        try:
            if p['processo'].poll() is not None:
                # None: significa que nenhum código de fechamento foi retornado
                p['status'] = False
                p['processo'] = None
            programas[i] = p
        except AttributeError as e:
            pass

    return programas