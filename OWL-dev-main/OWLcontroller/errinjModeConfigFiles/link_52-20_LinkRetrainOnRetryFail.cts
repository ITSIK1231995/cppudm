TestAnalyzer =  PETracer   ;
TestGroup    = "Link Layer";

TestName     = "Link 52-20 LinkRetrainOnRetryFail";
TestCode     = "Test 52-20";

TestDescription = "The intent of this test is to ensure that the link connected to the DUT 
will go into retraining after trying for REPLAY_NUM of times to get a TLP
through and failing. It will also test that while in retraining
the retry buffer and link states are not changed and the pending TLP
is retransmitted after link retraining completes.";

//AssertionsTested=DLL.5.2#2, DLL.5.2#7


RecordingOptions   = "Endpoint\\link_layer.rec";
GenerationOptions  = "Endpoint\\link_layer.gen";
TrainerScript      = "Endpoint\\LinkLayer\\link_52-20_LinkRetrainOnRetryFail.peg";

VerificationScript = "Endpoint\\LinkLayer\\link_52-20_LinkRetrainOnRetryFail.pevs";
GenerationTimeout = 3000;

