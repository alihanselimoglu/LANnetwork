import socket
import json
import os
import time
from datetime import datetime

content_dictionary = {}

def write_dictionary_to_file(dictionary, filename):
    with open(filename, 'w') as f:
        json.dump(dictionary, f)

def start_discovery():
    global content_dictionary
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('0.0.0.0', 5001))
        while True:
            data, addr = s.recvfrom(1024)
            chunks = json.loads(data)["chunks"]
            for chunk in chunks:
                if chunk not in content_dictionary:
                    content_dictionary[chunk] = []
                content_dictionary[chunk].append(addr[0])
            print("Updated content dictionary: ", content_dictionary)
            write_dictionary_to_file(content_dictionary, 'content_dictionary.json')

if __name__ == "__main__":
    filepath = 'ad.png'
    chunksize = 1024  # Adjust as needed
    content_name = 'ad.png'

    start_discovery()