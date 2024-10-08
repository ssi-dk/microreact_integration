from base64 import b64encode
from dataclasses import dataclass, asdict, field
from abc import ABC
from typing import Optional
from uuid import uuid4
from jsonschema import validate
from json import loads
from pathlib import Path

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


class Element(ABC):
    """
    Subclasses of this class are only used for creating NEW elements (not yet in Microreact).
    __post_init__ in all subclasses must call super().set_id().
    """
    id: str=''

    def set_id(self):
        if self.id == '':
            self.id = str(uuid4())
            return self.id


@dataclass
class Dataset(Element):
    file: str
    idFieldName: str

    def __post_init__(self):
        super().set_id()

    def to_dict(self):
        return asdict(self)

@dataclass
class File(Element):
    type: str
    body: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = ''
    format: Optional[str] = ''
    mimetype: Optional[str] = ''

    def __post_init__(self):
        super().set_id()
        if self.type == 'data':
            if self.name == '':
                self.name = 'metadata.csv'
            if self.format == '':
                self.format = 'text/csv'
            if self.mimetype == '':
                self.mimetype = 'data:application/vnd.ms-excel;base64'
        elif self.type == 'tree':
            if self.name == '':
                self.name = 'tree.nwk'
            if self.format == '':
                self.format = 'text/x-nh'
            if self.mimetype == '':
                self.mimetype = 'data:application/octet-stream;base64'
        else:
            raise ValueError("Invalid file type: " + type)
    
    def to_dict(self):
        if self.body:
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
        elif self.url:
            return {
                "id": self.id,
                "type": self.type,
                "name": self.name,
                "format": self.format,
                "url": self.url
            }
        else:
            raise ValueError("File object must contain either body or url")

@dataclass
class Column:
    field: str
    fixed: bool

@dataclass
class Table(Element):
    title: str
    columns: list
    file: str
    dataset: str  # TODO Should this be optional? There might be cases in my code where I don't use it
    hidden: list

    def __post_init__(self):
        if self.hidden is None:
            self.hidden = list()
        super().set_id()

    def get_col_list(self):
        col_list = list()
        for column in self.columns:
            col_list.append({
						"field": column,
						"fixed": False,
                        "hidden": True if column in self.hidden else False
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
class Matrix(Element):
    file: str
    title: str = "Matrix"

    def __post_init__(self):
        super().set_id()
    
    def to_dict(self):
        return {
            'file': self.file,
            'title': self.title,
            'id': self.id
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

    def __post_init__(self):
        super().set_id()

@dataclass
class Tree(Element):
    file: File
    type: str = "rc"
    title: str = "Tree"
    labelField: str = "ID"
    highlightedId: str = None

    def __post_init__(self):
        super().set_id()

    def to_dict(self):
        return {
            "id": self.id,
            "file": self.file,
            "type": self.type,
            "title": self.title,
            "labelField": self.labelField,
            "highligthedId": self.highlightedId,
            "showBranchLengths": True,
            "branchLengthsDigits": 0,
            "showLeafLabels": True,
            "labelField": self.labelField,
        }

@dataclass
class Project:
    """Main class for structuring data that will be sent to Microreact when creating a new project.
    Use the built-in asdict method to convert data to a dict which in turn can be converted to JSON."""

    meta: Meta
    datasets: list
    files: list
    tables: list
    trees: list
    matrices: list = field(default_factory=list)

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

    # schema_url is not actively used for anything; it is just a reference.
    schema_url: str="https://microreact.org/schema/v1.json"

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
            'views',
            'matrices'
        ]

    def dictify_section(self, section_name: str):
        section_dict = dict()
        for element in getattr(self, section_name):
            assert getattr(element, 'id') not in section_dict  # Make sure ids are not duplicated
            section_dict[element.id] = element.to_dict()
        return section_dict
    
    def to_dict(self):
        output_dict = {
            'schema': self.schema_url,
            'meta': self.meta.to_dict()
        }
        for section in self.get_sections():
            output_dict[section] = self.dictify_section(section)
        
        validate_json(output_dict)
        return output_dict