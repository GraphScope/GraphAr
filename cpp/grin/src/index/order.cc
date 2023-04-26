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

#include "grin/include/index/order.h"
#include "grin/src/predefine.h"

#ifdef GRIN_ASSUME_ALL_VERTEX_LIST_SORTED
bool grin_smaller_vertex(GRIN_GRAPH g, GRIN_VERTEX v1, GRIN_VERTEX v2) {
  auto _v1 = static_cast<GRIN_VERTEX_T*>(v1);
  auto _v2 = static_cast<GRIN_VERTEX_T*>(v2);
  return (_v1->type_id < _v2->type_id ||
          (_v1->type_id == _v2->type_id && _v1->id < _v2->id));
}
#endif

#if defined(GRIN_ASSUME_ALL_VERTEX_LIST_SORTED) && \
    defined(GRIN_ENABLE_VERTEX_LIST_ARRAY)
size_t grin_get_position_of_vertex_from_sorted_list(GRIN_GRAPH g,
                                                    GRIN_VERTEX_LIST vl,
                                                    GRIN_VERTEX v) {
  auto _g = static_cast<GRIN_GRAPH_T*>(g);
  auto _v = static_cast<GRIN_VERTEX_T*>(v);
  auto _vl = static_cast<GRIN_VERTEX_LIST_T*>(vl);
  auto vtype = _v->type_id;
  size_t pos;
  if (vtype < _vl->type_begin || vtype >= _vl->type_end)
    return GRIN_NULL_SIZE;
  auto offset = _g->vertex_offsets[vtype] + _v->id;
  if (offset < _g->vertex_offsets[vtype + 1]) {
    pos = offset - _g->vertex_offsets[_vl->type_begin];
    return pos;
  }
  return GRIN_NULL_SIZE;
}
#endif