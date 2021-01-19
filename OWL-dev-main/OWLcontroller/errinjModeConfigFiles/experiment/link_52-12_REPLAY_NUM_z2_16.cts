TestAnalyzer =  PETracer   ;
TestGroup    = "Link Layer";

TestName     = "Link 52-12 REPLAY_NUM";
TestCode     = "Test 52-12";

TestDescription = "The intent of this test is to ensure that a DUT will keep retransmitting
a transaction for which a NAK has been issued on purpose
until the number of times its REPLAY_NUM supports.";

//AssertionsTested=DLL.5.2#1.2


RecordingOptions   = "Endpoint\\link_layer.rec";
GenerationOptions  = "Endpoint\\link_layer.gen";
TrainerScript      = "Endpoint\\LinkLayer\\link_52-12_REPLAY_NUM_z2_16.peg";

VerificationScript = "Endpoint\\LinkLayer\\link_52-12_REPLAY_NUM.pevs";


TestExerciser = "Z2-16";