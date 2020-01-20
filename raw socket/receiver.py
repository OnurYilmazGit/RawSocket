import sys
from socket import *
from struct import *
 
#create an INET, STREAMing socket
try:
    s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
except error:
    print ('Socket could not be created.')
    sys.exit()
 
# receive a packet

#host = ''

source_ip = '10.0.2.5'

host = gethostname()

s.bind((host,IPPROTO_UDP))

outdata = ""

file_name='2.mp4'

f=open(file_name,"w+")

while True:
    print('Data recieved')
    packet = s.recvfrom(65535)
    #print(packet) 
    #packet string from tuple
    packet = packet[0]
    
    #take first 20 characters for the ip header
    ip_header = packet[0:20]
    #print(packet)
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
     
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    #print(2)
    iph_length = ihl * 4
     
    ttl = iph[5]
    protocol = iph[6]
    s_addr = inet_ntoa(iph[8]);
    d_addr = inet_ntoa(iph[9]);
    
    if str(s_addr) == source_ip:
		udp_header = packet[iph_length:iph_length+8]
		udph = unpack('!HHHH',udp_header)
		source_port = udph[0]
		dest_port = udph[1]
		udp_length = udph[2]
		checksum = udph[3]
		data_size = len(packet) - 28
		print ('Packet size : ',len(packet))
		print ('Data size : ',data_size)
		data = packet[28:]
		if data[0:4] == "@#EN".encode():
			f.write(outdata)
			break
		else:
			outdata += data
        	     
