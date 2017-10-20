from functools import singledispatch
import random
import collections
import re

@singledispatch
def roll_dice(max_val=20, num_dice=1):
    """Returns a list of random dice rolls.

    Keyword arguments:
    max_val -- maximum value of the dice, also the number of sides (default 20)
    num_dice -- number of dice to roll (default 1)
    """
    # check inputs
    if max_val <= 0 or not isinstance(max_val, int):
        raise ValueError("".join([str(max_val),
                         '-sided die does not have a positive integer',
                         ' number of faces.']))
    if num_dice <= 0 or not isinstance(num_dice, int):
        raise ValueError("".join([str(num_dice),
                         ' dice is not a positive integer',
                         ' number of dice.']))
    if max_val > 200:
        raise ValueError("".join([str(max_val),
                         '-sided die is too large.',
                         ' Maximum sides is 200.']))
    if num_dice > 100:
        raise ValueError("".join([str(num_dice),
                         ' dice is too many. Only roll',
                         ' up to 100 dice at once.']))
    return [random.randint(1, max_val) for die in range(num_dice)]


@roll_dice.register(str)
def _(roll_str):
    roll = mod_roll(roll_str)
    return roll_dice(int(roll.max_val),int(roll.num_dice))


def mod_roll(roll_str):
    """Modify a roll to normalize and expand abbreviations"""
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
        raise ValueError(''.join([
            "invalid literal for int() with base 10: 'num_dice=",
            num_dice, "'"]))
    if '.' in max_val:
        raise ValueError(''.join([
            "invalid literal for int() with base 10: 'max_val=",
            max_val, "'"]))
    if '.' in keep_str:
        raise ValueError(''.join([
            "invalid literal for int() with base 10: 'keep_str=",
            keep_str, "'"]))
    mod_roll_str = num_dice + 'd' + max_val + keep_str
    Roll = collections.namedtuple('Roll', ['roll_str', 'num_dice',
                                           'max_val', 'keep_str'])
    return Roll(mod_roll_str, num_dice, max_val, keep_str)

def chat_roll(roll_str, verbose=False, formatted=False):
    """Parse input by commas, call chat_roll_single on each token."""
    while '{' in roll_str:
        brace_index = roll_Str.find('}')
        if brace_index == -1:
            raise ValueError('Unmatched brace.')
        next_brace_index = roll_str.index('}')
        brace_str = roll_str[brace_index+1:next_brace_index]
        brace_list = brace_str.split(',')
        repeated_list = [chat_roll_single(brace_list(0))
                       for roll in range(int(brace_list(1)))]
        roll_str.replace(roll_str[brace_index,next_brace_index],
                         ', '.join(repeated_list))
    chat_list = roll_str.split(',')
    rolls = [chat_roll_single(roll_str, verbose, formatted)
             for roll_str in chat_list]
    return '\n'.join(rolls)

def chat_roll_single(roll_str='', verbose=False, formatted=False):
    """Interpet and compute rolls from a string.
    
    Keyword arguments:
    roll_str -- what to interpret as a roll (default '')
    verbose -- whether each roll is returned (default False)
    formatted -- whether to format for Discord (default false)
    """
    return_msg = ''
    mod_msg = ''
    roll_str = roll_str.lower()
    roll_list = re.split(r'([\s\+\-\*\/\(\)])', roll_str)
    roll_list = list(filter(None, roll_list))
    if roll_list == []: roll_list = ['d']
    for i in range(len(roll_list)):
        if 'd' in roll_list[i]:
            roll = mod_roll(roll_list[i])
            mod_msg += roll.roll_str
            roll_res = roll_dice(int(roll.max_val), int(roll.num_dice))
            if roll.keep_str:
                roll_res_trimmed, trim_ndcs = sort_and_trim(roll_res,
                                                            roll.keep_str)
                roll_sum = sum(roll_res_trimmed)
            else:
                roll_sum = sum(roll_res)
            if verbose:
                verbose_str = str(roll_res)
                if formatted:
                    verbose_str = "**" + verbose_str + "**"
                    if roll.keep_str:
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
                    if roll.num_dice == '1' or roll.keep_str[1:] == '1':
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
    """Returns a sorted subset of values and the indices of the subset.
    
    Arguments:
    vals -- values to sort
    keep -- which values to keep
    """
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


