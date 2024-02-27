
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class MockFTPServer(FTPServer):
    ROOT = './server_root'
    HOST = '127.0.0.1'
    PORT = 21

    @classmethod
    def get_authorizer(cls):
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(cls.ROOT)
        return authorizer

    @classmethod
    def get_handler(cls):
        handler = FTPHandler
        handler.authorizer = cls.get_authorizer()
        return handler

    def __init__(self):
        handler = MockFTPServer.get_handler()
        bind = (MockFTPServer.HOST, MockFTPServer.PORT)
        super().__init__(bind, handler, None, 5)

if __name__ == '__main__':
    server = MockFTPServer()
    server.serve_forever(handle_exit=True)

