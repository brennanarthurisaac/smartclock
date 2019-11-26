# -*- coding: utf-8 -*-
"""Routes

This module contains view functions which return templates and redirections
associated with routes and links.

This module constitutes the main operation of the program.
"""
from app import app
from app.forms import AddAlarmForm
from app.models import AlarmManager
from app.api import get_news_content
from app.api import get_weather_html
from datetime import datetime
from flask import render_template
from flask import redirect
from flask import Response

ALARM_MANAGER = AlarmManager()

# ##################
# # VIEW FUNCTIONS #
# ##################

@app.route("/")
@app.route("/notifications")
def notifications() -> str:
    """Routes the notifications page.
    
    Returns:
        Notifications template with assigned titles.
    """
    return render_template("notifications.html",
                           title="Alarms",
                           subtitle="Present")

@app.route("/error/<error_message>")
def error(error_message: str) -> str:
    """Routes the error page.
    
    Args:
        error_message (str): Display message.

    Returns: 
        An error page filled with relevant message
    """
    return render_template("error.html",
                           error_message = error_message)

@app.route("/alarms/<int:add_alarm>", methods=['GET', 'POST'])
def alarms(add_alarm: int) -> str:
    """Returns the alarms template filled with alarms information.

    The alarms template is an extension of the table template with added
    add alarm button.

    Args:
        add_alarm (int): Condition deciding whether the new alarm form is
            provided or else the button to navigate to it.
            0: Shows button to navigate to -
            1: A form to add a new alarm, also showing a button to go back.
    Returns:
        alarms template filled with alarms information.
    """
    form = AddAlarmForm()
    if form.validate_on_submit():
        print("Creating alarm frontend")
        ALARM_MANAGER.create_alarm(form.name.data, form.time.data)
        return redirect("/alarms/0")

    return render_template("alarms.html",
                           add_alarm=add_alarm,
                           title="Alarms",
                           subtitle="Upcoming Alarms",
                           form=form) # array of event objects

# ##################
# # FEED FUNCTIONS #
# ##################

@app.route("/notifications_feed")
def notifications_feed() -> str:

    def generate():
        return render_template("alarms_table.html", 
                               items = ALARM_MANAGER.finished_alarms)

    return Response(generate(), mimetype="text")

@app.route("/alarms_feed")
def alarms_feed() -> str:
    """Routes the alarm feed.

    Returns:
        A resposne containing the alarm table rendered with upcoming alarms.
    """
    def generate():
        return render_template("alarms_table.html", 
                               items=ALARM_MANAGER.pending_alarms)

    return Response(generate(), mimetype="text")

@app.route("/time_feed")
def time_feed() -> str:
    """Routes the time feed.

    Returns:
        A response containing the time in a string format.
    """
    def generate():
        return datetime.now().strftime("%H:%M")
        
    return Response(generate(), mimetype="text")

@app.route("/news_feed")
def news_feed() -> str:
    """
    """
    def generate():
        return render_template("news_table.html", articles=get_news_content())
    return Response(generate(), mimetype="text")
@app.route("/weather_feed")
def weather_feed() -> str:
    """Routes the weather feed.

    Returns:
        A response containing html content concerning the weather.
    """
    return Response(get_weather_html(), mimetype="text")
        
@app.route("/remove_notification_feed/<alarm_id>")
def remove_notification(alarm_id: str) -> str:
    """Routes the function to remove a notification.

    Given an alarm_id from web front end, passes this to the notifications to
    remove.

    Args:
        alarm_id (str): Id related to notification to remove.

    Returns:
        A redirection to notifications.
    """
    ALARM_MANAGER.remove_finished_alarm(alarm_id)
    return redirect("/notifications")

@app.route("/remove_alarm_feed/<alarm_id>")
def remove_alarm(alarm_id: str) -> str:
    """Routes the remove alarm functionality.

    Given an alarm_id from web front end, passes this to the scheduler to
    remove.

    Args:
        alarm_id (str): Id related to the event to remove.

    Returns:
        A redirection to alarms/0.
    """
    ALARM_MANAGER.remove_pending_alarm(alarm_id)
    return redirect("/alarms/0")

