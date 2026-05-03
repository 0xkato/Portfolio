In libs/gltfio/src/DracoCache.cpp (convertAttribs), Filament allocates the destination buffer using the destination accessor stride:

```
alloc size ≈ target->stride * n
```

If the glTF provides inconsistent accessor metadata (e.g. type=SCALAR / stride=4) but Draco decodes multi-component attributes (VEC2/VEC3/VEC4), the decode writes more bytes than allocated.

This is guarded by assert() checks; in release-like builds (-DNDEBUG) the asserts are removed, and the mismatch causes a heap-buffer-overflow (WRITE).

Reproduce:

```
python3 poc2.py
```

```
./build.sh -m -b debug mipgen cmake --build out/cmake-debug --target dracodec
```

```
clang++ -std=c++17 -O1 -g -DNDEBUG -fsanitize=address,undefined
-DGLTFIO_DRACO_SUPPORTED=1
-Ilibs/gltfio/src -Ilibs/utils/include
-Ithird_party/cgltf -Ithird_party/robin-map
-Ithird_party/draco/src -Iout/cmake-debug/third_party/draco/tnt
/poc2.cpp
libs/gltfio/src/DracoCache.cpp
out/cmake-debug/third_party/draco/tnt/libdracodec.a
out/cmake-debug/libs/utils/libutils.a
-framework Foundation
-o ./poc2
```

```
./poc2
./poc_draco_stride_underalloc2.gltf
```

Attack scenario

Any application/pipeline that loads untrusted Draco-compressed glTF with Filament gltfio can be crashed / corrupted via a crafted model file (heap OOB write).