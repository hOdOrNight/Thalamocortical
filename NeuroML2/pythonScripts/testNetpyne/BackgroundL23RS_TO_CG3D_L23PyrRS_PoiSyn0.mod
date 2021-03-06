TITLE Mod file for component: Component(id=BackgroundL23RS_TO_CG3D_L23PyrRS_PoiSyn0 type=poissonFiringSynapse)

COMMENT

    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.0
         org.neuroml.model   v1.5.0
         jLEMS               v0.9.8.7

ENDCOMMENT

NEURON {
    POINT_PROCESS BackgroundL23RS_TO_CG3D_L23PyrRS_PoiSyn0
    ELECTRODE_CURRENT i
    RANGE averageRate                       : parameter
    RANGE averageIsi                        : parameter
    
    RANGE i                                 : exposure
    RANGE Syn_AMPA_SupPyr_SupPyr_tau        : parameter
    RANGE Syn_AMPA_SupPyr_SupPyr_gbase      : parameter
    RANGE Syn_AMPA_SupPyr_SupPyr_erev       : parameter
    
    RANGE Syn_AMPA_SupPyr_SupPyr_i          : exposure
    
}

UNITS {
    
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
    
}

PARAMETER {
    
    averageRate = 0.1 (kHz)
    averageIsi = 10 (ms)
    Syn_AMPA_SupPyr_SupPyr_tau = 2 (ms)
    Syn_AMPA_SupPyr_SupPyr_gbase = 1.8393973E-4 (uS)
    Syn_AMPA_SupPyr_SupPyr_erev = 0 (mV)
}

ASSIGNED {
    v (mV)
    
    Syn_AMPA_SupPyr_SupPyr_i (nA)          : derived variable
    
    i (nA)                                 : derived variable
    rate_tsince (ms/ms)
    rate_Syn_AMPA_SupPyr_SupPyr_g (uS/ms)
    rate_Syn_AMPA_SupPyr_SupPyr_A (uS/ms)
    
}

STATE {
    tsince (ms) 
    isi (ms) 
    Syn_AMPA_SupPyr_SupPyr_g (uS) 
    Syn_AMPA_SupPyr_SupPyr_A (uS) 
    
}

INITIAL {
    rates()
    rates() ? To ensure correct initialisation.
    
    tsince = 0
    
    isi = -  averageIsi  * log(1 - random_float(1))
    
    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state
    
    Syn_AMPA_SupPyr_SupPyr_g = 0
    
    Syn_AMPA_SupPyr_SupPyr_A = 0
    
}

BREAKPOINT {
    
    SOLVE states METHOD cnexp
    
    
}

NET_RECEIVE(flag) {
    
    LOCAL weight
    
    
    if (flag == 1) { : Setting watch for top level OnCondition...
        WATCH (tsince  >  isi) 1000
    }
    if (flag == 1000) {
    
        tsince = 0
    
        isi = -  averageIsi  * log(1 - random_float(1))
    
        : Child: Component(id=Syn_AMPA_SupPyr_SupPyr type=alphaSynapse)
    
        : This child is a synapse; defining weight
        weight = 1
    
        : paramMappings: {Syn_AMPA_SupPyr_SupPyr_notes={}, BackgroundL23RS_TO_CG3D_L23PyrRS_PoiSyn0={averageRate=averageRate, i=i, tsince=tsince, isi=isi, averageIsi=averageIsi}, Syn_AMPA_SupPyr_SupPyr={A=Syn_AMPA_SupPyr_SupPyr_A, gbase=Syn_AMPA_SupPyr_SupPyr_gbase, erev=Syn_AMPA_SupPyr_SupPyr_erev, g=Syn_AMPA_SupPyr_SupPyr_g, tau=Syn_AMPA_SupPyr_SupPyr_tau, i=Syn_AMPA_SupPyr_SupPyr_i}}
    ?    state_discontinuity(Syn_AMPA_SupPyr_SupPyr_A, Syn_AMPA_SupPyr_SupPyr_A  + ( Syn_AMPA_SupPyr_SupPyr_gbase *weight))
        Syn_AMPA_SupPyr_SupPyr_A = Syn_AMPA_SupPyr_SupPyr_A  + ( Syn_AMPA_SupPyr_SupPyr_gbase *weight)
    
        net_event(t)
        WATCH (tsince  >  isi) 1000
    
    }
    
}

DERIVATIVE states {
    rates()
    tsince' = rate_tsince 
    Syn_AMPA_SupPyr_SupPyr_g' = rate_Syn_AMPA_SupPyr_SupPyr_g 
    Syn_AMPA_SupPyr_SupPyr_A' = rate_Syn_AMPA_SupPyr_SupPyr_A 
    
}

PROCEDURE rates() {
    
    Syn_AMPA_SupPyr_SupPyr_i = Syn_AMPA_SupPyr_SupPyr_g  * ( Syn_AMPA_SupPyr_SupPyr_erev  - v) ? evaluable
    ? DerivedVariable is based on path: synapse/i, on: Component(id=BackgroundL23RS_TO_CG3D_L23PyrRS_PoiSyn0 type=poissonFiringSynapse), from synapse; Component(id=Syn_AMPA_SupPyr_SupPyr type=alphaSynapse)
    i = Syn_AMPA_SupPyr_SupPyr_i ? path based
    
    rate_tsince = 1 ? Note units of all quantities used here need to be consistent!
    
     
    rate_Syn_AMPA_SupPyr_SupPyr_g = (2.7182818284590451 *  Syn_AMPA_SupPyr_SupPyr_A  -  Syn_AMPA_SupPyr_SupPyr_g )/ Syn_AMPA_SupPyr_SupPyr_tau ? Note units of all quantities used here need to be consistent!
    rate_Syn_AMPA_SupPyr_SupPyr_A = - Syn_AMPA_SupPyr_SupPyr_A  /  Syn_AMPA_SupPyr_SupPyr_tau ? Note units of all quantities used here need to be consistent!
    
     
    
}


: Returns a float between 0 and max
FUNCTION random_float(max) {
    
    random_float = scop_random()*max
    
}

