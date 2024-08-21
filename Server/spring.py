import os
import subprocess

def start_server():
    print("Iniciando el servidor Spring Boot ...")
    stop_server()
    subprocess.run([
        "docker", "run", "-d", "--name", "springboot-container", "-p", "8080:8080",
        "server-springboot"
    ])

def stop_server():
    subprocess.run(["docker", "stop", "springboot-container"], stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "rm", "springboot-container"], stderr=subprocess.DEVNULL)

def main():
    start_server()
    os.system('clear')
    print("\n----------------------------------------")
    print(" SERVIDOR SPRING BOOT EJECUTÁNDOSE - LOCAL")
    print("----------------------------------------\n")
    
    while True:
        user_input = input(f"Escribe 'exit' para detener el servidor... ")

        if user_input.lower() == "exit":
            break

    stop_server()

if __name__ == "__main__":
    main()
