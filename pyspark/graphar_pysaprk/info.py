"""
Copyright 2022-2023 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from py4j.java_gateway import JavaObject

from graphar_pysaprk import GraphArSession
from graphar_pysaprk.enums import AdjListType, FileType, GarType

# TODO: Discuss who should check and catch Java NPEs and other JVM-exceptionsin


class Property:
    """The property information of vertex or edge."""

    def __init__(
        self,
        name: Optional[str],
        data_type: Optional[GarType],
        is_primary: Optional[bool],
        jvm_obj: Optional[JavaObject] = None,
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_obj is not None:
            self._jvm_property_obj = jvm_obj
        else:
            property = GraphArSession._graphar.Property()
            property.setName(name)
            property.setData_type(data_type.value)
            property.setIs_primary(is_primary)

            self._jvm_property_obj = property

    def get_name(self) -> str:
        return self._jvm_property_obj.getName()

    def set_name(self, name: str) -> None:
        self._jvm_property_obj.setName(name)

    def get_data_type(self) -> GarType:
        return GarType(self._jvm_property_obj.getData_type())

    def set_data_type(self, data_type: GarType) -> None:
        self._jvm_property_obj.setData_type(data_type.to_scala())

    def get_is_primary(self) -> bool:
        return self._jvm_property_obj.getIs_primary()

    def set_is_primary(self, is_primary: bool) -> None:
        self._jvm_property_obj.setIs_primary(is_primary)

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_property_obj

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "Property":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return Property(None, None, None, jvm_obj)

    @staticmethod
    def from_python(name: str, data_type: GarType, is_primary: bool) -> "Property":
        return Property(name, data_type, is_primary, None)


class PropertyGroup:
    """PropertyGroup is a class to store the property group information."""

    def __init__(
        self,
        prefix: Optional[str],
        file_type: Optional[FileType],
        properties: Optional[list[Property]],
        jvm_obj: Optional[JavaObject],
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_obj is not None:
            self._jvm_property_group_obj = jvm_obj
        else:
            property_group = GraphArSession._graphar.PropertyGroup()
            property_group.setPrefix(prefix)
            property_group.setFile_type(file_type.value)
            property_group.setProperties(
                [property.to_scala() for property in properties]
            )
            self._jvm_property_group_obj = property_group

    def get_prefix(self) -> str:
        return self._jvm_property_group_obj.getPrefix()

    def set_prefix(self, prefix: str) -> None:
        self._jvm_property_group_obj.setPrefix(prefix)

    def get_file_type(self) -> FileType:
        return FileType(self._jvm_property_group_obj.getFile_type())

    def set_file_type(self, file_type: FileType) -> None:
        self._jvm_property_group_obj.setFile_type(file_type.value)

    def get_properties(self) -> list[Property]:
        return [
            Property.from_scala(jvm_property)
            for jvm_property in self._jvm_property_group_obj.getProperties()
        ]

    def set_properties(self, properties: list[Property]) -> None:
        self._jvm_property_group_obj.setProperties(
            [property.to_scala() for property in properties]
        )

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_property_group_obj

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "PropertyGroup":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return PropertyGroup(None, None, None, jvm_obj)

    @staticmethod
    def from_python(
        prefix: str, file_type: FileType, properties: list[Property]
    ) -> "PropertyGroup":
        return PropertyGroup(prefix, file_type, properties, None)


class VertexInfo:
    """VertexInfo is a class to store the vertex meta information."""

    def __init__(
        self,
        label: Optional[str],
        chunk_size: Optional[int],
        prefix: Optional[str],
        property_groups: Optional[list[PropertyGroup]],
        version: Optional[str],
        jvm_obj: Optional[JavaObject],
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_obj is not None:
            self._jvm_vertex_info_obj = jvm_obj
        else:
            vertex_info = GraphArSession._graphar.VertexInfo()
            vertex_info.setLabel(label)
            vertex_info.setChunk_size(chunk_size)
            vertex_info.setPrefix(prefix)
            vertex_info.setProperty_groups(
                [py_property_group.to_scala() for py_property_group in property_groups]
            )
            vertex_info.setVersion(version)
            self._jvm_vertex_info_obj = vertex_info

    def get_label(self) -> str:
        return self._jvm_vertex_info_obj.getName()

    def set_label(self, label: str) -> None:
        self._jvm_vertex_info_obj.setLabel(label)

    def get_chunk_size(self) -> int:
        return self._jvm_vertex_info_obj.getChunk_size()

    def set_chunk_size(self, chunk_size: int) -> None:
        self._jvm_vertex_info_obj.setChunk_size(chunk_size)

    def get_prefix(self) -> str:
        self._jvm_vertex_info_obj.getPrefix()

    def set_prefix(self, prefix: str) -> None:
        self._jvm_vertex_info_obj.setPrefix(prefix)

    def get_property_groups(self) -> list[PropertyGroup]:
        return [
            PropertyGroup(jvm_property_group)
            for jvm_property_group in self._jvm_vertex_info_obj.getProperty_groups()
        ]

    def set_property_groups(self, property_groups: list[PropertyGroup]) -> None:
        self._jvm_vertex_info_obj.setProperty_groups(
            [py_property_group.to_scala() for py_property_group in property_groups]
        )

    def get_version(self) -> str:
        return self._jvm_vertex_info_obj.getVersion()

    def set_version(self, version: str) -> None:
        self._jvm_vertex_info_obj.setVersion(version)

    def contain_property_group(self, property_group: PropertyGroup) -> bool:
        """Check if the vertex info contains the property group.

        :param property_group: the property group to check.
        :returns: true if the vertex info contains the property group, otherwise false.
        """

        self._jvm_vertex_info_obj.containPropertyGroup(property_group.to_scala())

    def contain_property(self, property_name: str) -> bool:
        """Check if the vertex info contains certain property.

        :param property_name: name of the property.
        :returns: true if the vertex info contains the property, otherwise false.
        """
        self._jvm_vertex_info_obj.containProperty(property_name)

    def get_property_group(self, property_name: str) -> PropertyGroup:
        """Get the property group that contains property.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_name: name of the property.
        :returns: property group that contains the property, otherwise raise IllegalArgumentException error.
        """
        return PropertyGroup.from_scala(
            self._jvm_vertex_info_obj.getPropertyGroup(property_name)
        )

    def get_property_type(self, property_name: str) -> GarType:
        """Get the data type of property.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_name: name of the property.
        :returns: the data type in gar of the property. If the vertex info does not contains the property, raise IllegalArgumentException error.
        """
        return GarType.from_scala(
            self._jvm_vertex_info_obj.getPropertyType(property_name)
        )

    def is_primary_key(self, property_name: str) -> bool:
        """Check if the property is primary key.

        :param property_name: name of the property to check.
        :returns: true if the property if the primary key of vertex info, otherwise return false.
        """
        return self._jvm_vertex_info_obj.isPrimaryKey(property_name)

    def get_primary_key(self) -> str:
        """Get primary key of vertex info.

        :returns: name of the primary key.
        """
        return self._jvm_vertex_info_obj.getPrimaryKey()

    def is_validated(self) -> bool:
        """Check if the vertex info is validated.

        :returns: true if the vertex info is validated, otherwise return false.
        """
        return self._jvm_vertex_info_obj.isValidated()

    def get_vertices_num_file_path(self) -> str:
        """Get the vertex num file path of vertex info.

        :returns: vertex num file path of vertex info.
        """
        return self._jvm_vertex_info_obj.getVerticesNumFilePath()

    def get_file_path(self, property_group: PropertyGroup, chunk_index: int) -> str:
        """Get the chunk file path of property group of vertex chunk.

        :param property_group: the property group.
        :param chunk_index: the index of vertex chunk
        :returns: chunk file path.

        """
        return self._jvm_vertex_info_obj.getFilePath(
            property_group.to_scala(), chunk_index
        )

    def get_path_prefix(self, property_group: PropertyGroup) -> str:
        """Get the path prefix for the specified property group.

        :param property_group: the property group.
        :returns: the path prefix of the property group chunk files.
        """
        return self._jvm_vertex_info_obj.getPathPrefix(property_group.to_scala())

    def dump(self) -> str:
        """Dump to Yaml string.

        :returns: yaml string
        """
        return self._jvm_vertex_info_obj.dump()

    @staticmethod
    def load_vertex_info(vertex_info_path: str) -> "VertexInfo":
        """Load a yaml file from path and construct a VertexInfo from it.

        :param vertexInfoPath: yaml file path
        :returns: VertexInfo object
        """
        scala_obj = VertexInfo(
            GraphArSession._graphar.VertexInfo(vertex_info_path, GraphArSession._jss)
        )

        return VertexInfo.from_scala(scala_obj)

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_vertex_info_obj

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "VertexInfo":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return VertexInfo(
            None,
            None,
            None,
            None,
            None,
            jvm_obj,
        )

    @staticmethod
    def from_python(
        label: str,
        chunk_size: int,
        prefix: str,
        property_groups: list[PropertyGroup],
        version: str,
    ) -> "VertexInfo":
        return VertexInfo(label, chunk_size, prefix, property_groups, version, None)


class AdjList:
    """AdjList is a class to store the adj list information of edge."""

    def __init__(
        self,
        ordered: Optional[bool],
        aligned_by: Optional[str],
        prefix: Optional[str],
        file_type: Optional[FileType],
        property_groups: Optional[list[PropertyGroup]],
        jvm_obj: Optional[JavaObject],
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_obj is not None:
            self._jvm_adj_list_obj = jvm_obj
        else:
            jvm_adj_list = GraphArSession._graphar.AdjList()
            jvm_adj_list.setOrdered(ordered)
            jvm_adj_list.setAligned_by(aligned_by)
            jvm_adj_list.setPrefix(prefix)
            jvm_adj_list.setFile_type(file_type.value)
            jvm_adj_list.setProperty_groups(
                [py_property_group.to_scala() for py_property_group in property_groups]
            )
            self._jvm_adj_list_obj = jvm_adj_list

    def get_ordered(self) -> bool:
        return self._jvm_adj_list_obj.getOrdered()

    def set_ordered(self, ordered: bool) -> None:
        self._jvm_adj_list_obj.setOrdered(ordered)

    def get_aligned_by(self) -> str:
        return self._jvm_adj_list_obj.getAligned_by()

    def set_aligned_by(self, aligned_by: str) -> None:
        self._jvm_adj_list_obj.setAligned_by(aligned_by)

    def get_prefix(self) -> str:
        return self._jvm_adj_list_obj.getPrefix()

    def set_prefix(self, prefix: str) -> None:
        self._jvm_adj_list_obj.setPrefix(prefix)

    def get_file_type(self) -> FileType:
        return FileType(self._jvm_adj_list_obj.getFile_type())

    def set_file_type(self, file_type: FileType) -> None:
        self._jvm_adj_list_obj.setFile_type(file_type.value)

    def get_property_groups(self) -> list[PropertyGroup]:
        return [
            PropertyGroup.from_scala(jvm_property_group)
            for jvm_property_group in self._jvm_adj_list_obj.getProperty_groups()
        ]

    def get_adj_list_type(self) -> AdjListType:
        """Get adj list type.

        :returns: adj list type.
        """
        return AdjListType(self._jvm_adj_list_obj.getAdjList_type())

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_adj_list_obj

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "AdjList":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return AdjList(None, None, None, None, None, jvm_obj)

    @staticmethod
    def from_python(
        ordered: bool,
        aligned_by: str,
        prefix: str,
        file_type: FileType,
        property_groups: list[PropertyGroup],
    ) -> "AdjList":
        return AdjList(ordered, aligned_by, prefix, file_type, property_groups, None)


class EdgeInfo:
    """Edge info is a class to store the edge meta information."""

    def __init__(
        self,
        src_label: Optional[str],
        edge_label: Optional[str],
        dst_label: Optional[str],
        chunk_size: Optional[int],
        src_chunk_size: Optional[int],
        dst_chunk_size: Optional[int],
        directed: Optional[bool],
        prefix: Optional[str],
        adj_lists: list[AdjList],
        version: Optional[str],
        jvm_edge_info_obj: JavaObject,
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_edge_info_obj is not None:
            self._jvm_edge_info_obj = jvm_edge_info_obj
        else:
            edge_info = GraphArSession._graphar.EdgeInfo()
            edge_info.setSrc_label(src_label)
            edge_info.setEdge_label(edge_label)
            edge_info.setDst_label(dst_label)
            edge_info.setChunk_size(chunk_size)
            edge_info.setSrc_chunk_size(src_chunk_size)
            edge_info.setDst_chunk_size(dst_chunk_size)
            edge_info.setDirected(directed)
            edge_info.setPrefix(prefix)
            edge_info.setAdj_lists(
                [py_adj_list.to_scala() for py_adj_list in adj_lists]
            )
            edge_info.setVersion(version)
            self._jvm_edge_info_obj = edge_info

    def get_src_label(self) -> str:
        return self._jvm_edge_info_obj.getSrc_label()

    def set_src_label(self, src_label: str) -> None:
        self._jvm_edge_info_obj.setSrc_label(src_label)

    def get_edge_label(self) -> str:
        return self._jvm_edge_info_obj.getEdge_label()

    def set_edge_label(self, edge_label: str) -> None:
        self._jvm_edge_info_obj.setEdge_label(edge_label)

    def get_dst_label(self) -> str:
        return self._jvm_edge_info_obj.getDst_label()

    def set_dst_label(self, dst_label: str) -> None:
        self._jvm_edge_info_obj.setDst_label(dst_label)

    def get_chunk_size(self) -> int:
        return self._jvm_edge_info_obj.getChunk_size()

    def set_chunk_size(self, chunk_size: int) -> None:
        self._jvm_edge_info_obj.setChunk_size(chunk_size)

    def get_src_chunk_size(self) -> int:
        return self._jvm_edge_info_obj.getSrc_chunk_size()

    def set_src_chunk_size(self, src_chunk_size: int) -> None:
        self._jvm_edge_info_obj.setSrc_chunk_size(src_chunk_size)

    def get_dst_chunk_size(self) -> int:
        return self._jvm_edge_info_obj.getDst_chunk_size()

    def set_dst_chunk_size(self, dst_chunk_size: int) -> None:
        self._jvm_edge_info_obj.setDst_chunk_size(dst_chunk_size)

    def get_directed(self) -> bool:
        return self._jvm_edge_info_obj.getDirected()

    def set_directed(self, directed: bool) -> None:
        self._jvm_edge_info_obj.setDirected(directed)

    def get_prefix(self) -> str:
        return self._jvm_edge_info_obj.getPrefix()

    def set_prefix(self, prefix: str) -> None:
        self._jvm_edge_info_obj.setPrefix(prefix)

    def get_adj_lists(self) -> list[AdjList]:
        return [
            AdjList.from_scala(jvm_adj_list)
            for jvm_adj_list in self._jvm_edge_info_obj.getAdj_lists()
        ]

    def set_adj_lists(self, adj_lists: list[AdjList]) -> None:
        self._jvm_edge_info_obj.setAdj_lists(
            [py_adj_list.to_scala() for py_adj_list in adj_lists]
        )

    def get_version(self) -> str:
        return self._jvm_edge_info_obj.getVersion()

    def set_version(self, version: str) -> None:
        self._jvm_edge_info_obj.setVersion(version)

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_edge_info_obj()

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "EdgeInfo":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return EdgeInfo(
            None, None, None, None, None, None, None, None, None, None, jvm_obj
        )

    @staticmethod
    def from_python(
        src_label: str,
        edge_label: str,
        dst_label: str,
        chunk_size: int,
        src_chunk_size: int,
        dst_chunk_size: int,
        directed: bool,
        prefix: str,
        adj_lists: list[AdjList],
        version: str,
    ) -> "EdgeInfo":
        return EdgeInfo(
            src_label,
            edge_label,
            dst_label,
            chunk_size,
            src_chunk_size,
            dst_chunk_size,
            directed,
            prefix,
            adj_lists,
            version,
            None,
        )

    def contain_adj_list(self, adj_list_type: AdjListType) -> bool:
        """Check if the edge info supports the adj list type.

        :param adj_list_type: adjList type in gar to check.
        :returns: true if edge info supports the adj list type, otherwise return false.
        """
        return self._jvm_edge_info_obj.containAdjList(adj_list_type.to_scala())

    def get_adj_list_prefix(self, adj_list_type: AdjListType) -> str:
        """Get path prefix of adj list type.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: The input adj list type in gar.
        :returns: path prefix of the adj list type, if edge info not support the adj list type, raise an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.getAdjListPrefix(adj_list_type.to_scala())

    def get_adj_list_file_type(self, adj_list_type: AdjListType) -> FileType:
        """Get the adj list topology chunk file type of adj list type.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: the input adj list type.
        :returns: file format type in gar of the adj list type, if edge info not support the adj list type,
        raise an IllegalArgumentException error.
        """
        return FileType.from_scala(
            self._jvm_edge_info_obj.getAdjListFileType(adj_list_type.to_scala())
        )

    def get_property_groups(self, adj_list_type: AdjListType) -> list[PropertyGroup]:
        """Get the property groups of adj list type.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: the input adj list type.
        :returns: property group of the input adj list type, if edge info not support the adj list type,
        raise an IllegalArgumentException error.
        """
        return [
            PropertyGroup.from_scala(property_group)
            for property_group in self._jvm_edge_info_obj.getPropertyGroups(
                adj_list_type.to_scala()
            )
        ]

    def contain_property_group(
        self, property_group: PropertyGroup, adj_list_type: AdjListType
    ) -> bool:
        """Check if the edge info contains the property group in certain adj list structure.

        :param property_group: the property group to check.
        :param adj_list_type: the type of adj list structure.
        :returns: true if the edge info contains the property group in certain adj list
        structure. If edge info not support the given adj list type or not
        contains the property group in the adj list structure, return false.
        """
        return self._jvm_edge_info_obj.containPropertyGroup(
            property_group.to_scala(), adj_list_type.to_scala()
        )

    def contain_property(self, property_name: str) -> bool:
        """Check if the edge info contains the property.

        :param property_name: name of the property.
        :returns: true if edge info contains the property, otherwise false.
        """
        return self._jvm_edge_info_obj.containProperty(property_name)

    def get_property_group(
        self, property_name: str, adj_list_type: AdjListType
    ) -> PropertyGroup:
        """Get property group that contains property with adj list type.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_name: name of the property.
        :param adj_list_type: the type of adj list structure.
        :returns: property group that contains the property. If edge info not support the
        adj list type, or not find the property group that contains the property,
        return false.
        """
        return PropertyGroup.from_scala(
            self._jvm_edge_info_obj.getPropertyGroup(
                property_name, adj_list_type.to_scala()
            )
        )

    def get_property_type(self, property_name: str) -> GarType:
        """Get the data type of property.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_name: name of the property.
        :returns: data type in gar of the property. If edge info not contains the property, raise an IllegalArgumentException error.
        """
        return GarType.from_scala(
            self._jvm_edge_info_obj.getPropertyType(property_name)
        )

    def is_primary_key(self, property_name: str) -> bool:
        """Check the property is primary key of edge info.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_name: name of the property.
        :returns: true if the property is the primary key of edge info, false if not. If
        edge info not contains the property, raise an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.isPrimaryKey()

    def get_primary_key(self) -> str:
        """Get Primary key of edge info.

        :returns: primary key of edge info.
        """
        return self._jvm_edge_info_obj.getPrimaryKey()

    def is_validated(self) -> bool:
        """Check if the edge info is validated.

        :returns: true if edge info is validated or false if not.
        """
        return self._jvm_edge_info_obj.isValidated()

    def get_vertices_num_file_path(self, adj_list_type: AdjListType) -> str:
        """Get the vertex num file path.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: type of adj list structure.
        :returns: the vertex num file path. If edge info not support the adj list type,
        raise an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.getVerticesNumFilePath(adj_list_type.to_scala())

    def get_edges_num_path_prefix(self, adj_list_type: AdjListType) -> str:
        """Get the path prefix of the edge num file path.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: type of adj list structure.
        :returns: the edge num file path. If edge info not support the adj list type, raise
        an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.getEdgesNumPathPrefix(adj_list_type.to_scala())

    def get_edges_num_file_path(
        self, chunk_index: int, adj_list_type: AdjListType
    ) -> str:
        """Get the edge num file path of the vertex chunk.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param chunk_index: index of vertex chunk.
        :param adj_list_type: type of adj list structure.
        :returns: the edge num file path. If edge info not support the adj list type, raise
        an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.getEdgesNumFilePath(
            chunk_index, adj_list_type.to_scala()
        )

    def get_adj_list_offset_file_path(
        self, chunk_index: int, adj_list_type: AdjListType
    ) -> str:
        """Get the adj list offset chunk file path of vertex chunk the offset chunks is aligned with the vertex chunks.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param chunk_index: index of vertex chunk.
        :param adj_list_type: type of adj list structure.
        :returns: the offset chunk file path. If edge info not support the adj list type, raise an IllegalArgumentException error.

        """
        return self._jvm_edge_info_obj.getAdjListOffsetFilePath(
            chunk_index, adj_list_type.to_scala()
        )

    def get_offset_path_prefix(self, adj_list_type: AdjListType) -> str:
        """Get the path prefix of the adjacency list offset for the given adjacency list type.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param adj_list_type: type of adj list structure.
        :returns: the path prefix of the offset. If edge info not support the adj list type, raise an IllegalArgumentException error.

        """
        return self._jvm_edge_info_obj.getOffsetPathPrefix(adj_list_type.to_scala())

    def get_adj_list_file_path(
        self, vertex_chunk_index: int, chunk_index: int, adj_list_type: AdjListType
    ) -> str:
        """Get the file path of adj list topology chunk.

        :param vertex_chunk_index: index of vertex chunk.
        :param chunk_index: index of edge chunk.
        :param adj_list_type: type of adj list structure.
        :returns: adj list chunk file path.
        """
        return self._jvm_edge_info_obj.getAdjListFilePath(
            vertex_chunk_index, chunk_index, adj_list_type.to_scala()
        )

    def get_adj_list_path_prefix(
        self, vertex_chunk_index: Optional[int], adj_list_type: AdjListType
    ) -> str:
        """Get the path prefix of adj list topology chunk of certain vertex chunk.

        :param vertex_chunk_index: index of vertex chunk (optional).
        :param adj_list_type: type of adj list structure.
        :returns: path prefix of the edge chunk of vertices of given vertex chunk.
        """
        if vertex_chunk_index is None:
            return self._jvm_edge_info_obj.getAdjListPathPrefix(
                adj_list_type.to_scala()
            )

        return self._jvm_edge_info_obj.getAdjListPathPrefix(
            vertex_chunk_index, adj_list_type.to_scala()
        )

    def get_property_file_path(
        self,
        property_group: PropertyGroup,
        adj_list_type: AdjListType,
        vertex_chunk_index: int,
        chunk_index: int,
    ) -> str:
        """Get the chunk file path of adj list property group. the property group chunks is aligned with the adj list topology chunks.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_group: property group
        :param adj_list_type: type of adj list structure.
        :param vertex_chunk_index: index of vertex chunk.
        :param chunk_index: index of edge chunk.
        :returns: property group chunk file path. If edge info not contains the property group, raise an IllegalArgumentException error.
        """
        return self._jvm_edge_info_obj.getPropertyFilePath(
            property_group.to_scala(),
            adj_list_type.to_scala(),
            vertex_chunk_index,
            chunk_index,
        )

    def get_property_group_path_prefix(
        self,
        property_group: PropertyGroup,
        adj_list_type: AdjListType,
        vertex_chunk_index: Optional[int] = None,
    ) -> str:
        """Get path prefix of adj list property group of certain vertex chunk.

        WARNING! Exceptions from the JVM are not checked inside, it is just a proxy-method!

        :param property_group: property group.
        :param adj_list_type: type of adj list structure.
        :param vertex_chunk_index: index of vertex chunk (optional, default is None).
        :returns: path prefix of property group chunks of of vertices of given vertex
        chunk. If edge info not contains the property group, raise an IllegalArgumentException error.
        """
        if vertex_chunk_index is not None:
            return self._jvm_edge_info_obj.getPropertyGroupPathPrefix(
                property_group.to_scala(),
                adj_list_type.to_scala(),
                vertex_chunk_index,
            )
        else:
            return self._jvm_edge_info_obj.getPropertyGroupPathPrefix(
                property_group.to_scala(),
                adj_list_type.to_scala(),
            )

    def get_concat_key(self) -> str:
        """Get concat key.

        :returns: concat key
        """
        return self._jvm_edge_info_obj.getConcatKey()

    def dump(self) -> str:
        """Dump to Yaml string.

        :returns: yaml-string representation.
        """
        return self._jvm_edge_info_obj.dump()

    @staticmethod
    def load_edge_info(edge_info_path: str) -> "EdgeInfo":
        """Load a yaml file from path and construct a EdgeInfo from it.

        :param edge_info_path: path of edge info YAML file.
        :returns: EdgeInfo object.
        """
        return EdgeInfo.from_scala(
            GraphArSession._graphar.EdgeInfo.loadEdgeInfo(
                edge_info_path, GraphArSession._jss
            )
        )


class GraphInfo:
    """GraphInfo is a class to store the graph meta information."""

    def __init__(
        self,
        name: Optional[str],
        prefix: Optional[str],
        vertices: Optional[list[str]],
        edges: Optional[list[str]],
        version: Optional[str],
        jvm_grpah_info_obj: Optional[JavaObject],
    ) -> None:
        """One should not use this constructor directly, please use `from_scala` or `from_python`."""
        if jvm_grpah_info_obj is not None:
            self._jvm_graph_info_obj = jvm_grpah_info_obj
        else:
            graph_info = GraphArSession._graphar.GraphInfo()
            graph_info.setName(name)
            graph_info.setPrefix(prefix)
            graph_info.setVertices(vertices)
            graph_info.setEdges(edges)
            graph_info.setVersion(version)
            self._jvm_graph_info_obj = graph_info

    def get_name(self) -> str:
        return self._jvm_graph_info_obj.getName()

    def set_name(self, name: str) -> None:
        self._jvm_graph_info_obj.setName(name)

    def get_prefix(self) -> str:
        return self._jvm_graph_info_obj.getPrefix()

    def set_prefix(self, prefix: str) -> None:
        self._jvm_graph_info_obj.setPrefix(prefix)

    def get_vertices(self) -> list[str]:
        return self._jvm_graph_info_obj.getVertices()

    def set_vertices(self, vertices: list[str]) -> None:
        self._jvm_graph_info_obj.setVertices(vertices)

    def get_edges(self) -> list[str]:
        return self._jvm_graph_info_obj.getEdges()

    def set_edges(self, edges: list[str]) -> None:
        self._jvm_graph_info_obj.setEdges(edges)

    def get_version(self) -> str:
        return self._jvm_graph_info_obj.getVersion()

    def set_version(self, version: str) -> None:
        self._jvm_graph_info_obj.setVersion(version)

    def to_scala(self) -> JavaObject:
        """Transform object to JVM representation.

        :returns: JavaObject
        """
        return self._jvm_graph_info_obj

    @staticmethod
    def from_scala(jvm_obj: JavaObject) -> "GraphInfo":
        """Create an instance of the Class from the corresponding JVM object.

        :param jvm_obj: scala object in JVM.
        :returns: instance of Python Class.
        """
        return GraphInfo(None, None, None, None, None, jvm_obj)

    @staticmethod
    def from_python(
        name: str, prefix: str, vertices: list[str], edges: list[str], version: str
    ) -> "GraphInfo":
        return GraphInfo(name, prefix, vertices, edges, version, None)

    def add_vertex_info(self, vertex_info: VertexInfo) -> None:
        self._jvm_graph_info_obj.addVertexInfo(vertex_info.to_scala())

    def add_edge_info(self, edge_info: EdgeInfo) -> None:
        self._jvm_graph_info_obj.addEdgeInfo(edge_info.to_scala())

    def get_vertex_info(self, label: str) -> VertexInfo:
        return VertexInfo.from_scala(self._jvm_graph_info_obj.getVertexInfo(label))

    def get_edge_info(
        self, src_label: str, edge_label: str, dst_label: str
    ) -> EdgeInfo:
        return EdgeInfo.from_scala(
            self._jvm_graph_info_obj.getEdgeInfo(src_label, edge_label, dst_label)
        )

    def get_vertex_infos(self) -> dict[str, VertexInfo]:
        return {
            key: VertexInfo.from_scala(value)
            for key, value in self._jvm_graph_info_obj.getVertexInfos().items()
        }

    def get_edge_infos(self) -> dict[str, EdgeInfo]:
        return {
            key: EdgeInfo.from_scala(value)
            for key, value in self._jvm_graph_info_obj.getEdgeInfos().items()
        }

    def dump(self) -> str:
        """Dump to Yaml string.

        :returns: YAML-string representation of object.
        """
        return self._jvm_graph_info_obj.dump()

    @staticmethod
    def load_graph_info(graph_info_path: str) -> "GraphInfo":
        """Load a yaml file from path and construct a GraphInfo from it.

        :param graph_info_path: path of GraphInfo YAML file.
        :returns: GraphInfo object.
        """
        return GraphInfo.from_scala(GraphArSession._graphar.GraphInfo.loadGraphInfo(graph_info_path))