import random
from subject import Subject

subject = Subject()

subject.create({"count":1})
subject.create({"count":2})
subject.create({"count":3})
subject.create({"count":4})
subject.create({"count":5})

list = subject.read()
if not list:
  print("List is empty")
  exit(1)
selected = random.choice(list)
value = selected.get("value", "{}")
id = selected.get("key")

selected = Subject(data=value, id=id)
value.update(max = 100,time=random.random())
selected.update(value)

updated = subject.read(id)
print(updated)
selected.delete()
updated = subject.read(id)
print(updated)
# selected = Subject(data=selected.value,id=selected.key)
