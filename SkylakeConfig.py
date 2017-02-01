#-*- coding: utf-8 -*-

def get_status_info(status):
    if type(status) != str:
        status = str(status)
    status_code = {}
    status_code['100'] = 'Continue'
    status_code['200'] = 'OK'
    status_code['201'] = 'Created'
    status_code['204'] = 'No Content'
    status_code['206'] = 'Partial Content'
    status_code['301'] = 'Moved Permanently'
    status_code['302'] = 'Found'
    status_code['303'] = 'See Other'
    status_code['304'] = 'Not Modified'
    status_code['307'] = 'Temporary Redirect'
    status_code['400'] = 'Bad Request'
    status_code['401'] = 'Unauthorized'
    status_code['403'] = 'Forbidden'
    status_code['404'] = 'Not Found'
    status_code['405'] = 'Method Not Allowed'
    status_code['408'] = 'Request Timeout'
    status_code['410'] = 'Gone'
    status_code['411'] = 'Length Required'
    status_code['413'] = 'Request Entity Too Large'
    status_code['414'] = 'Request-url Too Long'
    status_code['500'] = 'Internal Server Error'
    status_code['501'] = 'Not Implemented'
    status_code['502'] = 'Bad Gateway'
    status_code['503'] = 'Service Unavailable'
    status_code['504'] = 'Gateway Timeout'
    status_code['505'] = 'HTTP Version Not Supported'
    if status in status_code.keys():
        return status_code[status]
    else:
        return 'Unknown'

def get_server_config():
    config = {}
    config['MAX_LENGTH'] = 102400
    config['TIMED_OUT'] = 10
    config['GZIP'] = True
    config['GZIP_MIN'] = 5
    config['GZIP_TYPE'] = 'text/html,text/plain,text/css,text/xml,text/javascript,text/x-component,application/json,application/javascript,application/xml,application/xhtml+xml,application/xml+rss,application/rss+xml,application/atom+xml,application/x-font-ttf,application/x-web-app-manifest+json,font/opentype,image/svg+xml,image/x-icon'
    config['ENABLE_LOG'] = False
    config['LOG_PATH'] = 'G:/skylake.log'
    config['0'] = {}
    config['0']['MODE'] = 'CGI'
    config['0']['CGI_SUFFIX'] = {'.py': 'python.exe','.php': 'php-cgi.exe'}
    config['0']['HOME_PATH'] = 'D:/phpstudy/www111'
    config['0']['DENIED_SUFFIX'] = ('.py')
    config['0']['DEFAULT_PAGE'] = 'index.php,index.html,index.htm'
    config['0']['DIR_LIST'] = True
    config['0']['BIND_HOST'] = '127.0.0.1:8888'
    return config
	
def get_error_page():
    page = {}
    return page
	
def get_mime_type():
    mime = {}
    mime['.html'] = 'text/html'
    mime['.htm'] = 'text/html'
    mime['.xml'] = 'text/xml'
    mime['.xhtml'] = 'application/xhtml+xml'
    mime['.txt'] = 'text/plain'
    mime['.py'] = 'text/plain'
    mime['.php'] = 'text/plain'
    mime['.c'] = 'text/plain'
    mime['.rtf'] = 'application/rtf'
    mime['.pdf'] = 'application/pdf'
    mime['.doc'] = 'application/msword'
    mime['.docx'] = 'application/msword'
    mime['.png'] = 'image/png'
    mime['.gif'] = 'image/gif'
    mime['.jpeg'] = 'image/jpeg'
    mime['.jpg'] = 'image/jpeg'
    mime['.au'] = 'audio/basic'
    mime['.midi'] = 'audio/midi,audio/x-midi'
    mime['.mid'] = 'audio/midi,audio/x-midi'
    mime['.ra'] = 'audio/x-pn-realaudio'
    mime['.ram'] = 'audio/x-pn-realaudio'
    mime['.mpg'] = 'video/mpeg'
    mime['.mpeg'] = 'video/mpeg'
    mime['.avi'] = 'video/x-msvideo'
    mime['.gz'] = 'application/x-gzip'
    mime['.tar'] = 'application/x-tar'
    mime['.mp3'] = 'audio/mpeg'
    mime['.wav'] = 'audio/x-wav'
    mime['.bmp'] = 'image/bmp'
    mime['.svg'] = 'image/svg+xml'
    mime['.tif'] = 'image/tiff'
    mime['.tiff'] = 'image/tiff'
    mime['.ico'] = 'image/x-icon'
    mime['.css'] = 'text/css'
    mime['.js'] = 'application/x-javascript'
    mime['.woff'] = 'application/font-woff'
    return mime
