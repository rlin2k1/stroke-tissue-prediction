# :: utilities.py
#####################################################
# Utility functions for usage in all modules.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 30 May 2019


def represents_int(s):
    """
    Determines if the given string represents an integer.

    :param str s:
    :return: True if the string represents an int, else False.
    :rtype: bool
    """
    try: 
        int(s)
        return True
    except ValueError:
        return False