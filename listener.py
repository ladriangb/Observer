
class Listener:
    def __init__(self, name, subject):
        self.name = name
        subject.register(self)

    def notify(self, event):
        #TODO: Send Push Notification ...
        print (self.name, "received event", event)