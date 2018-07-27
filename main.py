import webapp2
import os
import jinja2
# from models import * #imports all

from models import Post
from models import Author

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('templates/my_blog.html')
        self.response.write(template.render())

class AboutMeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('templates/about_me.html')
        self.response.write(template.render())

class PostsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('templates/posts.html')
        self.response.write(template.render())
    def post(self):
        title = self.request.get('post_title')
        username = self.request.get('username')
        post = self.request.get('post')
        tags = self.request.get('tags')
        tags = tags.split(', ')
        # for tag in tags:
        #     tag

        new_post = Post(title=title, content=post, tags=tags) #tags = tags
        new_post.put()

        check_author = Author.query(Author.name == username).fetch()
        if len(check_author) > 0:
            author = check_author[0]
            author.post.append(new_post.key)
        else:
            author = Author(name=username, post=[new_post.key])

        author.put()

        blog_posts = []
        for blog_post_key in author.post:
            blog_posts.append(blog_post_key.get())

        tags_list=[]
        for tag in tags_list:
            tags_list.append(tag)

        template_vars = {
            # 'post_title': title,
            'username': username,
            # 'post': post,
            # 'tags':tags,
            'blog_posts': blog_posts
        }

        # template = jinja_current_dir.get_template('templates/show_post.html')
        # self.response.write(template.render(template_vars))
        template = jinja_current_dir.get_template('templates/show_many_posts.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aboutme', AboutMeHandler),
    ('/posts', PostsHandler), #these don't have to be the same as the html page
], debug=True)
