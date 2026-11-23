# ASTRON İHA Masterclass — Sabit Kanatlı İHA Otonom Görev ve Telemetri Uygulaması


Bu depo; **PX4 SITL**, **Gazebo** ve **QGroundControl (QGC)** simülasyon ortamında sabit kanatlı bir İHA'nın (Fixed-Wing / `gz_rc_cessna`) kalkış (**Takeoff**), ara nokta takibi (**Waypoint**) ve süzülüş inişi (**Landing Pattern**) görevlerini **MAVSDK-Python** kullanarak otonom olarak gerçekleştiren kaynak kodları, teknik dokümantasyonu ve uçuş kaydını içerir.

---

##  Simülasyon Uçuş ve Canlı Telemetri Kaydı

Uçağın otomatik **ARM** edilmesini, pistten kalkışını, belirlenen ara noktalardan geçişini, piste süzülerek inişini ve terminaldeki anlık telemetri akışını içeren tam uçuş kaydı:


https://github.com/user-attachments/assets/be182e40-48ae-4d47-81ae-27502f866f19




* **Alternatif Bağlantı (Google Drive):** [Simülasyon Ekran Kaydını İzle](https://drive.google.com/file/d/10vMWy3ts2Qml6MocGK-i3M0e6rc8aPPz/view?usp=drive_link)

---

## Depo İçeriği ve Dosya Açıklamaları

| Dosya Adı | Açıklama |
| :--- | :--- |
| **`fixed_wing_mission.py`** | MAVSDK-Python kütüphanesi ile İHA'ya UDP (`14540`) üzerinden bağlanan, GPS/ARM sağlık kontrollerini yapan, QGroundControl üzerinden yüklenen görevi doğrulayıp başlatan (`start_mission()`) ve uçuş boyunca canlı telemetri (ARM durumu, uçuş modu, konum, irtifa, yer hızı) verilerini ekrana basan ana Python betiği. |
| **`teknik_rapor.md`** | 1. Aşama teorik kavramların (PX4, SITL, Gazebo, QGC, MAVLink, MAVSDK, ROS 2) açıklamalarını, sistem mimarisini, kodun çalışma mantığını ve karşılaşılan teknik sorunların çözümlerini içeren kısa teknik rapor. |
| **`requirements.txt`** | Projenin çalışması için gereken Python kütüphane bağımlılıklarını (`mavsdk`) içeren kurulum dosyası. |
| **`ucus_kaydi.mp4`** | Simülasyon ortamındaki kalkış, ara nokta takibi, piste süzülüş inişi ve canlı telemetri çıktısını gösteren uçuş kaydı. |
| **`README.md`** | Projenin genel tanıtımı, simülasyon uçuş videosu ve adım adım kurulum/kullanım kılavuzu. |

---

## Gereksinimler ve Kurulum

Projeyi çalıştırmak için aşağıdaki ortam ve paketlerin kurulu olması gerekir:

* **İşletim Sistemi:** Ubuntu 22.04 LTS (veya uyumlu Linux dağıtımı)
* **Uçuş Kontrol Yazılımı ve Simülatör:** PX4-Autopilot (SITL) ve Gazebo (`gz_rc_cessna` sabit kanat modeli)
* **Yer Kontrol İstasyonu:** QGroundControl (QGC)
* **Python ve Bağımlılıklar:** Python 3.10+ ve `mavsdk`
* **Kurulum Komutu:** `pip3 install -r requirements.txt`

---

## Adım Adım Kullanım Kılavuzu

Sistemi çalıştırmak ve otonom görevi yürütmek için aşağıdaki adımları sırasıyla uygulayın:

### 1. PX4 SITL ve Gazebo Simülasyonunu Başlatma
Terminalde `PX4-Autopilot` dizinine giderek sabit kanatlı Cessna modelini başlatın:
* `cd ~/PX4-Autopilot`
* `make px4_sitl gz_rc_cessna`

Simülasyon açılıp `INFO [commander] Ready for takeoff!` mesajı göründüğünde, iniş yaklaşmasında arazi yüksekliği kestirimi kaynaklı beklemeleri önlemek için PX4 konsoluna (`pxh>`) şu parametreyi girin:
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
2. Küresel konum (GPS), ev konumu (Home Position) ve ARM edilebilirlik kontrollerini bekler.
3. QGroundControl ile yüklenen görevi doğrular, aracı **ARM** eder ve otonom görevi başlatır.
4. Kalkış, waypoint geçişleri ve piste teker koyma (iniş) tamamlanana kadar terminalde canlı telemetri verilerini raporlar.
