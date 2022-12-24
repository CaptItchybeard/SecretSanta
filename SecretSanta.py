from random import shuffle, randrange
import sys
import yaml

options = {}

with open('secretSanta.yaml', 'r') as file:
    contents = yaml.safe_load(file)
    if 'singles' in contents:
        for person in contents['singles']:
            options[person] = ''
    if 'couples' in contents:
        for couple in contents['couples']:
            for person in contents['couples'][couple]:
                options[person] = couple

# Put all people in hat
hat = list(options.keys())
shuffle(hat)

# Create empty final dict
secretSantas = {}

# Commence choosing
for santa in options:
    print(santa + ' is picking...')
    while True:
        choice = hat[randrange(0, len(hat))]
        if santa != choice and (options[santa] == '' or options[santa] != options[choice]):
            secretSantas[santa] = choice
            hat.remove(choice)
            break
        if len(hat) == 2 and options[hat[0]] == options[hat[1]] and (options[hat[0]] or options[hat[1]]):
            print('Impossible situation...')
            sys.exit(1)
        if len(hat) == 1 and santa == hat[0]:
            print('Last santa matches last choice...')
            sys.exit(1)

# Write out choices
for santa in secretSantas:
    fileName = santa + '.txt'
    with open(fileName, 'w') as file:
        file.write('You are the Secret Santa for ' + secretSantas[santa])

sys.exit(0)
