from . import numdifftools, numpy as np
from pyRSD.rsd.power.qso.derivatives import dPqso_dsigma8_z

NMU = 41

def test_partial(driver):

    model = driver.theory.model

    # get the deriv arguments
    k    = driver.data.combined_k
    mu = np.linspace(0., 1., NMU)

    # get the deriv arguments
    k    = driver.data.combined_k
    mu = np.linspace(0., 1., NMU)

    # broadcast to the right shape
    k     = k[:, np.newaxis]
    mu    = mu[np.newaxis, :]
    k, mu = np.broadcast_arrays(k, mu)
    k     = k.ravel(order='F')
    mu    = mu.ravel(order='F')

    pars = driver.theory.fit_params
    args = (model, pars, k, mu)

    # our derivative
    x = dPqso_dsigma8_z.eval(*args)

    # numerical derivative
    def f(x):
        model.sigma8_z = x
        return driver.theory.model.power(k, mu)
    g = numdifftools.Derivative(f, step=1e-3)
    y = g(model.sigma8_z)

    # compare
    np.testing.assert_allclose(x, y, rtol=1e-2)
