from os import getenv
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    jsonify
)
from lib.bot_methods import Bot  # Importe a classe Bot do seu arquivo app.py
from utils.extract_json import tokenBot, SigningSecret, queue
import schedule

load_dotenv()
app = Flask(__name__)
bot = Bot(tokenBot, queue)

@app.route(f'/command/queue/generate', methods=['POST'])
def queue_generate():
    if request.args.get('token') == str(SigningSecret):
        if not bot.queue_generated:
            bot.send_queue_channel()
            response_text = "Fila gerada e enviada ao canal!"
            return jsonify(text=response_text)
        else:
            response_text = "Fila já se encontra gerada."
            return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido.")

@app.route(f'/command/help', methods=['POST'])
def help_bot():
    if request.args.get('token') == str(SigningSecret):
        bot.help_bot()
        response_text = "Lista de comandos disponíveis gerados."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido.")

@app.route(f'/command/queue/show', methods=['POST'])            
def show_queue():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            user = request.args.get('user_name')
            bot.current_queue()
            response_text = f"Envio da fila feita por {user}"
            return jsonify(text=response_text)
        else:
            response_text = f"Fila não gerada."
            return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")
    
@app.route(f'/command/queue/save', methods=['POST'])
def save_technician():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            bot.save_queue_to_json()
            response_text = "Fila enviada para o json com sucesso"
        else:
            response_text = f"Fila não gerada."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")


@app.route(f'/command/queue/tech/pause', methods=['PUT'])
def pause_technician():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            text = request.args.get('text')
            response = bot.remove_technician(text)
            if response == 'Ok':
                response_text = f"Técnico {text} removido da fila com sucesso!"
            else:
                response_text = response
        else:
            response_text = f"Fila não gerada."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")

@app.route(f'/command/queue/tech/unpause', methods=['PUT'])
def unpause_technician():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            text = request.args.get('text')
            response = bot.return_technician(text)
            if response == 'Ok':
                response_text = f"Técnico {text} retornou a fila com sucesso!"
            else:
                response_text = response
        else:
            response_text = f"Fila não gerada."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")

@app.route(f'/command/queue/tech/add', methods=['POST'])
def add_technician():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            text = request.args.get('text')
            response = bot.add_technician(text)
            if response == 'Ok':
                response_text = f"Técnico {text} adicionado na fila com sucesso!"
            else:
                response_text = response
        else:
            response_text = f"Fila não gerada."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")
        
@app.route(f'/command/queue/tech/delete', methods=['DELETE'])       
def delete_technician():
    if request.args.get('token') == str(SigningSecret):
        if bot.queue_generated:
            text = request.args.get('text')
            response = bot.delete_technician(text)
            if response == 'Ok':
                response_text = f"Técnico {text} removido da fila com sucesso!"
            else:
                response_text = response
        else:
            response_text = f"Fila não gerada."
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")

@app.route(f'/command/queue/reset', methods=['POST'])
def reset_queue():
    if request.args.get('token') == str(SigningSecret):
        bot.reset_queue()
        response_text = "Fila resetada com sucesso!"
        return jsonify(text=response_text)
    else:
        return jsonify(text="Token inválido")

if __name__ == '__main__':
    app.run(host=getenv("API_HOST"), port=getenv("API_PORT"), debug=True)