from flask import Response, request
from flask_restful import Resource
import json

from models import db, Comment
from views import can_view_post

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()
        post_id = body.get('post_id')
        text = body.get('text')

        if type(post_id) != int:
            return Response(json.dumps({'message':'"post_id" with wrong format.'}), mimetype="application/json", status=400)
   
        if post_id > 1000:
            return Response(json.dumps({'message':'"post_id" is required.'}), mimetype="application/json", status=404)
        
        if not post_id or not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'messgae':'Comment does not exist'}), mimetype='application/json', status=404)
        
        if text is None:
            return Response(json.dumps({'message':'"text" is required.'}), mimetype="application/json", status=400)
        user_id = self.current_user.id

        comment = Comment(text, user_id, post_id)
        db.session.add(comment)
        db.session.commit()
        
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment or comment.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Comment does not exist'}), mimetype="application/json", status=404)
       
        # delete "Comment" record where "id"=id
        Comment.query.filter_by(id=id).delete()
        db.session.commit()

        serialized_data = {
            'message' : 'Comment {0} successfully deleted.'.format(id) 
        }

        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
