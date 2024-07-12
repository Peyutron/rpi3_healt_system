# Fuente original: https://github.com/mklements/PWMFanControl/tree/main

import RPi.GPIO as IO
from healt_functions_class import *

class System_PWM_Fan():
	def __init__(self, pwm_pin=14, mode=0, perfil=1):
		self.pwm_pin = pwm_pin
		self.mode = mode		# mode=0: Proportional; mode=1: Stepped
		self.perfil = perfil
		IO.setwarnings(False)		# No mostrar alertas GPIO
		IO.setmode(IO.BCM)		# Número de pin BCM - El PIN8 es 'GPIO14'
		IO.setup(self.pwm_pin, IO.OUT)		# Inicializa GPIO14 como pin de salida
		self.fan = IO.PWM(self.pwm_pin, 50)	# Establece GPIO14 como salida PWM a 50Hz
		self.fan.start(0)			# Inicia la señal PWM iniciada al 0% (apagado)
		self.hfc = System_Functions()


		self.perfiles = ([40, 60, 80],	# Without heatsink
				[30, 50, 70],	# With heatsink
				[30, 40, 60],	# Active heatsink
				[ 0,  0,  0]	# Custom
				)
		# print("perfiles: {}, : {} Perfil: {}".format(self.pwm_pin, self.mode, self.perfil))
		self.speed_min = 0
		self.speed_max = 100

	## Función para proporcional
	def renormalize(self, n, range1, range2):
		delta1 = range1[1] - range1[0]
		delta2 = range2[1] - range2[0]
		return (delta2 * (n -range1[0]) /delta1) + range2[0]

	## Función velocidad proporcional del ventilador
	# @ return int: 0 a 100 valor pwm normalizado
	def Proportional(self):
		
		temp = self.hfc.GetTemp()
		if temp < self.perfiles[self.perfil][0]:       # Constrain temperature to set range limits
			temp = self.perfiles[self.perfil][0]
		elif temp > self.perfiles[self.perfil][2]:
				temp = self.perfiles[self.perfil][2]
		pwm = int(self.renormalize(temp, [self.perfiles[self.perfil][0], self.perfiles[self.perfil][2]], [self.speed_min, self.speed_max]))
		self.fan.ChangeDutyCycle(pwm) # Set fan duty based on temperature, from minSpeed to maxSpeed
		return pwm

	## Función selocidad del ventilador por pasos de temperatura
	# @ return int: 0 a 100 valor pwm normalizado
	def Stepped(self):
		temp = self.hfc.GetTemp()
		speed = 0
		if temp > self.perfiles[self.perfil][2]:
			print("mas de ")
			speed = 100
		elif temp  > self.perfiles[self.perfil][1]:
			speed = 50
		elif temp > self.perfiles[self.perfil][0]:
			speed = 25
		self.fan.ChangeDutyCycle(speed)
		return speed
