import argparse
import json
import os
from random import shuffle, randrange
import yaml

class NaughtyList(Exception): pass

class SantaHat:
    def __init__(self, filename:str):
        self.individuals = []
        self.groups = {}
        self.matches = {}

        print(f'Loading configuration from {filename}...', end='')
        with open(filename, 'r') as f:
            if filename.endswith(('.yaml', '.yml')):
                yaml_obj = yaml.safe_load(f)
                self.individuals = yaml_obj['individuals']
                groups = yaml_obj['groups']
                for group in groups:
                    self.groups[group] = list(groups[group])
            elif filename.endswith('.json'):
                json_obj = json.load(f)
                self.individuals = json_obj['individuals']
                for group in json_obj['groups']:
                    self.groups[group] = list(json_obj['groups'][group])
            else:
                print('Naughty')
                raise NaughtyList('ERROR: Unsupported file type')
        print('Nice')

    def pick_all(self):
        print('Filling hat...', end='')
        hat = self.individuals[:]
        for group in self.groups:
            hat += self.groups[group]
        pickers = hat[:]
        shuffle(pickers)
        print('Nice')

        print('Commencing picking ritual')
        self.matches = {}
        for santa in pickers:
            print(f'{santa} is picking...', end='')
            if ((len(hat) == 1 and santa == hat[0]) or
                self.__in_same_group(hat + [santa])):
                print('Naughty')
                raise NaughtyList('ERROR: Unable to complete matching with remaining options in hat')
            while True:
                shuffle(hat)
                choice = hat[0]
                if (not self.__in_same_group([santa, choice]) and
                    santa != choice):
                    break
            self.matches[santa] = choice
            hat.pop(0)
            print('Nice')
        print('Ritual complete')
    
    def __str__(self)->str:
        return '\n'.join([
            f'indivs: {self.individuals}',
            f'groups: {self.groups}'
        ])

    def __in_same_group(self, people:list[str])->bool:
        # Return False if no groups are defined
        if not self.groups:
            return False
        
        # For each group, check if all options in people are in same group
        for group in self.groups:
            if set(people).issubset(self.groups[group]):
                return True
        return False

    def dump_matches(self, path:str=''):
        if not self.matches:
            raise NaughtyList('No matches to dump')
        
        print(f'Dumping match files to {path}...', end='')
        if not path:
            path = os.getcwd()
        elif not os.path.isdir(path):
            os.mkdir(path)
        
        for match in self.matches:
            with open(os.path.join(path, f'{match}.txt'), 'w') as f:
                lines = [
                    f'Dear [{match}],',
                    f'Please be a good Secret Santa for [{self.matches[match]}].',
                    '    Warmest Regards,',
                    '    Actual Santa',
                    ' '*randrange(10, 100)
                ]
                f.write('\n'.join(lines))
        print('Nice')

def main(input_config:str, output_path:str=''):
    if not os.path.isfile(input_config):
        raise NaughtyList(f'{input_config} does not exist')
    
    hat = SantaHat(input_config)
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
        '-o',
        '--output-path',
        type=str,
        help='Path to dump match txt files'
    )
    args = parser.parse_args()
    print(args.config_file)
    main(args.config_file, args.output_path)
