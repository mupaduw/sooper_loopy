
"""
Small example OSC client
This program swithes between 2 sooperloopers. 
"""
import argparse
import random
import time
import threading
import math

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

def start_server(ip, port, dispatcher):
    print("Starting Server")
    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

def start_clients(ip, ports):
    print("Starting Client")
    clients = [udp_client.SimpleUDPClient(ip, port) for port in ports]
    # print("Sending on {}".format(client.))
    thread = threading.Thread(target=switch_values(clients))
    thread.start()

# send random values between 0-1 to the three addresses
def switch_values(clients):        
    looper = True
    sl = int(looper)
    x = 0
    for i in range(9):
        x = random.randrange(2300, 2800)
        time.sleep(x/1000)

        #select all current looper
        # clients[sl].send_message("/sl/-1/forceup", ['mute'])
        clients[sl].send_message("/sl/-1/hit", ['pause'])
        
        #select new looper
        looper = not looper
        sl = int(looper)
        clients[sl].send_message("/sl/-1/hit", ['trigger'])

    #stop ...
    time.sleep(x/1000)
    clients[sl].send_message("/sl/-1/hit", ['pause'])



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--serverport", type=int, default=5050, help="The port the OSC Server is listening on")    
    parser.add_argument("--looperip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--looperport1", type=int, default=9951,
                        help="The port the sooperlooper server 1 is listening on")
    parser.add_argument("--looperport2", type=int, default=9952,
                        help="The port the sooperlooper server 2 is listening on")
    args = parser.parse_args()

    clients =[
        udp_client.SimpleUDPClient(args.looperip, args.looperport1),
        udp_client.SimpleUDPClient(args.looperip, args.looperport2)]

    # setup callback handlers
    dispatcher = dispatcher.Dispatcher()

    #start server for callbacks
    start_server(args.serverip, args.serverport, dispatcher)
    start_clients(args.looperip, [args.looperport1, args.looperport2])
 