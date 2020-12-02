def part1(fn):
    """
    Day 2. Part 1.

    ############################################################################
    Your flight departs in a few days from the coastal airport; the easiest way
    down to the coast from here is via toboggan.

    The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day.
    "Something's wrong with our computers; we can't log in!" You ask if you can
    take a look.

    Their password database seems to be a little corrupted: some of the
    passwords wouldn't have been allowed by the Official Toboggan Corporate
    Policy that was in effect when they were chosen.

    To try to debug the problem, they have created a list (your puzzle input) of
    passwords (according to the corrupted database) and the corporate policy
    when that password was set.

    For example, suppose you have the following list:

    1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc
    Each line gives the password policy and then the password. The password
    policy indicates the lowest and highest number of times a given letter must
    appear for the password to be valid. For example, 1-3 a means that the
    password must contain a at least 1 time and at most 3 times.

    In the above example, 2 passwords are valid. The middle password, cdefg, is
    not; it contains no instances of b, but needs at least 1. The first and
    third passwords are valid: they contain one a or nine c, both within the
    limits of their respective policies.

    How many passwords are valid according to their policies?
    ############################################################################
    """
    import pandas as pd
    # Lets create a pandas database with the data
    df = pd.read_csv(fn, delim_whitespace=True, header=None,
                        names=['vminVmax','letterC','pwd'])
    # That should make three columns, number of occurrences (min-max), letter,
    # and the actual password. Split the min-max column:
    df[['minLetter','maxLetter']] = df.vminVmax.str.split('-',expand=True)
    # Set the above to ints (we'll need to compare with them later)
    df = df.astype({'minLetter':'int32',
                    'maxLetter':'int32'})
    # There is a nasty ':' in the data - coud do with a nicer way of (quickly)
    # getting rid of that
    df[['letter','__']] = df.letterC.str.split(':',expand=True)
    # Now count how many letters appear in each password
    df['letterCount'] = df.apply(lambda x: x.pwd.count(x.letter),axis=1)
    # Now check if our password has a valid number of letters:
    df['validPwd'] = (df.letterCount >= df.minLetter) & (df.letterCount <= df.maxLetter)

    # Return number of valid passwords:
    return df.validPwd.sum()

################################################################################
def part2(fn):
    """
    Day 2. Part 2.

    ############################################################################
    While it appears you validated the passwords correctly, they don't seem to
    be what the Official Toboggan Corporate Authentication System is expecting.

    The shopkeeper suddenly realizes that he just accidentally explained the
    password policy rules from his old job at the sled rental place down the
    street! The Official Toboggan Corporate Policy actually works a little
    differently.

    Each policy actually describes two positions in the password, where 1 means
    the first character, 2 means the second character, and so on. (Be careful;
    Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of
    these positions must contain the given letter. Other occurrences of the
    letter are irrelevant for the purposes of policy enforcement.

    Given the same example list from above:

    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

    How many passwords are valid according to the new interpretation of the
    policies?
    ############################################################################
    """
    import pandas as pd
    # Lets create a pandas database with the data
    df = pd.read_csv(fn, delim_whitespace=True, header=None,
                        names=['vminVmax','letterC','pwd'])
    # That should make three columns, place of occurrences (first-second),
    # letter, and the actual password. Split the first-second column:
    df[['firstPos','secondPos']] = df.vminVmax.str.split('-',expand=True)
    # Set the above to ints (we'll need to compare with them later)
    df = df.astype({'firstPos':'int32',
                    'secondPos':'int32'})
    # This database doesn't use index 0, so we need to subtract 1 off them
    df[['firstPos','secondPos']] -= 1
    # There is a nasty ':' in the data - coud do with a nicer way of (quickly)
    # getting rid of that
    df[['letter','__']] = df.letterC.str.split(':',expand=True)
    # Now we check the letter in each position (which will return True/False)
    # and then sum these together. The sum will be exactly 1 if the password
    # is valid
    df['boolCount'] = df.apply(lambda x: ((x.pwd[x.firstPos] == x.letter) +
                                       (x.pwd[x.secondPos] == x.letter)),axis=1)

    # Return number of valid passwords:
    return (df.boolCount==1).sum()

################################################################################
if __name__ == "__main__":
    # print(part1('day2.dat'))
    print(part2('day2.dat'))
