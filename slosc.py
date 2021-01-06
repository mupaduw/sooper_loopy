
"""Small example OSC client
This program does some basic interactions with sooperlooper. 
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

def handle_wet(unused_addr, args, value1, value2):
    db = 20 * math.log10(float(value2))
    print('handle_wet', args, value1, value2, db)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--serverport", type=int, default=5050, help="The port the OSC Server is listening on")    
    parser.add_argument("--looperip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--looperport", type=int, default=9951,
                        help="The port the sooperlooper server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.looperip, args.looperport)

    # setup callback handlers
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/sooper/loopcount/new", print)
    dispatcher.map("/sooper/sync_source/new", print)
    dispatcher.map("/sooper/wet/new", handle_wet)

    #start server for callbacks
    start_server(args.serverip, args.serverport, dispatcher)
    # start_client(args.looperip, args.looperport)
    
    #register for loopcount updates with sooper
    client.send_message("/register", 
         ["osc.udp://%s:%s/" % (args.serverip, args.serverport),
         "/sooper/loopcount/new"])

    #register for sync_source
    #sync_source  :: -3 = internal,  -2 = midi, -1 = jack, 0 = none, # > 0 = loop number (1 indexed) 
    client.send_message("/register_update", 
         ["sync_source",
         "osc.udp://%s:%s/" % (args.serverip, args.serverport),
         "/sooper/sync_source/new"])

    #register for output volume
    client.send_message("/register_update", 
         ["wet",
         "osc.udp://%s:%s/" % (args.serverip, args.serverport),
         "/sooper/wet/new"])

    #create a new loop 
    client.send_message("/loop_add", [2, 14.0,])

    #set tempo
    client.send_message("/set", ["tempo", 100.6])

    #set master volume
    # ref https://stackoverflow.com/a/31598914
    db = -0.0
    slval = 10 ** (db/20)
    client.send_message("/set", ["wet", slval])