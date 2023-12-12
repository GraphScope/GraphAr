/*
 * Copyright 2022-2023 Alibaba Group Holding Limited.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.alibaba.graphar.writers;

import static com.alibaba.graphar.graphinfo.GraphInfoTest.root;

import com.alibaba.graphar.arrow.ArrowTable;
import com.alibaba.graphar.graphinfo.EdgeInfo;
import com.alibaba.graphar.stdcxx.StdSharedPtr;
import com.alibaba.graphar.stdcxx.StdString;
import com.alibaba.graphar.types.AdjListType;
import com.alibaba.graphar.types.ValidateLevel;
import com.alibaba.graphar.util.Result;
import com.alibaba.graphar.util.Yaml;
import org.apache.arrow.dataset.file.FileFormat;
import org.apache.arrow.dataset.file.FileSystemDatasetFactory;
import org.apache.arrow.dataset.jni.NativeMemoryPool;
import org.apache.arrow.dataset.scanner.ScanOptions;
import org.apache.arrow.dataset.scanner.Scanner;
import org.apache.arrow.dataset.source.Dataset;
import org.apache.arrow.dataset.source.DatasetFactory;
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowReader;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;

@Ignore("FIXME: the test would raise memory lead error(arrow object not released)")
public class EdgeChunkWriterTest {
    @Test
    public void test1() {
        String uri =
                "file:"
                        + root
                        + "/ldbc_sample/parquet/edge/person_knows_person/"
                        + "unordered_by_source/adj_list/part0/chunk0";
        ScanOptions options = new ScanOptions(/*batchSize*/ 32768);
        StdSharedPtr<ArrowTable> table = null;
        try (BufferAllocator allocator = new RootAllocator();
                DatasetFactory datasetFactory =
                        new FileSystemDatasetFactory(
                                allocator, NativeMemoryPool.getDefault(), FileFormat.PARQUET, uri);
                Dataset dataset = datasetFactory.finish();
                Scanner scanner = dataset.newScan(options);
                ArrowReader reader = scanner.scanBatches()) {
            while (reader.loadNextBatch()) {
                try (VectorSchemaRoot root = reader.getVectorSchemaRoot()) {
                    table = ArrowTable.fromVectorSchemaRoot(allocator, root, reader);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        Assert.assertNotNull(table);

        StdString edgeMetaFile =
                StdString.create(root + "/ldbc_sample/csv/person_knows_person.edge.yml");
        Result<StdSharedPtr<Yaml>> maybeEdgeMeta = Yaml.loadFile(edgeMetaFile);
        Assert.assertFalse(maybeEdgeMeta.hasError());
        Result<EdgeInfo> maybeEdgeInfo = EdgeInfo.load(maybeEdgeMeta.value());
        Assert.assertFalse(maybeEdgeInfo.hasError());
        EdgeInfo edgeInfo = maybeEdgeInfo.value();
        Assert.assertTrue(edgeInfo.containAdjList(AdjListType.ordered_by_source));
        EdgeChunkWriter writer =
                EdgeChunkWriter.factory.create(
                        edgeInfo, StdString.create("/tmp/"), AdjListType.ordered_by_source);

        // Get & set validate level
        Assert.assertEquals(ValidateLevel.no_validate, writer.getValidateLevel());
        writer.setValidateLevel(ValidateLevel.strong_validate);
        Assert.assertEquals(ValidateLevel.strong_validate, writer.getValidateLevel());

        // Valid cases
        // Write adj list of vertex chunk 0 to files
        Assert.assertTrue(writer.sortAndWriteAdjListTable(table, 0, 0).ok());
        // Write number of edges for vertex chunk 0
        Assert.assertTrue(
                writer.writeEdgesNum(0, table.get().num_rows(), writer.getValidateLevel()).ok());
        // Write number of vertices
        Assert.assertTrue(writer.writeVerticesNum(903).ok());
    }
}
