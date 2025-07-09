#!/usr/bin/env python3

import argparse
import struct
import pathlib
import io
import os
import shutil

from elftools.elf.elffile import ELFFile


parser = argparse.ArgumentParser()
parser.add_argument("--output", "-o", type=pathlib.Path, default=pathlib.Path("update"))
parser.add_argument("IMG_NAME", type=pathlib.Path)
args = parser.parse_args()

with open(args.IMG_NAME, "rb") as f:
    fw_img = f.read()

# since all paths are relative to the firehose subdirectory
output_path = args.output / "firehose"
os.makedirs(output_path)

base_offset = 0x1000
offset = base_offset + 0x2e4

# number of files in the table
(table_size,) = struct.unpack("<I", fw_img[offset:offset+4])
offset += 4

# reversed engineered struct layout
#
# struct fw_file_table_entry {
#     uint8_t unknown1[24];
#     uint32_t offset;
#     uint32_t size;
#     uint8_t unknown2[4];
#     char name[64];
# }

for _ in range(table_size):
    file_struct = fw_img[offset:offset+100]
    (file_offset, file_size, file_name) = struct.unpack("<24xII4x64s", file_struct)
    file_name = pathlib.PureWindowsPath(file_name.decode().rstrip('\x00'))
    print(f"Extracting {file_name}, offset={file_offset}, size={file_size}")
    with open(output_path / file_name, "wb+") as f:
        f.write(fw_img[base_offset+file_offset:base_offset+file_offset+file_size])
    offset += len(file_struct)

offset = 0x2000

# make an in-memory IO buffer from the beginning of the ELF file
# until the end of the MS package
with io.BytesIO(fw_img[offset:]) as f:
    elf = ELFFile(f)
    seg_offset = 0
    seg_size = 0
    # compute the ELF total size, by getting the offset & size of its last segment
    for segm in elf.iter_segments():
        seg_offset = segm.header.p_offset
        seg_size = segm.header.p_filesz
    assert seg_offset > 0
    assert seg_size > 0

with open(output_path / "prog_firehose_9x65.mbn", "wb+") as f:
    print(f"Extracting {f.name}, offset={offset}, size={seg_offset + seg_size}")
    f.write(fw_img[offset:offset+seg_offset+seg_size])

# simply copied since they are not included in the MS package
# and they seem to remain identical between versions
# (checked EM12GPAR01A09M4G_MSFT_01.001.01.001 & EM12GPAR01A21M4G_01.204.01.204)
script_dir = pathlib.Path(os.path.dirname(__file__))
for name in ["patch_p4K_b256K.xml", "rawprogram_nand_p4K_b256K_update.xml"]:
    print(f"Copying {name}")
    shutil.copy(script_dir / "res" / name, output_path)
