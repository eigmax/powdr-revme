# To run manually:
# $ qemu-riscv32 -plugin ../../qemu-6.2+dfsg/contrib/plugins/libexeclog.so -d plugin -g 1234 target/riscv32imac-unknown-none-elf/release/evm
# $ gdb-multiarch target/riscv32imac-unknown-none-elf/release/evm -ex "target remote :1234" -ex "set \$a0 = <TEST_IDX>" -ex "c" -ex "c" -ex "exit"
# where <TEST_IDX> is the idx of the test to run.

import subprocess
import sys

def run_test(idx):
    print(f"Running test case number {idx}", file=sys.stderr)

    qemu_proc = subprocess.Popen(
        ["qemu-riscv32", "-plugin", "../../qemu-6.2+dfsg/contrib/plugins/libexeclog.so", "-d", "plugin", "-g", "1234", "target/riscv32imac-unknown-none-elf/release/evm"],
        stderr=subprocess.PIPE, stdout=sys.stderr
    )

    wc_proc = subprocess.Popen(["wc"], stdin=qemu_proc.stderr, stdout=subprocess.PIPE)

    gdb_proc = subprocess.Popen(["gdb-multiarch", "target/riscv32imac-unknown-none-elf/release/evm", "-ex", "target remote :1234", "-ex", f"set $a0 = {idx}", "-ex", "c", "-ex", "c", "-ex", "exit"], stdout=sys.stderr, stderr=sys.stderr)

    for line in wc_proc.stdout:
        wc_out = line

    gdb_proc.wait()    
    qemu_proc.wait()
    wc_proc.wait()

    num_steps = wc_out.split()[0].decode("ascii")

    print(f"{idx};{num_steps}")
    sys.stdout.flush()

for i in range(64):
    run_test(i)
