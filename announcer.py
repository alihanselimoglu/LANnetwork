import socket
import json
import os
import math
import time
import threading

def get_broadcast_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    broadcast_ip = local_ip.rsplit('.', 1)[0] + '.255'
    return broadcast_ip

def chunk_files(filepath, num_chunks):
    file_chunks = []
    file_size = os.path.getsize(filepath)
    chunk_size = math.ceil(file_size / num_chunks)

    with open(filepath, 'rb') as f:
        for i in range(num_chunks):
            chunk_filename = f"{filepath}_{i+1}"
            chunk_data = f.read(chunk_size)
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk_data)
            file_chunks.append(chunk_filename)

    return file_chunks


def start_announcer(file_chunks):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            message = json.dumps({"chunks": file_chunks}).encode('utf-8')
            s.sendto(message, (get_broadcast_ip(), 5001))
            time.sleep(60)

def serve_chunks(port, file_chunks):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(5)
        print(f"Listening for incoming connections on port {port}...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                requested_chunk = conn.recv(1024).decode('utf-8')
                if requested_chunk in file_chunks:
                    with open(requested_chunk, 'rb') as f:
                        data = f.read()
                        conn.sendall(data)
                else:
                    print(f"Requested chunk {requested_chunk} not found.")

if __name__ == "__main__":
    filepath = input("Please specify the file to be hosted: ")
    num_chunks = 5  # Divide the file into 5 chunks
    file_chunks = chunk_files(filepath, num_chunks)
    print(f"The file is divided into {len(file_chunks)} chunks: {file_chunks}")
    print("Starting to announce these files...")

    serve_chunks_thread = threading.Thread(target=serve_chunks, args=(5001, file_chunks))
    serve_chunks_thread.start()

    start_announcer(file_chunks)
