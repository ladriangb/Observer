import json
import uuid
import redis

from listener import Listener

r = redis.Redis(db=5)


class Model:

    def __init__(self, id=None, data=None):
        if data is None:
            data = {}
        self.listeners = []
        self.attributes = data
        self.id = id
        listenerA = Listener("<Crud Notification>", self)

    def register(self, listener):
        self.listeners.append(listener)

    def unregister(self, listener):
        self.listeners.remove(listener)

    def notify_listeners(self, event):
        for listener in self.listeners:
            listener.notify(event)

    def create(selfs, data):
        id = selfs.get_classname() + ":" + str(uuid.uuid4())
        selfs.attributes = data
        r.set(id, json.dumps(data))
        selfs.notify_listeners("create new " + selfs.get_classname())

    def update(selfs, data):
        selfs.attributes = data
        r.set(selfs.id, json.dumps(data))
        selfs.notify_listeners("update " + selfs.get_classname() + " (" + selfs.id + ") Set new attributes=" + str(data))

    def read(selfs, id=""):
        if (id):
            selfs.notify_listeners("read by id" + selfs.get_classname())
        else:
            selfs.notify_listeners("read all" + selfs.get_classname())
        out = []
        if (not id):
            keys = r.keys(selfs.get_classname() + ":*")
        else:
            keys = [id]
        for key in keys:
            if(not isinstance(key, str)):
                key = key.decode("utf-8")
            try:
                out.append({"key": key, "value": json.loads(r.get(key).decode("utf-8"))})
            except:
                print(key+" Not found")

        return out

    def delete(selfs):
        r.delete(selfs.id)
        selfs.notify_listeners("delete " + selfs.get_classname() + " (" + selfs.id + ")")

    @classmethod
    def get_classname(cls):
        return cls.__name__

    def use_classname(self):
        return self.get_classname()
