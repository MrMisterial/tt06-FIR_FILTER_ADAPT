`timescale 1ns / 1ps

module FIR #(
	parameter TAP_SIZE = 3,
	parameter NBR_OF_TAPS = 3,
	parameter X_N_SIZE = 8,
	parameter Y_N_SIZE = 11 //TAP_SIZE + X_N_SIZE minimum
) (
    input clk,
    input reset,
    input signed [X_N_SIZE-1:0] x_n, 
    input s_axis_fir_tvalid,
    input s_set_coeffs,
    output wire signed [Y_N_SIZE-1:0] o_y_n
    );


    parameter BUFF_SIZE = 6;//NBR_OF_TAPS*2-1; //NBR_OF_TAPS;//
    reg signed [TAP_SIZE-1:0] taps [0:NBR_OF_TAPS-1];
    reg signed [X_N_SIZE-1:0] buffs [0:BUFF_SIZE-1];
    //reg signed [TAP_SIZE-1:0] tap;
    //reg signed [X_N_SIZE-1:0] buff;
    
    reg signed [TAP_SIZE-1:0] new_taps [0:NBR_OF_TAPS-1];
    reg signed [X_N_SIZE-1:0] new_buffs [0:BUFF_SIZE-1];
    
    reg signed [Y_N_SIZE-1:0] new_y_n;
    reg signed [Y_N_SIZE-1:0] y_n;
    
    reg signed [Y_N_SIZE-1:0] new_act_y_n;
    reg signed [Y_N_SIZE-1:0] act_y_n;
    
    
    reg [1:0] cnt_setup;
    reg [1:0] new_cnt_setup;
    
    reg [1:0] cnt_tap;
    reg [1:0] new_cnt_tap;
    
    reg [2:0] cnt_buff;
    reg [2:0] new_cnt_buff;
    

    reg [2:0] next_state, state;
    
    /*
    wire signed [X_N_SIZE-1:0] buff0 = buffs[0];
    wire signed [X_N_SIZE-1:0] buff1 = buffs[1];
    wire signed [X_N_SIZE-1:0] buff2 = buffs[2];
    wire signed [X_N_SIZE-1:0] buff3 = buffs[3];
    */
    
    
    localparam SETUP        = 3'b000;
    localparam IDLE         = 3'b001;
    localparam GET_DATA     = 3'b010;
    localparam CALC         = 3'b011;
    localparam SET_OUTPUT   = 3'b100;
    localparam CONFIG       = 3'b101;
    
     
    
    integer e;
    integer r;
    always @ (posedge clk) begin
	
    		if(reset == 1'b1) begin
    			state <= SETUP; 
    			cnt_setup <= 2'b00;  //???
    			cnt_tap <= 2'b00;
    			cnt_buff <= 3'b000;
    			y_n <= {Y_N_SIZE{1'b0}};
    			act_y_n <= {Y_N_SIZE{1'b0}};
    			
    			for (e =0; e<(NBR_OF_TAPS); e = e + 1) begin //geht das so???
				taps[e] <= {TAP_SIZE{1'b1}};
			end
			
			for (r =0; r<(BUFF_SIZE); r = r + 1) begin //geht das so???
				buffs[r] <= {X_N_SIZE{1'b0}};
			end
    		end
    		else begin
    			state <= next_state;
    			cnt_setup <= new_cnt_setup;
    			y_n <= new_y_n;
    			cnt_tap <= new_cnt_tap;
    			cnt_buff <= new_cnt_buff;
    			//buff <= new_taps[0];
    			act_y_n <= new_act_y_n;
    			
    			for (e =0; e<(NBR_OF_TAPS); e = e + 1) begin //geht das so???
				taps[e] <= new_taps[e];
			end
			
			for (r =0; r<(BUFF_SIZE); r = r + 1) begin //geht das so???
				buffs[r] <= new_buffs[r];
			end
			
			
    		end
    end
    			
    integer i;    	
    integer j;
    integer w;
    always @* begin //, posedge clk, 
    
    //state,s_set_coeffs,s_axis_fir_tvalid, cnt_setup
    
    	next_state = state;
    	new_cnt_setup = cnt_setup;
    	new_cnt_tap = cnt_tap;
	new_cnt_buff = cnt_buff;
	new_y_n = y_n;
	new_act_y_n = act_y_n;
    	
    	for (w =0; w<(BUFF_SIZE); w = w + 1) begin //geht das so???
		new_buffs[w] = buffs[w];
	end
	
	for (w =0; w<(NBR_OF_TAPS); w = w + 1) begin //geht das so???
		new_taps[w] = taps[w];
	end
	
	
    
    	case (state)
    	    SETUP: begin
    	    	if(cnt_setup == 2'b11) begin
    	    		next_state = IDLE;
    	    	end
    	    	
    	    	new_cnt_setup = cnt_setup + 2'b01;
    	    	
    	    	new_taps[0] = 3'b101;//{TAP_SIZE{1'b1}};
		new_taps[1] = 3'b010;//{TAP_SIZE{1'b0}};
		new_taps[2] = 3'b011;//{TAP_SIZE{1'b1}};
		
		/*
    	    	
		new_taps[0] = {TAP_SIZE{1'b1}};
		new_taps[1] = {TAP_SIZE{1'b0}};
		new_taps[2] = {TAP_SIZE{1'b1}};
    	    	
    	    	*/
    	    
    	    end
    	    
            IDLE: begin
		if (s_axis_fir_tvalid == 1'b1) begin
			next_state = GET_DATA;
		end
		
		if (s_set_coeffs == 1'b1) begin
			next_state = CONFIG;
		end
		
		for (w =0; w<(BUFF_SIZE-1); w = w + 1) begin //geht das so???
			new_buffs[w] = {X_N_SIZE{1'b0}};
		end
		
		
		
            end
            GET_DATA: begin
            /*  set this to idle
            	if (s_set_coeffs == 1'b1) begin
            		next_state = CONFIG;
            	end
            */
            
            	new_cnt_tap = 2'b00;
    		new_cnt_buff = 3'b000;
    		new_y_n = {Y_N_SIZE{1'b0}};
            	
            
            	if (s_axis_fir_tvalid == 1'b0 && s_set_coeffs == 1'b0) begin
            		next_state = IDLE;
            	end else begin
            		next_state = CALC;
            	end
            	
            	
            	
            	new_buffs[0] = x_n;
	        for (j =0; j<(BUFF_SIZE-1); j = j + 1) begin //geht das so???
			new_buffs[j+1] = buffs[j];
		end
		
 
            end 
            
            CALC: begin
            
            	if (cnt_tap == 2'b11) begin //make generic
            		next_state = SET_OUTPUT;
            	end else begin
		    	new_y_n = y_n + (taps[cnt_tap]*buffs[cnt_buff]+taps[cnt_tap]*buffs[(BUFF_SIZE-1)-new_cnt_buff]);
		    	
		    	new_cnt_tap = cnt_tap + 2'b1;
		    	new_cnt_buff = cnt_buff + 2'b1;
            	end
            	
            	/*
            	if (s_axis_fir_tvalid == 1'b0) begin
            		next_state = IDLE;
            	end
            	*/

            end
            
            SET_OUTPUT: begin
            	
            	new_act_y_n = y_n;
            	if (s_set_coeffs == 1'b0) begin
            		next_state = GET_DATA;
            	end else begin
            		next_state = CONFIG;
            	end
            	
            
            end
            
            
            CONFIG: begin
            	if (s_set_coeffs == 1'b0) begin
                	next_state = IDLE;
                end else begin
                	next_state = CONFIG;
                end
                
                new_taps[0] = x_n[TAP_SIZE-1:0];
		
		
		for (i =1; i<(NBR_OF_TAPS); i = i + 1) begin //geht das so???
			new_taps[i] = taps[i-1];
		end
            end
            
            default: begin
		next_state = IDLE;
		for (w =0; w<(BUFF_SIZE-1); w = w + 1) begin //geht das so???
			new_buffs[w] = {X_N_SIZE{1'b0}};
		end
		end
        endcase
        
        
    end
    
    



	//sum to next_sum
	/*
    reg signed [Y_N_SIZE-1:0] sum;
    integer k;
    always @( posedge clk) begin    	    
	    sum <= 0;	
	    
	    //sum = taps[0]*buffs[0] + taps[1]*buffs[1] + taps[2]*buffs[2]  +   taps[1]*buffs[3] + taps[0]*buffs[4];
	    //buff <= taps[2]*buffs[2];
	    
	    for (k =0; k<(BUFF_SIZE); k = k + 1) begin //geht das so???
	    	//sum = sum + (taps[k]*buffs[k]);
	    	//sum = sum + 1;
	    	
	    	if (k < (NBR_OF_TAPS)) begin
	    		sum <= sum + (taps[k]*buffs[k]);
	    	end
	    	else begin
	    		sum <= sum + (taps[(BUFF_SIZE-1)-k]*buffs[k]);
	    	end
	    	
	    	
	    
	    	

	    end    
	    
    end
    */
    assign o_y_n = act_y_n;//(state == SET_OUTPUT) ? () : {Y_N_SIZE{1'b0}}; // (sum >>TAP_SIZE) ???
    
    
    
endmodule

