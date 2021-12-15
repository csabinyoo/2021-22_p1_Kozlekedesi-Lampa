# Könyvtárak importálása
import RPi.GPIO as GPIO
import time

# GPIO beállítása
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Pinek kiosztása a táblázat alapján
pJarmuPiros = 21
pJarmuSarga = 20
pJarmuZold = 16

pGyalogosPiros = 26
pGyalogosZold = 13

# Pinek tömbjének létrehozása
pinek = [pJarmuPiros, pJarmuSarga, pJarmuZold, pGyalogosPiros, pGyalogosZold]

# Pinek kimenetnek definiálása for ciklussal
for pin in pinek:    
    GPIO.setup(pin, GPIO.OUT)
    
# Függvények

def JarmuLampa(piros, sarga, zold):
    GPIO.output(pJarmuPiros, piros)
    GPIO.output(pJarmuSarga, sarga)
    GPIO.output(pJarmuZold, zold)

def GyalogosLampa(piros, zold):
    GPIO.output(pGyalogosPiros, piros)
    GPIO.output(pGyalogosZold, zold)

def Teszt(n):
    print("Teszt folyamatban...")
    onOff = True
    for i in range(0,n):      
        JarmuLampa(onOff, onOff, onOff)
        GyalogosLampa(onOff, onOff)
        onOff = not onOff
        time.sleep(1)
    onOff = False
    JarmuLampa(onOff, onOff, onOff)
    GyalogosLampa(onOff, onOff)
    print("Teszt befejezve!")


# A program paraméterei
T = 1.0 # Órajel periódusideje (1s)
k = 2 # Gyorgyítási faktor
TvalosIdo = T/k # Valós várakozás: tényleges órajel ütem

frequency = 3
fill = 30

# Gyalogos zöld villogási frekvenciája
f = TvalosIdo/T*2
t = 0

# Lámpaidők: meddig égnek az egyes lámpák
tPiros = 10
tPirosSarga = 3
tZold = 10
tSarga = 3

# Összidő
tOsszido = tPiros + tPirosSarga + tZold + tSarga

# A program indulási pontja
try:
    #Teszt(5)
    print("Közlekedési lámpa")
    print("Kilépés: CTRL+C")
    print(f"Gyorsítási érték --> {k}")
    while True:
        if t == tOsszido:
            # Ha elértük az összidőt, akkor az idő újra fog indulni
            t = 0
            
        # Kezdés
        if t == 0:
            # Járműlámpa: piros
            JarmuLampa(True, False, False)
            # Gyalogos lámpa: zöld
            GyalogosLampa(False, True)
        
        # Vége a pirosnak(jármű)
        if t == tPiros:
            # Járműlámpa: piros-sárga
            JarmuLampa(True, True, False)
            # Gyalogos zöld f-el villog
            p = GPIO.PWM(pGyalogosZold, frequency)
            p.ChangeFrequency(frequency)
            p.ChangeDutyCycle(fill)
            p.start(fill)
        
        # Vége a piros-sárgának(jármű)
        if t == tPiros + tPirosSarga:
            # Járműlámpa: zöld
            JarmuLampa(False, False, True)
            # Gyalogos lámpa zöld villogásának befejezése
            p.stop()
            # Gyalogos lámpa: piros
            GyalogosLampa(True, False)
        
        # Vége a zöldnek(jármű)
        if t == tPiros + tPirosSarga + tZold:
            # Járműlámpa: sárga
            JarmuLampa(False, True, False)
            # Gyalogos lámpa: piros
            GyalogosLampa(True, False)
        
        # Megnöveljük a t változót 1-el
        t += 1
        # Valós órajel ideig várakozunk
        time.sleep(TvalosIdo)

except KeyboardInterrupt:
    print("Pinek lekapcsolva")
    GPIO.cleanup()