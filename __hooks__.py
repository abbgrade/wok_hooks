''' __hooks__.py

Attach Python functions to wok hooks.
'''

from hook_janitor import clean_temp_files
from hook_distribute import distribute_output
from hook_diaspora import add_diaspora_posts_to_timeline
from hook_github import add_github_activities_to_timeline
from hook_digg import add_diggs_to_timeline
from hook_stackexchange import add_stackexchange_questions_to_timeline
from hook_comments import add_mails_to_comments
from hook_vcard import add_vcard_to_contact
from hook_wikipedia import add_wikipedia_actions_to_timeline

# The `hooks` dictionary that wok will import
hooks = {
    'site.start': [clean_temp_files,
                   add_diaspora_posts_to_timeline,
                   add_github_activities_to_timeline,
                   add_diggs_to_timeline,
                   add_stackexchange_questions_to_timeline,
                   add_wikipedia_actions_to_timeline,
                   add_mails_to_comments],
    'site.content.gather.pre': [add_vcard_to_contact],
    'site.done': [distribute_output],
}
