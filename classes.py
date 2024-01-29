from base64 import b64encode
from json import loads
from pathlib import Path
from dataclasses import dataclass, asdict, field
from abc import ABC
from uuid import uuid4

from jsonschema import validate

current_dir = Path(__file__).parent
with open(Path(current_dir, 'microreact_project_schema_v1.json'), 'r') as schema_file:
    MR_PROJECT_SCHEMA = loads(schema_file.read())

def validate_json(json_dict:dict):
    return validate(json_dict, MR_PROJECT_SCHEMA)

@dataclass
class Meta:
    name: str
    # description: str

    def to_dict(self):
        return {'name': self.name}


@dataclass
class Element(ABC):
    """
    An id string must be provided; however, if it's empty, a unique id will be created
    """

    id:str

    def __post_init__(self):
        if self.id == '':
            self.id = str(uuid4())


@dataclass
class Dataset(Element):
    file: str
    idFieldName: str

    def to_dict(self):
        return asdict(self)

class File(Element):
    type: str
    name: str
    format: str
    mimetype: str
    body: str

    def __init__(self, project_name, type, body):
        if type == 'data':
            self.id = project_name + '_metadata'
            self.name = project_name + '_metadata.csv'
            self.format = 'text/csv'
            self.mimetype = 'data:application/vnd.ms-excel;base64'
        elif type == 'tree':
            self.id = project_name + '_tree'
            self.name = project_name + '_tree.nwk'
            self.format = 'text/x-nh'
            self.mimetype = 'data:application/octet-stream;base64'
        else:
            raise ValueError("Invalid file type: " + type)
        self.type = type
        self.body = body
    
    def to_dict(self):
        blob = b64encode(self.body.encode('utf-8'))
        blob_str = str(blob)
        blob_str = blob_str[2:-1]
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "format": self.format,
            "blob": self.mimetype + ',' + blob_str
        }

@dataclass
class Column:
    field: str
    fixed: bool

@dataclass
class Table(Element):
    title: str
    columns: list
    file: str

    def get_col_list(self):
        col_list = list()
        for column in self.columns:
            col_list.append(					{
						"field": column,
						"fixed": False
					},)
        return col_list
    
    def to_dict(self):
        return {
            'title': self.title,
            'id': self.id,
            'columns': self.get_col_list(),
            'file': self.file
        }

@dataclass
class Timeline(Element):
    bounds: None
    controls: False
    nodeSize: 14
    playing: False
    speed: 1
    laneField: None
    unit: None
    viewport: None
    style: str = "bar"
    title: str = "Timeline"
    dataType: str = "year-month-day"
    yearField: str = "Year"

@dataclass
class Tree(Element):
    file: File
    type: str = "rc"
    title: str = "Tree"
    labelField: str = "ID"
    highlightedId: str = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Project:
    """Main class for structuring data that will be sent to Microreact when creating a new project.
    Use the built-in asdict method to convert data to a dict which in turn can be converted to JSON."""

    meta: Meta
    datasets: list
    files: list
    tables: list
    trees: list

    """These element types are not necessary for a basic project;
    however, empty lists must be present for the schema to validate."""
    timelines: list = field(default_factory=list)
    charts: list = field(default_factory=list)
    filters: list = field(default_factory=list)
    maps: list = field(default_factory=list)
    networks: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    panes: list = field(default_factory=list)
    slicers: list = field(default_factory=list)
    styles: list = field(default_factory=list)
    timelines: list = field(default_factory=list)
    views: list = field(default_factory=list)

    schema: str="https://microreact.org/schema/v1.json"

    def get_sections(self):
        return [
            'datasets',
            'files',
            'tables',
            'trees',
            'timelines',
            'charts',
            'filters',
            'maps',
            'networks',
            'notes',
            'panes',
            'slicers',
            'styles',
            'timelines',
            'views'
        ]

    def dictify_section(self, section_name: str):
        section_dict = dict()
        for element in getattr(self, section_name):
            assert getattr(element, 'id') not in section_dict  # Make sure ids are not duplicated
            section_dict[element.id] = element.to_dict()
        return section_dict
    
    def to_dict(self):
        output_dict = {
            'schema': self.schema,
            'meta': self.meta.to_dict()
        }
        for section in self.get_sections():
            output_dict[section] = self.dictify_section(section)
        
        validate(instance=output_dict, schema=MR_PROJECT_SCHEMA)
        return output_dict