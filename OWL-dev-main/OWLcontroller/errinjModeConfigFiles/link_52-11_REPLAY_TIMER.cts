TestAnalyzer =  PETracer   ;
TestGroup    = "Link Layer";

TestName     = "Link 52-11 REPLAY_TIMER";
TestCode     = "Test 52-11";

TestDescription = "The intent of this test is to ensure that a DUT's REPLAY_TIMER is working properly by not sending
neither an ACK nor a NAK.";

//AssertionsTested=DLL.5.2#1.1


RecordingOptions   = "Endpoint\\link_layer.rec";
GenerationOptions  = "Endpoint\\link_layer.gen";
TrainerScript      = "Endpoint\\LinkLayer\\link_52-11_REPLAY_TIMER.peg";

VerificationScript = "Endpoint\\LinkLayer\\link_52-11_REPLAY_TIMER.pevs";

