# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: probe.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='probe.proto',
  package='probemon',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bprobe.proto\x12\x08probemon\"\xd8\x01\n\x06Probes\x12\x0b\n\x03mac\x18\x01 \x01(\t\x12\x0e\n\x06vendor\x18\x02 \x01(\t\x12\r\n\x05known\x18\x03 \x01(\x08\x12$\n\x05ssids\x18\x04 \x03(\x0b\x32\x15.probemon.Probes.Ssid\x12+\n\x08probereq\x18\x05 \x03(\x0b\x32\x19.probemon.Probes.Probereq\x1a\x14\n\x04Ssid\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\x39\n\x08Probereq\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x0c\n\x04rssi\x18\x02 \x01(\x11\x12\x0c\n\x04ssid\x18\x03 \x01(\x05\"*\n\x06MyData\x12 \n\x06probes\x18\x01 \x03(\x0b\x32\x10.probemon.Probesb\x06proto3')
)




_PROBES_SSID = _descriptor.Descriptor(
  name='Ssid',
  full_name='probemon.Probes.Ssid',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='probemon.Probes.Ssid.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=163,
  serialized_end=183,
)

_PROBES_PROBEREQ = _descriptor.Descriptor(
  name='Probereq',
  full_name='probemon.Probes.Probereq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='probemon.Probes.Probereq.timestamp', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rssi', full_name='probemon.Probes.Probereq.rssi', index=1,
      number=2, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssid', full_name='probemon.Probes.Probereq.ssid', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=185,
  serialized_end=242,
)

_PROBES = _descriptor.Descriptor(
  name='Probes',
  full_name='probemon.Probes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mac', full_name='probemon.Probes.mac', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vendor', full_name='probemon.Probes.vendor', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='known', full_name='probemon.Probes.known', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssids', full_name='probemon.Probes.ssids', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='probereq', full_name='probemon.Probes.probereq', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PROBES_SSID, _PROBES_PROBEREQ, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=242,
)


_MYDATA = _descriptor.Descriptor(
  name='MyData',
  full_name='probemon.MyData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='probes', full_name='probemon.MyData.probes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=244,
  serialized_end=286,
)

_PROBES_SSID.containing_type = _PROBES
_PROBES_PROBEREQ.containing_type = _PROBES
_PROBES.fields_by_name['ssids'].message_type = _PROBES_SSID
_PROBES.fields_by_name['probereq'].message_type = _PROBES_PROBEREQ
_MYDATA.fields_by_name['probes'].message_type = _PROBES
DESCRIPTOR.message_types_by_name['Probes'] = _PROBES
DESCRIPTOR.message_types_by_name['MyData'] = _MYDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Probes = _reflection.GeneratedProtocolMessageType('Probes', (_message.Message,), dict(

  Ssid = _reflection.GeneratedProtocolMessageType('Ssid', (_message.Message,), dict(
    DESCRIPTOR = _PROBES_SSID,
    __module__ = 'probe_pb2'
    # @@protoc_insertion_point(class_scope:probemon.Probes.Ssid)
    ))
  ,

  Probereq = _reflection.GeneratedProtocolMessageType('Probereq', (_message.Message,), dict(
    DESCRIPTOR = _PROBES_PROBEREQ,
    __module__ = 'probe_pb2'
    # @@protoc_insertion_point(class_scope:probemon.Probes.Probereq)
    ))
  ,
  DESCRIPTOR = _PROBES,
  __module__ = 'probe_pb2'
  # @@protoc_insertion_point(class_scope:probemon.Probes)
  ))
_sym_db.RegisterMessage(Probes)
_sym_db.RegisterMessage(Probes.Ssid)
_sym_db.RegisterMessage(Probes.Probereq)

MyData = _reflection.GeneratedProtocolMessageType('MyData', (_message.Message,), dict(
  DESCRIPTOR = _MYDATA,
  __module__ = 'probe_pb2'
  # @@protoc_insertion_point(class_scope:probemon.MyData)
  ))
_sym_db.RegisterMessage(MyData)


# @@protoc_insertion_point(module_scope)
