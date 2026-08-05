module top(input clk, input en, output [3:0] count);

wire dut_en, d1, d2;

DUT dut_i (.clk(clk), .en(dut_en), .count(count));

Delay delay_i (.i(en), .o(d1));
Delay #(.PARAM(42)) delay42_i (.i(d1), .o(d2));
Unknown bb_i (.i(d2), .o(dut_en));

always @(posedge clk ) begin
    assert (count < 4'd6);
    cover (count == 4'd5);
end

endmodule

module DUT (input clk, input en, output [3:0] count);

    reg [3:0] c = 4'd0;

    always @(posedge clk) begin
        if (en)
            if (c == 5)
                c <= 4'd0;
            else
                c <= c + 4'd1;
    end

    assign count = c;

endmodule

module Delay #(parameter PARAM = 0) (input clk, input i, output o);
    reg [PARAM:0] r;
    assign o = r[PARAM];

    always @(posedge clk) begin
        r <= {r[PARAM-1:0], i};
    end
endmodule

(* blackbox *)
module Unknown (input i, output o);
endmodule