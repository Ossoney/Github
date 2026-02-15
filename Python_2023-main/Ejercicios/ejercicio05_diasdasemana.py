from gtts import gTTS
import os

diassemana=["Luns","Martes","Mercores","Xoves","Venres","Sábado","Domingo"]

for elemento in diassemana:
    audio = gTTS(text=elemento,lang="es",slow=False)
    audio.save("elemento.mp3")
    os.system("start elemento.mp3")
    time.sleep(2)