`timescale 1ns/1ps

module tb_fir_filter;
    reg clk;
    reg reset;
    reg in_valid;
    reg  signed [15:0] in;
    wire signed [31:0] out;

    // DUT instantiation
    fir_filter dut (
        .clk(clk),
        .reset(reset),
        .in_valid(in_valid),
        .in(in),
        .out(out)
    );

    // 100 MHz clock (10 ns period)
    initial clk = 0;
    always #5 clk = ~clk;

    integer k;

    initial begin
        // power‑on
        reset    = 1'b1;
        in_valid = 1'b0;
        in       = 16'sd0;
        #20;                 // keep reset high for two cycles
        reset = 1'b0;

        // feed 16 samples
        for (k = 0; k < 16; k = k + 1) begin
            @(negedge clk);
            in       = k;    // simple ramp; change as needed
            in_valid = 1'b1;
        end

        // stop driving in_valid
        @(negedge clk);
        in_valid = 1'b0;

        // allow a few cycles for the last output to settle, then finish
        #50;
        $finish;
    end

    // simple run‑time printout
    always @(posedge clk) begin
            $display("%0t ns : clk = %b| reset = %b | in = %0d  --> out = %0d", $time,clk, reset, in, out);
    end
endmodule
