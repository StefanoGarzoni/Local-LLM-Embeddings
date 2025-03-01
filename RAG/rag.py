import subprocess
import os

os.chdir("code")
try:
    result=subprocess.run(["python", "pdfToTxt.py"])
    if(result):
        print("PDF to TXT conversion | executed successfully")
    else:
        print("python pdfToTxt.py | execution error")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running: {' '.join("python pdfToTxt.py")}")
    print("Return code:", e.returncode)
    print("Standard Error:", e.stderr)

try:
    result=subprocess.run(["python", "addVet.py"])
    if(result):
        print("embedding vectors upload to db | executed successfully")
    else:
        print("python addVet.py | execution error")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running: {' '.join("python addVet.py")}")
    print("Return code:", e.returncode)
    print("Standard Error:", e.stderr)




