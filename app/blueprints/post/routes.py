from . import post
from .forms import CreatePostForm
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Post, db

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


#edit_route
@post.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = CreatePostForm()
    if post and post.user_id == current_user.id:
        if request.method == 'POST' and form.validate_on_submit():
            post.img_url = form.img_url.data
            post.caption = form.caption.data
            post.location = form.location.data

            post.save()
            flash('Successfully updated post', 'info')
            return redirect(url_for('post.feed'))
        else:
            return render_template('edit_post.html', form=form, post=post)
    else:
        flash('This post doesn\'t belong to you SNAKE', 'danger')
        return redirect(url_for('post.feed'))


#delete_post_route
    
@post.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash('Post was succefully deleted', 'warning')
        return redirect(url_for('post.feed'))
    else:
        flash('This post doesn\'t belong to you SNAKE', 'danger')
        return redirect(url_for('post.feed'))