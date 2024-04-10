# A power calculator for imbalanced experiments

<img src="imbalanced.png" alt="Project Logo or Image" width="100">

This is a statistical power calculator designed for experiments that do not allocate their treatment to equally sized groups. It utilizes the [pwr.2p2n.test](https://www.rdocumentation.org/packages/pwr/versions/1.3-0/topics/pwr.2p2n.test) function from the R [pwr](https://cran.r-project.org/web/packages/pwr/) package. Here's the link to the public web app deployed on Streamlit Community Cloud:

https://ggiannarakis-imbalanced-power-calc-main-k5d1d9.streamlit.app/

## Documentation

### Inputs

#### 1. Control Group Size

The size of the control group in your experiment. It represents the number of subjects or units in the control group.

- **Values:** Positive integer ranging from 100 to 50000.
- **Example:** 150, 2200, 50000.

#### 2. Imbalance

Imbalance is a multiplier that determines the size of the treatment group relative to the control group.

- **Values:** Choose from x1, x3, x5, x7, x9.
- **Example:** x5 indicates a treatment group size five times that of the control group.

#### 3. Control Group Conversion Rate

The probability of success in the control group.

- **Values:** Multiples of 0.01, smaller than 0.5.
- **Example:** 0.01, 0.22, 0.5

#### 4. Treatment Group Conversion Rate

The probability of success in the treatment group.

- **Values:** Multiples of 0.01, smaller than 0.5.
- **Example:** 0.01, 0.22, 0.5

#### 5. Significance Level alpha

The significance level (alpha) determines the probability of rejecting a true null hypothesis.

- **Values:** Choose from 0.01, 0.05, 0.10, 0.15, 0.20.
- **Example:** 0.05 indicates a 5% significance level.

### Output

#### 1. Statistical power

Percent of the time the minimum effect size will be detected, assuming it exists!