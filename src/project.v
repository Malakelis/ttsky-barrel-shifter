/*
 * Copyright (c) 2026 Alan Aquino
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// Tiny Tapeout wrapper: 8-bit barrel shifter / rotator (n_shifter, N = 8)
module tt_um_barrel_shifter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // ui_in       = data_in[7:0]
  // uio_in[2:0] = k (shift/rotate amount)
  // uio_in[3]   = left        (0 = right, 1 = left)
  // uio_in[4]   = shift       (0 = rotate, 1 = shift)
  // uio_in[5]   = arithmetic  (1 = arithmetic right shift)
  // uo_out      = data_out[7:0]
  n_shifter #(.N(8)) shifter (
      .data_in   (ui_in),
      .k         (uio_in[2:0]),
      .left      (uio_in[3]),
      .shift     (uio_in[4]),
      .arithmetic(uio_in[5]),
      .data_out  (uo_out)
  );

  // The bidirectional pins are all inputs.
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, uio_in[7:6], 1'b0};

endmodule
