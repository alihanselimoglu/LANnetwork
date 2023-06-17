import socket
import json
import os
import time

def read_dictionary_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def combine_chunks(chunks, output_file):
    with open(output_file, 'wb') as f:
        for chunk in chunks:
            f.write(chunk)

def log_downloaded_chunk(chunk_name, ip_address):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("download_log.txt", "a") as log_file:
        log_file.write(f"{timestamp}, {chunk_name}, {ip_address}\n")
        
def download_chunk(ip, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 5001))
        s.sendall(filename.encode('utf-8'))  # Send the requested chunk name
        data = b''
        while True:
            packet = s.recv(1024)
            if not packet:
                break
            data += packet
        with open(filename, 'wb') as f:
            f.write(data)
        return data

def start_downloader(content_name):
    content_dictionary = read_dictionary_from_file('content_dictionary.json')
    print("Starting downloader...")
    chunks = []
    for chunk_name in sorted(content_dictionary.keys()):
        ips = content_dictionary[chunk_name]
        chunk_downloaded = False
        for ip in ips:  
            try:
                chunk = download_chunk(ip, chunk_name)
                chunks.append(chunk)
                log_downloaded_chunk(chunk_name, ip)
                chunk_downloaded = True
                break
            except Exception as e:
                print(f"Failed to download {chunk_name} from {ip}: {e}")
            if not chunk_downloaded:
                print(f"CHUNK {chunk_name} CANNOT BE DOWNLOADED FROM ONLINE PEERS.")
                return
    combine_chunks(chunks, f'downloaded_{content_name}')
    print(f"{filepath} has been successfully downloaded.")

if __name__ == "__main__":
    filepath = input("Enter the content name to download (or type 'exit' to quit): ")
    chunksize = 1024  # Adjust as needed
    content_name = 'ad.png'

    start_downloader(content_name)
