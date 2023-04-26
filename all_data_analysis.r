library(tidyverse)
library(readr)
library(GGally)
library(FactoMineR)

# file <- "draco6_data.csv"
file <- "draco12_data.csv"

df <- read_csv(file)

df <- df[2:ncol(df)]

df$detected <- factor(df$trk_rate > 0.0)
# # cor(df$trk_rate, df$mean_mean_err)
# df$trk_rate <- factor(df$trk_rate)

# cor(df$trk_rate, df$mean_mean_err)

df <- df |> 
    group_by(trk_rate) |> 
    filter(length(trk_rate) > 10) |>
    ungroup()

df |>
    ggplot(aes(trk_rate)) +
    geom_histogram()
    
# df$trk_rate <- factor(df$trk_rate)
# ggpairs(df)

df_cr <- scale(df[2:(ncol(df) - 1)])
# df_cr <- scale(df[1:(ncol(df) - 1)])

library(cluster)
library(ClusterR)

kmeans_res <- kmeans(df_cr, centers = 2, nstart = 1000)

# kmeans_res$cluster
# pca <- PCA(df_cr)

# plot(pca)
# cm <- table(df$detected, kmeans_res$cluster)


# =============== hc ==================
dist_mat <- dist(df_cr)
hc <- hclust(dist_mat)
plot(hc)

hc_cut <- cutree(hc, k = 2)
# cm_hc <- table(df$detected, hc_cut)

# cm
# cm_hc

library(caret)

predicted_k <- factor(kmeans_res$cluster)
predicted_hc <- factor(hc_cut)


if (predicted_hc[1] == 2) {
    levels(predicted_hc) <- c("FALSE", "TRUE")
} else {
    levels(predicted_hc) <- c("TRUE", "FALSE")
}


if (predicted_k[1] == 2) {
    levels(predicted_k) <- c("FALSE", "TRUE")
} else {
    levels(predicted_k) <- c("TRUE", "FALSE")
}

actual <- df$detected

predicted_k[1:20]
actual[1:20]

cm_k <- confusionMatrix(predicted_k, actual)
cm_hc <- confusionMatrix(predicted_hc, actual)


library(MASS)

predictor_vars = df[2:(ncol(df) - 1)]

lda_fit <- lda(predictor_vars, df$detected)

predictions_lda <- predict(lda_fit, predictor_vars)
predictions_lda <- predictions_lda$class

cm_lda <- confusionMatrix(predictions_lda, actual)

cm_k
cm_hc
cm_lda