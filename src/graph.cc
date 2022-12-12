/** Copyright 2022 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include "gar/graph.h"
#include "gar/utils/convert_to_arrow_type.h"

namespace GAR_NAMESPACE_INTERNAL {

template <Type type>
Status CastToAny(std::shared_ptr<arrow::Array> array,
                 std::any& any) {  // NOLINT
  using ArrayType = typename ConvertToArrowType<type>::ArrayType;
  auto column = std::dynamic_pointer_cast<ArrayType>(array);
  any = column->GetView(0);
  return Status::OK();
}

template <>
Status CastToAny<Type::STRING>(std::shared_ptr<arrow::Array> array,
                               std::any& any) {  // NOLINT
  using ArrayType = typename ConvertToArrowType<Type::STRING>::ArrayType;
  auto column = std::dynamic_pointer_cast<ArrayType>(array);
  any = column->GetString(0);
  return Status::OK();
}

Status TryToCastToAny(const DataType& type, std::shared_ptr<arrow::Array> array,
                      std::any& any) {  // NOLINT
  switch (type.id()) {
  case Type::BOOL:
    return CastToAny<Type::BOOL>(array, any);
  case Type::INT32:
    return CastToAny<Type::INT32>(array, any);
  case Type::INT64:
    return CastToAny<Type::INT64>(array, any);
  case Type::FLOAT:
    return CastToAny<Type::FLOAT>(array, any);
  case Type::DOUBLE:
    return CastToAny<Type::DOUBLE>(array, any);
  case Type::STRING:
    return CastToAny<Type::STRING>(array, any);
  default:
    return Status::TypeError();
  }
  return Status::TypeError();
}

Vertex::Vertex(IdType id,
               std::vector<VertexPropertyArrowChunkReader>& readers)  // NOLINT
    : id_(id) {
  // get the first row of table
  for (auto& reader : readers) {
    GAR_ASSIGN_OR_RAISE_ERROR(auto chunk_table, reader.GetChunk());
    auto schema = chunk_table->schema();
    for (int i = 0; i < schema->num_fields(); ++i) {
      auto field = chunk_table->field(i);
      auto type = DataType::ArrowDataTypeToDataType(field->type());
      GAR_RAISE_ERROR_NOT_OK(TryToCastToAny(
          type, chunk_table->column(i)->chunk(0), properties_[field->name()]));
    }
  }
}

Edge::Edge(
    AdjListArrowChunkReader& adj_list_reader,                          // NOLINT
    std::vector<AdjListPropertyArrowChunkReader>& property_readers) {  // NOLINT
  // get the first row of table
  GAR_ASSIGN_OR_RAISE_ERROR(auto adj_list_chunk_table,
                            adj_list_reader.GetChunk());
  src_id_ = std::dynamic_pointer_cast<arrow::Int64Array>(
                adj_list_chunk_table->column(0)->chunk(0))
                ->GetView(0);
  dst_id_ = std::dynamic_pointer_cast<arrow::Int64Array>(
                adj_list_chunk_table->column(1)->chunk(0))
                ->GetView(0);
  for (auto& reader : property_readers) {
    // get the first row of table
    GAR_ASSIGN_OR_RAISE_ERROR(auto chunk_table, reader.GetChunk());
    auto schema = chunk_table->schema();
    for (int i = 0; i < schema->num_fields(); ++i) {
      auto field = chunk_table->field(i);
      auto type = DataType::ArrowDataTypeToDataType(field->type());
      GAR_RAISE_ERROR_NOT_OK(TryToCastToAny(
          type, chunk_table->column(i)->chunk(0), properties_[field->name()]));
    }
  }
}
}  // namespace GAR_NAMESPACE_INTERNAL
