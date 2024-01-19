from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from app.models import Student, Admin

# ... (rest of the code remains the same)
