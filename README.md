# ASTRON İHA Masterclass — Sabit Kanatlı İHA Otonom Görev ve Telemetri Uygulaması

Bu depo; **PX4 SITL**, **Gazebo** ve **QGroundControl (QGC)** simülasyon ortamında sabit kanatlı bir İHA'nın (Fixed-Wing / `gz_rc_cessna`) kalkış (**Takeoff**), ara nokta takibi (**Waypoint**) ve süzülüş inişi (**Landing Pattern**) görevlerini **MAVSDK-Python** kullanarak otonom olarak gerçekleştiren kaynak kodları, teknik dokümantasyonu ve uçuş kaydını içerir.

---

## Simülasyon Uçuş ve Canlı Telemetri Kaydı

Uçağın otomatik **ARM** edilmesini, pistten kalkışını, belirlenen ara noktalardan geçişini, piste süzülerek inişini ve terminaldeki anlık telemetri akışını içeren tam uçuş kaydı:

https://github.com/ebr8r/ASTRON-IHA-Masterclass/raw/main/ucus_kaydi.mp4

* **Alternatif Bağlantı (Google Drive):** [Simülasyon Ekran Kaydını İzle](https://drive.google.com/file/d/10vMWy3ts2Qml6MocGK-i3M0e6rc8aPPz/view?usp=drive_link)

---

## Depo İçeriği ve Dosya Açıklamaları

| Dosya Adı | Açıklama |
| :--- | :--- |
| **`fixed_wing_mission.py`** | MAVSDK-Python kütüphanesi ile İHA'ya UDP (`14540`) üzerinden bağlanan, GPS ve uçuşa hazırlık kontrollerini yapan, aracı otonom olarak `ARM` edip QGroundControl üzerinden yüklenen görevi (`start_mission()`) başlatan ve uçuş boyunca anlık telemetri (uçuş modu, konum, irtifa, yer hızı) verilerini ekrana basan ana Python betiği. |
| **`teknik_rapor.md`** | Temel kavramsal soruların (PX4, SITL, Gazebo, QGC, MAVLink, MAVSDK, ROS 2) açıklamalarını, sistem mimarisini, görev planlama parametrelerini ve karşılaşılan teknik sorunların çözüm adımlarını içeren kapsamlı teknik rapor. |
| **`ucus_kaydi.mp4`** | Simülasyon ortamındaki kalkış, ara nokta takibi, piste süzülüş inişi ve canlı telemetri çıktısını gösteren uçuş kaydı. |
| **`README.md`** | Projenin genel tanıtımı, simülasyon uçuş videosu ve tüm dosyaların adım adım kurulum ve kullanım kılavuzu. |

---

## Gereksinimler ve Kurulum

Projeyi çalıştırmak için aşağıdaki ortam ve paketlerin kurulu olması gerekir:

* **İşletim Sistemi:** Ubuntu 22.04 LTS (veya uyumlu Linux dağıtımı)
* **Uçuş Kontrol Yazılımı ve Simülatör:** PX4-Autopilot (SITL) ve Gazebo (`gz_rc_cessna` sabit kanat modeli)
* **Yer Kontrol İstasyonu:** QGroundControl (QGC)
* **Python ve Kütüphane:** Python 3.10+ ve `mavsdk`
* **Kurulum Komutu:** `pip3 install mavsdk`

---

## Adım Adım Kullanım Kılavuzu

Sistemi çalıştırmak ve otonom görevi yürütmek için aşağıdaki adımları sırasıyla uygulayın:

### 1. PX4 SITL ve Gazebo Simülasyonunu Başlatma
Terminalde `PX4-Autopilot` dizinine giderek sabit kanatlı Cessna modelini başlatın:
* `cd ~/PX4-Autopilot`
* `make px4_sitl gz_rc_cessna`

Simülasyon açılıp `INFO [commander] Ready for takeoff!` mesajı göründüğünde, iniş sırasında arazi kaynaklı beklemeleri önlemek için PX4 konsoluna (`pxh>`) şu parametreyi girin:
* `param set FW_LND_USETER 0`

### 2. QGroundControl Üzerinden Görev Rotası Oluşturma ve Yükleme
1. **QGroundControl** uygulamasını açın (simülasyon ile otomatik bağlantı kurulacaktır).
2. Sol üst menüden **Plan** sekmesine geçin ve harita üzerinde sırasıyla şu görev noktalarını oluşturun:
   * **Takeoff:** Pist doğrultusunda kalkış ve tırmanış noktası (ör. 50 m irtifa).
   * **Waypoint:** Seyir güzergâhı ara noktaları.
   * **Pattern → Landing Pattern:** Piste hizalı süzülüş ve iniş hattı *(doğrudan süzülüş için sağ panelden `Use loiter to altitude` seçeneği kapalı tutulur)*.
3. Sağ üstteki **Upload** butonuna basarak görevi İHA'ya yükleyin (`Done` durumuna geçtiğini doğrulayın) ve **Fly** ekranına dönün.

### 3. Otonom Uçuş Betiğini (`fixed_wing_mission.py`) Çalıştırma
Yeni bir terminal sekmesinde proje klasörüne gidin ve Python betiğini çalıştırın:
* `python3 fixed_wing_mission.py`

**Betik Çalıştırıldığında Gerçekleşen İşlemler:**
1. `udp://:14540` portu üzerinden PX4 otopilotuna bağlanır.
2. Küresel konum (GPS) ve ev konumu (Home Position) kilitlenene kadar sağlık kontrollerini bekler.
3. Aracı otomatik olarak **ARM** eder ve QGroundControl ile yüklenen görevi başlatır.
4. Kalkış, waypoint geçişleri ve piste teker koyma (iniş) tamamlanana kadar terminalde canlı telemetri verilerini raporlar.
pip3 install mavsdk

```bash
pip3 install mavsdk
