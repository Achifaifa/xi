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
        self.hole=self.s
        self.hole.connect((ip,port))
        self.hole.send("[].")
      if not ip:
        self.s.bind((ip, port))
        self.s.listen(5)
        self.hole, self.addr = self.s.accept()
    except Exception as e:
      raise e, None, sys.exc_info()[2]

  def closeconn(self):

    self.s.close()

  def receive(self):

    data=""
    while 1:
      buff=self.hole.recv(1024).decode()
      data+=buff
      if "." in data: 
        break
    data=data.rstrip(".")
    return ast.literal_eval(data)

  def send(self,data):

    self.hole.send(str(data)+".")

