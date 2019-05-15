def random_sample_2d(mu, sigma):
    """
    Randomly sample point from a normal distribution.
    
    Parameters
    --------------------
        mu    -- numpy array of shape (2,), mean along each dimension
        sigma -- numpy array of shape (2,), standard deviation along each dimension
    
    Returns
    --------------------
        point -- numpy array of shape (2,), sampled point
    """
    
    x = np.random.normal(mu[0], sigma[0])
    y = np.random.normal(mu[1], sigma[1])
    return np.array([x,y])

def generate_points_2d(N, seed=1234) :
    """
    Generate toy dataset of 3 clusters each with N points.
    
    Parameters
    --------------------
        N      -- int, number of points to generate per cluster
        seed   -- random seed
    
    Returns
    --------------------
    """
    np.random.seed(seed)
    
    mu = [[0,0.5], [1,1], [2,0.5]]
    sigma = [[0.1,0.1], [0.25,0.25], [0.15,0.15]]
    
    label = 0
    points = []
    for m,s in zip(mu, sigma) :
        label += 1
        for i in xrange(N) :
            x = random_sample_2d(m, s)
            points.append(x)
    return points