#!/usr/bin/env python3
"""Reproduce the S901B-tested ViPER r5 ZIP and compare independent DSP rebuilds."""
import hashlib
import sys
import zipfile
from pathlib import Path

UPSTREAM_SHA = "e1c800985448b748a0d8ee611f741955a8a0ab62cc695dbac6a006ac7ca0bd54"
TESTED_R5_SHA = "94f63d9f912503654475411724b7fe3e85398e57e9eacc61b7ba52b05b675126"
PATCHED = {
    "common/install.sh": "ac27edda54133467ed7a78b3bbc4cef190897fa2a92c08dd6ce7bb71d2574e5c",
    "post-fs-data.sh": "a9e68e8e20bc9993217791285d786073d13973068925d6dd0c8558d96e01f2b4",
    "module.prop": "ce393a4d7ee2ea15b221e6986da2e4b958d217bf8ac0b32d97e44f28bdc2425e",
}
DRIVERS = {
    "libv4a_re_armeabi-v7a.so": "c1b660b4ad7d51562279bae51744b183575f209eb930d6b28cd4b244f51f3cc9",
    "libv4a_re_arm64-v8a.so": "a2808803c5623d14fb9589d842bed5fd79742dd96aa04156c102d6122f7b091c",
    "libv4a_re_x86.so": "9eead289108d53e70776daf261cc821fbc3034e7be4e963b3e8ee7e9b400a7c5",
    "libv4a_re_x86_64.so": "4c235cd844994a2056eb9dc5af194814d8d989faf77836f80a56400ea6dd5ae9",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def die(message):
    raise SystemExit("FAIL: " + message)


def package(source, module_dir, output):
    if sha(source.read_bytes()) != UPSTREAM_SHA:
        die("upstream ViPER 8.0 ZIP differs from the S901B-tested original")
    seen = set()
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(output, "w") as zout:
        if zin.testzip() is not None:
            die("upstream ZIP CRC failure")
        for entry in zin.infolist():
            name = entry.filename
            if name in seen:
                die("duplicate archive member: " + name)
            seen.add(name)
            data = zin.read(name)
            repo_path = module_dir / name
            if name in PATCHED:
                if not repo_path.is_file():
                    die("missing tested r5 patch: " + str(repo_path))
                data = repo_path.read_bytes()
                if sha(data) != PATCHED[name]:
                    die("r5 patch changed without renewed device validation: " + name)
            elif name.startswith("common/files/") and name.endswith(".so"):
                if sha(data) != DRIVERS.get(Path(name).name):
                    die("original driver checksum mismatch: " + name)
            elif repo_path.is_file() and repo_path.read_bytes() != data:
                die("unexpected change to original module file: " + name)
            zout.writestr(entry, data)
    if set(PATCHED) - seen:
        die("missing patched entries")
    if len([n for n in seen if n.endswith(".so")]) != 4:
        die("expected exactly four architecture DSP drivers")
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None:
            die("output ZIP CRC failure")
    print("PASS: original members preserved; only 3 tested r5 file replacements; 4 pinned DSPs")
    result_sha = sha(output.read_bytes())
    if result_sha != TESTED_R5_SHA:
        die("package differs from the byte-for-byte S901B-tested r5 ZIP: " + result_sha)
    print("PASS: package matches device-tested r5 ZIP SHA-256:", result_sha)


def compare(directory):
    differences = 0
    for name, expected in DRIVERS.items():
        paths = sorted(directory.rglob(name))
        if len(paths) != 1:
            die("expected one rebuilt " + name + "; found " + str(len(paths)))
        actual = sha(paths[0].read_bytes())
        matched = actual == expected
        differences += not matched
        print(("MATCH" if matched else "DIFF ") + " " + name +
              " " + actual + " (validated " + expected + ")")
    print("Byte-identical DSP rebuilds: %d/4" % (4 - differences))
    if differences:
        print("NOTE: independently rebuilt DSPs are not interchangeable with the tested release binaries.")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "package":
        package(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    elif len(sys.argv) == 3 and sys.argv[1] == "compare":
        compare(Path(sys.argv[2]))
    else:
        die("usage: verify_r5.py package <original.zip> <module-dir> <output.zip> | compare <built-dir>")
