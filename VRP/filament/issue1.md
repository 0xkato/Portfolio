In libs/gltfio/src/Utility.cpp (decodeMeshoptCompression), Filament allocates the meshopt decompression output buffer using unchecked multiplication of attacker-controlled fields from EXT_meshopt_compression:

```
void* destination = malloc(compression->count * compression->stride);
assert_invariant(destination);
error = meshopt_decodeVertexBuffer(destination, compression->count,
        compression->stride, source, compression->size);
```

compression->count and compression->stride come from the glTF JSON extension. If count * stride overflows size_t, the allocation wraps to a small value, so malloc() under-allocates.

meshopt_decodeVertexBuffer() then writes decoded output into this undersized buffer, producing a heap-buffer-overflow.

```
./attach/run1.sh
```
```
=================================================================
==89390==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x611000006cc0 at pc 0x0001064f312c bp 0x00016f31d870 sp 0x00016f31d020
WRITE of size 8192 at 0x611000006cc0 thread T0
    #0 0x0001064f3128  (/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/17/lib/darwin/libclang_rt.asan_osx_dynamic.dylib:arm64e+0x3b128)
    #1 0x0001025d47d8  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x101af87d8)
    #2 0x0001025d1b60  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x101af5b60)
    #3 0x000100ebc668  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x1003e0668)
    #4 0x000100dc1f18  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x1002e5f18)
    #5 0x000100dc0cb8  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x1002e4cb8)
    #6 0x000100add68c  (/Users/0xkato/Desktop/Hobby/pgj-p0/filament/repro/out/poc:arm64+0x10000168c)
    #7 0x00018085dd50  (<unknown module>)
    ```