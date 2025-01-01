import argparse
import json
import os
import random
import sys
import yaml

class NaughtyList(Exception): pass

__OUTPUT_PATH_DEFAULT='results'
__MAX_RETRIES_DEFAULT=10

class SantaHat:
    def __init__(self, filename:str, max_retries:int=__MAX_RETRIES_DEFAULT):
        self.people:list[tuple[str,str]] = []
        self.matches:dict[str:str] = {}
        self.max_retries:int = max_retries

        print(f'Loading configuration from {filename}...', end='')
        with open(filename, 'r') as f:
            if filename.endswith(('.yaml', '.yml')):
                cfg_obj = yaml.safe_load(f)
            elif filename.endswith('.json'):
                cfg_obj = json.load(f)
            else:
                print('Naughty')
                raise NaughtyList('ERROR: Unsupported file type')
        for person in cfg_obj['individuals']:
            self.people.append((person, ''))
        for group in cfg_obj['groups']:
            for person in cfg_obj['groups'][group]:
                self.people.append((person, group))
        print('Nice')

    def __str__(self)->str:
        return f'people: {self.people}'

    def pick_all(self):
        print('Commencing picking ritual')
        
        # Initialize variables
        hat = self.people[:]
        pickers = hat[:]

        # Retry loop
        for retry in range(self.max_retries):
            self.matches = {}
            random.shuffle(hat)
            random.shuffle(pickers)
            try:
                for i in range(len(pickers)):
                    if pickers[i][1] and pickers[i][1] == hat[i][1]:
                        # Both options are in same group
                        raise NaughtyList()
                    elif not pickers[i][1] and not hat[i][1] and pickers[i][0] == pickers[i][0]:
                        # Both options are same individual
                        raise NaughtyList()
                    # Assign match
                    self.matches[f'{pickers[i][0]} {pickers[i][1]}'] = f'{hat[i][0]} {hat[i][1]}'
            except NaughtyList:
                if retry+1 == self.max_retries:
                    print(f'ERROR: max_retries({self.max_retries}) met with no successful matches')
                    sys.exit(1)
                continue
        print('Ritual complete')

    def dump_matches(self, path:str=__OUTPUT_PATH_DEFAULT):
        if not self.matches:
            raise NaughtyList('No matches to dump')
        
        print(f'Dumping match files to {path}...', end='')
        if not os.path.isdir(path):
            os.mkdir(path)
        
        for match in self.matches:
            with open(os.path.join(path, f'{match.strip()}.txt'), 'w') as f:
                lines = [
                    f'Dear [{match.strip()}],',
                    f'Please be a good Secret Santa for [{self.matches[match]}].',
                    '    Warmest Regards,',
                    '    Actual Santa'
                ]
                f.write('\n'.join(lines))
        print('Nice')

def main(input_config:str, output_path:str=__OUTPUT_PATH_DEFAULT, max_retries:int=__MAX_RETRIES_DEFAULT):
    if not os.path.isfile(input_config):
        raise NaughtyList(f'{input_config} does not exist')
    
    hat = SantaHat(filename=input_config, max_retries=max_retries)
    hat.pick_all()
    hat.dump_matches(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='secret_santa',
        description='Generates random secret santa picks from provided config file',
    )
    parser.add_argument(
        'config_file',
        type=str,
        help='Config file including individual and group names (.yaml and .json supported)'
    )
    parser.add_argument(
        '-r',
        '--retries',
        type=int,
        default=__MAX_RETRIES_DEFAULT,
        help='Max number of retries defined for picking ritual, Default=10'
    )
    parser.add_argument(
        '-o',
        '--output-path',
        type=str,
        default=__OUTPUT_PATH_DEFAULT,
        help='Path to dump match txt files, Default="results"'
    )
    args = parser.parse_args()
    main(input_config=args.config_file, output_path=args.output_path, max_retries=args.retries)
