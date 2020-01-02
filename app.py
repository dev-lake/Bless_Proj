from flask import Flask, render_template, redirect, \
    jsonify, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy, Pagination
from flask_wtf.csrf import CSRFProtect
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)
csrf = CSRFProtect(app)

from models import Message, Category, User
from forms import MessageForm, DeleteMessageForm,\
    CategoryForm, DeleteCategoryForm, DeleteForm


@app.route('/', methods=["GET", "POST"])
@basic_auth.required
def index():
    page = int(request.args.get('page') or 1) 
    per_page = int(request.args.get('per_page') or 10) 
    pagination = Message.query.paginate(page=page, per_page=per_page, error_out=False)
    prev_url = url_for('index', page=pagination.prev_num)
    next_url = url_for('index', page=pagination.next_num)

    create_message_form = MessageForm()
    create_message_form.category.choices = [
        (c.id, c.name) for c in Category.query.all()
    ]
    if create_message_form.validate_on_submit():
        category = Category.query.get(create_message_form.category.data)
        if category == None:
            flash('No Such Category.')
            return redirect(url_for('index'))
        message = Message(
            body = create_message_form.body.data,
            category_id = category.id
        )
        db.session.add(message)
        db.session.commit()
        flash("Added Successful.")
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        title = "Manage",
        create_message_form = create_message_form,
        pagination = pagination,
        prev_url = prev_url,
        next_url = next_url
    )


@app.route('/delete_post/<int:id>', methods=['POST'])
@basic_auth.required
def delete_post(id):
    m = Message.query.filter_by(id=id).first()
    db.session.delete(m)
    db.session.commit()
    flash('Content Deleted.')
    return redirect(url_for('index'))

@app.route('/alter_post/<int:id>', methods=['GET', 'POST'])
@basic_auth.required
def alter_post(id):
    edit_form = MessageForm()
    edit_form.category.choices = [
        (c.id, c.name) for c in Category.query.all()
    ]
    message = Message.query.get(id)
    if not message:
        abort(404)
    if request.method == 'GET':        
        edit_form.category.data = message.category_id
        edit_form.body.data = message.body
        
    if edit_form.validate_on_submit():
        message.body = edit_form.body.data
        message.category_id = edit_form.category.data
        db.session.commit()
        flash('Content Submit')
        return redirect(url_for('index'))
    return render_template('edit_message.html', title='Edit Message', form=edit_form)


@app.route('/category', methods=['GET', 'POST'])
@basic_auth.required
def manage_category():
    category = Category.query.all()
    category_form = CategoryForm()
    if category_form.validate_on_submit():
        data = category_form.name.data
        query = Category.query.filter_by(name=data).first()
        if query is not None:
            flash('Category Exist.')
            return redirect(url_for('manage_category'))
        c = Category(name=data)
        db.session.add(c)
        db.session.commit()
        flash('Added.')
        return redirect(url_for('manage_category'))
    return render_template(
        'manage_category.html',
        title = 'Manage Category',
        category_form = category_form,
        category = category
    )



@app.route('/delete_category/<int:id>', methods=['POST'])
@basic_auth.required
def delete_category(id):
    c = Category.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()
    flash('Category Deleted.')
    return redirect(url_for('manage_category'))

@app.route('/user')
@basic_auth.required
def manage_user():
    page = int(request.args.get('page') or 1)
    pagination = User.query.paginate(
        page=page, 
        per_page=10, 
        error_out=False
    )
    prev_url = url_for('manage_user', page=pagination.prev_num)
    next_url = url_for('manage_user', page=pagination.next_num)
    return render_template(
        'manage_user.html',
        title = 'Manage User',
        pagination = pagination,
    )

@app.route('/delete_user/<int:id>', methods=['POST'])
@basic_auth.required
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return "No Such User."
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted')
    return redirect(url_for('manage_user'))

@app.route('/logout')
def logout():
    return render_template('logout.html')


########################################
################ API ###################
########################################


@app.route('/get_category')
def get_category():
    return jsonify(
        status = 'ok',
        amount = Category.get_category_amount(),
        body = Category.get_all_category()
    )


@app.route('/get_bless')
def get_bless():
    # Get args in Request
    page = int(request.args.get('page') or 1) 
    per_page = int(request.args.get('per_page') or 10) 
    category_id = int(request.args.get('category_id') or 0)

    if category_id != 0:
        bless = Message.query.filter(Message.category_id==category_id)
        pagination = bless.paginate(
            page=page, 
            per_page= per_page or app.config['API_ITEMS_PER_PAGE'], 
            error_out=False
        )
    else:
        pagination = Message.query.paginate(
            page=page, 
            per_page= per_page or app.config['API_ITEMS_PER_PAGE'], 
            error_out=False
        )
 
    m = []
    for i in pagination.items:
        m.append(
            {
                'id': i.id, 
                'body': i.body, 
                'category': {
                    'id': i.category.id,
                    'name': i.category.name
                }
            }
        )
    return jsonify(
        status = 'ok',  # response status
        page = pagination.page, # Current Page number
        pages = pagination.pages, # Total Page num
        items = len(m), # the amount of item in current page
        message = m
    )

########### User API ###########

### Add User ###
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)
    if not data.get('openid') or not data.get('nickname'):
        return jsonify(status='fail', message='openid and nickname required.')
    user = User(
        openId = data.get('openid'),
        nickname = data.get('nickname'),
        gender = data.get('gender'),
        city = data.get('city'),
        province = data.get('province'),
        country = data.get('country'),
        avatarUrl = data.get('avatarurl'),
        unionId = data.get('unionid')
    )
    q = User.query.filter_by(openId=data.get('openid')).first()
    if q:
        if user.openId == data.get('openid'):
            db.session.commit()
            return jsonify(status='updated', user=data.get('openid'))
    db.session.add(user)
    db.session.commit()
    return jsonify(status='created', user=data.get('openid'))


### Add Favorate to User ###
@app.route('/add_favourite', methods=['POST'])
def add_favourite():
    data = request.get_json()
    print(data)
    if data is None:
        return jsonify(status='fail', message='Nothing Received')
    if not data.get('message_id') or not data.get('user_id'):
        return jsonify(status='fail', message='Both message_id and user_id required')
    u = User.query.get(int(data.get('user_id')))
    m = Message.query.get(int(data.get('message_id')))
    if u is None:
        return jsonify(status='fail', message='User Not Exist.')
    if m is None:
        return jsonify(status='fail', message='Message Not Exist')
    u.messages.append(m)
    db.session.commit()
    return jsonify(status='ok', user_id=u.id, message_id=m.id)


### Get Favourate of User ###
@app.route('/get_user_collection/<int:id>')
def get_collection(id):
    if id is None:
        return jsonify(status='fail', message='User id Required.')
    u = User.query.get(id)
    if u is None:
        return jsonify(status='fail', message='No such a User.')
    return jsonify(
        status = 'ok',
        amount = u.favourates_amount(),
        favourate = u.favourates()
    )
