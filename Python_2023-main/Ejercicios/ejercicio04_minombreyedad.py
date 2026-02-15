from gtts import gTTS
import os

nombre=input("Introduce tu nombre: ")
edad=input("Introduce tu edad: ")
mytext=(f"Te llamas {nombre} y tienes {edad} años.")



audio = gTTS(text=mytext,lang="es",slow=False)
audio.save("example.mp3")

os.system("start example.mp3")