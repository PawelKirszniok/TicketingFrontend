from flask import render_template, redirect, url_for, request
from ticketingfrontend import app, database_service
from ticketingfrontend.forms.login import UserLoginForm
from ticketingfrontend.forms.registration import UserRegistrationForm
from ticketingfrontend.forms.ticket import NewTicketForm
from ticketingfrontend.forms.post import NewPostForm
from ticketingfrontend.forms.user_search_bar import UserSearchBar
from flask_login import login_user, current_user, logout_user, login_required
from ticketingfrontend.login import User
import hashlib
import secrets
import os


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserRegistrationForm()
    if form.validate_on_submit():
        picture_name = 'default.jpg'
        if form.picture.data:
            picture_name = save_picture(form.picture.data)

        password_hash = hashlib.md5(bytes(form.password.data, 'utf-8'))

        # validate data with the database
        user_id, _ = database_service.validate_user(password_hash.hexdigest(), form.login.data, form.email.data)

        # inform the user if the credentials are taken
        if user_id:
            return render_template('signup.html', title='Sign Up', form=form, duplicate=True)
        else:
            database_service.save_user(form.login.data, password_hash.hexdigest(), form.email.data, form.position.data, form.name.data, picture_name)
            # account created successfully
            return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserLoginForm()
    if form.validate_on_submit():
        password_hash = hashlib.md5(bytes(form.password.data, 'utf-8'))

        user_id, valid = database_service.validate_user(password_hash.hexdigest(), form.login.data)

        # inform the user if password did not match.
        if not valid:
            return render_template('login.html', title='Log In', form=form, invalid=True)

        # log the user in since the credentials matched
        user = User(database_service.get_user(user_id))
        login_user(user, form.remember.data)

        requested_page = request.args.get('next')
        if requested_page:
            return redirect(requested_page)
        return redirect(url_for('home'))
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def user_profile():
    user_image = url_for('static', filename=f"profile_pictures/{current_user.picture}")
    return render_template('profile.html', title='Profile', image=user_image)


@app.route('/tickets')
@login_required
def tickets_view():

    order_by = request.args.get('order_by')
    if order_by:
        tickets = database_service.get_tickets_ordered(current_user.id, order_by=order_by)
    else:
        tickets = database_service.get_tickets(current_user.id )

    return render_template('tickets.html', title='Tickets', tickets=tickets)


@app.route('/closed_tickets')
@login_required
def closed_tickets():

    order_by = request.args.get('order_by')
    if order_by:
        tickets = database_service.get_tickets_ordered(current_user.id, order_by=order_by, closed=True)
    else:
        tickets = database_service.get_tickets(current_user.id, closed = True )

    return render_template('closed_tickets.html', title='Tickets', tickets=tickets)


@app.route('/new_ticket', methods=['GET', 'POST'])
@login_required
def new_ticket():

    form = NewTicketForm()

    if form.validate_on_submit():
        ticket_id = database_service.save_ticket(form.title.data, form.status.data, form.deadline.data)

        if not ticket_id:
            return render_template('new_ticket.html', title='New Ticket', form=form)

        database_service.save_relation(current_user.id, ticket_id, 'author')

        database_service.save_post(current_user.id, ticket_id, form.content.data)

        return redirect(url_for('ticket')+'?ticket_id='+str(ticket_id))

    return render_template('new_ticket.html', title='New Ticket', form=form)


@app.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    ticket_id = request.args['ticket_id']

    ticket = database_service.get_ticket(ticket_id)

    posts = database_service.get_posts(ticket_id)

    for post in posts:
        post['user']['picture_url'] = url_for('static', filename=f"profile_pictures/{post['user']['picture']}")
    user_search = UserSearchBar()
    form = NewPostForm()

    if user_search.validate_on_submit():
        user = database_service.str_search_users(user_search.search_string.data)
        if user:
            database_service.save_relation(user['id'], ticket_id, 'developer')  # TODO

    if form.validate_on_submit():
        database_service.save_post(current_user.id,ticket_id, form.content.data, form.new_status.data)

    return render_template('ticket.html', title=f'Ticket - {ticket_id}', form=form, ticket=ticket, posts=posts, user_search=user_search)


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(picture.filename)
    new_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', new_filename)
    picture.save(picture_path)
    return new_filename

