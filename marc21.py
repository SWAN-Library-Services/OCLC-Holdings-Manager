# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Marc21(KaitaiStruct):
    """
    .. seealso::
       Source - https://www.loc.gov/marc/specifications/specrecstruc.html
    """

    class BibliographicLevel(Enum):
        monographic_component_part = 97
        serial_component_part = 98
        collection = 99
        subunit = 100
        integrating_resource = 105
        monograph_item = 109
        serial = 115

    class TypeOfControl(Enum):
        no_specified_type = 32
        archival = 97

    class CharacterCodingScheme(Enum):
        marc_8 = 32
        unicode = 97

    class MultipartResourceRecordLevel(Enum):
        not_specified_or_not_applicable = 32
        set = 97
        part_with_independent_title = 98
        part_with_dependent_title = 99

    class DescriptiveCatalogingForm(Enum):
        non_isbd = 32
        aacr_2 = 97
        isbd_punctuation_omitted = 99
        isbd_punctuation_included = 105
        non_isbd_punctuation_omitted = 110
        unknown = 117

    class EncodingLevel(Enum):
        full_level = 32
        full_level_material_not_examined = 49
        less_than_full_level_material_not_examined = 50
        abbreviated_level = 51
        core_level = 52
        partial_preliminary_level = 53
        minimum_level = 55
        prepublication_level = 56
        system_identified_marc_error_in_batchload_record = 69
        full_level_input_by_oclc_participants = 73
        deleted_record = 74
        less_than_full_input_by_oclc_participants = 75
        full_level_input_added_from_a_batch_process = 76
        less_than_full_level_input_added_from_a_batch_process = 77
        unknown = 117
        not_applicable = 122

    class RecordStatus(Enum):
        increase_in_encoding_level = 97
        corrected_or_revised = 99
        deleted = 100
        new = 110
        increse_in_encoding_level_from_prepublication = 112

    class TypeOfRecord(Enum):
        language_material = 97
        notated_music = 99
        manuscript_notated_music = 100
        cartographic_material = 101
        manuscript_cartographic_material = 102
        projected_medium = 103
        nonmusical_sound_recording = 105
        musical_sound_recording = 106
        two_dimensional_nonprojectable_graphic = 107
        computer_file = 109
        kit = 111
        mixed_materials = 112
        three_dimensional_artifact_or_naturally_occurring_object = 114
        manuscript_language_material = 116
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_record = []
        self.record = []
        i = 0
        while not self._io.is_eof():
            self._raw_record.append(self._io.read_bytes_term(29, False, True, True))
            io = KaitaiStream(BytesIO(self._raw_record[-1]))
            self.record.append(self._root.Record(io, self, self._root))
            i += 1


    class VariableFields(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variable_data = self._io.read_bytes_full()


    class Field(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.tag = (self._io.read_bytes(3)).decode(u"ascii")
            self.length_of_field = (self._io.read_bytes(4)).decode(u"ascii")
            self.starting_character_position = (self._io.read_bytes(5)).decode(u"ascii")

        @property
        def field_data(self):
            if hasattr(self, '_m_field_data'):
                return self._m_field_data if hasattr(self, '_m_field_data') else None

            io = self._parent._parent.variable_fields._io
            _pos = io.pos()
            io.seek(int(self.starting_character_position))
            _on = self._parent._parent.leader.character_coding_scheme
            if _on == ' ':
                self._m_field_data = (KaitaiStream.bytes_terminate(io.read_bytes(int(self.length_of_field)), 30, False)).decode(u"latin-1")
            elif _on == 'a':
                self._m_field_data = (KaitaiStream.bytes_terminate(io.read_bytes(int(self.length_of_field)), 30, False)).decode(u"utf-8")
            else:
                self._m_field_data = io.read_bytes(int(self.length_of_field))
            io.seek(_pos)
            return self._m_field_data if hasattr(self, '_m_field_data') else None


    class Leader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.record_length = (self._io.read_bytes(5)).decode(u"ascii")
            self.record_status = (self._io.read_bytes(1)).decode(u"ascii")
            self.type_of_record = (self._io.read_bytes(1)).decode(u"ascii")
            self.bibliographic_level = (self._io.read_bytes(1)).decode(u"ascii")
            self.type_of_control = (self._io.read_bytes(1)).decode(u"ascii")
            self.character_coding_scheme = (self._io.read_bytes(1)).decode(u"ascii")
            self.indicator_count = (self._io.read_bytes(1)).decode(u"ascii")
            self.subfield_code_length = (self._io.read_bytes(1)).decode(u"ascii")
            self.base_address_of_data = (self._io.read_bytes(5)).decode(u"ascii")
            self.encoding_level = (self._io.read_bytes(1)).decode(u"ascii")
            self.descriptive_cataloging_form = (self._io.read_bytes(1)).decode(u"ascii")
            self.multipart_resource_record_level = (self._io.read_bytes(1)).decode(u"ascii")
            self.entry_map = (self._io.read_bytes(4)).decode(u"ascii")


    class Record(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_leader = self._io.read_bytes(24)
            io = KaitaiStream(BytesIO(self._raw_leader))
            self.leader = self._root.Leader(io, self, self._root)
            self._raw_directory = self._io.read_bytes_term(30, False, True, True)
            io = KaitaiStream(BytesIO(self._raw_directory))
            self.directory = self._root.Directory(io, self, self._root)
            self._raw_variable_fields = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_variable_fields))
            self.variable_fields = self._root.VariableFields(io, self, self._root)


    class Directory(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fields = []
            i = 0
            while not self._io.is_eof():
                self.fields.append(self._root.Field(self._io, self, self._root))
                i += 1




