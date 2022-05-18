from flask import Response, request
from flask_restful import Resource
from models import Following, db
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # return all of the "following" records that the current user is following
        followings = Following.query.filter(Following.user_id == self.current_user.id)
        followings_json = [following.to_dict_following() for following in followings]
        return Response(json.dumps(followings_json), mimetype="application/json", status=200)

    def post(self):
        # create a new "following" record based on the data posted in the body 
        def checkInt(str):
            try:
                int(str)
                return True
            except ValueError:
                return False

        body = request.get_json()
        user_id = self.current_user.id
        following_id = body.get('user_id')

        if following_id is None:
            return Response(json.dumps({'message':'"user_id" does not exist'}), mimetype="application/json", status=400)    

        if not checkInt(following_id):
            return Response(json.dumps({'message':'"user_id" with wrong format.'}), mimetype="application/json", status=400)

        if int(following_id) > 100:
            return Response(json.dumps({'message':'"user_id" does not exist'}), mimetype="application/json", status=404)

        if Following.query.filter(Following.user_id == user_id, Following.following_id == following_id).first():
            return Response(json.dumps({'messgae':'Duplicated following'}), mimetype='application/json', status=400)

        follow = Following(user_id, following_id)
        db.session.add(follow)
        db.session.commit()
        return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "following" record where "id"=id
        following = Following.query.get(id)

        if not following or following.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Following does not exist'}), mimetype="application/json", status=404)

        Following.query.filter_by(id=id).delete()
        db.session.commit()

        serialized_data = {
            'message' : 'Following {0} successfully deleted.'.format(id) 
        }

        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)




def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
