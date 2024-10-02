# Menginstall packages
install.packages("tidyverse")
install.packages("rmarkdown")

# Memuat library
library(tidyverse)
library(lubridate)
library(ggplot2)
library(dplyr)

setwd("D:/Naura/Belajar/Google Data Analytic/Belajar R/Cyclistic_Data_Analysis")

#=====MENYIAPKAN DATA (prepare)=====
## Mengumpulkan data
data_202401 <- read_csv("data/202401-divvy-tripdata.csv")
data_202402 <- read.csv("data/202402-divvy-tripdata.csv")
data_202403 <- read.csv("data/202403-divvy-tripdata.csv")
data_202404 <- read.csv("data/202404-divvy-tripdata.csv")
data_202405 <- read.csv("data/202405-divvy-tripdata.csv")
data_202406 <- read.csv("data/202406-divvy-tripdata.csv")
data_202407 <- read.csv("data/202407-divvy-tripdata.csv")
data_202408 <- read.csv("data/202408-divvy-tripdata.csv")

## Menggabungkan semua dataset menjadi satu dataset
### Melihat nama kolom setiap dataset
colnames(data_202401)
colnames(data_202402)
colnames(data_202403)
colnames(data_202404)
colnames(data_202405)
colnames(data_202406)
colnames(data_202407)
colnames(data_202408)

### Melihat tipe data setiap dataset
str(data_202401)
str(data_202402)
str(data_202403)
str(data_202404)
str(data_202405)
str(data_202406)
str(data_202407)
str(data_202408)

### Pada data_202401, kolom started_at dan ended_at bertipe datetime. Ubah menjadi chr.
data_202401 <- data_202401 %>%
  mutate(
    started_at = as.character(started_at),
    ended_at = as.character(ended_at)
  )
str(data_202401)

### Gabung semua dataset
all_data <- bind_rows(
  data_202401, data_202402, data_202403, data_202404, data_202405, data_202406, 
  data_202407, data_202408
  )
all_data <- distinct(all_data)
View(all_data)


#=====MEMROSES DATA (process)=====
## Melihat seluruh data secara sekilas
glimpse(all_data)

## Melihat statistik data
summary(all_data)

## Mengecek data null di setiap kolom
colSums(is.na(all_data))

## Mengecek kolom rideable_type
table(all_data$rideable_type)

## Mengecek kolom member_casual untuk memastikan hanya casual dan member
table(all_data$member_casual)

## Mengubah kolom started_at dan ended_at ke tipe datetime agar dapat dilakukan kalkulasi
all_data <- all_data %>%
  mutate(
    started_at = as_datetime(started_at),
    ended_at = as_datetime(ended_at)
  )

### Membuat kolom date(yyyy-mm-dd), day_of_week (hari), day (tanggal), month (bulan), dan year (tahun)
all_data$date <- format(as.Date(all_data$started_at))
all_data$day_of_week <- format(as.Date(all_data$started_at), "%A") #sunday, Monday, etc.
all_data$day <- format(as.Date(all_data$started_at), "%d")
all_data$month <- format(as.Date(all_data$started_at), "%m")
all_data$year <- format(as.Date(all_data$started_at), "%Y")

## Melakukan kalkulasi kolom started_at dengan ended_at untuk memuat lama waktu perjalanan (menit)
all_data$ride_length <- as.numeric(difftime(all_data$ended_at, all_data$started_at, units = "mins"))

View(all_data)

#=====DESCRIPTIVE ANALYSIS (analyze)=====
## Melakukan analisis deskriptif untuk kolom ride_length
summary_ride <- all_data %>%
  summarise(
    mean = mean(ride_length),
    median = median(ride_length),
    max = max(ride_length),
    min = min(ride_length)
  )
summary_ride

### Filter ride_length yang kurang dari 0
all_data <- all_data %>%
  filter(ride_length >= 0)
min(all_data$ride_length)

## Melakukan analisis untuk mengetahui perbandingan banyak pengguna dan lama perjalanan
summary_user <- all_data %>%
  group_by(member_casual) %>%
  summarise(count = n(), # banyak pengguna
            mean_ride_length = mean(ride_length)) %>% 
  mutate(percentage = count / sum(count) * 100) # presentase pengguna
summary_user

## Mengelompokkan tipe sepeda yang digunakan pengendara
summary_rideable_type <- all_data %>%
  group_by(member_casual, rideable_type) %>%
  summarize(count = n(), 
            mean_ride_length = mean(ride_length),
            .groups = "keep",)
summary_rideable_type

## Melakukan analisis untuk melihat rata-rata ride_length per hari untuk pengendara
aggregate(all_data$ride_length ~ all_data$member_casual + all_data$day_of_week, FUN = mean)

### Mengurutkan nama hari 
all_data$day_of_week <- ordered(all_data$day_of_week, levels=c("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))

### Cek lagi untuk rata-rata ride_legth per hari untuk pengendara setelah mengurutkan hari
aggregate(all_data$ride_length ~ all_data$member_casual + all_data$day_of_week, FUN = mean)

## Menganalisis perjalanan berdasarkan pengguna dan hari
summary_data <- all_data %>% 
  group_by(member_casual, day_of_week) %>%  
  summarise(number_of_rides = n(),  #jumlah baris di setiap group
            average_duration = mean(ride_length),
            .groups = "keep") %>%
  arrange(member_casual, day_of_week)
summary_data

#=====VISUALISASI DATA (share)=====
# Membuat pie chart untuk melihat jumlah perjalanan yang dilakukan pengendara
summary_user %>% 
  ggplot(aes(x = "", y = count, fill = member_casual)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar(theta = "y") +
  labs(title = "Jumlah Perjalanan Pengendara Biasa (Casual) vs Anggota (Member)",
       subtitle = "Data Januari sampai Agustus 2024",
       fill = "Tipe Pengguna") +
  scale_fill_manual(values = c("member" = "#1f77b4", "casual" = "#ff7f0e")) +
  theme_void() +
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, size = 12, face = "italic", margin = margin(t = 5, b = 5)),
        legend.position = "top") +
  geom_text(aes(label = paste0(count, " (", round(percentage, 1), "%)")), 
            position = position_stack(vjust = 0.5))
ggsave(filename = "Jumlah Pengguna Biasa vs Anggota.png", width = 8, height = 6, dpi = 300)

# Membuat bar chart untuk rata-rata durasi perjalanan pengguna berdasarkan jenis sepeda
summary_rideable_type %>% 
  ggplot(aes(x = rideable_type, y = mean_ride_length, fill = member_casual)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Rata-rata Durasi Perjalanan Pengendara",
       subtitle = "Berdasarkan Jenis Sepeda yang Digunakan",
       x = "Jenis Sepeda",
       y = "Rata-rata Durasi Perjalanan (menit)") +
  scale_fill_manual(values = c("member" = "#1f77b4", "casual" = "#ff7f0e")) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, size = 12, face = "italic"),
        axis.title.x = element_text(size = 12, face = "bold"),
        axis.title.y = element_text(size = 12, face = "bold")) +
  geom_text(aes(label = round(mean_ride_length, 1)), 
            position = position_dodge(width = 0.9), 
            vjust = -0.5, 
            size = 3)
ggsave(filename = "Rata-rata durasi perjalanan.png", width = 8, height = 6, dpi = 300)

# Membuat bar chart untuk banyak perjalanan yang dilakukan pengendara
summary_data  %>% 
  ggplot(aes(x = day_of_week, y = number_of_rides, fill = member_casual)) +
  geom_col(position = "dodge") +
  labs(title = "Jumlah Perjalanan yang Dilakukan Pengendara",
       subtitle = "per Hari dari Bulan Januari sampai Agustus 2024",
       x = "Hari",
       y = "Banyak Perjalanan",
       fill = "Tipe Pengguna") +
  scale_fill_manual(values = c("member" = "#1f77b4", "casual" = "#ff7f0e")) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, size = 12, face = "italic"),
        axis.title.x = element_text(size = 12, face = "bold"),
        axis.title.y = element_text(size = 12, face = "bold"),
        legend.position = "top") +
  geom_text(aes(label = number_of_rides), 
            position = position_dodge(width = 0.9), 
            vjust = -0.5,
            size = 3)
ggsave(filename = "Banyak Perjalanan pengedara.png", width = 8, height = 6, dpi = 300)

# Membuat bar chart untuk rata-rata durasi perjalanan pengendara
summary_data %>% 
  ggplot(aes(x = day_of_week, y = average_duration, fill = member_casual)) +
  geom_col(position = "dodge") +
  labs(title = "Distribusi Rata-rata Durasi Perjalanan Pengendara",
       subtitle = "per Hari dari Bulan Januari sampai Agustus 2024",
       x = "Hari",
       y = "Rata-rata Durasi Perjalanan (menit)",
       fill = "Rider Type") +
  scale_fill_manual(values = c("member" = "#1f77b4", "casual" = "#ff7f0e")) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5, size = 12, face = "italic"),
        axis.title.x = element_text(size = 12, face = "bold"),
        axis.title.y = element_text(size = 12, face = "bold"),
        legend.position = "top") +
  geom_text(aes(label = round(average_duration, 1)), 
            position = position_dodge(width = 0.9), 
            vjust = -0.5, 
            size = 3)
ggsave(filename = "Rata-rata durasi perjalan per hari.png", width = 8, height = 6, dpi = 300)
