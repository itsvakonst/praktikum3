#!/usr/bin/python3

import socket
import asyncio
import os
import json
from datetime import datetime
import subprocess

#----------------------------
# Для клиента 1
def get_programs_in_path(path):
    """
    Функция, получает список программ в указанной директории.
    принимает:
        path (str): путь к директории.
    возвращает:
        list: список программ.
    """
    programs = []

    # существует ли указанная директория и является ли она директорией
    if os.path.exists(path) and os.path.isdir(path):
        # получаем список файлов в директории
        files = os.listdir(path)
        # фильтруем файлы, чтобы остались только исполняемые программы
        programs = [file for file in files if
                    (file.endswith(".exe") or file.endswith(".dll"))]
        
    return programs


def get_programs_in_path_env():
    """
    Функция, получает информацию о директориях из переменной окружения PATH
    и список программ в каждой директории.
    возвращает: словарь с информацией о директориях и программах.
    """
    # значение переменной окружения PATH
    path_env = os.getenv("PATH")
    # делим значение на отдельные пути
    paths = path_env.split(os.pathsep)

    programs_info = {}

    # для каждого пути получаем список программ
    for path in paths:
        programs = get_programs_in_path(path)
        programs_info[path] = programs

    return programs_info


def save_programs_info_to_file(programs_info, filepath):
    """
    Функция, сохраняет информацию о программах в файл в формате JSON
        programs_info (dict): словарь с информацией о программах
        filepath (str): путь к файлу который JSON
    """
    with open(filepath, "w") as file:
        # сохраняем словарь в файл в формате JSON с отступами 4
        json.dump(programs_info, file, indent=4)
#----------------------------

   
class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port


    async def handle_client(self, reader, writer):
        result = None
        input_data = await reader.read(1)
        input_data = input_data.decode('utf-8')

        if input_data == "1":
            print("varya")
            result = await self.varya(reader)

        #elif input_data == "2":
            #print("polina")
            #result = await self.polina(reader)

        if result:
            writer.write(result)
            writer.close()
            await writer.wait_closed()


    #1
    async def varya(self, reader):
        # Получаем команду от клиента
        command = ""
        piece = await reader.read(64)
        if piece:
                command += piece.decode()
                if command == "update":
                    # Получаем информацию о программах
                    programs_info = get_programs_in_path_env()
                    # Сохраняем информацию в файл
                    save_programs_info_to_file(programs_info, "programs_info.json")
        json_file = json.dumps(programs_info).encode('utf-8')
        return json_file

    
    def start(self, is_async=True):
        #if is_async:
        asyncio.run(self._async_start())
        #else:
        #    self._thread_start()

    async def _async_start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self._host, self._port)
        addr = self.server.sockets[0].getsockname()
        print(f'Сервер запущен на {addr}')
        async with self.server:
            await self.server.serve_forever()

    def _thread_start(self):
        #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.bind((self._host, self._port))
        #server_socket.listen(1)
        #print(f"Сервер запущен и слушает на {self._host}:{self._port}")
        #try:
            #while True:
                #client_sock, address = server_socket.accept()
                #print(f"Принято соединение от {address}")
                #client_handler = threading.Thread(
                    #target=handle_client,
                    #args=(client_sock,)  # Передаем сокет клиента в поток
                #)
                #client_handler.start()
        #finally:
            #server_socket.close()
        pass


if __name__ == "__main__":
    HOST = '127.0.0.1'  # IP-адрес сервера
    PORT = 8888  # порт сервера
    server = Server(HOST, PORT)
    server.start()