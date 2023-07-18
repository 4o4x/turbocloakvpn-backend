from flask import Flask ,request ,jsonify
import subprocess
from flask_cors import CORS
import pexpect
import time 


app = Flask(__name__)
CORS(app)

def generate_ovpn_config(id):
    
    process = pexpect.spawn("sudo bash /home/openvpn-install.sh", encoding="utf-8")
    process.sendline("1")
    process.sendline(id)    
    process.sendeof()
    output = process.read()
    


def revoke_ovpn_config(id):
    process = pexpect.spawn("sudo bash /home/openvpn-install.sh", encoding="utf-8")
    process.sendline("2")
    process.expect("Select the client to revoke:\n")
    print(process.after)

    # Menüdeki seçenekleri taramak için bir döngü başlatın
    while True:
        # Menüden çıktıyı alın ve satırlara bölelim
        menu_output = process.after.splitlines()

        # Her satırı kontrol edelim
        for line in menu_output:
            # Eğer "id" ismi içeren bir satır bulduysak, ilgili indeks numarasını alalım
            if id in line:
                selected_index = line.split(")")[0].strip()
                break
        else:
            # "id" ismi bulunamadıysa, kullanıcıya hata mesajı gösterelim ve çıkış yapalım
            print(f"'{id}' ismi menüde bulunamadı!")
            process.terminate()
            raise Exception(f"{id} is not found")

        # Eğer "selected_index" değeri boş değilse, yani "id" ismi menüde bulunmuşsa, döngüden çık
        if selected_index:
            break

    # Seçimi gönderin ve çıktıyı bekleyin
    process.sendline(selected_index)
    process.sendline("y")
    process.sendeof()
    output = process.read()
    #process.expect(pexpect.EOF)


@app.route('/create',methods=['GET'])
def create():
    try:
        id = request.args.get('id')

        print(id)

        generate_ovpn_config(id)
        print("func")

        print(str(id))

        file_path = f"/root/{id}.ovpn"

        print(file_path)

        try:
            # Open the file and read its contents
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Create a Python dictionary containing the file content
            data = {
                'content': file_content
            }

            # Convert the dictionary to a JSON response using jsonify
            return jsonify(data),200

        except FileNotFoundError:
            return jsonify(error="File not found"), 404


    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/revoke',methods=['GET'])
def revoke():
    try:
        id = request.args.get('id')
        revoke_ovpn_config(id)
        return jsonify(status="OK"),200

    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__=='__main__':
    app.run(port=3750,debug=True)
