// SPDX-License-Identifier: Apache-2.0
module traffic_light (
    input  wire clk,
    input  wire reset_n,
    output wire red,
    output wire amber,
    output wire green
);
    localparam RED       = 2'd0;
    localparam RED_AMBER = 2'd1;
    localparam GREEN     = 2'd2;
    localparam AMBER     = 2'd3;
    reg [1:0] state;

    // Hold reset low for a rising edge to select red.
    always @(posedge clk) begin
        if (!reset_n)
            state <= RED;
        else begin
            case (state)
                RED:       state <= RED_AMBER;
                RED_AMBER: state <= GREEN;
                GREEN:     state <= AMBER;
                AMBER:     state <= RED;
                default:   state <= RED;
            endcase
        end
    end

    assign red   = (state == RED) || (state == RED_AMBER);
    assign amber = (state == AMBER) || (state == RED_AMBER);
    assign green = (state == GREEN);
endmodule
