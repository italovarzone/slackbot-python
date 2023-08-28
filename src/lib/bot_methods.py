from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from utils.extract_json import *
from utils.remove_special_chars import remove_special_chars
import json
import pathlib
import random

class Bot:
    def __init__(self, tokenBot=str, Queue=str):
        self.tokenBot = tokenBot
        self.Queue = Queue
        self.client = WebClient(token=tokenBot)
        self.queue_generated = False
        
    def help_bot(self):
        channel_id = 'C05NR3VV4HE'
        help_text = {
            '*OBSERVAÇÃO:*': "Todos os comandos relacionado a fila e técnicos só serão realizados após gerar a fila.\n",
            '`/montar_fila`': "Gera a fila de técnicos.",
            '`/fila`': "Exibe a fila atual de técnicos.",
            '`/remover NOMETECNICO`': "Remove um técnico da fila.",
            '`/retornar NOMETECNICO`': "Retorna um técnico à fila.",
            '`/adicionar NOMETECNICO`': "Adiciona um técnico à fila.",
            '`/deletar NOMETECNICO`': "Remove definitivamente um técnico da fila.",
            '`/reset`': "Reseta a fila para o estado original."
        }
        lista = []
        for command, text in help_text.items():
            lista.append(f"{command} - {text}")

        help_list = "\n".join(
            [f"{i}" for i in lista])
        # print(help_list)
        message_text = f"Comandos disponíveis:\n\n{help_list}"
        self.client.chat_postMessage(channel=channel_id, text=message_text)
        
    def save_queue_to_json(self):
        new_list = [remove_special_chars(item) for item in self.Queue]
        with open('config/queue.json', 'w', encoding='UTF-8') as json_file:
            data = {"technical": new_list}
            json.dump(data, json_file, indent=4)
    
    def reset_queue(self):
        with open('config/queue.json', "r", encoding='utf-8', errors='ignore') as jsonini:
            iniQueue = load(jsonini)
        self.Queue = iniQueue['technical']
        self.queue_generated = False
        
    def generate_random_sequence(self):
        random_sequence = random.sample(self.Queue, len(self.Queue))
        return random_sequence

    # Pega o nome da ultima pessoa que deu 'ok' no canal
    def take_ok(self):
        channel_id = "C05N469H6V8"
        user_name = None  # Inicialize user_name como None para o caso de não encontrar nenhum "ok"
        
        try:
            response = self.client.conversations_history(channel=channel_id)
            if response["ok"]:
                for message in response["messages"]:
                    if "user" in message and "text" in message:
                        if "ok" in message["text"].lower():
                            user_id = message["user"]
                            user_info = self.client.users_info(user=user_id)
                            user_name = user_info["user"]["profile"]["display_name"]
                            break  # Encerra o loop ao encontrar o primeiro "ok" do usuário
            else:
                print(f"Error getting message history: {response['error']}")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
            
        if user_name is None:
            print("No 'ok' message found from the user.")
            
        return user_name


    def generate_queue(self):
        random_sequence = self.generate_random_sequence()
        last_name = self.take_ok()

        if last_name in random_sequence:
            index = random_sequence.index(last_name)
            # Remove o elemento da posição atual
            element = random_sequence.pop(index)
            # Adiciona o elemento à última posição
            random_sequence.append(element)
            self.Queue = random_sequence
            self.queue_generated = True

        queue_technical = "\n".join(
            [f"{technical}" for technical in random_sequence])
        return queue_technical

    def send_queue_channel(self):
        new_queue = self.generate_queue()
        channel_id = "C05N5RKJLCU"
        try:
            message_text = f"Segue a fila de hoje <!here>\n\n{new_queue}"
            self.client.chat_postMessage(channel=channel_id, text=message_text)
        except SlackApiError as e:
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")  
    
    def current_queue(self):
        channel_id = "C05N5RKJLCU"
        queue_technical = "\n".join(
        [f"{technical}" for technical in self.Queue])
        try:
            message_text = f"Segue a fila <!here>\n\n{queue_technical}"
            self.client.chat_postMessage(channel=channel_id, text=message_text)
        except SlackApiError as e:
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
    
    def remove_technician(self, technician):
        technician_to_remove = technician
        if not technician_to_remove:
            text_response = 'Erro! Digite o nome do técnico.'
        else:
            if technician_to_remove in self.Queue:
                strikethrough_technician = f"~{technician_to_remove}~"
                index = self.Queue.index(technician_to_remove)
                self.Queue.insert(index, strikethrough_technician)
                self.Queue.pop(index + 1)
                text_response = 'Ok'
            else:
                text_response = 'Técnico não encontrado, digite o nome de exibição do técnico.'
        return text_response
                
    def return_technician(self, technician):
        technician_to_remove = technician
        if not technician_to_remove:
            text_response = 'Erro! Digite o nome do técnico.'
        else:
            technician_to_remove = f"~{technician_to_remove}~"
            if technician_to_remove in self.Queue:
                index = self.Queue.index(technician_to_remove)
                new_technician = technician_to_remove.replace('~', '')
                self.Queue.insert(index, new_technician)
                self.Queue.pop(index + 1) 
                text_response = 'Ok'
            else:
                text_response = 'Técnico não encontrado, digite o nome de exibição do técnico'
        return text_response
    
    def add_technician(self, technician):
        if technician in self.Queue:
            text_response = 'Técnico já está na fila.'
            return text_response
        else:
            technician_to_add = technician
            last_name = self.take_ok()
            if last_name in self.Queue:
                index = self.Queue.index(last_name)
                self.Queue.insert(index + 1, technician_to_add)
            text_response = 'Ok'
        return text_response
    
    def delete_technician(self, technician):
        if technician not in self.Queue:
            text_response = 'Técnico não está na fila.'
            return text_response
        else:
            technician_to_delete = technician
            if not technician_to_delete:
                text_response = 'Erro! Digite o nome do técnico.'
            else:
                if technician_to_delete in self.Queue:
                    index = self.Queue.index(technician_to_delete)
                    self.Queue.pop(index)
                text_response = 'Ok'
        return text_response