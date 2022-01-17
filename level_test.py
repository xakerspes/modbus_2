import asyncio, time
import socketserver
import struct
import time
import os,sys
lists = []
sn_modem = b""
class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.request.settimeout(5)
    def handle(self):
        #print(self.client_address[0])
        self.data = self.request.recv(1024)
        time_1 = time.time()
        if(self.data.isdigit()):
            if(sn_modem in self.data):
                print(self.data)
                # sn_modem == self.data[0:4]
                b=struct.pack('BBBBBBBB', 0x01, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD5, 0xCA) #Level METER
                self.request.send(b)
                response=self.request.recv(512)
                print(response)
                data=struct.unpack('>h',response[3:-2])
                # print(int(data[0]-1116)/10)
                print(data[0])
               
                print("-------------------------------------")
                self.finish()
    def handle_timeout(self):
        print('error timeout')
        print("-------------------------------------")
               

if __name__ == "__main__":
    HOST, PORT = "", 1010
    try:
        if (len(sys.argv)>0):
            sn_modem = (sys.argv[1]).encode() 
        server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler, bind_and_activate=False)
        server.allow_reuse_address = True
        server.daemon_threads = True
        server.server_bind()
        server.server_activate()
        server.timeout = 7 
        server.serve_forever()

    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()
