#!/usr/bin/env python3
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
import csv

reader = SimpleMFRC522()

fi = open('idcards.csv', 'w')
writer = csv.writer(fi, delimiter=',')

while True:
	print('Go')
	id, text = reader.read()
	print('ID = ' + str(id) + ' Text = ' + str(text))
	writer.writerow(str(id))


