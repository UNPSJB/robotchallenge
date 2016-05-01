# encoding: utf-8
import os
import sys

def encontrar_kivy():
    '''
    Encuentra kivy buscando en un:
        * `virtualenv` llamado kivy
        * Instalación de kivy del sistema
        * algún `virtualenv` que tenga kivy?
    '''
    # Si no se pudo importar desde el sistema, buscamos si hay un entorno
    instalacion_alt = os.path.expanduser(
        '~/.virtualenvs/kivy/lib/python2.7/site-packages'
    )
    sys.path.append(instalacion_alt)
    import kivy
