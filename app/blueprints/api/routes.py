from . import api
from flask import request, jsonify
from app.models import Post, db



#CRUD

#CREATE using a POST

@api.post('/create_post')
def create_post_api():
    '''
    payload should include
    {
    "img_url": "test",
    "caption": "from api",
    "location": "api",
    "user_id": 1
    }
    '''

    data = request.get_json()
    new_post = Post(img_url = data['img_url'], caption = data['caption'], location=data['location'], user_id=data['user_id'])

    new_post.save()
    return jsonify({
        'status': 'ok',
        'message': 'Post was successfully created'
    })



#READ using GET
@api.get('/view_all_posts')
def view_all_posts_api():
    posts = Post.query.all()

    post_list = []
    for post in posts:
        post_dict = {
            'id': post.id,
            'img_url': post.img_url,
            'caption': post.caption,
            'location': post.location,
            'user_id': post.user_id,
            'date': post.date
        }
        post_list.append(post_dict)
    
    return jsonify({'posts': post_list, 'status': 'ok'})



@api.get('/view_post/<post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)

    if post:
        post_dict = {
                'id': post.id,
                'img_url': post.img_url,
                'caption': post.caption,
                'location': post.location,
                'user_id': post.user_id,
                'date': post.date
            }
        
        return jsonify({'post': post_dict, 'status': 'ok'})
    else:
        return jsonify({'status':  'not ok', 'message': f'no post with id {post_id}'})




#UPDATE using PATCH(specific changes to an object) and PUT(changing the entire object)

@api.put('/update_post/<post_id>')
def update_post_api(post_id):
    '''
    payload should include
    {
    "img_url": "test",
    "caption": "from api",
    "location": "api",
    }
    '''
    data = request.get_json()

    post = Post.query.get(post_id)
    if post:
        post.img_url = data['img_url']
        post.caption = data['caption']
        post.location = data['location']

        post.save()
        return jsonify({'status': 'ok', 'message': 'Post updated'})
    else:
        return jsonify({'status':  'not ok', 'message': f'no post with id {post_id}'})

#DELETE using DELETE
    
@api.delete('delete_post/<post_id>')
def delete_post_api(post_id):
    post = Post.query.get(post_id)

    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'status': 'ok','message': 'Post deleted'})
    else:
        return jsonify({'status':  'not ok', 'message': f'no post with id {post_id}'})