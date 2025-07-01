// 8‑tap FIR filter, 16‑bit data, fixed coefficients 1‑8
module fir_filter (
    input  wire              clk,
    input  wire              reset,       // synchronous, active‑high
    input  wire              in_valid,
    input  wire signed [15:0] in,
    output wire signed [31:0] out          // widened to avoid overflow
);

    // shift‑register for the last 8 samples
    reg signed [15:0] shift_reg [0:7];

    // coefficient ROM
    reg signed [15:0] coeff [0:7];
    initial begin
        coeff[0] = 16'd1;  coeff[1] = 16'd2;
        coeff[2] = 16'd3;  coeff[3] = 16'd4;
        coeff[4] = 16'd5;  coeff[5] = 16'd6;
        coeff[6] = 16'd7;  coeff[7] = 16'd8;
    end

    reg signed [31:0] acc;
    assign out = acc;

    integer i;
    always @(posedge clk) begin
        if (reset) begin
            for (i = 0; i < 8; i = i + 1) begin
                shift_reg[i] <= 16'sd0;
            end
            acc <= 32'sd0;
        end else if (in_valid) begin
            // shift in the new sample
            for (i = 7; i > 0; i = i - 1)
                shift_reg[i] <= shift_reg[i-1];
            shift_reg[0] <= in;

            // multiply–accumulate
            acc <= 32'sd0;
            for (i = 0; i < 8; i = i + 1)
                acc <= acc + shift_reg[i] * coeff[i];
        end
    end
endmodule
