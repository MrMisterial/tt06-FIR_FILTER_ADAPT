`timescale 1ns / 1ps
`include "fir_main.v"


//this testbench is similar to the test.py test
//for development efficency and to create plots for the documentation this tb was added additionally
//further documentation can be found in test.py
module fir_tb;

    reg clk, reset, s_axis_fir_tvalid;
    reg signed [7:0] s_axis_fir_tdata;
    wire m_axis_fir_tvalid;
    reg s_set_coeffs;
    wire [10:0] m_axis_fir_tdata;
    

    always begin
        clk = 1; #5;
        clk = 0; #5;
    end
    
    always begin
    	reset = 0; #10;
        reset = 1; #10;
        reset = 0; #100000;
    end

    always begin
    	s_axis_fir_tvalid = 1;
        s_set_coeffs = 0; #2000000;

        
    end
    
    
    /* Instantiate FIR module to test. */
    fir_main fir_main_instance(
        .clk(clk),
        .reset(reset),
        .x_n(s_axis_fir_tdata),       
        .s_axis_fir_tvalid(s_axis_fir_tvalid), 
        .s_set_coeffs(s_set_coeffs),  
        .o_y_n(m_axis_fir_tdata));  

   
        
        
    
    
    
    initial begin
    	$dumpfile("fir_tb.vcd");
    	$dumpvars;
    	
    	//initial impulse response test
	s_axis_fir_tdata <= 8'd0; #300; 
	
	s_axis_fir_tdata <= 8'd1; #10 //10
	
	s_axis_fir_tdata <= 8'd0; #998
	
	#10
	//set new fir coeffs
	s_set_coeffs = 1;
	s_axis_fir_tvalid = 0; 
	#2
	s_axis_fir_tdata <= 8'd1; #10
	s_axis_fir_tdata <= 8'd2; #10
	s_axis_fir_tdata <= 8'd3; #10
	s_axis_fir_tdata <= 8'd0;
	s_axis_fir_tvalid = 1;
	s_set_coeffs = 0; #2; #100
	
	//impulse response with new coeffs
	s_axis_fir_tdata <= 8'd0; #300
	
	#20; #10;
	s_axis_fir_tdata <= 8'd1; #10
	
	s_axis_fir_tdata <= 8'd0; #1000
	
	
	//reset fir to old coeffs
	reset = 1; #10;
	reset = 0; #10;
	
	//impulse response after coeffs
	s_axis_fir_tdata <= 8'd0; # 283
	
	s_axis_fir_tdata <= 8'd1; #10
	
	s_axis_fir_tdata <= 8'd0; #1000
	
	
	//test tvalid flag
	s_axis_fir_tdata <= 8'd1; #18

	#1000
    	$finish;
    end
          
    
endmodule

