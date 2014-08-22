from flask_wtf import Form
import wtforms
from wtforms import FieldList, FormField, SelectField, StringField, TextAreaField
from wtforms import validators
from . import models

class AddMemberForm(Form):
    name = StringField('Name', [validators.Required()])
    phone = StringField('Phone Number', [
        validators.Required(), 
        validators.Regexp(r'\d{10}', message="Please enter 10 digit phone number")])
    email = StringField('Email Address', [validators.Email()])
    voterid = StringField('Voter ID')

class RoleForm(wtforms.Form):
    # Extending from wtforms.Form instead of flask_wtf.Form as this adds
    # unnecessary CSRF token even this is an inner form.
    # Source: http://stackoverflow.com/a/15651474/189776

    name = StringField('Name')
    multiple = SelectField('Multiple?', choices=[("no", "One Member"), ("yes", "Multiple Members")])
    permission = SelectField('Permissions', choices=[("read", "Read"), ("read,write", "Read and Write")])

class NewCommitteeForm(Form):
    name = StringField('Name', [validators.Required()])
    slug = StringField('Slug', [validators.Required()])
    level = SelectField('Level', choices=[])
    description = TextAreaField('Description', [])
    roles = FieldList(FormField(RoleForm), min_entries=0)

    def __init__(self, place, *a, **kw):
        Form.__init__(self, *a, **kw)
        self.place = place
        self.level.choices = [(t.short_name, t.name) for t in models.PlaceType.all()]

        # Ensure that there are at least 5 empty slots
        empty_slots = sum(1 for role in self.data['roles'] if not role['name'].strip())
        for i in range(5-empty_slots):
            self.roles.append_entry()

    def validate_slug(self, field):
        if models.CommitteeType.find(self.place, field.data):
            raise validators.ValidationError("Already used")

class SignupForm(Form):
    name = StringField('Name', [validators.Required()])
    phone = StringField('Phone Number', [validators.Required()])
    voterid = StringField('Voter ID', [validators.Required()])