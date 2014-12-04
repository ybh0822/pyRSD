%{
#include "ZeldovichPS.h"
%}

class ZeldovichPS {
public:
    
    ZeldovichPS(const PowerSpectrum& P_L);
    virtual ~ZeldovichPS();
    
    // translated to __call__ -> calls Evaluate(K)
    double operator()(const double k) const;
    
    // translated to __call__ -> calls EvaluateMany(K)
    parray operator()(const parray& k) const;
    
    const PowerSpectrum& GetLinearPS() const;
    const double& GetRedshift() const;
    const double& GetSigma8() const;
    const Cosmology& GetCosmology() const;
    
    void SetRedshift(double z); 
    void SetSigma8(double sigma8);
};

class ZeldovichP00 : public ZeldovichPS {

public:
    
    ZeldovichP00(const PowerSpectrum& P_L);
    ZeldovichP00(const ZeldovichPS& ZelPS);

};


class ZeldovichP01 : public ZeldovichPS {

public:
    
    ZeldovichP01(const PowerSpectrum& P_L);
    ZeldovichP01(const ZeldovichPS& ZelPS);
    
};
