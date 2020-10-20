import json

class OhmSettings:

    def __init__(self, settings_file):
        with open(settings_file) as settings:
            self.settings = json.load(settings)

        self.oclc_credentials = (self.settings['client_id'], self.settings['client_secret'])
        self.database = self.settings['database']
        self.exclude_periodical = self.settings['exclude_periodical']
        self.oclc_number = self.settings['oclc_number']
        self.ils_catalog_key = self.settings['ils_catalog_key']
        self.item = self.settings['item']
        self.bib_exclusions = self.settings['bib_exclusions']
        self.holding_map = self.settings['holding_codes']
        self.extract_naming_scheme = self.settings['extract_naming_scheme']

    def relevant_tags(self):
        tags = set()

        # Add field that holds OCLC tag, and second tag if required
        tags.add(self.oclc_number['tag'])
        if self.oclc_number['prefix_in_second_tag']:
            tags.add(self.oclc_number['second_tag'])
        
        # Add field for ILS key
        tags.add(self.ils_catalog_key['tag'])

        # Add field for items
        tags.add(self.item['tag'])

        # Add 008 if periodicals are to be excluded
        if self.exclude_periodical:
            tags.add('008')

        # Add all fields for bib exclusions
        for exclusion in self.bib_exclusions:
            tags.add(exclusion)
        
        return tags
