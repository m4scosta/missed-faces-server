import os

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

THREADS_PER_PAGE = 2

# CSRF
CSRF_ENABLED = True
CSRF_SESSION_KEY = "_x(445[U3}YV$G?9R=j}5ojR2Zs<!ur6L)'ocfM!3v.8<1305NjlE06*~s/W!)K"
SECRET_KEY = "),rowPbh;49Q1q1nYL4.hLS4I1e9r97D83oi]%N7^1K{mUw'5|bw8wQ2^h2;4Uk"


# TASK QUEUE
CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'


# DATABASE
MONGODB_SETTINGS = {'DB': 'missed_faces'}


# EMAIL
SENDGRID_API_KEY = "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"
DEFAULT_MAIL_SENDER = "missedfaces@noreply.com"
