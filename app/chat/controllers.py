from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Member, Membership, Room, Message
from .forms import CreateRoomForm, JoinRoomForm, LeaveRoomForm, TextMessageForm


chat = Blueprint('chat', __name__)


@chat.route('/create-room', methods=['POST', 'GET'])
@login_required
def create_room():
    form = CreateRoomForm()
    return render_template('chat/createroom.html', form=form)


@chat.route('/join-room/<room_id>', methods=['POST', 'GET'])
@login_required
def join_room(room_id):
    form = JoinRoomForm()
    return render_template('chat/joinroom.html', form=form)


@chat.route('/leave-room/<room_id>', methods=['POST', 'GET'])
@login_required
def leave_room(room_id):
    form = LeaveRoomForm()
    return render_template('chat/leaveroom.html', form=form)