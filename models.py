from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now = True)
    tags = ndb.StringProperty(repeated=True)

class Author(ndb.Model):
    name = ndb.StringProperty()
    post = ndb.KeyProperty(kind="Post", repeated=True)
