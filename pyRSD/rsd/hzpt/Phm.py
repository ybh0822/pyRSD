from . import HaloZeldovichBase, tools
from . import Cache, parameter, cached_property
from ... import pygcl, numpy as np

def default_parameters():
    """
    The default parameters
    """
    d = {}
    
    # A0 power law
    d['_A0_amp']   = 780.
    d['_A0_alpha'] = 1.57
    d['_A0_beta']  = 3.50
    d['_A0_run']   = 0.
    
    # R1 power law
    d['_R1_amp']   = 4.88
    d['_R1_alpha'] = -0.59
    d['_R1_beta']  = 0.12
    d['_R1_run']   = 0.
    
    # R1h power law
    d['_R1h_amp']   = 8.00
    d['_R1h_alpha'] = -0.92
    d['_R1h_beta']  = -0.36
    d['_R1h_run']   = 0.
    
    # R2h power law
    d['_R2h_amp']   = 2.92
    d['_R2h_alpha'] = -1.07
    d['_R2h_beta']  = -0.35
    d['_R2h_run']   = 0.
    
    # R power law
    d['_R_amp']   = 14.7
    d['_R_alpha'] = 0.22
    d['_R_beta']  = -0.18
    d['_R_run']   = 0
    
    return d
    

class HaloMatterBase(HaloZeldovichBase):
    """
    The halo-matter cross-correlation Phm, using HZPT
    """ 
    def __init__(self, zel, sigma8_z, enhance_wiggles=False):
        """
        Parameters
        ----------
        zel : ZeldovichP00 or ZeldovichCF
            the Zel'dovich power spectrum or correlation function instance 
        sigma8_z : float
            The desired sigma8 to compute the power at
        enhance_wiggles : bool, optional (`False`)
            using the Hy1 model from arXiv:1509.02120, enhance the wiggles
            of pure HZPT
        """   
        super(HaloMatterBase, self).__init__(zel, enhance_wiggles)
        self.sigma8_z = sigma8_z
        
        # set the defaults
        self.update(**default_parameters())
                
    #---------------------------------------------------------------------------
    # parameters
    #---------------------------------------------------------------------------
    @parameter
    def b1(self, val):
        """
        The linear bias
        """
        return val
    
    #---------------------------------------------------------------------------
    # A0 parameter
    #---------------------------------------------------------------------------
    @parameter
    def _A0_amp(self, val):
        return val
    
    @parameter
    def _A0_alpha(self, val):
        return val
    
    @parameter
    def _A0_beta(self, val):
        return val
    
    @parameter
    def _A0_run(self, val):
        return val
        
    #---------------------------------------------------------------------------
    # R parameter
    #---------------------------------------------------------------------------
    @parameter
    def _R_amp(self, val):
        return val
    
    @parameter
    def _R_alpha(self, val):
        return val
    
    @parameter
    def _R_beta(self, val):
        return val
    
    @parameter
    def _R_run(self, val):
        return val
        
    #---------------------------------------------------------------------------
    # R1 parameter
    #---------------------------------------------------------------------------
    @parameter
    def _R1_amp(self, val):
        return val
    
    @parameter
    def _R1_alpha(self, val):
        return val
    
    @parameter
    def _R1_beta(self, val):
        return val
    
    @parameter
    def _R1_run(self, val):
        return val
        
    #---------------------------------------------------------------------------
    # R1h parameter
    #---------------------------------------------------------------------------
    @parameter
    def _R1h_amp(self, val):
        return val
    
    @parameter
    def _R1h_alpha(self, val):
        return val
    
    @parameter
    def _R1h_beta(self, val):
        return val
    
    @parameter
    def _R1h_run(self, val):
        return val
        
    #---------------------------------------------------------------------------
    # R2h parameter
    #---------------------------------------------------------------------------
    @parameter
    def _R2h_amp(self, val):
        return val
    
    @parameter
    def _R2h_alpha(self, val):
        return val
    
    @parameter
    def _R2h_beta(self, val):
        return val
        
    @parameter
    def _R2h_run(self, val):
        return val
        
    #---------------------------------------------------------------------------
    # cached parameters
    #---------------------------------------------------------------------------
    @cached_property('sigma8_z', 'b1', '_A0_amp', '_A0_alpha', '_A0_beta', '_A0_run')
    def A0(self):
        """
        Returns the A0 radius parameter

        Note: the units are power [(h/Mpc)^3]
        """
        return self.__powerlaw__(self._A0_amp, self._A0_alpha, self._A0_beta, self._A0_run)
        
    @cached_property('sigma8_z', 'b1', '_R1_amp', '_R1_alpha', '_R1_beta', '_R1_run')
    def R1(self):
        """
        Returns the R1 radius parameter

        Note: the units are length [Mpc/h]
        """
        return self.__powerlaw__(self._R1_amp, self._R1_alpha, self._R1_beta, self._R1_run)
            
    @cached_property('sigma8_z', 'b1', '_R1h_amp', '_R1h_alpha', '_R1h_beta', '_R1h_run')
    def R1h(self):
        """
        Returns the R1h radius parameter

        Note: the units are length [Mpc/h]
        """
        return self.__powerlaw__(self._R1h_amp, self._R1h_alpha, self._R1h_beta, self._R1h_run)
    
    @cached_property('sigma8_z', 'b1', '_R2h_amp', '_R2h_alpha', '_R2h_beta', '_R2h_run')
    def R2h(self):
        """
        Returns the R2h radius parameter

        Note: the units are length [Mpc/h]
        """
        return self.__powerlaw__(self._R2h_amp, self._R2h_alpha, self._R2h_beta, self._R2h_run)
                
    @cached_property('sigma8_z', 'b1', '_R_amp', '_R_alpha', '_R_beta', '_R_run')
    def R(self):
        """
        Returns the R radius parameter

        Note: the units are length [Mpc/h]
        """
        return self.__powerlaw__(self._R_amp, self._R_alpha, self._R_beta, self._R_run)
              
    def __powerlaw__(self, A, alpha, beta, running):
        """
        Return a power law as a linear bias and sigma8(z) with the specified 
        parameters
        """
        return A * self.b1**(alpha+running*np.log(self.b1)) * (self.sigma8_z/0.8)**beta
        
        
class HaloZeldovichPhm(HaloMatterBase):
    """
    The halo-matter cross-correlation Phm, using HZPT
    """         
    @classmethod
    def from_cosmo(cls, cosmo, sigma8_z, enhance_wiggles=False):
        """
        Initialize from an existing zeldovich power spectrum
        """
        Pzel = pygcl.ZeldovichP00(cosmo, 0.)
        return cls(Pzel, sigma8_z, enhance_wiggles)
                
    def __call__(self, b1, k):
        """
        Return the total power, equal to the b1 * Zeldovich power + broadband 
        correction
        
        Parameters
        ----------
        b1 : float
            the linear bias to compute the bias at
        k : array_like
            the wavenumbers in `h/Mpc` to compute the power at
        """
        # make sure sigma8 is set properly
        if self.zeldovich.GetSigma8AtZ() != self.sigma8_z:
            self.zeldovich.SetSigma8AtZ(self.sigma8_z)
            
        self.b1 = b1
        return self.__broadband__(k) + b1*self.__zeldovich__(k) + b1*self.__wiggles__(k)
        
class HaloZeldovichCFhm(HaloMatterBase):
    """
    The dark matter - halo correlation function using Halo-Zel'dovich Perturbation Theory
    """ 
    @classmethod
    def from_cosmo(cls, cosmo, sigma8_z):
        """
        Initialize from an existing zeldovich power spectrum
        """
        zel = pygcl.ZeldovichPCF(cosmo, 0.)
        return cls(zel, sigma8_z, False)
                       
    def __broadband__(self, r):
        """
        The broadband power correction as given by Eq. 7 in arXiv:1501.07512.
        """
        A0, R, R1, R1h, R2h = self.A0, self.R, self.R1, self.R1h, self.R2h
        
        # define some values
        S = np.sqrt(R1h**4 - 4*R2h**4)
        norm = -A0*np.exp(-r/R) / (4*np.pi*r*R**2)
        A = R**2*(-2*R2h**4 + R1**2*(R1h**2-S)) + R2h**4*(R1h**2-S) + R1**2*(-R1h**4+2*R2h**4+R1h**2*S)
        A /= 2*R2h**4*S
        B = R2h**4*(R1h**2+S) - R1**2*(R1h**4-2*R2h**4+R1h**2*S) + R**2*(-2*R2h**4+R1**2*(R1h**2+S))
        B *= -1
        B /= 2*R2h**4*S
        
        num_term1 = 1. - (self.R1/self.R)**2
        num_term2 = A*np.exp(r*(1./self.R - (0.5*(self.R1h**2-S))**0.5/self.R2h**2))
        num_term3 = B*np.exp(r*(1./self.R - (0.5*(self.R1h**2+S))**0.5/self.R2h**2))
        denom = (1 - (R1h/R)**2 + (R2h/R)**4)
        
        return norm * (num_term1 + num_term2 + num_term3) / denom

    @tools.unpacked
    def __zeldovich__(self, r):
        """
        Return the Zel'dovich correlation at the specified `r`
        """
        return np.nan_to_num(self.zeldovich(r)) # set any NaNs to zero
            
    def __call__(self, b1, r):
        """
        Return the total correlation
        
        Parameters
        ----------
        b1 : float
            the linear bias to compute correlation at
        r : array_like
            the separations in `Mpc/h` to correlation at
        """
        self.b1 = b1
        return self.__broadband__(r) + b1*self.__zeldovich__(r)
