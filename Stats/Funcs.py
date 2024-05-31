

def P(rv:"RV", c):
    return rv.pdf(c)

def E(rv:"RV|Sample"):
    return rv.expectation

def recognize(data):
    distributions = [sci.norm, sci.expon, sci.uniform]

    # Perform the KS test for each distribution
    for dist in distributions:
        # Fit the distribution parameters to the data
        params = dist.fit(data)
        
        # Perform the KS test
        D, p_value = sci.kstest(data, dist.name, args=params)

__all__ = ["P", "E", "recognize"]
