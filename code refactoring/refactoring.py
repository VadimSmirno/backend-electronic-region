from urllib.parse import urlparse
import requests
import re
import base64


class HtmlCopyTo:

    def __init__(self, url, referer_url, user_agent, http_username, http_password):
        self.url = url
        self.referer_url = referer_url
        self.user_agent = user_agent
        self.http_username = http_username
        self.http_password = http_password
        self.data = None
        self.allowed_mime_types = ['image', 'text', 'application']
        self.real_extension = ''
        self.real_mime_type = ''
        self.real_charset = ''

    def save_file(self):
        # Реализация сохранения файла
        pass

    def set_response(self, response):
         # Реализация установки ответа
        pass

    def download_source(self):
        request_headers = {'User-Agent': self.user_agent}

        if self.referer_url:
            referer_parsed_url = urlparse(self.referer_url)
            self.scheme = referer_parsed_url.scheme
            self.host = referer_parsed_url.netloc
            request_headers['Referer'] = self.referer_url

        if self.http_username or self.http_password:
            auth_credentials = f"{self.http_username}:{self.http_password}".encode('ascii')
            base64_encoded_auth = base64.b64encode(auth_credentials).decode('utf-8')
            request_headers['Authorization'] = f'Basic {base64_encoded_auth}'

        try:
            response = requests.get(self.url, headers=request_headers)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            if content_type:
                mime_type = re.sub('[;].*$', '', content_type).strip().lower()
                mime_type = re.sub('/x-', '/', mime_type)

                if mime_type in self.allowed_mime_types:
                    self.data = response.content

                    extension = re.sub('^(image|text|application)\/', '', mime_type)
                    extension = re.sub('(windows[-]bmp|ms[-]bmp)', 'bmp', extension)
                    extension = re.sub('(svg[+]xml|svg[-]xml)', 'svg', extension)
                    extension = extension.replace('xhtml[+]xml', 'xhtml')
                    extension = extension.replace('jpeg', 'jpg')

                    self.real_extension = extension
                    self.real_mime_type = mime_type

                    charset_position = content_type.find(';')
                    if charset_position != -1:
                        self.real_charset = content_type[charset_position:].strip()

                    self.save_file()
                else:
                    self.set_response(f'error:Invalid mime-type: {content_type}')
            else:
                self.set_response('error:No mime-type defined')
        except requests.exceptions.RequestException as e:
            self.set_response(f'error:SOCKET: {str(e)}')
