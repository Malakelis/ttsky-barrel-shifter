<!---
This file is used to generate your project datasheet.
-->

## How it works

An 8-bit combinational barrel shifter built as a cascade of 2:1 mux rows
(Weste & Harris, *CMOS VLSI Design* 4e, Fig. 11.68). It is built up in three levels:

1. **`n_ror_barrel`** - log2(N) rows of N muxes; row *j* rotates right by 2^j when `k[j]` = 1.
2. **`n_ror_l`** - adds XORs that invert `k` when rotating left, plus a fixed "rotate right by 1" preshift row
   (left by k = right by ~k + 1, so no adder is needed).
3. **`n_shifter`** - adds a masking unit. A thermometer code marks the bits that wrapped around and
   replaces them with a kill value (0, or the sign bit for an arithmetic right shift).

The chip uses level 3 with N = 8 (`tt_um_barrel_shifter` wraps `n_shifter`). The design is purely
combinational; the clock and reset are unused.

| left | shift | arithmetic | operation              |
|------|-------|------------|------------------------|
| 0    | 0     | x          | rotate right           |
| 1    | 0     | x          | rotate left            |
| 0    | 1     | 0          | logical shift right    |
| 0    | 1     | 1          | arithmetic shift right |
| 1    | 1     | x          | shift left             |

## Pinout

| Pin        | Function                          |
|------------|-----------------------------------|
| `ui[7:0]`  | data in                           |
| `uio[2:0]` | shift / rotate amount `k` (0-7)   |
| `uio[3]`   | `left`                            |
| `uio[4]`   | `shift`                           |
| `uio[5]`   | `arithmetic`                      |
| `uo[7:0]`  | data out                          |

## How to test

Set `ui` to a byte, choose `k`, `left`, `shift` and `arithmetic` on the `uio` pins, and read `uo`.
Example: `ui = 0b10010110`, `k = 2`, `left = 0`, `shift = 1`, `arithmetic = 1`
gives `uo = 0b11100101`.

Simulation: `cd test && make` runs an exhaustive check of the top level against the Python golden model
(`test/model.py`). `cd test/levels && make regress` tests each level at N = 4, 8 and 16.

## External hardware

None. Use switches for the inputs and LEDs for the outputs.
