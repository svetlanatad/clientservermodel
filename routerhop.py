import socket
import time
import random

router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router.bind(("localhost", 8100))

router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8200))

router_mac = "05:10:0A:CB:24:EF"

# Define potential IPs for source IP hopping
hopping_ips = [
    "192.168.0.1",
    "192.168.0.2",
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
]

server = ("localhost", 8000)

client1_ip = "92.10.10.15"
client1_mac = "32:04:0A:EF:19:CF"
client2_ip = "92.10.10.20"
client2_mac = "10:AF:CB:EF:19:CF"
client3_ip = "92.10.10.25"
client3_mac = "AF:04:67:EF:19:DA"

router_send.listen(4)

# Connection placeholders
client1 = None
client2 = None
client3 = None

# Accept client connections
while (client1 == None or client2 == None or client3 == None):
    client, address = router_send.accept()
    
    if client1 == None:
        client1 = client
        print("Client 1 is online")
    
    elif client2 == None:
        client2 = client
        print("Client 2 is online")
    
    else:
        client3 = client
        print("Client 3 is online")

# ARP tables for clients' MAC addresses and sockets
arp_table_socket = {
    client1_ip: client1,
    client2_ip: client2,
    client3_ip: client3
}

arp_table_mac = {
    client1_ip: client1_mac,
    client2_ip: client2_mac,
    client3_ip: client3_mac
}

# Connect the router to the server
router.connect(server) 

# Router loop to receive, modify, and forward packets with IP hopping
while True:
    # Receive a packet from the server
    received_message = router.recv(1024)
    received_message = received_message.decode("utf-8")
    
    source_mac = received_message[0:17]
    destination_mac = received_message[17:34]
    source_ip = received_message[34:45]
    destination_ip = received_message[45:56]
    message = received_message[56:]
    
    print("Received packet:")
    print(" Source MAC address:", source_mac)
    print(" Destination MAC address:", destination_mac)
    print(" Source IP address:", source_ip)
    print(" Destination IP address:", destination_ip)
    print(" Message:", message)
    
    # Choose a new source IP randomly from the hopping IPs
    new_source_ip = random.choice(hopping_ips)
    
    # Create new headers with the new source IP
    ethernet_header = router_mac + arp_table_mac[destination_ip]
    IP_header = new_source_ip + destination_ip
    
    # Create the packet with the new IP header
    packet = ethernet_header + IP_header + message
    
    # Find the appropriate client socket
    destination_socket = arp_table_socket[destination_ip]
    
    # Send the packet to the client
    destination_socket.send(bytes(packet, "utf-8"))
    
    time.sleep(2)  # Simulate a delay between packets

