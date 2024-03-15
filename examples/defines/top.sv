`include "include.svh"

module top(input [N-1:0] i, output o);

assign o = i[ `IDX0 ] & i[ `IDX1 ];

endmodule