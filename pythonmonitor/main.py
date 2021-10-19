import grpc
import sys
import os
import time
import select
import secrets

from blessed import Terminal
from concurrent import futures
# I don't like this, but it is the simplest way to grab the proto files.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'protobuf'))

from proto import status_pb2
from proto import statusservice_pb2_grpc

from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.highlighter import Highlighter
from random import randint

term = Terminal()

class Menu:
    def __init__(self):
        self.selected = ""
        self.selected_idx = 0
        self.items = []
    def set_items(self, newItems):
        self.items = newItems
        self.selected_idx = (self.selected_idx) % len(self.items)
        self.selected = self.items[self.selected_idx]
    def next(self):
        if not self.items or len(self.items) == 0:
            return
        self.selected_idx = (self.selected_idx + 1) % len(self.items)
        if self.selected_idx < len(self.items):
            self.selected = self.items[self.selected_idx]
    def prev(self):
        if not self.items:
            return
        self.selected_idx = (self.selected_idx - 1) % len(self.items)
        self.selected = self.items[self.selected_idx]
    def layout(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="right")
        for idx, item in enumerate(self.items):
            grid.add_row(f"[green]> {item}" if item == self.selected else item)
        return Panel(grid, padding=1)

class Node:
    def __init__(self, node):
        #todo: add the rest of these boys as the params become available. Probably could short circuit out of this if the schema is legit.
        self.name = node.name
        
        #these are just arbitrary parameters. The UI will draw whatever is in node.
        signs = ['leo', 'cancer', 'donner', 'blitson', "salsa"]
        self.zodiac_sign = secrets.choice(signs)
        self.baskets_of_cats = 10
        self.requests = 1
        
    def layout(self):
        info = Table.grid(expand=True)
        info.add_column()
        info.add_column(justify="right")
        for key,value in vars(self).items():
            info.add_row(key, f"[green]{value}")
        return Panel(info, padding=1)
        

class Monitor:
    def __init__(self):
        self.last_request_time = time.time()
        self.time_since_last_request = float('inf')
        self.total_requests_received = 0
        self.events = []
        self.msgs = []
        self.nodes = {}
        self.menu = Menu()
        self.dirty = True
        self.selected_menu = self.menu #will make it a bit easier if there's more menus later.
        
    def listen(self, request):
        self.total_requests_received += 1
        self.time_since_last_request = (time.time() - self.last_request_time)
        self.last_request_time = time.time()
        self.events.append(request)
        self.dirty = True #you can be smarter about this. Don't redraw if you aren't on a thing thats changed.
        
        if request.name in self.nodes:
            self.nodes[request.name].requests += 1
        else:
            self.nodes[request.name] = Node(request)
            #update menu keys with new nodes.
            self.menu.set_items(list(self.nodes.keys()))

    def draw(self):
        with Live(generate_ui(self), refresh_per_second=4) as live:
            with term.cbreak(), term.hidden_cursor():
                while True:
                    if self.dirty:
                        live.update(generate_ui(self), refresh=True)
                        self.dirty = False
                        
                    val = term.inkey(timeout=1)
                    if not val:
                       continue
                    elif val.is_sequence:
                        if val.name == "KEY_DOWN":
                            self.selected_menu.next()
                        elif val.name == "KEY_UP":
                            self.selected_menu.prev()
                        self.dirty = True
                        #live.update(update_ui(), refresh=True)
                       #print("got sequence: {0}.".format((str(val), val.name, val.code)))
                    elif val:
                       continue
                    
                    if self.dirty:
                        live.update(generate_ui(self), refresh=True)
                        self.dirty = False
                    
                print(f'bye!{term.normal}')
    def print(self, msg):
        self.msgs.append(msg)

def build_details(item) -> Layout:
    info = Table.grid(expand=True)
    info.add_column()
    info.add_column(justify="right")
    info.add_row("Request Frequency", f"[green]{round(60.125, 4)}hz")
    info.add_row("Requests Received", f"[green]{125125}")
    return Panel(info, padding=1)


def generate_ui(monitor) -> Layout:
    """Make a new table."""
    layout = Layout()
    header = Table.grid(expand=True)
    header.add_column(justify="center", ratio=1)
    header.add_row("Node Monitor")
    
    if(monitor.menu.selected in monitor.nodes):
        info = monitor.nodes[monitor.menu.selected].layout()
    else:
        info = Table.grid(expand=True)
        info.add_column()
        info.add_column(justify="right")
        info.add_row("Request Frequency", f"[green]{round(1.0 / monitor.time_since_last_request, 4)}hz")
        info.add_row("Requests Received", f"[green]{monitor.total_requests_received}")

    request_table = Table(expand=True)
    request_table.add_column("Last 10 Requests")
    
    #add the last 10 requests to a table.
    for event in monitor.events[-9:]:
        request_table.add_row(
            f"{event}"
        )
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="console", size=7),
    )
    
    layout["header"].update(header)
    #summary stats and the log
    layout["main"].split_row(
        Layout(monitor.menu.layout(), ratio=1),
        Layout(info, ratio=4),
        Layout(request_table, ratio=2)
    )
    #Layout(request_table)
    #print lines (monitor.print replaces print()) 

    console = Table.grid(expand=True)
    console.add_column(justify="left")
    for msg in monitor.msgs:
        console.add_row(
            f"{msg}"
        )
        
    layout["console"].update(Panel(console))
        
    return layout

class StatusSerivceServicer(statusservice_pb2_grpc.StatusServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, monitor):
        self.monitor = monitor
        monitor.print("initializing status service")

    def GetStatus(self, request, context):
        self.monitor.listen(request)

def run():
    monitor = Monitor()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    statusservice_pb2_grpc.add_StatusServiceServicer_to_server(
        StatusSerivceServicer(monitor), server)
    server.add_insecure_port('[::]:50051')
    
    server.start()
    monitor.draw()
    
    server.wait_for_termination()

if __name__ == '__main__':
    run()

