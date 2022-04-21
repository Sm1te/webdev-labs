from flask import Response, request
from flask_restful import Resource
from models import Post, db
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # get posts created by one of these users:
        ids = get_authorized_user_ids(self.current_user)
        posts = Post.query.filter(Post.user_id.in_(ids))
        limit = request.args.get('limit')
        if limit:
            try:
                limit = int(limit)
            except:
                return Response(json.dumps({'message': 'Limit must be an integer'}), mimetype="application/json", status=400)
            if limit > 50 or limit < 1:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
        else:
            limit = 10
        posts = posts.order_by(Post.pub_date.desc()).limit(limit)

        # note: if you pass the current user into to_dict(), it will tell you
        # whether or not the current user liked and/or bookmarked any of the posts
        data = [
            item.to_dict(user=self.current_user) for item in posts.all()
        ]
        # print(get_authorized_user_ids(self.current_user))
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()
        image_url = body.get('image_url')
        if image_url is None:
            return Response(json.dumps({'message':'"image_url" is required.'}), mimetype="application/json", status=400)
        caption = body.get('caption')
        alt_text = body.get('alt_text')
        user_id = self.current_user.id

        #Create post:
        post = Post(image_url, user_id, caption, alt_text)
        db.session.add(post)
        db.session.commit()
        return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        post = Post.query.get(id)
        body = request.get_json()

        # a user can only edit their own post:
        if not post or post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
       
        post.image_url = body.get('image_url') or post.image_url
        post.caption = body.get('caption') or post.caption
        post.alt_text = body.get('alt_text') or post.alt_text
        
        # commit changes:
        db.session.commit()       
        # return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=200)
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

    def delete(self, id):

        # a user can only delete their own post:
        post = Post.query.get(id)
        if not post or post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
       
        # delete post where "id"=id
        Post.query.filter_by(id=id).delete()
        db.session.commit()
        
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


    def get(self, id):
        # get the post based on the id
        post = Post.query.get(id)
        return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )