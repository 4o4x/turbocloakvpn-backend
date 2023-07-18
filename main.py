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
    process.expect("Select the client to revoke:")
    print(process.before)
    process.sendline(id)
    process.sendline("y")
    process.sendeof()
    output = process.read()


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
