// Here we will learn to write a verilog HDL to design a 4 bit counter
module counter(clk,count);
  //define input and output ports
  input clk;
  output reg [2:0] count;
  //always block will be executed at each and every positive edge of the clock
  always@(posedge clk) 
  begin
    count <= count + 1;
  end
endmodule
