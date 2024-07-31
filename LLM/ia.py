import os
import subprocess
import json
import requests

# Establecer VALORES API de ChatGPT Local

def start_ia():
    print("Iniciando IA ...")
    stop_ia()
    subprocess.run([
        "docker", "run", "-d", "--name", "sclgpt", "-ti", "-p", "5000:5000",
        "-v", f"{os.getcwd()}/llama-2-7b-chat.Q2_K.gguf:/app/llama-2-7b-chat.Q2_K.gguf", "llama2"
    ])

def stop_ia():
    subprocess.run(["docker", "stop", "sclgpt"], stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "rm", "sclgpt"], stderr=subprocess.DEVNULL)


def main():
    start_ia()
    os.system('clear')
    print("\n----------------------------------------")
    print(" LLAMA 2 RUNNING - LOCAL API")
    print("----------------------------------------\n")
    
    while True:
        # Solicitar una pregunta al usuario
        scl_pregunta = input(f"Type 'exit' to abort the model... ")

        # Si escribe "salir", salimos del programa
        if scl_pregunta.lower() == "exit":
            break

    stop_ia()

if __name__ == "__main__":
    main()
