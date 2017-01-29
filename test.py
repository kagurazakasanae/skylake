import sys,Skylake

SERVER_ADDRESS = (HOST, PORT) = '', 8888
def make_server(server_address):
    server = Skylake.SkylakeServer(server_address)
    return server

if __name__ == '__main__':
    httpd = make_server(SERVER_ADDRESS)
    print('SkylakeWebServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()