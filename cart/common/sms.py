from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, tokens: dict, template):
    """
        sending common that needs template
    """
    try:
        api = KavenegarAPI(
            '47476645384A4F5A48726849766C4661472B394B3631552F4B54594B4E71766A59624E6F465564494B35303D'
        )
        params = {
            'receptor': '09944326389',
            'template': template,
        }
        for key, value in tokens.items():
            params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


def send_sms_normal():
    print('------------------------------------0')
    try:
        api = KavenegarAPI(
            '47476645384A4F5A48726849766C4661472B394B3631552F4B54594B4E71766A59624E6F465564494B35303D')
        params_buyer = {
            'receptor': '09944326389',
            'message': 'hi',
            'sender': '1000689696'
        }
        response = api.sms_send(params_buyer)
        print(response)
        print('------------------------------------1')
    except APIException as e:
        print(e)
        print('------------------------------------2')
    except HTTPError as e:
        print(e)
        print('------------------------------------3')