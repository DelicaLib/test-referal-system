from referal_system.settings import MOCK_PHONE_SENDER

if MOCK_PHONE_SENDER:
    from .phone_sender import MockPhoneSender as PhoneSender
else:
    from .phone_sender import PhoneSender