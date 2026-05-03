#include <cstdint>
#include <cstdlib>
#include <iostream>

#define CGLTF_IMPLEMENTATION
#include <cgltf.h>
#undef CGLTF_IMPLEMENTATION

#include "DracoCache.h"

static cgltf_accessor* findAccessor(const cgltf_primitive* prim, cgltf_attribute_type type,
        cgltf_int index) {
    for (cgltf_size i = 0; i < prim->attributes_count; i++) {
        const cgltf_attribute& attr = prim->attributes[i];
        if (attr.type == type && attr.index == index) {
            return attr.data;
        }
    }
    return nullptr;
}

int main(int argc, char** argv) {
    const char* const gltfPath = argc > 1
            ? argv[1]
            : " ./poc_draco_stride_underalloc2.gltf";

    cgltf_options options = {};
    cgltf_data* data = nullptr;

    cgltf_result result = cgltf_parse_file(&options, gltfPath, &data);
    if (result != cgltf_result_success) {
        std::cerr << "cgltf_parse_file failed: " << result << "\n";
        return 1;
    }

    result = cgltf_load_buffers(&options, data, gltfPath);
    if (result != cgltf_result_success) {
        std::cerr << "cgltf_load_buffers failed: " << result << "\n";
        cgltf_free(data);
        return 1;
    }

    filament::gltfio::DracoCache cache;

    size_t decodedPrimitives = 0;
    for (cgltf_size m = 0; m < data->meshes_count; ++m) {
        const cgltf_mesh& mesh = data->meshes[m];
        for (cgltf_size p = 0; p < mesh.primitives_count; ++p) {
            const cgltf_primitive& prim = mesh.primitives[p];
            if (!prim.has_draco_mesh_compression) {
                continue;
            }

            const cgltf_draco_mesh_compression& draco = prim.draco_mesh_compression;
            filament::gltfio::DracoMesh* decoded = cache.findOrCreateMesh(draco.buffer_view);
            if (!decoded) {
                std::cerr << "DracoMesh decode failed.\n";
                continue;
            }

            decodedPrimitives++;
            std::cerr << "Decoded Draco primitive #" << decodedPrimitives
                      << " (attributes=" << draco.attributes_count << ")\n";

            if (prim.indices) {
                (void) decoded->getFaceIndices(prim.indices);
            }

            for (cgltf_size i = 0; i < draco.attributes_count; ++i) {
                // In cgltf, the Draco attribute id is stored as a pointer offset from gltf->accessors.
                const uint32_t id = uint32_t(draco.attributes[i].data - data->accessors);
                cgltf_accessor* dst = findAccessor(&prim, draco.attributes[i].type,
                        draco.attributes[i].index);
                if (!dst) {
                    std::cerr << "No destination accessor for Draco attribute id " << id << "\n";
                    continue;
                }

                std::cerr << "Decoding Draco attribute id " << id
                          << " (dst stride=" << dst->stride << ", type=" << int(dst->type)
                          << ", component_type=" << int(dst->component_type) << ")\n";

                (void) decoded->getVertexAttributes(id, dst);
            }
        }
    }

    std::cerr << "Done (decoded primitives: " << decodedPrimitives << ").\n";
    cgltf_free(data);
    return 0;
}
