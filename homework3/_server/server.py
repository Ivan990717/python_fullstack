from _server.src.ioserver import IoServer
from _server.src.wangpan import Pan

if __name__ =="__main__":
    server = IoServer()
    server.run_server(Pan)
