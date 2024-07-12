import json
class System_Files():
	def __init__(self, filename="healt_datas.json"):
		self.filename = filename

    ## Guarda los datos en archivo JSON
    # @ datas: Dict -> datos del programa en formato diccionario
	def Save_Dict(self, datas):
		# print(f"Datos del diccionario:\n {datas}")	# Debug Only
		try:
			# Abre el archivo en modo escritura
			with open(self.filename, "w") as file:

				# Pasa el archivo al archivo en formato JSON
				json.dump(datas, file, indent=4, sort_keys=True)	#file.write(json.dumps(datas)) # También es valido

				# Cierra el archivo
				file.close()

		except Exception as err:
			print(str(err))

	## Lee el archivo y lo transforma en diccionario JSON
	# @ return: Dict -> Diccionario con los datos del programa
	def Read_Dict(self):
		try:
			# Abre el archivo
			file = open(self.filename, "r")

			# Lee el archivo en formato JSON y lo carga en la variable datas
			datas = json.load(file)

			# Cierra archivo
			file.close()

			# Retorna el contenido del archivo file como diccionario
			return datas

		# Si hay un error por no encontrar el archivo
		except Exception:
			# Lee la respuesta y crea un archivo vacio con nombre 'filename'
			# resp = input(f"El archivo {self.filename} no existe. Crear archivo?(y/n)")
			resp = 'y' # Comentar esta linea para que 
			# Si la respuesta es 'y'
			if resp == 'y':

				# Crea el archivo
				with open(self.filename, "w") as file:
					json.dump(self.get_form(), file, indent=4, sort_keys=True)
				file.close()
				# open(self.filename, "w")
				print(f"Archivo {self.filename} creado")
				return -1

	## Lee una llave del diccionario
	# @ key -> LLave del valor que queremos recuperar
	# @ return: str, float, int -> valor respecto a la llave 'key'
	def Get_json_value(self, key):
		try:
			# Recupera el diccionario
			datas = self.Read_Dict()

			# Devuelve el valor de la llave
			return  datas[key]
		except Exception as err:
			print(f"pues hay un error: {err}")

	## Guarda un valor en el archivo JSON
	# @ key -> Llave del valor para cambiar en el archivo
	# @ value -> Valor del elemento dado por la 'key'
	def Add_json_value(self, key, value):
		try:
			datas = self.Read_Dict()
			datas[key] = value
			self.Save_Dict(datas)
		except Exception as err:
			print(f"pues hay un error: {err}")

	##
	def get_form(self):
		return {"filename" : "healt_datas.json"}
'''
if __name__ == '__main__':
	a = System_Files()
'''



