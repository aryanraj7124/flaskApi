# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/run_container', methods=['POST'])
# def run_container():


#     # Run the command
#     try:
#         data = request.json
        
#         # Extract parameters
#         image_name = data.get('image_name')
#         cpu = data.get('cpu')
#         gpu_memory = data.get('gpu_memory')
#         mount = data.get('mount')
#         ram = data.get('ram')

#         # Construct the docker run command
#         command = [
#             'genv-docker', 'run', '-it', '--rm', 
#             f'--gpus=1', f'--gpu-memory={gpu_memory}mi', 
#             f'--cpus={cpu}', f'--memory={ram}m', 
#             '--mount', f'type=bind,source={mount},target=/workspace',
#             image_name
#         ]
#         data=subprocess.run(command, check=True, capture_output=True)
#         print("success",data)
#         return jsonify({'message': 'Container started successfully!'}), 200
#     except Exception as e:
#         print("error")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)




# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)


# @app.route('/test', methods=['POST'])
# def test():
#     result = subprocess.run(command, capture_output=True, text=True, check=True)
#             return jsonify({"output": result.stdout})

# @app.route('/run_container', methods=['POST'])
# def run_container():
#     try:
#         data = request.json
#         image_name = data.get('image_name')
#         cpu = data.get('cpu')
#         gpu_memory = data.get('gpu') + "mi"  # GPU memory should be in MiB and appended with 'mi'
#         mount = data.get('mount')
#         ram = data.get('ram')  # RAM is already in correct format like '4gb'

#         # Constructing the Docker command
#         command = [
#             'genv-docker', 'run', '-it', '--rm', '--gpus=1', f'--gpu-memory={gpu_memory}',
#             f'--cpus={cpu}', f'--memory={ram}', '--mount', f'type=bind,source={mount},target=/workspace', image_name
#         ]

#         # Running the Docker command
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         return jsonify({"output": result.stdout})

#     except subprocess.CalledProcessError as e:
#         return jsonify({"error": str(e)}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)








# @app.route('/run_container', methods=['POST'])
# def run_container():
#     try:
#         data = request.json

#         # Extracting parameters
#         image_name = data.get('image_name')
#         cpu = data.get('cpu')
#         mount = data.get('mount')
#         ram = data.get('ram')  # Assuming the format is '4gb' already

#         # Constructing the Docker run command
#         command = [
#     'genv-docker', 'run', '-d', '--rm', '--gpus', '0', 
#     f'--cpus={cpu}', 
#     f'--memory={ram}', 
#     '--ipc=host',
#     '--ulimit', 'memlock=-1',
#     '--ulimit', 'stack=67108864',
#     '--mount', f'type=bind,source={mount},target=/workspace', 
#     '--pid', 'host',
#     '--entrypoint', 'bash', 
#     image_name
# ]

#         # Print the command for debugging
#         print("Running command:", " ".join(command))

#         # Running the Docker command
#         result = subprocess.run(command, capture_output=True, text=True, check=True)

#         # Capture the container ID
#         container_id = result.stdout.strip()
        
#         # Print the container ID to the console
#         print("Container started with ID:", container_id)

#         # Returning the container ID as the response
#         return jsonify({"container_id": container_id}), 200

#     # Catching specific errors for better error handling
#     except subprocess.CalledProcessError as e:
#         return jsonify({"error": f"Subprocess error: {e.stderr}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"General error: {str(e)}"}), 500






from flask import Flask, request, jsonify
import subprocess,json

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    # Test command for simplicity
    command = ['echo', 'Hello, World!']
    
    try:
        result = subprocess.run(command, check=True, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        return jsonify({"output": output}), 200  # Added return statement for success
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Subprocess error: {e.stderr.decode()}"}), 500
    except Exception as e:
        return jsonify({"error": f"General error: {str(e)}"}), 500
       


from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_container', methods=['POST'])
def run_container():
    try:
        data = request.json

        # Extracting parameters
        image_name = data.get('image_name')
        cpu = data.get('cpu')
        gpu_memory = data.get('gpu') + "mi"  # GPU memory should be in MiB
        mount = data.get('mount')
        ram = data.get('ram')  # Assuming the format is '4gb' already
        base_url = data.get('base_url', 'notebook')  # Default base URL if not provided
        token = data.get('token', 'default_token')   # Default token if not provided
        port = data.get('port', '8888')              # Default port if not provided

        # Constructing the Docker run command
        command = [
            'genv-docker', 'run', '-it', '-d', '--rm', '--gpus=0',  # Updated gpus to 0
            f'--gpu-memory={gpu_memory}', 
            f'--cpus={cpu}', 
            f'--memory={ram}', 
            '--mount', f'type=bind,source={mount},target=/workspace', 
            image_name,
            'jupyter', 'notebook', '--allow-root', '--ip', '0.0.0.0',
            f'--NotebookApp.base_url=/{base_url}',
            '--NotebookApp.allow_origin=*',
            f'--NotebookApp.token={token}', '--no-browser', f'--port={port}'
        ]

        # Running the Docker command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Returning container ID or success message
        return jsonify({"container_id": result.stdout.strip()}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Subprocess error: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"General error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
