# Teknik Rapor — Sabit Kanatlı İHA Otonom Görev ve Telemetri Sistemi

## 1. Teorik Kavramlar (1. Aşama)

* **PX4:** İHA ve insansız sistemler için geliştirilmiş açık kaynaklı uçuş kontrol yazılımıdır (autopilot). Sensör verilerini işleyerek durum kestirimi yapar ve kontrol yüzeylerine (aileron, elevator, rudder, gaz) komut üretir.
* **SITL (Software-In-The-Loop):** Fiziksel uçuş kontrol kartına ihtiyaç duymadan PX4 yazılımının doğrudan bilgisayar işlemcisi üzerinde derlenip çalıştırılmasını sağlayan yazılım tabanlı simülasyon yöntemidir.
* **Gazebo:** Aerodinamik kuvvetleri, yerçekimini, rüzgârı ve sensör (GPS, IMU, barometre) gürültülerini fizik motoruyla modelleyen 3B robotik simülasyon ortamıdır. Bu projede sabit kanatlı `gz_rc_cessna` modeli kullanılmıştır.
* **QGroundControl (QGC):** PX4 ile haberleşen yer kontrol istasyonu (GCS) yazılımıdır. Uçuş öncesi parametre ayarları, harita üzerinde görev rotası (Takeoff, Waypoint, Landing) planlama ve canlı telemetri takibi için kullanılır.
* **MAVLink:** Otopilot, yer kontrol istasyonu ve görev bilgisayarı arasında düşük gecikmeli veri paketi alışverişi sağlayan hafif haberleşme protokolüdür.
* **MAVSDK:** MAVLink protokolünü doğrudan paket seviyesinde kodlama zorunluluğunu ortadan kaldıran; Python, C++ gibi dillerle yüksek seviyeli asenkron uçuş komutları (`arm()`, `start_mission()`, telemetri akışları) yazmayı sağlayan yazılım geliştirme kitidir.
* **ROS 2 ve PX4 Birlikteliği:** PX4 içindeki **uXRCE-DDS** istemcisi ile bilgisayarda çalışan **Micro XRCE-DDS Agent** üzerinden köprü kurulur. Bu sayede PX4'ün dahili uORB mesajları doğrudan ROS 2 topic'leri olarak yayınlanır ve görüntü işleme veya yüksek seviyeli otonomi düğümleri PX4 ile gerçek zamanlı haberleşir.

---

## 2. Sistem Mimarisi ve Çalışma Mantığı

Sistem dört parçadan oluşur:
1. **Gazebo:** Sabit kanatlı uçağın (`gz_rc_cessna`) fiziğini ve sanal sensörlerini üretir.
2. **PX4 SITL:** Gazebo'dan gelen sensör verileriyle uçağı kontrol eden otopilot yazılımıdır.
3. **QGroundControl:** Harita üzerinde Takeoff, Waypoint ve Landing Pattern görevlerini oluşturup PX4'e yükler (Upload).
4. **Python + MAVSDK betiği:** MAVLink üzerinden UDP `14540` portuyla PX4'e bağlanır; rotayı oluşturmaz, yüklü görevi kontrol eder, aracı ARM eder, mission'ı başlatır ve uçuşu izler.

### Betiğin Akışı
1. PX4'e bağlan ve bağlantıyı bekle.
2. GPS ve Home konumu hazır olana kadar sağlık kontrolünü bekle.
3. QGC'den yüklenen mission'ı indirip (`download_mission()`) boş olup olmadığını kontrol et.
4. Aracı ARM et.
5. `start_mission()` ile otonom görevi başlat.
6. `mission_progress()` ile tamamlanan nokta sayısını izle.
7. `in_air()` `False` olunca iniş tamamlanmış sayılır.
8. Uçuş boyunca ayrı bir asenkron görev konum, irtifa, yer hızı ve uçuş modunu her saniye terminale yazar.

### Görev Parametreleri
* **Takeoff ve Seyir Rotası:** QGroundControl üzerinden pist doğrultusunda **50 m** kalkış irtifası (Takeoff), ardından seyir ara noktaları (Waypoint) tanımlanmıştır.
* **Landing Pattern ve `FW_LND_USETER 0`:** Piste doğrudan süzülüş inişi yapılabilmesi için Landing Pattern ayarında irtifa bekleme döngüsü (`Use loiter to altitude`) kapatılmış; ayrıca son yaklaşmada arazi verisi kaynaklı irtifa beklemesini önlemek amacıyla PX4 konsolundan `param set FW_LND_USETER 0` parametresi tanımlanmıştır.

### Karşılaşılan Sorunlar ve Çözümler
* **İniş Yaklaşmasında İrtifa Beklemesi:** Sabit kanatlı İHA `Landing Pattern` aşamasına geçtiğinde arazi yükseklik verisini beklediği için inişi tamamlamakta gecikmiştir. `FW_LND_USETER` parametresi `0` yapılarak göreli/barometrik irtifa üzerinden doğrudan piste süzülüş inişi sağlanmıştır.
* **Kütüphane İçe Aktarma Farklılığı:** Ortam kurulumuna bağlı olarak `mavsdk` ve `mavsdk_grpc` modül adları arasında oluşabilecek uyumsuzluğu gidermek için kodun başına `try/except ImportError` kontrolü eklenmiştir.
