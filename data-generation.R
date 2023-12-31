install.packages("pwr")
library(pwr)

n_c = 5000
n_t = 5000
total = n_c + n_t
bal = max(n_c, n_t) / min(n_c, n_t)
bal_str = paste(toString(max(n_c, n_t) / min(n_c, n_t)), "1", sep =":")
p_c = 0.15
p_t = 0.16
mde_abs = abs(p_t - p_c)
mde_rel = abs((p_t - p_c) / p_c)
h = abs(2*asin(sqrt(p_c))-2*asin(sqrt(p_t)))
alpha = 0.10
pow = pwr.2p2n.test(h, n1=n_c, n2=n_t, sig.level=alpha)$power

calculate_power <- function(n_c, n_t, p_c, p_t, alpha) {
  total <- n_c + n_t
  bal <- max(n_c, n_t) / min(n_c, n_t)
  bal_str <- paste(toString(max(n_c, n_t) / min(n_c, n_t)), "1", sep = ":")
  mde_abs <- abs(p_t - p_c)
  mde_rel <- abs((p_t - p_c) / p_c)
  h <- abs(2 * asin(sqrt(p_c)) - 2 * asin(sqrt(p_t)))
  
  pow <- pwr.2p2n.test(h, n1 = n_c, n2 = n_t, sig.level = alpha)$power
  
  return(pow)
}

# Create an empty data frame to store the results
results_df <- data.frame()

# Define the range of values for each parameter
n_c_values <- c(500, 1000, 2000)
n_t_values <- c(500, 1000, 2000)
p_c_values <- c(0.1, 0.2, 0.3)
p_t_values <- c(0.15, 0.25, 0.35)
alpha_values <- c(0.05, 0.1, 0.15)

# Nested loop to iterate over all combinations of parameters
for (n_c in n_c_values) {
  for (n_t in n_t_values) {
    for (p_c in p_c_values) {
      for (p_t in p_t_values) {
        for (alpha in alpha_values) {
          # Call the function to calculate power
          pow <- calculate_power(n_c, n_t, p_c, p_t, alpha)
          
          # Create a data frame with the results and input parameters
          result_entry <- data.frame(
            n_c = n_c,
            n_t = n_t,
            p_c = p_c,
            p_t = p_t,
            alpha = alpha,
            power = pow
          )
          
          # Append the result to the main data frame
          results_df <- rbind(results_df, result_entry)
        }
      }
    }
  }
}

# Export the data frame to a CSV file
write.csv(results_df, "power_results.csv", row.names = TRUE)