TestAnalyzer =  PETracer   ;
TestGroup    = "Link Layer";

TestName     = "Link 52-10 RetransmitOnNak";
TestCode     = "Test 52-10";

TestDescription = "The intent of this test is to ensure that a DUT will retransmit a transaction 
for which a NAK has been issued.";

//AssertionsTested=DLL.5.2#1


RecordingOptions   = "Endpoint\\link_layer.rec";
GenerationOptions  = "Endpoint\\link_layer.gen";
TrainerScript      = "Endpoint\\LinkLayer\\link_52-10_RetransmitOnNak.peg";

VerificationScript = "Endpoint\\LinkLayer\\link_52-10_RetransmitOnNak.pevs";

