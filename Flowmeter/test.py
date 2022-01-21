# try:
#     print(future.result())
# except requests.ConnectTimeout:
#     print("ConnectTimeout.")


import asyncio, time
import socketserver
import struct
import time
import os, sys

lists = []
sn_modem = b""


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.request.settimeout(5)

    def handle(self):
        # print(self.client_address[0])
        self.data = self.request.recv(1024)
        time_1 = time.time()
        if (self.data.isdigit()):
            # if (sn_modem == self.data[-4:]):
            #     print(self.data)
            #     sn_modem == self.data[-4:]
                b = struct.pack('BBBBBBBB', 0x01, 0x03, 0x00, 0x71, 0x00, 0x02, 0x94, 0x10)
                # b=struct.pack('BBBBBBBB', 0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B)
                # b=struct.pack('BBBBBBBB', 0x01, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xCB)

                # b=struct.pack('BBBBBBBB', 0x01, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD5, 0xCA) #Level METER
                # b=struct.pack('BBBBBBBB', 0x05, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC5, 0x8F) #QUQUMBOY
                # b=struct.pack('BBBBBBBB', 0x05, 0x03, 0x00, 0x10, 0x00, 0x02, 0xC4, 0x4A) #QUQUMBOY
                self.request.send(b)
                response = self.request.recv(512)
                print(response)
                data = struct.unpack('>f', response[3:-2])
                # data=struct.unpack('>I',response[3:-2]) # QUQUMBOY
                print(data[0])

                print("-------------------------------------")
                self.finish()

    def handle_timeout(self):
        print('error timeout')
        print("-------------------------------------")


if __name__ == "__main__":
    HOST, PORT = "", 7777
    try:
        # if (len(sys.argv) > 0):
        #     sn_modem = (sys.argv[1]).encode()
        server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler, bind_and_activate=False)
        server.allow_reuse_address = True
        server.daemon_threads = True
        server.server_bind()
        server.server_activate()
        server.timeout = 7
        server.serve_forever()
    except OSError:
        print(" OS error")
        server.socket.close()

    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

