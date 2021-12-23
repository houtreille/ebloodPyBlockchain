import cherrypy
from ebloodCoin.blockchain.Block import Block
from pywin.framework.toolmenu import tools



class HelloWorld(object):

    
    @cherrypy.expose
    def generate(self, previousHashId):
      block = Block(previousHashId)
      
      return "AA" + str(block)
  
    @cherrypy.expose
    def index(self):
        return """ 
        <html>
           <head></head>
           <body>
              <form action = "hello.html" method = "post">
                 <input type = "text" name = "name" value = "" />
                 <button type="submit" form="form1" value="Submit">Submit</button>
              </form>
           </body>
        </html>
        """ 
          
    @cherrypy.expose
    def hello(self, name="John Doe"):
        return "Hello %s" % (name, )