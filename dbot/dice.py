from functools import singledispatch
import random
import collections
import re

@singledispatch
def roll_dice(max_val=20, num_dice=1):
    # check inputs
    if max_val <= 0 or not isinstance(max_val, int):
        raise ValueError(str(max_val) +
                         '-sided die does not have a positive integer'
                         ' number of faces.')
    if num_dice <= 0 or not isinstance(num_dice, int):
        raise ValueError(str(num_dice) + ' dice is not a positive integer'
                         ' number of dice.')

    if max_val > 200:
        raise ValueError(str(max_val) + '-sided die is too large.'
                         ' Maximum sides is 200.')
    if num_dice > 100:
        raise ValueError(str(num_dice) + ' dice is too many. Only roll'
                         ' up to 100 dice at once.')
    roll_res = [0] * num_dice
    for i in range(num_dice):
        roll_res[i] = random.randint(1, max_val)
    return roll_res


@roll_dice.register(str)
def _(roll_str):
    d = mod_roll(roll_str)
    return roll_dice(int(d.max_val),int(d.num_dice))


def mod_roll(roll_str):
    roll_str = roll_str.lower()
    if roll_str == '': roll_str = 'd'
    num_dice, rest = tuple(roll_str.split('d'))
    keep_str = ''
    if 'h' in rest:
        max_val, keep_str = tuple(rest.split('h'))
        keep_str = 'h' + keep_str
    elif 'l' in rest:
        max_val, keep_str = tuple(rest.split('l'))
        keep_str = 'L' + keep_str
    else:
        max_val = rest
    # set defaults
    if num_dice == '': num_dice = '1'
    if max_val == '': max_val = '20'
    if keep_str.endswith('h') or keep_str.endswith('L') or (
            keep_str.endswith('!')):
        keep_str = keep_str + '1'
    # check for decimals
    if '.' in num_dice:
        raise ValueError("invalid literal for int() with base 10: 'num_dice="
                         + d.num_dice + "'")
    if '.' in max_val:
        raise ValueError("invalid literal for int() with base 10: 'max_val="
                         + d.max_val + "'")
    if '.' in keep_str:
        raise ValueError("invalid literal for int() with base 10: 'keep_str="
                         + d.keep_str + "'")
    roll = num_dice + 'd' + max_val + keep_str
    Dice = collections.namedtuple('Dice', ['roll_str', 'num_dice',
                                           'max_val', 'keep_str'])
    return Dice(roll, num_dice, max_val, keep_str)

def chat_roll_wrap(chat_str, verbose=False, formatted=False):
    """Parse input by commas, call chat_roll on each token."""
    chat_str = chat_str.split(',')


def chat_roll(roll_str='', verbose=False, formatted=False):
    return_msg = ''
    mod_msg = ''
    roll_str = roll_str.lower()
    roll_list = re.split(r'([\s\+\-\*\/\(\)])', roll_str)
    roll_list = list(filter(None, roll_list))
    if roll_list == []: roll_list = ['d']
    for i in range(len(roll_list)):
        if 'd' in roll_list[i]:
            d = mod_roll(roll_list[i])
            mod_msg += d.roll_str
            roll_res = roll_dice(int(d.max_val), int(d.num_dice))
            if d.keep_str:
                roll_res_trimmed, trim_ndcs = sort_and_trim(roll_res,
                                                            d.keep_str)
                roll_sum = sum(roll_res_trimmed)
            else:
                roll_sum = sum(roll_res)
            if verbose:
                verbose_str = str(roll_res)
                if formatted:
                    verbose_str = "**" + verbose_str + "**"
                    if d.keep_str:
                        verbose_str = "**["
                        first_num = True
                        bold_on = True
                        for n in range(len(roll_res)):
                            if n in trim_ndcs:
                                if bold_on:
                                    if first_num:
                                        verbose_str += str(roll_res[n])
                                        first_num = False
                                    else:
                                        verbose_str += (
                                            "**, **" + str(roll_res[n]))
                                else:
                                    verbose_str += ", **" + str(roll_res[n])
                                    bold_on = True
                            else:
                                if bold_on:
                                    if first_num:
                                        verbose_str += "**" + str(roll_res[n])
                                        first_num = False
                                        bold_on = False
                                    else:
                                        verbose_str += (
                                            "**, " + str(roll_res[n]))
                                        bold_on = False
                                else:
                                    verbose_str += ", " + str(roll_res[n])
                        if bold_on:
                            verbose_str += "]**"
                        else:
                            verbose_str += "**]**"
                    if d.num_dice == '1' or d.keep_str[1:] == '1':
                        return_msg += verbose_str
                    else:
                        return_msg += (verbose_str
                                       + "{" + str(roll_sum) + "}")
                else:
                    return_msg += str(verbose_str) + "{" + str(roll_sum) + "}"
            roll_list[i] = str(roll_sum)
        else:
            mod_msg += roll_list[i]
            if verbose:
                return_msg += roll_list[i]
    return_msg = mod_msg + " = " + return_msg
    if verbose:
        return_msg += " = "
    if formatted:
        return_msg += "**" + str(eval(''.join(roll_list))) + "**"
    else:
        return_msg += str(eval(''.join(roll_list)))
    return return_msg


def sort_and_trim(vals, keep):
    keep = keep.lower()
    trim_ndcs = sorted(range(len(vals)), key=vals.__getitem__)
    num_keep = int(keep[1:].replace('!', '-'))
    if num_keep < 0:
        if keep.startswith('h'):
            keep = keep.replace('h', 'l')
        elif keep.startswith('l'):
            keep = keep.replace('l', 'h')
        num_keep = len(vals) + num_keep
    if keep.startswith('h'):
        trim_ndcs = trim_ndcs[-num_keep:]
    elif keep.startswith('l'):
        trim_ndcs = trim_ndcs[:num_keep]
    vals = [vals[i] for i in trim_ndcs]
    return vals, trim_ndcs

