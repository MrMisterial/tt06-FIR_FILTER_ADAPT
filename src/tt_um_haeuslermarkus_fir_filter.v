/*
 * Copyright (c) 2024 Your Name
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

  // All output pins must be assigned. If not used, assign to 0.
  //assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  //assign uio_out = 0;
  //assign uio_oe  = 0;
  
    wire reset = rst_n;

    assign uio_oe[7:0] = 8'b00111111;
    
    wire [10:0] m_axis_fir_tdata; //FIR OUTPUT DATA
    assign uo_out = m_axis_fir_tdata[7:0]; //8Bits output
    
    assign uio_out[2:0] = m_axis_fir_tdata[10:8]; //2Bits output
    assign uio_out[5:3] = 3'b000;
    
    assign uio_out[7:6] = 2'b00;
    
    //set param
    wire s_set_coeffs;
    assign s_set_coeffs = uio_in[6];
    
    wire s_axis_fir_tvalid;
    assign s_axis_fir_tvalid = uio_in[7];
   
    
    wire [7:0] s_axis_fir_tdata; //FIR INPUT DATA 
    assign s_axis_fir_tdata = ui_in[7:0]; //8 Bit in

    
    
    fir_main fir_main_instance(
        .clk(clk),
        .reset(reset),
        .x_n(s_axis_fir_tdata),       
        .s_axis_fir_tvalid(s_axis_fir_tvalid), 
        .s_set_coeffs(s_set_coeffs),   
        .o_y_n(m_axis_fir_tdata));  

endmodule
