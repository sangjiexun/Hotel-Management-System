from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, RoomForm, MeetingForm, TeamForm
from app.models import User, Team, Room, Meeting, CostLog, Participants_user, Participants_partner, Businesspartner
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form.teamId.choices = [(team.id, team.teamName) for team in Team.query.all()]
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    fullname=form.fullname.data, 
                    position=form.position.data, 
                    teamId=form.teamId.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = MeetingForm()
    form.roomId.choices = [(room.id, room.roomName) for room in Room.query.all()]
    if form.validate_on_submit():
        meeting = Meeting(title=form.title.data, 
                         roomId=form.roomId.data, 
                         bookerId=current_user.id, 
                         teamId=current_user.teamId, 
                         date=form.date.data, 
                         startTime=form.startTime.data, 
                         duration=form.duration.data, 
                         endTime=form.startTime.data + form.duration.data)
        db.session.add(meeting)
        db.session.commit()
        
        # Add cost log
        room = Room.query.get(form.roomId.data)
        cost = room.cost * form.duration.data
        team = Team.query.get(current_user.teamId)
        cost_log = CostLog(teamId=current_user.teamId, 
                          teamName=team.teamName, 
                          title=form.title.data, 
                          date=form.date.data, 
                          cost=cost)
        db.session.add(cost_log)
        db.session.commit()
        
        flash('Meeting booked successfully!')
        return redirect(url_for('index'))
    return render_template('book.html', title='Book Meeting', form=form)

@app.route('/roomavailable')
@login_required
def roomavailable():
    return render_template('roomavailable.html', title='Room Availability')

@app.route('/roomavailablelist', methods=['POST'])
@login_required
def roomavailablelist():
    date = request.form.get('date')
    start_time = int(request.form.get('start_time'))
    end_time = int(request.form.get('end_time'))
    
    # Convert date string to datetime object
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # Get all rooms
    rooms = Room.query.all()
    
    # Get all meetings on that date
    meetings = Meeting.query.filter_by(date=date_obj).all()
    
    # Find available rooms
    available_rooms = []
    for room in rooms:
        is_available = True
        for meeting in meetings:
            if meeting.roomId == room.id:
                if not (meeting.endTime <= start_time or meeting.startTime >= end_time):
                    is_available = False
                    break
        if is_available:
            available_rooms.append(room)
    
    return render_template('roomavailablelist.html', title='Available Rooms', rooms=available_rooms, date=date, start_time=start_time, end_time=end_time)

@app.route('/roomoccupation')
@login_required
def roomoccupation():
    return render_template('roomoccupation.html', title='Room Occupation')

@app.route('/roomoccupationlist', methods=['POST'])
@login_required
def roomoccupationlist():
    date = request.form.get('date')
    
    # Convert date string to datetime object
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # Get all meetings on that date
    meetings = Meeting.query.filter_by(date=date_obj).all()
    
    # Get room information for each meeting
    for meeting in meetings:
        meeting.room = Room.query.get(meeting.roomId)
        meeting.booker = User.query.get(meeting.bookerId)
        meeting.team = Team.query.get(meeting.teamId)
    
    return render_template('roomoccupationlist.html', title='Room Occupation List', meetings=meetings, date=date)

@app.route('/costs')
@login_required
def costs():
    return render_template('costs.html', title='Cost Management')

@app.route('/costcheck', methods=['POST'])
@login_required
def costcheck():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    team_id = request.form.get('team_id')
    
    # Convert date strings to datetime objects
    start_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_obj = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Get cost logs
    if team_id:
        cost_logs = CostLog.query.filter(
            CostLog.teamId == team_id,
            CostLog.date >= start_obj,
            CostLog.date <= end_obj
        ).all()
    else:
        cost_logs = CostLog.query.filter(
            CostLog.date >= start_obj,
            CostLog.date <= end_obj
        ).all()
    
    # Calculate total cost
    total_cost = sum(log.cost for log in cost_logs)
    
    return render_template('costcheck.html', title='Cost Check', cost_logs=cost_logs, total_cost=total_cost, start_date=start_date, end_date=end_date)

@app.route('/allrecords')
@login_required
def allrecords():
    meetings = Meeting.query.all()
    for meeting in meetings:
        meeting.room = Room.query.get(meeting.roomId)
        meeting.booker = User.query.get(meeting.bookerId)
        meeting.team = Team.query.get(meeting.teamId)
    return render_template('allrecords.html', title='All Meetings', meetings=meetings)

@app.route('/addteam', methods=['GET', 'POST'])
@login_required
def addteam():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(teamName=form.teamName.data)
        db.session.add(team)
        db.session.commit()
        flash('Team added successfully!')
        return redirect(url_for('index'))
    return render_template('addteam.html', title='Add Team', form=form)

@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    form = RegistrationForm()
    form.teamId.choices = [(team.id, team.teamName) for team in Team.query.all()]
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    fullname=form.fullname.data, 
                    position=form.position.data, 
                    teamId=form.teamId.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('index'))
    return render_template('adduser.html', title='Add User', form=form)

@app.route('/deleteteam', methods=['GET', 'POST'])
@login_required
def deleteteam():
    if request.method == 'POST':
        team_id = request.form.get('team_id')
        team = Team.query.get(team_id)
        if team:
            # Check if team has members
            users = User.query.filter_by(teamId=team_id).all()
            if users:
                flash('Cannot delete team with members!')
                return redirect(url_for('deleteteam'))
            # Check if team has meetings
            meetings = Meeting.query.filter_by(teamId=team_id).all()
            if meetings:
                flash('Cannot delete team with meetings!')
                return redirect(url_for('deleteteam'))
            db.session.delete(team)
            db.session.commit()
            flash('Team deleted successfully!')
            return redirect(url_for('index'))
    teams = Team.query.all()
    return render_template('deleteteam.html', title='Delete Team', teams=teams)

@app.route('/deleteuser', methods=['GET', 'POST'])
@login_required
def deleteuser():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if user:
            # Check if user has booked meetings
            meetings = Meeting.query.filter_by(bookerId=user_id).all()
            if meetings:
                flash('Cannot delete user with booked meetings!')
                return redirect(url_for('deleteuser'))
            # Check if user is a participant in meetings
            participations = Participants_user.query.filter_by(userId=user_id).all()
            if participations:
                flash('Cannot delete user with meeting participations!')
                return redirect(url_for('deleteuser'))
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!')
            return redirect(url_for('index'))
    users = User.query.all()
    return render_template('deleteuser.html', title='Delete User', users=users)

@app.route('/cancelbooking', methods=['GET', 'POST'])
@login_required
def cancelbooking():
    if request.method == 'POST':
        meeting_id = request.form.get('meeting_id')
        meeting = Meeting.query.get(meeting_id)
        if meeting:
            # Check if user is the booker
            if meeting.bookerId != current_user.id:
                flash('You can only cancel your own bookings!')
                return redirect(url_for('cancelbooking'))
            db.session.delete(meeting)
            db.session.commit()
            flash('Booking cancelled successfully!')
            return redirect(url_for('index'))
    meetings = Meeting.query.filter_by(bookerId=current_user.id).all()
    for meeting in meetings:
        meeting.room = Room.query.get(meeting.roomId)
    return render_template('cancelbooking.html', title='Cancel Booking', meetings=meetings)
