from urllib.parse import uses_relative
from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from views import can_view_post

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter(Bookmark.user_id == self.current_user.id)
        bookmarks_json = [bookmark.to_dict() for bookmark in bookmarks]
        return Response(json.dumps(bookmarks_json), mimetype="application/json", status=200)

    def post(self):
        def checkInt(str):
            try:
                int(str)
                return True
            except ValueError:
                return False

        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        user_id = self.current_user.id
        post_id = body.get('post_id')

        if post_id is None:
            return Response(json.dumps({'messgae':'Bookmark does not exist'}), mimetype='application/json', status=400)

        if not checkInt(post_id):
            return Response(json.dumps({'message':'"post_id" with wrong format.'}), mimetype="application/json", status=400)

        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'messgae':'No access to this bookmark'}), mimetype='application/json', status=404)

        if Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.post_id == post_id).first():
            return Response(json.dumps({'messgae':'Duplicated bookmarks'}), mimetype='application/json', status=400)

        bookmark = Bookmark(user_id, post_id)
        db.session.add(bookmark)
        db.session.commit()
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "bookmark" record where "id"=id
        bookmark = Bookmark.query.get(id)

        if not bookmark or bookmark.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Bookmark does not exist'}), mimetype="application/json", status=404)

        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()

        serialized_data = {
            'message' : 'Bookmark {0} successfully deleted.'.format(id) 
        }

        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
