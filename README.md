# ASTRON İHA Masterclass — Sabit Kanatlı İHA Otonom Görev ve Telemetri Uygulaması

Bu depo; **PX4 SITL**, **Gazebo** ve **QGroundControl (QGC)** simülasyon ortamında sabit kanatlı bir İHA'nın (Fixed-Wing / `gz_rc_cessna`) kalkış (**Takeoff**), ara nokta takibi (**Waypoint**) ve süzülüş inişi (**Landing Pattern**) görevlerini **MAVSDK-Python** kullanarak otonom olarak gerçekleştiren kaynak kodları, teknik dokümantasyonu ve uçuş kaydını içerir.

---

## 🎥 Simülasyon Uçuş ve Canlı Telemetri Kaydı

Uçağın otomatik **ARM** edilmesini, pistten kalkışını, belirlenen ara noktalardan geçişini, piste süzülerek inişini ve terminaldeki anlık telemetri akışını içeren tam uçuş kaydı:

https://github.com/ebr8r/ASTRON-IHA-Masterclass/raw/main/ucus_kaydi.mp4

* ▶️ **Alternatif Bağlantı (Google Drive):** [Simülasyon Ekran Kaydını İzle](https://drive.google.com/file/d/10vMWy3ts2Qml6MocGK-i3M0e6rc8aPPz/view?usp=drive_link)

---

## 📁 Depo İçeriği ve Dosya Açıklamaları

| Dosya Adı | Açıklama |
| :--- | :--- |
| **`fixed_wing_mission.py`** | MAVSDK-Python kütüphanesi ile İHA'ya UDP (`14540`) üzerinden bağlanan, GPS ve uçuşa hazırlık kontrollerini yapan, aracı otonom olarak `ARM` edip QGroundControl üzerinden yüklenen görevi (`start_mission()`) başlatan ve uçuş boyunca anlık telemetri (uçuş modu, konum, irtifa, yer hızı) verilerini ekrana basan ana Python betiği. |
| **`teknik_rapor.md`** | Temel kavramsal soruların (PX4, SITL, Gazebo, QGC, MAVLink, MAVSDK, ROS 2) açıklamalarını, sistem mimarisini, görev planlama parametrelerini ve karşılaşılan teknik sorunların çözüm adımlarını içeren kapsamlı teknik rapor. |
| **`ucus_kaydi.mp4`** | Simülasyon ortamındaki kalkış, ara nokta takibi, piste süzülüş inişi ve canlı telemetri çıktısını gösteren uçuş kaydı. |
| **`README.md`** | Projenin genel tanıtımı, simülasyon uçuş videosu ve tüm dosyaların adım adım kurulum ve kullanım kılavuzu. |

---

## ⚙️ Gereksinimler ve Kurulum

Projeyi çalıştırmak için aşağıdaki ortam ve paketlerin kurulu olması gerekir:

* **İşletim Sistemi:** Ubuntu 22.04 LTS (veya uyumlu Linux dağıtımı)
* **Uçuş Kontrol Yazılımı ve Simülatör:** PX4-Autopilot (SITL) ve Gazebo (`gz_rc_cessna` sabit kanat modeli)
* **Yer Kontrol İstasyonu:** QGroundControl (QGC)
* **Python ve Kütüphane:** Python 3.10+ ve `mavsdk`

```bash
pip3 install mavsdk
pip3 install mavsdk

```bash
pip3 install mavsdk
