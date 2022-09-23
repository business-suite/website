# -*- coding: utf-8 -*-


import hashlib
import uuid

from datetime import datetime
from werkzeug import urls
from odoo import api, models

VALIDATION_KARMA_GAIN = 3


class Users(models.Model):
    _inherit = 'res.users'

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['karma']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'country_id', 'city', 'website', 'website_description', 'website_published',
        ]

    @api.model
    def _generate_profile_token(self, user_id, email):
        """Return a token for email validation. This token is valid for the day
        and is a hash based on a (secret) uuid generated by the forum module,
        the user_id, the email and currently the day (to be updated if necessary). """
        profile_uuid = self.env['ir.config_parameter'].sudo().get_param('website_profile.uuid')
        if not profile_uuid:
            profile_uuid = str(uuid.uuid4())
            self.env['ir.config_parameter'].sudo().set_param('website_profile.uuid', profile_uuid)
        return hashlib.sha256((u'%s-%s-%s-%s' % (
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            profile_uuid,
            user_id,
            email
        )).encode('utf-8')).hexdigest()

    def _send_profile_validation_email(self, **kwargs):
        if not self.email:
            return False
        token = self._generate_profile_token(self.id, self.email)
        activation_template = self.env.ref('website_profile.validation_email')
        if activation_template:
            params = {
                'token': token,
                'user_id': self.id,
                'email': self.email
            }
            params.update(kwargs)
            token_url = self.get_base_url() + '/profile/validate_email?%s' % urls.url_encode(params)
            with self._cr.savepoint():
                activation_template.sudo().with_context(token_url=token_url).send_mail(
                    self.id, force_send=True, raise_exception=True)
        return True

    def _process_profile_validation_token(self, token, email):
        self.ensure_one()
        validation_token = self._generate_profile_token(self.id, email)
        if token == validation_token and self.karma == 0:
            return self.write({'karma': VALIDATION_KARMA_GAIN})
        return False
