# Fuente:
# https://umeey.medium.com/system-monitoring-made-easy-with-pythons-psutil-library-4b9add95a443
import psutil
import subprocess
import time
import sys

class System_Functions():
    #def __init__(self):

    ## Obtiene la ip del equipo
    # @ return String "0.0.0.0"
    def GetIP(self):
        return str(subprocess.check_output(['hostname', '-I'])).split(' ')[0].replace("b'", "")

    ## Obtiene la carga de la CPU
    ## Crea una demora de 1 seg en el programa principal
    # @ return float
    def GetCPU(self):
        return psutil.cpu_percent(1)

    ## Obtiene la ip del equipo
    # @ return float
    def GetTemp(self):
        output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output= True)
        temp_str = output.stdout.decode()
        try:
            return float(temp_str.split('=')[1].split('\'')[0])
        except (IndexError, ValueError):
            raise RuntimeError('no se puede obtener temperatura')

    ## Obtiene la cantidad de RAM
    # @ return float
    def GetRAM(self):
        return psutil.virtual_memory()[2]

    ## Obtiene la velocidad del ventilador
    # @ hpc: healt_pwm_class.System_PWM_Fan
    # @ type_ int: 0=Proporcional, 1=Por pasos de temperatura
    # @ return int: valor de pwm aplicado en el pin
    def GetFanPWM(sef, hpc, type_):
        if type_ == 0:
            return hpc.Proportional()
        else:
            return hpc.Stepped()

    ## Obtiene el tiempo que lleva la maquina encendida
    # @ return String "0d 00h 00m 00s"
    def GetUpTime(sef):
        boot_time_timestamp = psutil.boot_time()
        current_time_timestamp = time.time()
        uptime_seconds = current_time_timestamp - boot_time_timestamp
        uptime_minutes = uptime_seconds // 60
        uptime_hours = uptime_minutes // 60
        uptime_days = uptime_hours // 24
        uptime_str = f"{int(uptime_days)}d {int(uptime_hours % 24)}h {int(uptime_minutes % 60)}m {int(uptime_seconds % 60)}s"
        # print("Uptime: " + uptime_str)
        return uptime_str


    ## Función que devuelve el SO en uso
    # @ return String
    def GetOS(self):
        platforms = {
        'linux1' : 'linux',
        'linux2' : 'linux',
        'darwin' : 'mac',
        'win32' : 'win32'
        }
        if sys.platform not in platforms:
            return sys.platform
        
        return platforms[sys.platform]    

    ## Reescalado de los datos para PWM
    # @ num: Número de entrada
    # @ inMin: Parte baja de los datos de entrada
    # @ inMax: Parte alta de los datos de entrada
    # @ outMin: Parte baja de los datos de salida
    # @ outMax: Parte alta de los datos de salida
    # @ return int 
    def rescale_data(self, num, inMin, inMax, outMin, outMax):
        return int(outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin)))

'''
if __name__ == '__main__':
   app = System_Functions().rescale_data(50, 0, 100, 2, 255) 
   print("data: " + str(app))
'''