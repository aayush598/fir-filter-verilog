`timescale 1ns/1ps

module tb_fir_filter;
    reg clk;
    reg reset;
    reg in_valid;
    reg signed [15:0] in;
    wire signed [31:0] out;

    // Instantiate the DUT
    fir_filter dut (
        .clk(clk),
        .reset(reset),
        .in_valid(in_valid),
        .in(in),
        .out(out)
    );

    // Clock generation: 100 MHz
    initial clk = 0;
    always #5 clk = ~clk;

    integer data_file, scan_file, output_file;
    integer status;
    integer value_count;

    // Output recording
    initial begin
        data_file   = $fopen("input_data.txt", "r");
        output_file = $fopen("output_data.txt", "w");

        if (data_file == 0) begin
            $display("Error: Cannot open input_data.txt");
            $finish;
        end
        if (output_file == 0) begin
            $display("Error: Cannot create output_data.txt");
            $finish;
        end

        // Initial reset
        reset    = 1;
        in_valid = 0;
        in       = 0;
        #20;
        reset = 0;

        // Feed input samples
        while (!$feof(data_file)) begin
            @(negedge clk);
            status = $fscanf(data_file, "%d\n", in);
            in_valid = 1;
        end

        // Stop driving input
        @(negedge clk);
        in_valid = 0;

        // Let filter flush out final outputs
        #100;

        $fclose(data_file);
        $fclose(output_file);
        $finish;
    end

    // Output display and write to file
    always @(posedge clk) begin
        $display("%0t ns : clk = %b | reset = %b | in = %0d | out = %0d", $time, clk, reset, in, out);
        if (!reset && in_valid)
            $fwrite(output_file, "%0d\n", out);
    end

    // Optional waveform
    initial begin
        $dumpfile("fir_filter.vcd");
        $dumpvars(0, tb_fir_filter);
    end

endmodule
