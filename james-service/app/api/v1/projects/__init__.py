from .messenger import Messenger

# init messenger for sections
SectionsMessenger = Messenger('http://sections-service:5000/api/v1/projects/sections?include_paragraphs=True%s')

SectionsListMessenger = Messenger('http://sections-service:5000/api/v1/projects/%i/sections%s')

SubSectionsMessenger = Messenger('http://sub-sections-service:5000/api/v1/projects/sections/sub-sections%s')

IdeasMessenger = Messenger('http://ideas-service:5000/api/v1/ideas%s')

# SectionsMessenger = Messenger('http://localhost:5003/api/v1/projects/sections')

from .managers import *
