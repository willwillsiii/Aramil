import os
import unicodedata
import re
import json

# grabbed from Django framework
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower()).strip()
    return re.sub(r'[-\s]+', '-', value)

class Profile:
    """Container for different macros."""

    def __init__(self, path=base_dir):
        """Creates profile directory inside <path>."""
        # check for profile folder and make if it doesn't exist
        if something:
            pass
        else:
            pass

    def c_loc(self, discorduser, path=base_dir):
        """Creates profile directory inside <path>."""
        # check for user folder and make if it doesn't exist
        if something:
            pass
        else:
            pass

    def rm_loc(self):
        """Delete's local files for the profile."""
        pass

    def sync(self):
        """Ensures local files match the profile instance."""
        pass

    def unsync(self):
        """Prevents updating of local files for the profile."""
        pass

    def c_macro(self, macro):
        """Create a macro and modify local files accordingly."""
        pass

    def mv_macro(self, macro):
        """Rename a macro and modify local files accordingly."""
        pass

    def rm_macro(self, macro):
        """Delete a macro and modify local files accordingly."""
        pass


class User:
    """Container for profiles associated with some unique user_id."""

    def __init__(self, user_id, user_path=None, sync=True):
        if path is None:
            path = base_dir

    def c_loc(self, discorduser, path=None):
        """Creates user directory inside <path>."""
        if path is None:
            path = base_dir
        # check for user folder and make if it doesn't exist
        if something:
            pass
        else:
            pass

    def rm_loc(self):
        """Delete's local files for the user."""
        pass

    def sync(self):
        """Ensures local files match the user instance."""
        pass

    def unsync(self):
        """Prevents updating of local files for the user."""
        pass

    def c_prof(self, name):
        """Create a profile including the necessary local files."""
        pass

    def mv_prof(self, profile):
        """Rename a profile including the necessary local files."""
        pass

    def rm_prof(self, profile):
        """Delete a profile including the necessary local files."""
        pass

    def active(self, profile):
        """Enable a profile for use."""
        pass


class Userbase:
    pass


# directory which will contain all users and therefore user profiles
base_dir = '.'
is_base_dir_default = True
def set_base_dir(path=None, update_bool=True):
    """Set the base directory for the module.
    This affects the defaults for other functions.
    """
    global base_dir
    global is_base_dir_default
    if path is None:
        path = '.'
        if update_bool:
            is_base_dir_default = True
    else:
        if update_bool:
            is_base_dir_default = False
    base_dir = path
    if is_users_file_default:
        set_users_file(update_bool=False)

# file whose contents correlates users with directories
users_file = os.path.join(base_dir, 'users.json')
is_users_file_default = True
def set_users_file(path=None, update_bool=True):
    """Set the users file for the module.
    This affects the defaults for other functions.
    """
    global users_file
    global is_users_file_default
    if path is None:
        path = os.path.join(base_dir, 'users.json')
        if update_bool:
            is_users_file_default = True
    else:
        if update_bool:
            is_users_file_default = False
    users_file = path
    if is_base_dir_default:
        set_base_dir(os.path.dirname(path), update_bool=False)

def write_dict(d, filename):
    """Convert the interpreter's instance of a dictionary into a human-
    readable file.
    """
    with open(filename, 'w') as f:
        json.dump(d, f, indent=4)

def read_dict(filename):
    """Returns a dictionary read from a file created by write_dict()."""
    with open(filename, 'r') as f:
        return json.load(f)

def duser_dir(discord_user)
    """Returns a directory name generated from a discord.User."""
    return f'{discord_user.display_name}#{discord_user.discriminator}'

def duser(discord_user, base_path=None, sync=True):
    """Returns a User correlated to the given discord.User."""
    user_id = discord_user.id
    if base_path is None:
        base_path = base_dir
    user_dir = duser_dir(discord_user)
    user_path = os.path.join(base_path, user_dir)
    return User(user_id, user_path=user_path, sync=sync)

def mv_duser_dir(user, discord_user)
    """Update a User (correlated with a discord.User) instance's
    directory name.
    """
    pass
