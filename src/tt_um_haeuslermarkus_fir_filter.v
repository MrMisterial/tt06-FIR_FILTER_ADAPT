/*
 * Copyright (c) 2024 Markus Häusler
 * SPDX-License-Identifier: Apache-2.0
 */

`define default_netname none

`include "fir_main.v"

module tt_um_haeuslermarkus_fir_filter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);


    wire reset = !rst_n;

    assign uio_oe[7:0] = 8'b00111111; //configs bidirectional pins as in- or output
    
    wire [10:0] m_axis_fir_tdata; //FIR OUTPUT DATA
    assign uo_out = m_axis_fir_tdata[7:0]; //8Bits output
    assign uio_out[2:0] = m_axis_fir_tdata[10:8]; //3Bits output
    assign uio_out[5:3] = 3'b000; //set unused outputs to zero
    assign uio_out[7:6] = 2'b00; //set bidirectional pin output - necessary for linter
    
    //set params
    wire s_set_coeffs;
    assign s_set_coeffs = uio_in[6]; // Input Pin to start configuration Mode
    
    wire s_axis_fir_tvalid;
    assign s_axis_fir_tvalid = uio_in[7]; // Input to activate FIR Filter output
   
    wire [7:0] s_axis_fir_tdata; //FIR INPUT DATA 
    assign s_axis_fir_tdata = ui_in[7:0]; //8 Bit input

    
    
    fir_main fir_main_instance(
        .clk(clk),
        .reset(reset),
        .x_n(s_axis_fir_tdata),       
        .s_axis_fir_tvalid(s_axis_fir_tvalid), 
        .s_set_coeffs(s_set_coeffs),   
        .o_y_n(m_axis_fir_tdata));  

endmodule
