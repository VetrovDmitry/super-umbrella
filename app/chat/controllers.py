from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import db, Member, Membership, Room, Message
from .forms import CreateRoomForm, JoinRoomForm, LeaveRoomForm, TextMessageForm
from app.auth.models import User


def room_required(func):
    @wraps(func)
    def decorated_view(room_id, *args, **kwargs):
        room = Room.query.filter_by(id=room_id)
        if not room:
            return 'room not found'
        return func(room_id, *args, **kwargs)

    return decorated_view


def access_required(func):
    @wraps(func)
    def decorated_view(room_id, *args, **kwargs):
        member_id = current_user.id
        membership = Membership.query.filter_by(room_id=room_id, member_id=member_id).all()
        if len(membership) == 0:
            return 'not have access'
        return func(room_id, *args, **kwargs)

    return decorated_view


chat = Blueprint('chat', __name__)


@chat.route('/index')
@login_required
def index():
    return render_template('chat/index.html')


@chat.route('/create-room', methods=['POST', 'GET'])
@login_required
def create_room():
    form = CreateRoomForm()

    if form.validate_on_submit():
        member_id = Member.query.get(current_user.id).id
        title = form.title.data
        details = form.details.data
        new_room = Room(member_id, title, details)
        db.session.add(new_room)
        db.session.commit()
        membership = Membership(member_id, new_room.id)
        db.session.add(membership)
        db.session.commit()
        return redirect(url_for('chat.room', room_id=new_room.id))

    return render_template('chat/createroom.html', form=form)


@chat.route('/room/<room_id>', methods=['POST', 'GET'])
@login_required
@room_required
@access_required
def room(room_id):
    current_room = Room.query.get(room_id)
    member_id = current_user.id
    messages = current_room.messages
    form = TextMessageForm()
    if form.validate_on_submit():
        new_message = Message(member_id, form.content.data, room_id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('chat.room', room_id=room_id))

    ready_messages = list()
    for message in messages:
        user = User.query.get(message.member_id)
        ready_messages.append({
            'content': message.content,
            'member_name': user.username
        })
    return render_template('chat/room.html', form=form, room_id=room_id, messages=ready_messages, member_id=member_id)


@chat.route('/join-room/<room_id>', methods=['POST', 'GET'])
@login_required
def join_room(room_id):
    form = JoinRoomForm()
    return render_template('chat/joinroom.html', form=form, room_id=room_id)


@chat.route('/leave-room/<room_id>', methods=['POST', 'GET'])
@login_required
@room_required
@access_required
def leave_room(room_id):
    form = LeaveRoomForm()
    return render_template('chat/leaveroom.html', form=form)