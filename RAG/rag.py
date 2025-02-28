import subprocess
import os

os.chdir("code")
try:
    result=subprocess.run(["python", "pdfToTxt.py"])
    if(result):
        print("conversione da pdf a txt | eseguito con successo")
    else:
        print("python pdfToTxt.py | errore nell'esecuzione")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running: {' '.join("python pdfToTxt.py")}")
    print("Return code:", e.returncode)
    print("Standard Error:", e.stderr)

try:
    result=subprocess.run(["python", "addVet.py"])
    if(result):
        print("caricamento su db vettori di embedding | eseguito con successo")
    else:
        print("python addVet.py | errore nell'esecuzione")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running: {' '.join("python addVet.py")}")
    print("Return code:", e.returncode)
    print("Standard Error:", e.stderr)




