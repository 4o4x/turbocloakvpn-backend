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
    



@app.route('/ovpn',methods=['GET'])
def ovpn():
    try:
        
        #data = request.json
        print("route")
        id = str(time.time()) #str(data.get("id"))
        generate_ovpn_config(id)
        print("func")

        file_path = f'/root/{id}.ovpn'


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


if __name__=='__main__':
    app.run(port=3750,debug=True)
