TestAnalyzer =  PETracer   ;
TestGroup    = "Link Layer";

TestName     = "Link 41-20 ReservedFieldsDLLPReceive";
TestCode     = "Test 41-20";

TestDescription = "The intent of this test is to verify that the DUT truly ignores reserved fields in an 
ACK DLLP by sending arbitrary data in those fields.";

//AssertionsTested=DLL.4.1#2


RecordingOptions   = "Endpoint\\link_layer.rec";
GenerationOptions  = "Endpoint\\link_layer.gen";
TrainerScript      = "Endpoint\\LinkLayer\\link_41-20_ReservedFieldsDLLPReceive.peg";

VerificationScript = "Endpoint\\LinkLayer\\link_41-20_ReservedFieldsDLLPReceive.pevs";


TestExerciser = "ALL";