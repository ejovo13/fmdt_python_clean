library(tidyverse)
library(readr)
library(GGally)

file <- "data_Draconids-6mm1.30-2050-173800.csv"

df <- read_csv(file)

df <- df[2:ncol(df)]

df |> ggplot(aes(trk_rate)) + geom_histogram()


df$detected <- factor(df$trk_rate > 0.0)

cor(df$trk_rate, df$mean_mean_err)
# cor(df$trk_rate, df$mean_mean_err)

ggpairs(df)