install.packages("pwr")
library(pwr)

# Define the functions that computes power of a design
calculate_power <- function(n_c, n_t, p_c, p_t, alpha) {
  
  total <- n_c + n_t
  #bal <- max(n_c, n_t) / min(n_c, n_t)
  #bal_str <- paste(toString(max(n_c, n_t) / min(n_c, n_t)), "1", sep = ":")
  #mde_abs <- abs(p_t - p_c)
  #mde_rel <- abs((p_t - p_c) / p_c)
  h <- abs(2 * asin(sqrt(p_c)) - 2 * asin(sqrt(p_t)))
  
  pow <- pwr.2p2n.test(h, n1 = n_c, n2 = n_t, sig.level = alpha)$power
  
  return(pow)
}

# Parameter ranges and step sizes
n_c_values <- c(seq(100, 1000, by = 50), 
                seq(1000, 5000, by = 100), 
                seq(5000, 25000, by = 500), 
                seq(25000, 50000, by = 1000))
imbalance <- c(1, 3, 5, 7, 9)
p_c_values <- seq(0.01, 0.50, by = 0.01)
p_t_values <- seq(0.01, 0.50, by = 0.01)
alpha_values <- c(0.01, 0.05, 0.10, 0.15, 0.20)

# Initialize empty list
results_list <- list()

# Nested loop to iterate over all combinations of parameters
for (n_c in n_c_values) {
  for (i in imbalance) {
    for (p_c in p_c_values) {
      for (p_t in p_t_values) {
        for (alpha in alpha_values) {
          
          # the size of the treatment group is a multiple of the control group
          n_t = n_c*i
          
          # Call the function to calculate power
          pow <- calculate_power(n_c, n_t, p_c, p_t, alpha)
          
          # Create a data frame with the results and input parameters
          result_entry <- data.frame(
            n_c = n_c,
            i = i,
            n_t = n_t,
            p_c = p_c,
            p_t = p_t,
            alpha = alpha,
            power = pow
          )
          
          # Append it to the result's list
          results_list[[length(results_list) + 1]] <- result_entry
          
        }
      }
    }
  }
}

# Combine all data frames
results <- do.call(rbind, results_list)

# Export the data frame to a CSV file
write.csv(results, "power_results_all.csv", row.names = TRUE)
