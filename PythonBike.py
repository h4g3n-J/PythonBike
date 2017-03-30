#!/usr/bin/env python

from time import sleep, clock
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StateLock = threading.Lock()

class GPIO_Switch:
	
	def __init__(self, gpio_number):
		self.GPIO_Number = gpio_number
		self.Switch_State = False
		self.Comfort_State = False
		
		GPIO.setup(self.GPIO_Number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			
	def Standard_Switch(self,):	# Version 2.1
		print("Standard Switch gestartet \nzum Schalten Enter Drücken:")
		while True:
			#~ input()
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
		print("Standard Switch beendet")
		return True
		
	def Comfort_Switch(self,):	# Version 2.1
		print("Comfort Switch gestartet \nzum schalten enter drücken")
		while True:
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			a = clock()
			print("falling edge detected")
			sleep(0.01)
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.RISING)
			print("rising edge detected")
			b = clock()
			c = b-a
			print("duration: ", c)
			if c > 0.0015:
				self.Comfort_State = True
			
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State, "\ncomfort switch: ", self.Comfort_State)
			sleep(0.1)
			self.Comfort_State = False
		print("Comfort Switch beendet")
		return True

class GPIO_Target:		
	
	def __init__(self, gpio_number):
		self.GPIO_Number = gpio_number
		self.State = False
		self.frequency = 0.6
		
		GPIO.setup(self.GPIO_Number, GPIO.OUT)

		
	def Turn(self, Ziel):
		i = 0
		while True:
			if Ziel.Switch_State and not Ziel.Comfort_State:	
				GPIO.output(self.GPIO_Number, GPIO.HIGH)
				sleep(self.frequency)
				GPIO.output(self.GPIO_Number, GPIO.LOW)
				sleep(self.frequency)
			if Ziel.Switch_State and Ziel.Comfort_State:
				print("\nKomfort-Blinker gestartet")
				while i < 5:
					GPIO.output(self.GPIO_Number, GPIO.HIGH)
					sleep(self.frequency)
					GPIO.output(self.GPIO_Number, GPIO.LOW)
					sleep(self.frequency)
					i += 1
				print("\nKomfort-Blinker beendet")
				Ziel.Switch_State = False
			if not Ziel.Switch_State and i > 0:
				i = 0
			else:
				sleep(0.1)			
		return True

		
class Switch:
	
	def __init__(self, pin_nr, is_comfort):
		self.Pin_Nr = pin_nr
		self.Is_Comfort = is_comfort
		self.Switch_State = False
		self.Comfort_State = False
		
	def Standard_Switch(self,):	# Version 2.1
		print("Standard Switch gestartet \nzum Schalten Enter Drücken:")
		while True:
			input()
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
		print("Standard Switch beendet")
		return True
		
	def Comfort_Switch(self,):	# Version 2.1
		print("Comfort Switch gestartet \nzum schalten enter drücken")
		
		while True:
			input()
			a = clock()
			input()
			b = clock()
			c = b-a
			
			if c > 0.7:
				self.Comfort_State = True
			
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State, "\ncomfort switch: ", self.Comfort_State)
			sleep(0.1)
			self.Comfort_State = False
			
		print("Comfort Switch beendet")
		return True
			
class Target:		
	
	def __init__(self,):
		self.State = False
		self.frequency = 0.7
		
	def Turn(self, Ziel):
		i = 0
		while True:
			if Ziel.Switch_State and not Ziel.Comfort_State:	
				print("\nStandard Blinker gestartet")
				i += 1
				sleep(self.frequency)
			if Ziel.Switch_State and Ziel.Comfort_State:
				print("\nKomfort-Blinker gestartet")
				while i < 5:
					i += 1
					sleep(self.frequency)
				print("\nKomfort-Blinker beendet")
				Ziel.Switch_State = False
			if not Ziel.Switch_State and i > 0:
				i = 0
			else:
				sleep(0.1)			
		return True
		
if __name__ == '__main__':

	'''Schalter1 = Switch(1, False)
	Blinker1 = Target()
	Schalter2 = Switch(1, False)
	Blinker2 = Target()
	
	thread1 = threading.Thread(target=Schalter1.Standard_Switch, args=())
	thread1.start()
	thread2 = threading.Thread(target=Blinker1.Turn, args=(Schalter1,))
	#thread2.start()
	thread3 = threading.Thread(target=Schalter2.Comfort_Switch, args=())
	#thread3.start()
	thread4 = threading.Thread(target=Blinker2.Turn, args=(Schalter2,))
	#thread4.start()'''
	
	'''Taster1 = GPIO_Switch(24)
	Blinker = GPIO_Target(17)
	
	thread1 = threading.Thread(target=Taster1.Standard_Switch, args=())
	thread1.start()
	thread2 = threading.Thread(target=Blinker.Turn, args=(Taster1,))
	thread2.start()'''
	
	Taster1 = GPIO_Switch(24)
	Blinker = GPIO_Target(17)
	
	thread1 = threading.Thread(target=Taster1.Comfort_Switch, args=())
	thread1.start()
	thread2 = threading.Thread(target=Blinker.Turn, args=(Taster1,))
	thread2.start()
