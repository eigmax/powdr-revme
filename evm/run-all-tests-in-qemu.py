# To run manually:
# $ qemu-riscv32 -plugin qemu-plugin/insn.so -d plugin -g 1234 target/riscv32imac-unknown-none-elf/release/evm
# $ gdb-multiarch target/riscv32imac-unknown-none-elf/release/evm -ex "target remote :1234" -ex "set \$a0 = <TEST_IDX>" -ex "c" -ex "c" -ex "exit"
# where <TEST_IDX> is the idx of the test to run.

import subprocess
import sys
import re

parser = re.compile(r"insns: (\d+)")

def run_test(idx):
    print(f"Running test case number {idx}", file=sys.stderr)

    qemu_proc = subprocess.Popen(
        ["qemu-riscv32", "-plugin", "qemu-plugin/insn.so", "-d", "plugin", "-g", "12345", "target/riscv32imac-unknown-none-elf/release/evm"],
        stderr=subprocess.PIPE, stdout=sys.stderr
    )

    gdb_proc = subprocess.Popen(["gdb-multiarch", "target/riscv32imac-unknown-none-elf/release/evm", "-batch", "-ex", "target remote :12345", "-ex", f"set $a0 = {idx}", "-ex", "c", "-ex", "kill", "-ex", "exit"], stdout=sys.stderr, stderr=sys.stderr)

    num_steps = None
    for line in qemu_proc.stderr:
        m = parser.search(line.decode('utf-8'))
        if m:
            num_steps = m.group(1)

    gdb_proc.wait()    
    qemu_proc.wait()

    print(f"{idx};{num_steps}")
    sys.stdout.flush()

for i in range(64):
    run_test(i)
