''' __hooks__.py

Attach Python functions to wok hooks.
'''

from hook_janitor import clean_temp_files
from hook_distribute import distribute_output
from hook_diaspora import add_diaspora_posts_to_microblog
from hook_github import add_github_posts_to_microblog
from hook_comments import add_mails_to_comments

# The `hooks` dictionary that wok will import
hooks = {
    'site.start': [clean_temp_files, add_diaspora_posts_to_microblog, add_github_posts_to_microblog, add_mails_to_comments],
    'site.done': [distribute_output],
}
