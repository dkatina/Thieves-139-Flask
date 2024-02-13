from . import post
from .forms import CreatePostForm
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Post

#create_post
@post.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST' and form.validate_on_submit:
        img_url = form.img_url.data
        caption = form.caption.data
        location = form.location.data
        user_id = current_user.id
        
        #create instance of Post with form data
        new_post = Post(img_url=img_url, caption=caption, location=location, user_id=user_id)
        new_post.save()
        flash('Successfully created new Post', 'success')
        return redirect(url_for('post.feed'))

    else:
        return render_template('create_post.html', form=form)


#feed_route
@post.route('/feed')
def feed():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)


#view_own_posts route


#edit_route


#delete_post_route