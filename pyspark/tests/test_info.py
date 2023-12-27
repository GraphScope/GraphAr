import yaml


from graphar_pyspark import initialize
from graphar_pyspark.enums import AdjListType, FileType, GarType
from graphar_pyspark.info import (
    AdjList,
    EdgeInfo,
    GraphInfo,
    Property,
    PropertyGroup,
    VertexInfo,
)


def test_property(spark):
    initialize(spark)
    property_from_py = Property.from_python("name", GarType.BOOL, False)

    assert property_from_py == Property.from_scala(property_from_py.to_scala())

    property_from_py.set_name("new_name")
    property_from_py.set_data_type(GarType.INT32)
    property_from_py.set_is_primary(True)

    assert property_from_py.get_name() == "new_name"
    assert property_from_py.get_data_type() == GarType.INT32
    assert property_from_py.get_is_primary() == True


def test_property_group(spark):
    initialize(spark)
    p_group_from_py = PropertyGroup.from_python(
        "prefix",
        FileType.CSV,
        [
            Property.from_python("non_primary", GarType.DOUBLE, False),
            Property.from_python("primary", GarType.INT64, True),
        ],
    )

    assert p_group_from_py == PropertyGroup.from_scala(p_group_from_py.to_scala())

    p_group_from_py.set_prefix("new_prefix")
    p_group_from_py.set_file_type(FileType.ORC)
    p_group_from_py.set_properties(
        p_group_from_py.get_properties()
        + [Property("another_one", GarType.LIST, False)]
    )

    assert p_group_from_py.get_prefix() == "new_prefix"
    assert p_group_from_py.get_file_type() == FileType.ORC
    assert all(
        p_left == p_right
        for p_left, p_right in zip(
            p_group_from_py.get_properties(),
            [
                Property.from_python("non_primary", GarType.DOUBLE, False),
                Property.from_python("primary", GarType.INT64, True),
                Property("another_one", GarType.LIST, False),
            ],
        )
    )


def test_adj_list(spark):
    initialize(spark)

    props_list_1 = [
        Property.from_python("non_primary", GarType.DOUBLE, False),
        Property.from_python("primary", GarType.INT64, True),
    ]

    props_list_2 = [
        Property.from_python("non_primary", GarType.DOUBLE, False),
        Property.from_python("primary", GarType.INT64, True),
        Property("another_one", GarType.LIST, False),
    ]

    adj_list_from_py = AdjList.from_python(
        True,
        "dest",
        "prefix",
        FileType.PARQUET,
        [
            PropertyGroup.from_python("prefix1", FileType.PARQUET, props_list_1),
            PropertyGroup.from_python("prefix2", FileType.ORC, props_list_2),
        ],
    )

    assert adj_list_from_py == AdjList.from_scala(adj_list_from_py.to_scala())
    assert adj_list_from_py.get_adj_list_type() == AdjListType.ORDERED_BY_DEST

    adj_list_from_py.set_aligned_by("src")
    assert adj_list_from_py.get_adj_list_type() == AdjListType.ORDERED_BY_SOURCE
    adj_list_from_py.set_ordered(False)
    assert adj_list_from_py.get_adj_list_type() == AdjListType.UNORDERED_BY_SOURCE
    adj_list_from_py.set_aligned_by("dest")
    assert adj_list_from_py.get_adj_list_type() == AdjListType.UNORDERED_BY_DEST

    adj_list_from_py.set_file_type(FileType.CSV)
    assert adj_list_from_py.get_file_type() == FileType.CSV

    adj_list_from_py.set_property_groups(
        adj_list_from_py.get_property_groups()
        + [
            PropertyGroup.from_python(
                "prefix3", FileType.CSV, props_list_1 + props_list_2
            )
        ]
    )
    assert all(
        pg_left == pg_right
        for pg_left, pg_right in zip(
            adj_list_from_py.get_property_groups(),
            [
                PropertyGroup.from_python("prefix1", FileType.PARQUET, props_list_1),
                PropertyGroup.from_python("prefix2", FileType.ORC, props_list_2),
                PropertyGroup.from_python(
                    "prefix3", FileType.CSV, props_list_1 + props_list_2
                ),
            ],
        )
    )


def test_vertex_info(spark):
    initialize(spark)

    props_list_1 = [
        Property.from_python("non_primary", GarType.DOUBLE, False),
        Property.from_python("primary", GarType.INT64, True),
    ]

    props_list_2 = [
        Property.from_python("non_primary", GarType.DOUBLE, False),
        Property.from_python("primary", GarType.INT64, True),
        Property("another_one", GarType.LIST, False),
    ]

    vertex_info_from_py = VertexInfo.from_python(
        "label",
        100,
        "prefix",
        [
            PropertyGroup.from_python("prefix1", FileType.PARQUET, props_list_1),
            PropertyGroup.from_python("prefix2", FileType.ORC, props_list_2),
        ],
        "1",
    )

    # TODO: revisit contain_* methods after resolving the discussion in github
    assert vertex_info_from_py.contain_property_group(PropertyGroup.from_scala(vertex_info_from_py.get_property_groups()[0].to_scala()))
    assert vertex_info_from_py.contain_property_group(PropertyGroup.from_python("prefix333", FileType.PARQUET, props_list_1)) == False

    assert vertex_info_from_py.contain_property("primary")
    assert vertex_info_from_py.contain_property("non_primary")
    assert vertex_info_from_py.contain_property("non_existen_one") == False

    yaml_string = vertex_info_from_py.dump()
    restored_py_obj = yaml.safe_load(yaml_string)

    assert restored_py_obj["label"] == "label"
    assert restored_py_obj["prefix"] == "prefix"

    # test setters
    vertex_info_from_py.set_label("new_label")
    assert vertex_info_from_py.get_label() == "new_label"

    vertex_info_from_py.set_chunk_size(101)
    assert vertex_info_from_py.get_chunk_size() == 101

    vertex_info_from_py.set_prefix("new_prefix")
    assert vertex_info_from_py.get_prefix() == "new_prefix"

    vertex_info_from_py.set_version("2")
    assert vertex_info_from_py.get_version() == "2"
