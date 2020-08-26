#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import socket

fermeture = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
fermeture.connect(('localhost',12800))
fermeture.send(b"fermeture reseau principal")
fermeture.close()