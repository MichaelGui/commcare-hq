import datetime
import json
import uuid
import requests

from django.test import SimpleTestCase

from mock import PropertyMock, patch

from corehq.apps.cowin.repeater_generators import (
    BeneficiaryRegistrationPayloadGenerator,
    BeneficiaryVaccinationPayloadGenerator,
)
from corehq.apps.cowin.repeaters import (
    BeneficiaryRegistrationRepeater,
    BeneficiaryVaccinationRepeater,
)
from corehq.form_processor.models import CommCareCaseSQL
from corehq.motech.models import ConnectionSettings
from corehq.motech.repeaters.models import RepeatRecord


class TestRepeaters(SimpleTestCase):
    domain = 'test-cowin'

    @patch('corehq.motech.repeaters.models.Repeater.connection_settings', new_callable=PropertyMock)
    @patch('corehq.motech.repeaters.models.CaseRepeater.payload_doc')
    def test_registration_payload(self, payload_doc_mock, connection_settings_mock):
        connection_settings_mock.return_value = ConnectionSettings(password="secure-api-key")

        case_id = uuid.uuid4().hex
        case_json = {
            'name': 'Nitish Dube',
            'birth_year': '2000',
            'gender_id': 1,
            'mobile_number': '9999999999',
            'photo_id_type': 1,
            'photo_id_number': 'XXXXXXXX1234',
        }
        case = CommCareCaseSQL(domain=self.domain, type='beneficiary', case_id=case_id, case_json=case_json,
                               server_modified_on=datetime.datetime.utcnow())
        payload_doc_mock.return_value = case

        repeater = BeneficiaryRegistrationRepeater()
        generator = BeneficiaryRegistrationPayloadGenerator(repeater)
        repeat_record = RepeatRecord()

        self.assertEqual(repeater.get_headers(repeat_record)['X-Api-Key'], "secure-api-key")

        payload = generator.get_payload(repeat_record=None, beneficiary_case=case)
        self.assertDictEqual(
            json.loads(payload),
            {
                'name': 'Nitish Dube',
                'birth_year': '2000',
                'gender_id': 1,
                'mobile_number': '9999999999',
                "photo_id_type": 1,
                'photo_id_number': 'XXXXXXXX1234',
                "consent_version": "1"
            }
        )

    @patch('corehq.motech.repeaters.models.RepeatRecord.handle_success', lambda *_: None)
    @patch('corehq.apps.cowin.repeaters.update_case')
    @patch('requests.Response.json')
    def test_registration_response(self, json_response_mock, update_case_mock):
        case_id = uuid.uuid4().hex

        response_json = {
            "beneficiary_reference_id": "1234567890123",
            "isNewAccount": "Y"
        }

        response = requests.Response()
        response.status_code = 200
        json_response_mock.return_value = response_json

        repeat_record = RepeatRecord(payload_id=case_id)
        repeater = BeneficiaryRegistrationRepeater(domain=self.domain)

        repeater.handle_response(response, repeat_record)

        update_case_mock.assert_called_with(
            self.domain, case_id, case_properties={'cowin_id': "1234567890123"},
            device_id='corehq.apps.cowin.repeaters.BeneficiaryRegistrationRepeater'
        )

    @patch('corehq.motech.repeaters.models.Repeater.connection_settings', new_callable=PropertyMock)
    @patch('corehq.motech.repeaters.models.CaseRepeater.payload_doc')
    def test_vaccination_payload(self, payload_doc_mock, connection_settings_mock):
        connection_settings_mock.return_value = ConnectionSettings(password="my-secure-api-key")

        case_id = uuid.uuid4().hex
        case = CommCareCaseSQL(domain=self.domain, type='vaccination', case_id=case_id,
                               server_modified_on=datetime.datetime.utcnow())
        payload_doc_mock.return_value = case

        repeater = BeneficiaryVaccinationRepeater()
        generator = BeneficiaryVaccinationPayloadGenerator(repeater)
        repeat_record = RepeatRecord()

        self.assertEqual(repeater.get_headers(repeat_record)['X-Api-Key'], "my-secure-api-key")

        # 1st dose
        case.case_json = {
            'cowin_id': '1234567890123',
            'center_id': 1234,
            'vaccine': "COVISHIELD",
            'vaccine_batch': '123456',
            'dose': '1',
            'dose1_date': "01-01-2020",
            'vaccinator_name': 'Neelima',
        }

        payload = generator.get_payload(repeat_record=None, vaccination_case=case)
        self.assertDictEqual(
            json.loads(payload),
            {
                "beneficiary_reference_id": "1234567890123",
                "center_id": 1234,
                "vaccine": "COVISHIELD",
                "vaccine_batch": "123456",
                "dose": 1,
                "dose1_date": "01-01-2020",
                "vaccinator_name": "Neelima"
            }
        )

        # 2nd dose
        case.case_json.update({
            'dose': '2',
            'dose2_date': "01-02-2020",
            'vaccinator_name': 'Sumanthra',
        })

        payload = generator.get_payload(repeat_record=None, vaccination_case=case)
        self.assertDictEqual(
            json.loads(payload),
            {
                "beneficiary_reference_id": "1234567890123",
                "center_id": 1234,
                "vaccine": "COVISHIELD",
                "vaccine_batch": "123456",
                "dose": 2,
                "dose1_date": "01-01-2020",
                "dose2_date": "01-02-2020",
                "vaccinator_name": "Sumanthra"
            }
        )