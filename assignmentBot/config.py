from os import environ

EMAIL = environ['EMAIL']
PASS = environ['PASSWORD']

ASSIGNMETS = ["Git", "Web", "Python", "Bash", "Android"]
LINKS = ['https://drive.google.com/file/d/1mDDSDg2mPDszgQBCIFUb3C6SDh-XrQHc/view?usp=sharing',
'https://drive.google.com/file/d/1HGgYLRd6xcbzFlESyp8MYxInxSVX646M/view?usp=sharing']

NEXT_MAIL_TEMPLATE = '''
Hi {NAME}! We recieved your {TOPIC} submission. Here's your next assignment: {LINK}.

DevClub IITD
'''

ERR_MAIL_TEMPLATE = '''
Hi {NAME}! The  URL you submitted for {TOPIC} assignment {ERROR}. Submit link to a valid public Github repo.

DevClub IITD
'''