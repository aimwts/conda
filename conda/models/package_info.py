# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from logging import getLogger

from .channel import Channel
from .enums import NoarchType
from .records import IndexJsonRecord, IndexRecord, PathsData
from .._vendor.auxlib.entity import (ComposableField, Entity, EnumField,
                                     ImmutableEntity, IntegerField, ListField, StringField)
from ..common.compat import string_types

log = getLogger(__name__)


class NoarchField(EnumField):
    def box(self, instance, instance_type, val):
        return super(NoarchField, self).box(instance, instance_type, NoarchType.coerce(val))


class Noarch(Entity):
    type = NoarchField(NoarchType)
    entry_points = ListField(string_types, required=False, nullable=True, default=None,
                             default_in_dump=False)


class PreferredEnv(Entity):
    name = StringField()
    executable_paths = ListField(string_types, required=False, nullable=True)
    softlink_paths = ListField(string_types, required=False, nullable=True)


class PackageMetadata(Entity):
    # from info/package_metadata.json
    package_metadata_version = IntegerField()
    noarch = ComposableField(Noarch, required=False, nullable=True)
    preferred_env = ComposableField(PreferredEnv, required=False, nullable=True, default=None,
                                    default_in_dump=False)


class PackageInfo(ImmutableEntity):

    # attributes external to the package tarball
    extracted_package_dir = StringField()
    channel = ComposableField(Channel)
    repodata_record = ComposableField(IndexRecord)
    url = StringField()

    # attributes within the package tarball
    index_json_record = ComposableField(IndexJsonRecord)
    icondata = StringField(required=False, nullable=True)
    package_metadata = ComposableField(PackageMetadata, required=False, nullable=True)
    paths_data = ComposableField(PathsData)

    def dist_str(self):
        return "%s::%s-%s-%s" % (self.channel.canonical_name, self.name, self.version, self.build)

    @property
    def name(self):
        return self.repodata_record.name

    @property
    def version(self):
        return self.repodata_record.version

    @property
    def build(self):
        return self.repodata_record.build

    @property
    def build_number(self):
        return self.repodata_record.build_number
