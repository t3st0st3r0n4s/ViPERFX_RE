# ViPERFX_RE

This is a reverse-engineering project aimed to make ViPER4Android more easy to access, modify, and improve.
Some QOL changes have been made, such as processing audio as float32, removing unused code, using more modern libraries, etc.
To view the progress, see [Issue #2](https://github.com/AndroidAudioMods/ViPERFX_RE/issues/2)

# Building

- Install the NDK, CMake and Make.
- Run `cmake . -DCMAKE_TOOLCHAIN_FILE=<NDKROOT>/build/cmake/android.toolchain.cmake -DANDROID_ABI=<ABI>` where <NDKROOT> is where you installed the NDK and <ABI> is the target ABI to build for.
- Run `make`
- You should now find a `libv4afx_r.so` file in your project root.

# CLion

Make sure to install `ninja`
In CLion, make sure to set the following custom arguments: `-DCMAKE_TOOLCHAIN_FILE=<NDKROOT>/build/cmake/android.toolchain.cmake -DANDROID_ABI=<ABI> -G Ninja`
Then you can build the project with `ninja` instead of `make`

# Credits

Zhuhang and ViPER520 for making ViPER4Android
Martmists and Iscle for reverse-engineering

## Tested r5 module and GitHub CI

The `module/` directory retains the original ViPER 8.0 installer, with only two configuration/ODM path fixes and `version=8.0-r5`. This variant has passed real audio-processing tests on Galaxy S22 (TachyonOS Android 15).

The [CI workflow](.github/workflows/build.yml) reproduces the exact device-tested r5 ZIP payload using the SHA-256-pinned upstream v8.0 module drivers. Independently rebuilt libraries are **comparison-only** until validated. A draft r5 release is available via manual workflow dispatch; nothing is automatically published.

See [r5 validation and release policy](docs/r5-validation.md) for the evidence, pinned hashes, and remaining RK3588/older Android tests.
