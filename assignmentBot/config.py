from os import environ

EMAIL = environ['EMAIL']
PASS = environ['PASSWORD']

ASSIGNMETS = ["Git", "Web", "Python", "Bash", "Android"]
LINKS = []

NEXT_MAIL_TEMPLATE = '''
Hi ${NAME}! We recieved you ${TOPIC} submission. Here's your next assignment: ${LINK}.

DevClub IITD
'''

ERR_MAIL_TEMPLATE = '''
HI ${NAME}! The repo URL you submitted for ${TOPIC} assignment doesn't exist. Either the repo is private or the link is wrong.

DevClub IITD
'''