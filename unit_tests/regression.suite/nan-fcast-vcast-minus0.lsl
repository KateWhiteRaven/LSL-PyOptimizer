default{timer(){llSetPrimitiveParams(
[ (float)"inf"
, (float)"-inf"
, (float)"+inf"
, (float)"--inf"
, (float)"+-inf"
, 1e400
, 1e39
, -1e400
, -0*1e40
, 0*1e40
, llList2CSV([(float)"nan"])
, llList2CSV([-(float)"nan"])
, llList2CSV([(float)"-nan"])
, llList2CSV([(float)"-nanometre"])
, llList2CSV([(float)"--nan"])
, -0.
, 0.
, -0
, 0
, (float)"-0x13"
, (float)"+0x13"
, (float)"-0x13p1"
, (float)"+0x13p1"
, <-0, -0., 0>
, (vector)"<nan,-0,-0.>"
, (vector)"<-nan,1,1>"
, (vector)"<nano,nano,nano>"
, (vector)"<nan,nan,nano>"
, (vector)"<nan(1),nan,nano>"
, (float)"1e-38"
, (vector)"<1e-38,0,0>"
, 1e40/1
, 1e40-1e40
, <3.,0.,-0.>/0.
, <3.,0.,-0.>/-0.
, <1e40,1e40*0,-1e40*0>/0.
, <1e40,1e40*0,-1e40*0>/-0.
]
);}}
