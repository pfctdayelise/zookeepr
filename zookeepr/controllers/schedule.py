import logging
import vobject
import json

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, abort
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

import formencode
from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from datetime import date, datetime, timedelta
from pytz import timezone

from zookeepr.lib.mail import email
from zookeepr.lib.ordereddict import OrderedDict

from zookeepr.model import meta
from zookeepr.model.schedule import Schedule
from zookeepr.model.proposal import Proposal
from zookeepr.model.time_slot import TimeSlot, TimeSlotValidator
from zookeepr.model.location import Location, LocationValidator
from zookeepr.model.event import Event, EventValidator
from zookeepr.model.event_type import EventType

from zookeepr.config.lca_info import lca_info
from zookeepr.config.zookeepr_config import file_paths

import os

class NewScheduleFormSchema(BaseSchema):
    time_slot = TimeSlotValidator(if_missing=None)
    location = LocationValidator(if_missing=None)
    event = EventValidator(if_missing=None)

class ScheduleSchema(BaseSchema):
    time_slot = TimeSlotValidator(not_empty=True)
    location = LocationValidator(not_empty=True)
    event = EventValidator(not_empty=True)
    video_url = validators.String(if_empty=None)
    audio_url = validators.String(if_empty=None)
    slide_url = validators.String(if_empty=None)

class NewScheduleSchema(BaseSchema):
    schedule = ScheduleSchema()
    pre_validators = [NestedVariables]

class EditScheduleSchema(BaseSchema):
    schedule = ScheduleSchema()
    pre_validators = [NestedVariables]

class ScheduleController(BaseController):

    # Use this to limit to organisers only.
    #@authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        if h.signed_in_person():
            c.can_edit = h.signed_in_person().has_role('organiser')
        else:
            c.can_edit = False

        c.subsubmenu = []
        c.subsubmenu.append([ '/programme/sunday', 'Sunday' ])
        c.scheduled_dates = TimeSlot.find_scheduled_dates()
        for scheduled_date in c.scheduled_dates:
            c.subsubmenu.append(['/programme/schedule/' + scheduled_date.strftime('%A').lower(), scheduled_date.strftime('%A')])

        c.subsubmenu.append([ '/programme/open_day', 'Saturday' ])

    def table(self, day=None):
        if len(c.scheduled_dates) == 0:
            return render('/schedule/no_schedule_available.mako')

        c.display_date = None

        available_days = {}
        for scheduled_date in c.scheduled_dates:
            available_days[scheduled_date.strftime('%A').lower()] = scheduled_date

        if day in available_days:
            c.display_date = available_days[day]

        if c.display_date is None:
            if date.today() in c.scheduled_dates:
                c.display_date = date.today()
            else:
                c.display_date = c.scheduled_dates[0]

        c.time_slots = TimeSlot.find_by_date(c.display_date)
        c.primary_times = {}
        for time_slot in TimeSlot.find_by_date(c.display_date, primary=True):
            c.primary_times[time_slot.start_time] = time_slot

        event_type = EventType.find_by_name('presentation')
        c.locations = Location.find_scheduled_by_date_and_type(c.display_date, event_type)
        c.schedule_collection = Schedule.find_by_date(c.display_date)

        c.time_increment = timedelta(minutes=5)

        c.programme = OrderedDict()

        for time_slot in c.time_slots:
            time = time_slot.start_time
            while time < time_slot.end_time:
                c.programme[time] = {}
                time = time + c.time_increment

        for schedule in c.schedule_collection:
            exclusive_event = schedule.time_slot.exclusive_event()
            time = schedule.time_slot.start_time
            if exclusive_event:
                c.programme[time]['exclusive'] = exclusive_event
            else:
                c.programme[time][schedule.location] = schedule

        return render('/schedule/table.mako')

    def table_view(self, id):
        c.schedlue = Schedule.find_by_id(id)
        return render('/schedule/table_view.mako')

    def ical(self):
        c.schedule_collection = Schedule.find_all()

        ical = vobject.iCalendar()
        for schedule in c.schedule_collection:
            if not schedule.time_slot.heading:
                event = ical.add('vevent')
                event.add('uid').value = str(schedule.id) + '@' + h.lca_info['event_host']
                # Created
                event.add('created').value = schedule.creation_timestamp.replace(tzinfo=timezone('Australia/Brisbane'))
                # Last Modified
                event.add('dtstamp').value = schedule.last_modification_timestamp.replace(tzinfo=timezone('Australia/Brisbane'))
                event.add('last-modified').value = schedule.last_modification_timestamp.replace(tzinfo=timezone('Australia/Brisbane'))
                # Start and End Time
                event.add('dtstart').value = schedule.time_slot.start_time.replace(tzinfo=timezone('Australia/Brisbane'))
                event.add('dtend').value = schedule.time_slot.end_time.replace(tzinfo=timezone('Australia/Brisbane'))
                # Title and Author (need to add Author here)
                event.add('summary').value = schedule.event.computed_title() + ' by ' + h.list_to_string(schedule.event.computed_speakers())
                # Abstract, if we have one
                event.add('description').value = schedule.event.computed_abstract()
                # Add a URL
                if schedule.event.proposal:
                    event.add('url').value = h.url_for(qualified=True, controller='schedule', action='view_talk', id=schedule.event.proposal.id)
                elif not (schedule.event.url is None or schedule.event.url == ''):
                    if schedule.event.url.startswith('https://') or schedule.event.url.startswith('http://'):
                        event.add('url').value = h.url_for(str(schedule.event.url))
                    else:
                        event.add('url').value = h.url_for(str(schedule.event.url), qualified=True)

                concurrent_schedules = schedule.event.schedule_by_time_slot(schedule.time_slot)
                for concurrent_schedule in concurrent_schedules:
                    if concurrent_schedule != schedule:
                        if concurrent_schedule in c.schedule_collection:
                            c.schedule_collection.remove(concurrent_schedule)

                locations = [concurrent_schedule.location.display_name for concurrent_schedule in concurrent_schedules]
                event.add('location').value = h.list_to_string(locations)

        response.charset = 'utf8'
        response.headers['content-type'] = 'text/calendar; charset=utf8'
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')
        return ical.serialize()

    def json(self):
        schedules = Schedule.find_all()
        output = []

        for schedule in schedules:
            if not schedule.time_slot.heading:
                row = {}
                speakers = schedule.event.computed_speakers()
                row['Id'] = schedule.id
                row['Event'] = schedule.event_id
                row['Title'] = schedule.event.computed_title()
                row['Room Name'] = schedule.location.display_name
                row['Start'] = str(schedule.time_slot.start_time)
                row['Duration'] = str(schedule.time_slot.end_time - schedule.time_slot.start_time)
                if speakers:
                    row['Presenters'] = ','.join(speakers)
                row['Description'] = schedule.event.computed_abstract()
                if schedule.event.proposal:
                    row['URL'] = h.url_for(qualified=True, controller='schedule', action='view_talk', id=schedule.event.proposal_id)
                output.append(row)

        response.charset = 'utf8'
        response.headers['content-type'] = 'application/json; charset=utf8'
        response.headers.add('content-transfer-encoding', 'binary')
        response.headers.add('Pragma', 'cache')
        response.headers.add('Cache-Control', 'max-age=3600,public')
        return json.write(output)

    @dispatch_on(POST="_new")
    @validate(schema=NewScheduleFormSchema(), on_get=True, post_only=False, variable_decode=True)
    def new(self):
        c.time_slots = TimeSlot.find_all()
        c.locations = Location.find_all()
        c.events = Event.find_all()


        form = render('/schedule/new.mako')
        object = { 'schedule': self.form_result }
        defaults = NewScheduleSchema().from_python(object)
        return htmlfill.render(form, defaults)

    @validate(schema=NewScheduleSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['schedule']

        c.schedule = Schedule(**results)
        meta.Session.add(c.schedule)
        meta.Session.commit()

        h.flash("Schedule created")
        redirect_to(action='new', id=None)

    def view(self, id):
        return redirect_to(action='edit')

    def index(self):
        c.schedule_collection = Schedule.find_all()
        return render('/schedule/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.time_slots = TimeSlot.find_all()
        c.locations = Location.find_all()
        c.events = Event.find_all()
        c.schedule = Schedule.find_by_id(id)


        defaults = h.object_to_defaults(c.schedule, 'schedule')
        defaults['schedule.time_slot'] = c.schedule.time_slot_id
        defaults['schedule.location'] = c.schedule.location_id
        defaults['schedule.event'] = c.schedule.event_id

        form = render('/schedule/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditScheduleSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        schedule = Schedule.find_by_id(id)

        for key in self.form_result['schedule']:
            setattr(schedule, key, self.form_result['schedule'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Schedule has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the schedule

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.schedule = Schedule.find_by_id(id)
        return render('/schedule/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.schedule = Schedule.find_by_id(id)
        meta.Session.delete(c.schedule)
        meta.Session.commit()

        h.flash("Schedule has been deleted.")
        redirect_to('index')
