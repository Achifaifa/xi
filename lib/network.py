import ast, socket, sys, time

class connection:

  def __init__(self,ip='',port=12345):
    """
    If no IP to connect to is specified, acts as server
    """

    self.ip=ip

    try:
      self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      if ip:
        self.s.connect((ip,port))
        self.s.send("[].")
      if not ip:
        self.s.bind((ip, port))
        self.s.listen(5)
        self.conn, self.addr = self.s.accept()
    except Exception as e:
      raise e, None, sys.exc_info()[2]

  def closeconn(self):

    self.s.close()

  def receive(self):

    data=""
    while 1:
      if not self.ip:
        buff=self.conn.recv(1024).decode()
      else:
        buff=self.s.recv(1024).decode()
      data+=buff
      if "." in data: 
        break
    data=data.rstrip(".")
    return ast.literal_eval(data)

  def send(self,data):

    if not self.ip:
      self.conn.send(str(data)+".")
    else:
      self.s.send(str(data)+".")

