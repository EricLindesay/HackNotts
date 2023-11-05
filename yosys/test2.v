    module counter(a,b,c,q);
input a,b,c;
output q;
assign q = (a&b) | c;
endmodule