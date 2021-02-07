//--------------------------------------------------------------------------------------------
//-  Copyright (c) Western Digital 2020
//-  Sub Script:  LowPowerSub.inc   Rev. 1.0  
//-  Description: Various help functions for main scripts
//-  History:
//-  Date	REV	Owner		Change
//-  		1.0 Matan Raveh	First Version
//   @PCIe functions input and output
//	  id8: Input value - Desired_CapabilityID
//    id9: Return value - Target Registeroffset/Next capability offset
//--------------------------------------------------------------------------------------------

sub GetCfgSpaceRegOffsetPCIe_STANDARD
//--------------------------------------------------------
//Returns register offset for a STANDARD particular capability id
//input paramaters: id8 - desired capability id
//return value: id9 - register offset for cap=id8
//                  - 0 if capability not found
//Check PCI capability ID starting at 0x34 offset
//--------------------------------------------------------
    inichcs 034h, id9 // place the Capabilities Pointer pointer in id9
    id9 = id9 & 000ffh  //extracting the next cap_ptr 
    while (id9 != 0)
        inichcs id9, id11 // read the reg in "ID9 address" into id11
        id10 = id11 & 00ffh // save the capability into id10
        if(id10 == id8) // if found the capability, stop
            goto break
        endif
        id9 = (id11 & 00ff00h)>>8 // save the pointer of next capability into id9
    endwhile
    if ((id9 == 0)) // if ended the search without break
        prnf "\nCapability id: %X,",id8
        prnf " not found!"
    endif
Break:endsub

sub GetCfgSpaceRegOffsetPCIe_EXTENDED
//--------------------------------------------------------
//Returns register offset for a particular EXTENDED capability id
//input paramaters: id8 - desired capability id
//return value: id9 - register offset for cap=id8
//                  - 0 if capability not found
//Check PCIe capbility ID starting at 0x100 offset
//--------------------------------------------------------
    id9 = 100h // place first list item address in id9
    while (id9 != 0) // as long as the pointer isn't 0
        inichcs id9, id11 // read the reg in "ID9 address" into id11
        id10 = id11 & 0ffffh // save the capability into id10
        //prnf "\nCapability ID: %X",id10
        if(id10 == id8) // if found the capability, stop
            goto break
        endif
        id9 = id11>>20 // save the pointer of next capability into id9
        //prnf "\nRegister Offset: %X",id9
    endwhile
    if ((id9 == 0)) // if ended the search without break
        prnf "\nCapability id: %X,",id8
        prnf " not found!"
    endif
Break:endsub
