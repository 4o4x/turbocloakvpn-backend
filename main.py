from flask import Flask ,request ,jsonify
import subprocess
from flask_cors import CORS
import pexpect


count = 0

app = Flask(__name__)
CORS(app)

def generate_ovpn_config():
    
    global count
    count = count + 1
   
    # bash komutunu çalıştırın ve pexpect.spawn nesnesini oluşturun
    process = pexpect.spawn("sudo bash openvpn-install.sh", encoding="utf-8")

    # Menüdeki ilk adımı (1. adımı) tamamlamak için "1" bilgisini gönderin
    process.sendline("1")

    # İkinci adım için gerekli bilgiyi gönderin (örneğin "randomid12345")
    process.sendline("rfsfs")

    # Menüden çıkmak için Ctrl+D (EOF) gönderin
    process.sendeof()

    # Menüden çıktıyı alın
    output = process.read()

    # Çıktıyı ekrana yazdırın
    print(output)

    return True


@app.route('/ovpn',methods=['GET'])
def ovpn():
    generate_ovpn_config()
    return "OK",200



if __name__=='__main__':
    app.run(port=3750,debug=True)
