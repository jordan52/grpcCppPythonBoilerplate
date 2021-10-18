import grpc
import sys
import os
import time

from concurrent import futures
# I don't like this, but it is the simplest way to grab the proto files.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'protobuf'))

from proto import status_pb2
from proto import statusservice_pb2_grpc

from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel


def generate_ui(monitor) -> Table:
    """Make a new table."""
    layout = Layout()
    
    #summary statistics table
    info = Table.grid(expand=True)
    info.add_column()
    info.add_column(justify="right")
    info.add_row("Request Frequency", f"[green]{round(1.0 / monitor.time_since_last_request, 4)}hz")
    info.add_row("Requests Received", f"[green]{monitor.total_requests_received}")
    

    #todo: print monitor.msgs to a list.

    request_table = Table(title = "Last 10 Requests", expand=True)
    request_table.add_column("Request")
    
    #add the last 10 requests to a table.
    for event in monitor.events[-9:]:
        request_table.add_row(
            f"{event}"
        )
        
        
    header = Table.grid(expand=True)
    header.add_column(justify="center", ratio=1)
    header.add_row("[b]Node Monitor")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="console", size=7),
    )
    
    layout["header"].update(header)
    #summary stats and the log
    layout["main"].split_row(
        Layout(info),
        Layout(request_table)
    )
    
    #print lines (monitor.print replaces print()) 
    #TODO: check and see if you can redirect standard out here..
    
    console = Table.grid(expand=True)
    console.add_column(justify="left")
    for msg in monitor.msgs:
        console.add_row(
            f"{msg}"
        )
        
    layout["console"].update(Panel(console))
        
    return layout
    
class Monitor:
    def __init__(self):
        self.last_request_time = time.time()
        self.time_since_last_request = float('inf')
        self.total_requests_received = 0
        self.events = []
        self.msgs = []
    def listen(self, event):
        self.total_requests_received += 1
        self.time_since_last_request = (time.time() - self.last_request_time)
        self.last_request_time = time.time()
        self.events.append(event)
    def draw(self):
        with Live(generate_ui(self), refresh_per_second=4, screen=True) as live:
            while True:
                time.sleep(0.1)
                live.update(generate_ui(self))
    def print(self, msg):
        self.msgs.append(msg)
    

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

