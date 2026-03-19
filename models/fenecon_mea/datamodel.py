# Auto generated from fenecon_mea.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-03-19T12:34:49
# Schema: sensor_payload
#
# id: https://example.org/sensor-data
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Float, Integer

metamodel_version = "1.7.0"
version = None

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = CurieNamespace('', 'https://example.org/sensor-data/')


# Types

# Class references



@dataclass(repr=False)
class SensorPayload(YAMLRoot):
    """
    The root object for the MQTT sensor message.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/SensorPayload")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "SensorPayload"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/SensorPayload")

    tags: Union[dict, "Metadata"] = None
    fields: Union[dict, "Measurements"] = None
    time: int = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.tags):
            self.MissingRequiredField("tags")
        if not isinstance(self.tags, Metadata):
            self.tags = Metadata(**as_dict(self.tags))

        if self._is_empty(self.fields):
            self.MissingRequiredField("fields")
        if not isinstance(self.fields, Measurements):
            self.fields = Measurements(**as_dict(self.fields))

        if self._is_empty(self.time):
            self.MissingRequiredField("time")
        if not isinstance(self.time, int):
            self.time = int(self.time)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Metadata(YAMLRoot):
    """
    Unique identifiers for BESS and FEMS units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/Metadata")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Metadata"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/Metadata")

    BESS_id: int = None
    FEMS_id: int = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.BESS_id):
            self.MissingRequiredField("BESS_id")
        if not isinstance(self.BESS_id, int):
            self.BESS_id = int(self.BESS_id)

        if self._is_empty(self.FEMS_id):
            self.MissingRequiredField("FEMS_id")
        if not isinstance(self.FEMS_id, int):
            self.FEMS_id = int(self.FEMS_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Measurements(YAMLRoot):
    """
    The actual telemetry values recorded.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/Measurements")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Measurements"
    class_model_uri: ClassVar[URIRef] = URIRef("https://example.org/sensor-data/Measurements")

    ctrlmode: Optional[int] = None
    activepower: Optional[float] = None
    soc: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ctrlmode is not None and not isinstance(self.ctrlmode, int):
            self.ctrlmode = int(self.ctrlmode)

        if self.activepower is not None and not isinstance(self.activepower, float):
            self.activepower = float(self.activepower)

        if self.soc is not None and not isinstance(self.soc, int):
            self.soc = int(self.soc)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.sensorPayload__tags = Slot(uri=DEFAULT_.tags, name="sensorPayload__tags", curie=DEFAULT_.curie('tags'),
                   model_uri=DEFAULT_.sensorPayload__tags, domain=None, range=Union[dict, Metadata])

slots.sensorPayload__fields = Slot(uri=DEFAULT_.fields, name="sensorPayload__fields", curie=DEFAULT_.curie('fields'),
                   model_uri=DEFAULT_.sensorPayload__fields, domain=None, range=Union[dict, Measurements])

slots.sensorPayload__time = Slot(uri=DEFAULT_.time, name="sensorPayload__time", curie=DEFAULT_.curie('time'),
                   model_uri=DEFAULT_.sensorPayload__time, domain=None, range=int)

slots.metadata__BESS_id = Slot(uri=DEFAULT_.BESS_id, name="metadata__BESS_id", curie=DEFAULT_.curie('BESS_id'),
                   model_uri=DEFAULT_.metadata__BESS_id, domain=None, range=int)

slots.metadata__FEMS_id = Slot(uri=DEFAULT_.FEMS_id, name="metadata__FEMS_id", curie=DEFAULT_.curie('FEMS_id'),
                   model_uri=DEFAULT_.metadata__FEMS_id, domain=None, range=int)

slots.measurements__ctrlmode = Slot(uri=DEFAULT_.ctrlmode, name="measurements__ctrlmode", curie=DEFAULT_.curie('ctrlmode'),
                   model_uri=DEFAULT_.measurements__ctrlmode, domain=None, range=Optional[int])

slots.measurements__activepower = Slot(uri=DEFAULT_.activepower, name="measurements__activepower", curie=DEFAULT_.curie('activepower'),
                   model_uri=DEFAULT_.measurements__activepower, domain=None, range=Optional[float])

slots.measurements__soc = Slot(uri=DEFAULT_.soc, name="measurements__soc", curie=DEFAULT_.curie('soc'),
                   model_uri=DEFAULT_.measurements__soc, domain=None, range=Optional[int])

