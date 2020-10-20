from marc21 import Marc21
import mmap
import time
from re import sub
from ohm_database import OhmDatabase
from ohm_settings import OhmSettings

class OhmMarc:

    def __init__(self, database: OhmDatabase, settings: OhmSettings, marc_file, table_name):
        self.database = database
        self.marc_file = marc_file
        self.settings = settings
        self.holding_map = self.settings.holding_map
        self.relevant_tags = self.settings.relevant_tags()
        self.table_name = table_name

        # Create the table that will be used to store data
        self.database.create_table(self.table_name)

    def get_all_subfields(self, field):
        return field.field_data.split(bytes.fromhex('1f').decode())

    # returns first result or empty string if not found
    def get_subfield_by_code(self, field, subfield_code):
        subfields = self.get_all_subfields(field)
        for subfield in subfields:
            if subfield.startswith(subfield_code):
                return subfield[1:]
        return ""

    def parse_record(self, marc_record):
        oclc_number = "0"
        ils_catalog_key = ""
        oclc_holdings = set()
        oclc_valid = False

        try:
        # loop through fields in the directory
            for field in marc_record.directory.fields:

                # look for relevent tags
                if field.tag in self.relevant_tags:
                    
                    # Exclusions for periodicals. Will not run unless the field tag is included based on config
                    if field.tag == '008':
                        # Field 008 holds info on determining periodicals
                        if marc_record.leader.type_of_record in ['a'] and marc_record.leader.bibliographic_level in ['b', 'i', 's']:
                            if field.field_data[21] in ['p'] and field.field_data[18] in ['b', 'c', 'd', 'e', 'f', 'i', 'j', 'm', 'q', 's', 't', 'w']:
                                return

                    # Check for OCLC number in field specified by config
                    if field.tag == self.settings.oclc_number["tag"]:
                        if self.settings.oclc_number["subfield"]:
                            oclc_number_temp = self.get_subfield_by_code(field, self.settings.oclc_number["subfield"])
                        else:
                            oclc_number_temp = field.field_data
                        
                        if self.settings.oclc_number["prefix"] and not self.settings.oclc_number["prefix_in_second_tag"]:
                            if oclc_number_temp.startswith(self.settings.oclc_number["prefix"]):
                                oclc_number_value = sub(r"\D", "", oclc_number_temp).lstrip("0")
                                if oclc_number_value and int(oclc_number_value) > int(oclc_number):
                                    oclc_number = oclc_number_value
                                    oclc_valid = True
                        else:
                            oclc_number_value = sub(r"\D", "", oclc_number_temp).lstrip("0")
                            if oclc_number_value and int(oclc_number_value) > int(oclc_number):
                                oclc_number = oclc_number_value
                                oclc_valid = True

                    # Check for prefix in secondary tag if configured
                    if self.settings.oclc_number["prefix_in_second_tag"] and field.tag == self.settings.oclc_number["second_tag"]:
                        if field.field_data == self.settings.oclc_number["prefix"]:
                            oclc_valid = True
                        else:
                            return
                    # Field 901, subfield a holds SWAN's catalog key
                    if field.tag == self.settings.ils_catalog_key["tag"]:
                        if self.settings.ils_catalog_key["subfield"]:
                            ils_catalog_key_temp = self.get_subfield_by_code(field, self.settings.ils_catalog_key["subfield"])
                        else:
                            ils_catalog_key_temp = field.field_data

                        if self.settings.ils_catalog_key["prefix"]:
                            if ils_catalog_key_temp.startswith(self.settings.ils_catalog_key["prefix"]):
                                ils_catalog_key = ils_catalog_key_temp
                        else:
                            ils_catalog_key = ils_catalog_key_temp

                    if field.tag in self.settings.bib_exclusions:
                        if self.settings.bib_exclusions[field.tag]["subfield"]:
                            subfields = self.get_all_subfields(field)
                            for subfield in subfields:
                                if subfield.startswith(self.settings.bib_exclusions[field.tag]["subfield"]): 
                                    if subfield[1:] in self.settings.bib_exclusions[field.tag]["data"]:
                                        return
                        else:
                            if self.settings.bib_exclusions[field.tag]["data"] == "*":
                                return
                            if field.field_data in self.settings.bib_exclusions[field.tag]["data"]:
                                return
                    # field 999 is SWAN's holding tag
                    if field.tag == self.settings.item["tag"]:

                        includeCopy = True
                        # split subfields by the subfield delimiter and store as array
                        # 0x1f is the subfield delimiter
                        subfields = self.get_all_subfields(field)
                        # loop through subfields to find relevant data
                        for subfield in subfields:
                            
                            if subfield[:1] in self.settings.item["exclusions"]:
                                if subfield[1:] in self.settings.item["exclusions"][subfield[:1]]:
                                    includeCopy = False

                            # subfield m is holding library for SWAN
                            if subfield.startswith(self.settings.item["subfield"]): 
                                if self.settings.item["ils_library_code_length"] > 0:
                                    ils_library_code = subfield[1:1+self.settings.item["ils_library_code_length"]]
                                else:
                                    ils_library_code = subfield[1:]
                                if ils_library_code in self.holding_map:
                                    oclc_symbol = self.holding_map[ils_library_code]
                                else:
                                    includeCopy = False
                        if includeCopy and "oclc_symbol" in locals():
                            oclc_holdings.add(oclc_symbol)

            #if oclc_number != "0" and oclc_valid:
            if oclc_valid:
                for oclc_symbol in oclc_holdings:
                    self.database.insert_record(self.table_name, ils_catalog_key, oclc_number, oclc_symbol)
        except TypeError:
            print(f"error in record {self.count}: {ils_catalog_key}")

    def parse_marc_file(self):
        # start time for benchmarking
        startTime = time.time()

        # count stores number of records processed
        self.count = 0

        # open file in read-only as binary
        with open(self.marc_file, "rb+") as f:
            # currentPos is used to keep track of location in file for mmap
            currentPos = 0
            # initialize mmap with open file
            # we are using mmap to open large files without needing to hold entire file in memory
            mm = mmap.mmap(f.fileno(), 0)
            # find size of file
            fileSize = mm.size()
            # 0x1d is the end of record delimitor of MARC21
            record_delimitor = bytes.fromhex('1d')

            # loop through file until full file is processed
            while( currentPos < fileSize):
                # find end of record using the end of record delimiter
                recordEnd = mm.find(record_delimitor, currentPos) + 1
                # read individual MARC21 record
                m = Marc21.from_bytes(mm[currentPos:recordEnd])
                # Run the logic to get relevent info from MARC record
                self.parse_record(m.record[0])

                # update position for mmap
                currentPos = recordEnd
                # increase processed record count
                self.count += 1

        # Write changes and close sqlite database
        self.database.commit_and_close()

        # display count
        print("count: " + str(self.count))

        # end time for benchmarking
        endTime = time.time()

        elapsedTime = endTime - startTime
        print("Elapsed time: " + str(elapsedTime / 60) + " minutes")

        print("Records per second: " + str(self.count / elapsedTime))