import random
import time


class PhoneSender:

    @staticmethod
    def send_code_phone_number(phone_number, code):
        raise NotImplementedError

class MockPhoneSender(PhoneSender):

    @staticmethod
    def send_code_phone_number(phone_number, code):
        time.sleep(random.randint(1000, 2000) / 1000)
        return