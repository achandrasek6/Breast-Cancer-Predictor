### Breast Cancer Project ###

# Calling packages
library(tidyverse)

# Importing raw count file
sample_data <- read.delim(file.choose(), header = TRUE, sep = "\t", stringsAsFactors = FALSE)
colnames(sample_data)

# Fixing sample names
colnames(sample_data)[-1] <- gsub("^X", "", colnames(sample_data)[-1])

## Transposing data

# Step 1: Set gene_id as the row names and remove the gene_id column
rownames(sample_data) <- sample_data$gene_id
sample_data <- sample_data[, -1]

# Step 2: Transpose the data frame
sample_data_transposed <- as.data.frame(t(sample_data))

# Step 3: Create a new column "sample name" from the row names (which are the original sample names)
sample_data_transposed <- cbind("sample_name" = rownames(sample_data_transposed), sample_data_transposed)

# Step 4: Remove row names
rownames(sample_data_transposed) <- NULL

# Inspect the first few rows of the transposed data frame
View(sample_data_transposed)

## Create data frame for sample_name vs tumor_status

# Define the sample names (after removing the "X")
sample_names <- c("3_620", "7_624", "9_626", "11_628", "4_621", "8_625", "10_627", "12_629", "16_635")

# Define the tumor status for each sample.
# Here, the first 4 samples are "Normal" and the remaining 5 are "Tumor"
tumor_status <- c(rep("Normal", 4), rep("Tumor", 5))

# Create a data frame with the two columns: sample_name and tumor_status
metadata <- data.frame(sample_name = sample_names, tumor_status = tumor_status, stringsAsFactors = FALSE)

# View the new table
View(metadata)

## Joining both tables together to include tumor_status with data
complete_data <- left_join(sample_data_transposed, metadata, by = "sample_name")

# Making tumor_data show up first
complete_data <- complete_data %>% select(sample_name, tumor_status, everything())

# Removing ensembl id from gene name for readability
colnames(complete_data)[3:ncol(complete_data)] <- sub(".*_", "", colnames(complete_data)[3:ncol(complete_data)])

# Check if any row names are duplicated
all_unique <- length(rownames(sample_data)) == length(unique(rownames(sample_data)))
all_unique

# Save data 
write.table(cleaned_data, 
            file = "C:/Users/funny/OneDrive/Documents/Breast_Cancer_Project/cleaned_data.txt", # *** CREATE A PATH IN YOUR MACHINE FOR THIS ***
            sep = "\t", 
            row.names = FALSE, 
            quote = FALSE)



