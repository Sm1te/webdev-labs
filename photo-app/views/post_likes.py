from flask import Response, request
from flask_restful import Resource
from models import LikePost, db
import json
from views import can_view_post

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        def checkInt(str):
            try:
                int(str)
                return True
            except ValueError:
                return False

        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()
        user_id = self.current_user.id
        post_id = body.get('post_id')

        if post_id is None:
            return Response(json.dumps({'messgae':'LikePost does not exist'}), mimetype='application/json', status=400)

        if not checkInt(post_id):
            return Response(json.dumps({'message':'"post_id" with wrong format.'}), mimetype="application/json", status=400)

        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'messgae':'Bookmark does not exist'}), mimetype='application/json', status=404)

        if LikePost.query.filter(LikePost.user_id == user_id, LikePost.post_id == post_id).first():
            return Response(json.dumps({'messgae':'Duplicated bookmarks'}), mimetype='application/json', status=400)

        like = LikePost(user_id, post_id)
        db.session.add(like)
        db.session.commit()
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "like_post" where "id"=id
        like = LikePost.query.get(id)
        if not like or like.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'LikePost does not exist'}), mimetype="application/json", status=404)

        like.query.filter_by(id=id).delete()
        db.session.commit()

        serialized_data = {
            'message' : 'Bookmark {0} successfully deleted.'.format(id) 
        }

        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
