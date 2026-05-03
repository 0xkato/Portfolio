#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$ROOT_DIR/repro/out"
BIN="$OUT_DIR/poc"
ASSET="$OUT_DIR/malicious.glb"

mkdir -p "$OUT_DIR"

if [[ ! -f "$ROOT_DIR/out/cmake-debug/libs/gltfio/libgltfio_core.a" ]] || \
   [[ ! -f "$ROOT_DIR/out/cmake-debug/third_party/meshoptimizer/tnt/libmeshoptimizer.a" ]]; then
  "$ROOT_DIR/build.sh" -m -b -y release debug gltfio >"$OUT_DIR/build.log" 2>&1 || {
    tail -n 80 "$OUT_DIR/build.log" >&2
    exit 1
  }
fi

clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fno-strict-aliasing -fsanitize=address,undefined \
  -isysroot "$(xcrun --sdk macosx --show-sdk-path)" -mmacosx-version-min=10.15 \
  -Ifilament/include -Ifilament/backend/include \
  -Ilibs/filabridge/include -Ilibs/gltfio/include -Iout/cmake-debug/libs/gltfio/materials \
  -Ilibs/utils/include -Ilibs/math/include \
  poc1.cpp \
  out/cmake-debug/libs/gltfio/libgltfio_core.a \
  out/cmake-debug/libs/gltfio/libuberarchive.a \
  out/cmake-debug/libs/uberz/libuberzlib.a \
  out/cmake-debug/filament/libfilament.a \
  out/cmake-debug/filament/backend/libbackend.a \
  out/cmake-debug/libs/geometry/libgeometry.a \
  out/cmake-debug/third_party/mikktspace/libmikktspace.a \
  out/cmake-debug/third_party/meshoptimizer/tnt/libmeshoptimizer.a \
  out/cmake-debug/third_party/draco/tnt/libdracodec.a \
  out/cmake-debug/libs/bluegl/libbluegl.a \
  out/cmake-debug/libs/bluevk/libbluevk.a \
  out/cmake-debug/libs/filaflat/libfilaflat.a \
  out/cmake-debug/libs/filabridge/libfilabridge.a \
  out/cmake-debug/third_party/smol-v/tnt/libsmol-v.a \
  out/cmake-debug/third_party/zstd/tnt/libzstd.a \
  out/cmake-debug/libs/math/libmath.a \
  out/cmake-debug/libs/utils/libutils.a \
  -framework Foundation -framework Cocoa -framework Metal -framework QuartzCore -framework CoreVideo -framework OpenGL \
  -o "$BIN"

python3 "$ROOT_DIR/make_malicious_asset1.py" --outdir "$OUT_DIR"

ASAN_OPTIONS=symbolize=0:halt_on_error=1:abort_on_error=1:detect_leaks=0 \
UBSAN_OPTIONS=halt_on_error=1:abort_on_error=1 \
"$BIN" "$ASSET" 2>&1 1>/dev/null | tee "$OUT_DIR/asan.log"
