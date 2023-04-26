import json

from django.utils.translation import gettext

from corehq.motech.generic_inbound.exceptions import GenericInboundUserError
from corehq.motech.generic_inbound.middleware.base import BaseApiMiddleware
from corehq.motech.generic_inbound.utils import ApiResponse


class JsonMiddleware(BaseApiMiddleware):
    """API middleware for handling JSON payloads"""

    def _get_body_for_eval_context(self, request_data):
        try:
            return json.loads(request_data.data)
        except json.JSONDecodeError:
            raise GenericInboundUserError(gettext("Payload must be valid JSON"))

    def _get_success_response(self, response_json):
        return ApiResponse(status=200, data=response_json)

    def _get_generic_error(self, status_code, message):
        return ApiResponse(status=status_code, data={'error': message})

    def _get_submission_error_response(self, status_code, form_id, message):
        return ApiResponse(status=status_code, data={
            'error': message,
            'form_id': form_id,
        })

    def _get_validation_error(self, status_code, message, errors):
        return ApiResponse(status=status_code, data={
            'error': message,
            'errors': errors,
        })
