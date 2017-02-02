#-*- coding: utf-8 -*-

import os,sys,socket,platform,errno,time,SkylakeResponseHandler
from urllib import unquote
from getpass import getuser
from SkylakeConfig import *

class SkylakeServer(object):
    def __init__(self, bind_parameter):
        self.server_config = get_server_config()
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(bind_parameter)
        self.listen_socket.listen(2)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.gethostname()
        self.server_addr = socket.gethostbyname(self.server_name)
        self.server_port = port
        self.isWindowsSystem = 'Windows' in platform.system()
        self.headers_array = []
        
        
    def set_app(self, application):
        self.application = application    
    
    def get_env(self):
        env = {}
        env['REQUEST_METHOD'] = self.req_method
        env['REQUEST_URI'] = self.req_uri
        env['REQUEST_HOST'] = self.req_host
        env['REQUEST_BODY'] = self.req_body
        env['REQUEST_HEADERS'] = self.req_headers
        env['USER-AGENT'] = ''
        env['HTTP_ACCEPT'] = '*/*'
        env['HTTP_ACCEPT_ENCODING'] = ''
        env['HTTP_ACCEPT_LANGUAGE'] = ''
        env['HTTP_COOKIE'] = ''
        for i in self.req_headers.keys():
            if i.lower() == 'user-agent':
                env['USER-AGENT'] = self.req_headers[i]
            elif i.lower() == 'accept':
                env['HTTP_ACCEPT'] = self.req_headers[i]
            elif i.lower() == 'accept-encoding':
                env['HTTP_ACCEPT_ENCODING'] = self.req_headers[i]
            elif i.lower() == 'accept-language':
                env['HTTP_ACCEPT_LANGUAGE'] = self.req_headers[i]
            elif i.lower() == 'cookie':
                env['HTTP_COOKIE'] = self.req_headers[i]
        env['CLIENT_ADDR'] = self.client_addr
        env['CLIENT_PORT'] = self.client_port
        env['HTTP_VERSION'] = self.req_protocol
        env['SERVER_NAME'] = self.server_name
        env['SERVER_ADDR'] = self.server_addr
        env['SERVER_PORT'] = str(self.server_port)
        return env
        
    def handle_single_req(self):
        firstloop = True
        recv_length = 4096
        self.client_conn.setblocking(0)
        self.client_conn.settimeout(self.server_config['TIMED_OUT'])
        try:
            while True:
                if firstloop == False:
                    if length_remain < recv_length:
                        recv_length = length_remain
                buffer = self.client_conn.recv(recv_length)
                if firstloop == True:
                    if self.parse_req_header(buffer) == False:
                        return False
                    firstloop = False
                    if len(buffer) < recv_length and not buffer.endswith('\r\n'):
                        break
                    elif self.req_method not in ('GET','DELETE'):
                        length_remain = self.req_body_length - len(self.req_body)
                        continue
                if self.req_method not in ('GET','DELETE'):
                    self.req_body += buffer
                    length_remain -= len(buffer)
                    if length_remain == 0:
                        break
                if len(buffer) < recv_length and self.req_method in ('GET','DELETE'):
                    break
        except:
            return False
            
        if 'ENABLE_LOG' not in self.server_config.keys():
            self.log_error('[ERROR]ENABLE_LOG required')
            self.set_error(500)
            return False
        else:
            if self.server_config['ENABLE_LOG'] == True:
                if 'LOG_PATH' not in self.server_config.keys():
                    self.log_error('[ERROR]Log path not set')
                    self.set_error(500)
                    return False
                
        self.req_body = self.req_body
        try:
            SRH = SkylakeResponseHandler.SkylakeResponseHandler(self.get_env())
        except:
            self.log_error('[ERROR]ResponseHandler reported an error')
            self.set_error(500)
            return False
        status, response_headers, response_body, no_CT = SRH.response_handler()
        if self.server_config['ENABLE_LOG'] == True:
            try:
                f = open(self.server_config['LOG_PATH'],'a')
                f.write('['+time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime(time.time()))+']IP='+self.client_addr+' UA='+self.get_env()['USER-AGENT']+' URI='+self.req_uri+' STATUS='+str(status)+'\n')
                f.close()
            except:
                self.log_error('[ERROR]Can not write access log')
        self.start_response(status, response_headers)
        self.finish_response(response_body, no_CT=no_CT)

    def parse_req_header(self, req_data):
        lines = req_data.split("\n")
        self.req_headers = {}
        self.req_host = ''
        self.req_body = ''
        self.req_body_length = 0
        flag = False
        for i in range(0,len(lines)):
            if i == 0:
                basic_info = lines[i].split()
                if len(basic_info) != 3:
                    self.set_error(400)
                    return False
                if basic_info[0] not in ('GET','POST','PUT','DELETE'):
                    self.set_error(501)
                    return False
                self.req_method = basic_info[0]
                if '/' not in basic_info[1]:
                    self.set_error(400)
                    return False
                if len(basic_info[1]) > 1024:
                    self.set_error(414)
                    return False
                self.req_uri = unquote(basic_info[1])
                if 'HTTP/' not in basic_info[2]:
                    self.set_error(400)
                    return False
                protocol = basic_info[2].split('/')
                if len(protocol) != 2 or protocol[1] not in ('1.0','1.1'):
                    self.set_error(505)
                    return False
                self.req_protocol = protocol[1]
                continue
            if lines[i] == "\r":
                flag = True
                continue
            if flag == False:
                offset = lines[i].find(':')
                header_key = lines[i][:offset]
                header_val = unquote(lines[i][offset+1:])
                if header_val.startswith(' '):
                    header_val = header_val[1:]
                if ' ' in header_key:
                    self.set_error(400)
                    return False
                self.req_headers[header_key] = header_val.replace("\r",'')
                if header_key == 'Host':
                    self.req_host = header_val.replace("\r",'')
            if flag == True:
                if 'Content-Length' in self.req_headers.keys():
                    try:
                        self.req_body_length = int(self.req_headers['Content-Length'])
                        if self.req_body_length > self.server_config['MAX_LENGTH']:
                            self.set_error(413)
                            return False
                    except ValueError:
                        self.set_error(400)
                        return False
                else:
                    if self.req_method not in ('GET','DELETE'):
                        self.set_error(411)
                        return False
                self.req_body += lines[i]
                if len(self.req_body) >= self.req_body_length:
                    self.req_body = self.req_body[:self.req_body_length]
                if len(self.req_body) == 0 and self.req_body_length > 0 and self.req_method not in ('GET','DELETE'):
                    self.send_continue()
                    
    def set_error(self, status):
        error_page = get_error_page()
        if str(status) in error_page.keys():
            if os.path.isfile(error_page[str(status)]):
                page = open(error_page[str(status)]).read()
        else:
            page = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>HTTP Error '+str(status)+'</title></head><body><div id="main"><i><h2>Something error:</h2></i><p><h3>HTTP Error '+str(status)+'</h3><h3><font color=red>'+get_status_info(status)+'.</font></h3></p><p>Please check or <a href="javascript:location.reload()">try again</a> later. </p>hostname: '+self.get_env()['SERVER_NAME']+'<hr><div id="pb">Generated by Skylake/0.1</a>.</div></div></body></html>'
        self.start_response(status=status, response_headers=[('Content-Type', 'text/html;charset=utf-8')])
        self.finish_response(response_body=page)

    def start_response(self, status, response_headers=[]):
        server_headers = [
            ('Server', 'Skylake/0.1'),
            ('Date', time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.localtime(time.time()-28800))),
            ('Vary', 'Accept-Encoding')
        ]
        self.headers_array = [status, get_status_info(status), response_headers+server_headers]
    
    def finish_response(self, response_body='', head_only=False, no_CT=False):
        try:
            status, info, headers_array = self.headers_array
            if no_CT == False:
                headers_array.append(('Content-Length', len(response_body)))
                if 'Connection' in self.req_headers.keys():
                    if self.req_headers['Connection'] == 'keep-alive':
                        headers_array.append(('Keep-Alive', 'timeout='+str(self.server_config['TIMED_OUT'])))
                        
            response = 'HTTP/1.1 {status} {info}\r\n'.format(status=status,info=info)
            if head_only == False:
                for header in headers_array:
                    response += '{0}: {1}\r\n'.format(*header)
                response += '\r\n'
                response += response_body
                response += '\r\n'
            response += '\r\n'
            try:
                self.client_conn.sendall(response)
            except socket.error as e:
                return False
        finally:
            try:
                if 'Connection' in self.req_headers.keys():
                    if self.req_headers['Connection'] != 'keep-alive':
                        self.client_conn.close()
                else:
                    self.client_conn.close()
            except AttributeError as e:
                self.client_conn.close()
    
        
    def send_continue(self):
        self.start_response(status='100')
        self.finish_response(head_only=True)

    def serve_forever(self):
        if not self.isWindowsSystem:
            import signal
            def grim_reaper(signum, frame):
                while True:
                    try:
                        pid, status = os.waitpid(-1, os.WNOHANG)
                    except OSError:
                        return
                    if pid == 0:
                        return
        
            signal.signal(signal.SIGCHLD, grim_reaper)    
        listen_socket = self.listen_socket
        while True:
            try:
                self.client_conn, client_address = listen_socket.accept()
                print '[INFO]New client connected '+client_address[0]
                self.client_addr = client_address[0]
                self.client_port = client_address[1]
            except IOError as e:
                if not self.isWindowsSystem:
                    code, msg = e.args
                else:
                    code = e.args
                if code == errno.EINTR:
                    continue
                else:
                    raise

            if not self.isWindowsSystem:
                pid = os.fork()
                if pid == 0:
                    listen_socket.close()
                    self.handle_single_req()
                    os._exit(0)
                else:
                    #self.client_conn.close()
                    pass
            else:
                self.handle_single_req()
                
    def log_error(self, error):
        try:
            f = open('error.log','a')
            f.write('['+time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime(time.time()))+']'+error+'\n')
            f.close()
        except:
            print '[WARNING]Can not write error log at current dir'

        print error

            