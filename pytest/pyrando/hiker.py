#! /usr/bin/env python
#-*- coding: iso-8859-15 -*-



import os
import sys
import shutil


    
    
    
    
    
    

class Hiker:
    """
    Classe hiker
    
    l'Objet Hiker...
    
    """
    

            
    def __init__(self, pseudo, name, picasa_mail, picasa_user, picasa_password):
        
        self.__pseudo = pseudo
        self.__name = name
        self.__picasa_mail = picasa_mail
        self.__picasa_user = picasa_user
        self.__picasa_password = picasa_password


    def getPseudo(self):
        return self.__pseudo;
    
    def getName(self):
        return self.__name;

    def getPicasaMail(self):
        return self.__picasa_mail;
        
    def getPicasaUser(self):
        return self.__picasa_user;

    def getPicasaPassword(self):
        return self.__picasa_password;

        
        
        
if __name__ == "__main__":
    h = Hiker('myHiker')
