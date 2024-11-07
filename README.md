# SecretSanta

This program is used to choose people for a Secret Santa gift exchange.

To use, add names into the SecretSanta.yaml file, with couples grouped together by last name or a unique string. These groups will not get eachother when names are picked.

Individuals who can pick anyone should be placed in the `individuals` group.

Program will create text files named by the secret Santa, with their person inside of it. These can then be distributed however you see fit.

Run `python secret_santa.py -h` for arguments to use.
