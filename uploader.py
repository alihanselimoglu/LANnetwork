import socket
import json
import os
import time
from datetime import datetime

def serve_chunk(conn, chunk):
    with open(chunk, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data)

def log_request(request, addr):
    with open('uploader_log.txt', 'a') as f:
        log_entry = f"{datetime.now()}: Received request from {addr} for {request}\n"
        f.write(log_entry)

def start_uploader():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 5000))
        s.listen()
        print('Uploader is ready and listening')
        while True:
            conn, addr = s.accept()
            print('Connection established')
            with conn:
                data = conn.recv(1024)
                request = json.loads(data)
                chunk = request["requested_content"]
                print('Processing request')

                # Log the request
                log_request(chunk, addr)

                serve_chunk(conn, chunk)

if __name__ == "__main__":
    filepath = 'ad.png'
    chunksize = 1024
    content_name = 'ad.png'
    content_dictionary = {}

    # Run each of these functions in separate threads or processes:
    start_uploader()
