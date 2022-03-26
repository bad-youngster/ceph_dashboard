# -*- coding: utf-8 -*-
import json
from socket import socket
from threading import Thread
from channels.generic.websocket import WebsocketConsumer
import paramiko


class StreamConsumer(object):
    def __init__(self, websocket):
        self.websocket = websocket

    def connect(self, host_ip, host_port=22, sys_user_name='root', sys_user_passwd='donotuseroot!', term='xterm', cols=140, rows=50):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(host_ip, host_port,
                               sys_user_name, sys_user_passwd, timeout=60)
            # print("connect success")
        except Exception as e:
            message = str(e)
            self.websocket.send(message)
            # print("connect faild")
            return False
        try:
            transport = ssh_client.get_transport()
            transport.set_keepalive(60)
            self.ssh_channel = transport.open_session()
            self.ssh_channel.get_pty(term=term, width=cols, height=rows)
            self.ssh_channel.invoke_shell()
            self.ssh_channel.transport.set_keepalive(30)
            msg = f"connect {sys_user_name}@{host_ip} \r\n"
            self.websocket.send(msg)
            # 经多次实现的到的数字，别乱动，除非有更好的方法
            # 遗留一个bug，多次刷新会导致channel管道堵塞
            for i in range(3):
                mess = self.ssh_channel.recv(1024).decode('utf-8')
                if not mess:
                    self.close(1234)
                    break
                message = json.dumps({'flag': 'success', 'message': mess})
                self.send_to_ws_mes(message)
        except socket.timeout:
            self.close(1234)
        except:
            self.close(1234)

    def close(self):
        try:
            self.websocket.close()
            self.ssh_channel.close()
        except Exception as e:
            pass

    def send_to_ws_mes(self, event):
        text_data = json.loads(event)
        message = text_data['message']
        self.websocket.send(message)

    def _ws_to_ssh(self, data):
        try:
            self.ssh_channel.send(data)
        except OSError as e:
            self.close()

    def _ssh_to_ws(self):
        try:
            while not self.ssh_channel.exit_status_ready():
                data = self.ssh_channel.recv(1024).decode('utf-8')
                message = {'flag': 'success', 'message': data}
                if len(data) != 0:
                    self.send_to_ws_mes(json.dumps(message))
                else:
                    break
        except Exception as e:
            message = {'flag': 'error', 'message': str(e)}
            self.send_to_ws_mes(json.dumps(message))
            self.close(1234)

    def shell(self, data):
        Thread(target=self._ws_to_ssh, args=(data,)).start()
        Thread(target=self._ssh_to_ws).start()

    def resize_pty(self, cols, rows):
        self.ssh_channel.resize_pty(width=cols, height=rows)


class SSHConsumer(WebsocketConsumer):
    def connect(self):
        host_ip = self.scope["url_route"]["kwargs"]["ip"]
        self.accept()
        self.ssh = StreamConsumer(websocket=self)
        self.ssh.connect(host_ip=host_ip)

    def disconnect(self, code):

        raise self.ssh.close()

    def receive(self, text_data=None):
        text_data = json.loads(text_data)

        if text_data['flag'] == 'resize':
            self.ssh.resize_pty(cols=text_data['cols'], rows=text_data['rows'])
        else:
            data = text_data['entered_key']
            self.ssh.shell(data=data)
