from socket import *
import struct
import sys
import time

socket = socket(AF_INET,SOCK_RAW,IPPROTO_RAW)

# now start constructing the packet
packet = '';
source_ip = '10.0.2.6'
dest_ip = '10.0.2.5'

#ip header fields
ip_ihl = 5
ip_ver = 4
ip_tos = 0
ip_tot_len = 0  # kernel will fill the correct total length
ip_id = 54321   #Id of this packet
ip_frag_off = 0
ip_ttl = 255
ip_proto  = IPPROTO_TCP
ip_check = 0    # kernel will fill the correct checksum
ip_saddr = inet_aton(source_ip)   #Spoof the source ip address if you want to
ip_daddr = inet_aton(dest_ip)

ip_ihl_ver = (ip_ver << 4) + ip_ihl

# the ! in the pack format string means network order
ip_header = struct.pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

socket.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

#data = 'string'.encode()
sport = 4711    # arbitrary source port
dport = 50002   # arbitrary destination port


checksum = 0

##H:unsinged short 2 bytes


#socket.bind(('', dport))            # Bind to the port
  

file_name= "1.mp4"

#print(sys.argv[1])

f=open(file_name,"rb")
data = f.read(1024)

while (data):
    #print(data)
    #time.sleep(0.00001)
    length = 8+len(data);
    udp_header = struct.pack('!HHHH', sport, dport, length, checksum)
    packet = ip_header + udp_header + data
    socket.sendto(packet, ('10.0.2.5',50002))    
    print ("sending ...")
    data = f.read(1024)
#time.sleep(0.00001)
data = "@#EN".encode()
length = 8+len(data)
udp_header = struct.pack('!HHHH', sport, dport, length, checksum)
packet = ip_header + udp_header + data
socket.sendto(packet, ('10.0.2.5',50002))  
print("Sending last packet")
socket.close()
f.close()
