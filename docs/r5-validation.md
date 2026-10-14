# ViPER4Android 8.0-r5 — validation and release policy

## Device evidence (2026-10-14)

- Galaxy S22 SM-S901B (r0s), TachyonOS Android 15, KernelSU Next, Meta Magic Mount RS: **r5 processing PASS** (user-reported).
- ViPER 8.0 unmodified: no processing.
- Registration isolation: r3-A (three XML registrations) PASS; r3-B (vendor primary) FAIL; r3-C (Samsung vendor) PASS; r3-D (system) FAIL.
- r4 (modified installer, removed legacy boot script): PASS on S901B.
- **r5** (original installer retained): PASS on S901B with only the configuration-copy fix, the corrected ODM bind source, and version=8.0-r5.
- RK3588 and older Android generations: **pending**. Do not describe this module as universally verified.
- The combined r5 test does not isolate which of its two changes is individually essential.

## Exact reference

The original WSTxda v8.0 `viper4android_module.zip` matches the user-supplied original's reported archive size (1,843,686 bytes); CI checks its complete SHA-256 against:

`e1c800985448b748a0d8ee611f741955a8a0ab62cc695dbac6a006ac7ca0bd54`

The SHA-256 of the **device-tested r5 ZIP** is:

`94f63d9f912503654475411724b7fe3e85398e57e9eacc61b7ba52b05b675126`

CI uses `ci/verify_r5.py` to check all three modified files by SHA-256, preserve the other original files, verify all four original DSP binaries, and reproduce the ZIP. It does not apply device-specific registrations, modify the DSP source or rely on an alternate mounting implementation.

The source-build matrix compiles separately for ARM32, ARM64, x86 and x86_64 and compares full binary hashes to the tested originals. **A successful compilation does not imply audio-processing validation, and a different DSP hash must not silently enter the r5 release ZIP.**

## Workflow

1. GitHub Actions `ViPER4Android r5` on `main` builds the pinned r5 ZIP artifact and independently compiles/comparisons drivers.
2. Review the ZIP SHA and rebuilt-driver comparison.
3. To create a **draft** release, manually run `ViPER4Android r5` with `draft_release=true`. The draft ZIP contains the original validated drivers.
4. Keep the release a draft until the pending cross-device tests meet the intended release scope.

The runtime module (installer, scripts, libraries and effects registration) is not altered by the CI changes.
