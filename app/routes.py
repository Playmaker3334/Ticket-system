from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Ticket, User
from . import db, login_manager
from flask import current_app as app
import csv

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, "")

@app.route('/')
@login_required
def index():
    open_tickets = Ticket.query.filter_by(status='open').all()
    in_progress_tickets = Ticket.query.filter_by(status='in progress').all()
    finished_tickets = Ticket.query.filter_by(status='finished').all()
    return render_template('index.html', open_tickets=open_tickets, in_progress_tickets=in_progress_tickets, finished_tickets=finished_tickets)

@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('ticket.html', ticket=ticket)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assigned_to = request.form['assigned_to']  # Nuevo campo
        new_ticket = Ticket(title=title, description=description, assigned_to=assigned_to)  # Nuevo campo
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_ticket.html')

@app.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        ticket.title = request.form['title']
        ticket.description = request.form['description']
        ticket.assigned_to = request.form['assigned_to']  # Nuevo campo
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_ticket.html', ticket=ticket)

@app.route('/delete/<int:ticket_id>')
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar usuario desde el archivo CSV
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    user = User(username, password)
                    login_user(user)
                    return redirect(url_for('index'))
        
        flash('Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/ticket/<int:ticket_id>/set_status/<string:status>')
@login_required
def set_status(ticket_id, status):
    ticket = Ticket.query.get_or_404(ticket_id)
    if status in ['open', 'in progress', 'finished']:
        ticket.status = status
        db.session.commit()
    return redirect(url_for('index'))





