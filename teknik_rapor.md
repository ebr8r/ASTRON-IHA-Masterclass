# ASTRON – İHA Masterclass ve Sabit Kanat Otonom Görev Teknik Raporu


## PX4, SITL ve Gazebo nedir? 
PX4: İHA'nın "beyni" olan açık kaynaklı otopilot yazılımıdır. Sensörlerden (GPS, ivmeölçer, jiroskop) gelen verileri işler ve motorlara/kontrol yüzeylerine ne kadar güç vereceğine karar vererek uçağın dengede kalmasını ve rota izlemesini sağlar.

SITL (Software In The Loop): Gerçek bir uçuş kontrol kartı (Pixhawk vb.) olmadan, PX4 otopilot yazılımını doğrudan kendi bilgisayarımızdaki işlemci üzerinde sanki gerçek bir donanımmış gibi çalıştırmamızı sağlayan test ortamıdır. Kırım riski olmadan kod denememize yarar.

Gazebo: İHA'nın içinde uçtuğu 3 boyutlu fizik ve simülasyon dünyasıdır. Yerçekimi, rüzgar, hava direnci ve sensör verilerini (kamera, GPS) sanal olarak üretir; PX4 ise bu sanal sensör verilerini okuyup uçağı Gazebo dünyasında hareket ettirir.

## QGroundControl ne işe yarar? 
QGroundControl, yerdeki operatör ile havadaki (veya simülasyondaki) İHA arasındaki köprüyü kuran yer kontrol istasyonu (GCS) yazılımıdır.

Harita üzerinde kalkış (Takeoff), ara nokta (Waypoint) ve iniş (Landing) içeren otonom uçuş rotaları planlayıp İHA'ya yüklememizi sağlar.

Uçuş sırasında İHA'nın anlık konumunu, hızını, irtifasını ve batarya durumunu harita üzerinden canlı takip etmemize yarar.

Kalibrasyon, uçuş modu değiştirme ve acil durum (Eve Dön / RTL) komutlarını yönetir.

## MAVLink ve MAVSDK nedir? 
MAVLink: İHA sistemlerinin "ortak konuşma dilidir" (haberleşme protokolü). PX4 otopilotu, QGroundControl ve görev bilgisayarları birbirleriyle veri paketleri (örneğin "konumum şu" veya "arm ol") alışverişi yaparken bu hafif ve hızlı mesajlaşma standartını kullanır.

MAVSDK: MAVLink'in karmaşık alt seviye veri paketleriyle tek tek uğraşmak yerine; Python veya C++ gibi dillerde arm(), takeoff(), start_mission() gibi hazır ve okunaklı komutlarla İHA'ya otonom görevler yazdığımız yazılım geliştirme kütüphanesidir.

## ROS 2 ve PX4 nasıl birlikte çalışır? 
PX4 tek başına uçağın dengesini ve temel uçuş kontrolünü yapar; ancak görüntü işleme, engel tanıma veya karmaşık yapay zeka kararları gibi yüksek işlem gücü gerektiren görevleri ROS 2 (görev bilgisayarı tarafı) üstlenir.

İkisi arasındaki iletişim, arka planda çalışan Micro XRCE-DDS (senin terminalde çalıştırdığın MicroXRCEAgent) adlı köprü üzerinden sağlanır.

Bu köprü sayesinde PX4'ün içindeki sensör ve durum verileri ROS 2 tarafında standart Topic'ler (yayın kanalları) olarak görünür; ROS 2'nin ürettiği hız veya konum komutları da aynı köprüden geçerek PX4'e iletilir.

## 5. İHA Masterclass Eğitim Serisi – Öne Çıkan Notlar (1–16. Bölümler)
* **Avyonik ve Sistem Mimarisi:** Bir İHA'nın sadece mekanik ve motordan ibaret olmadığı; sensörler, uçuş kontrol kartı (otopilot), yer istasyonu ve görev bilgisayarının bir bütün olarak haberleştiği kavrandı.
* **Simülasyon Ortamının Önemi:** Gerçek uçuş testlerinden önce PX4 SITL ve Gazebo ortamında yapılan testlerin hem donanım maliyeti hem de uçuş güvenliği (kırım riskini sıfırlama) açısından kritik olduğu görüldü.
* **Haberleşme ve Otonom Kontrol:** Yer kontrol istasyonu ile İHA arasındaki MAVLink veri akışı, uçuş modları (Takeoff, Mission, RTL/Land) ve yazılım üzerinden otonom görev tetikleme mantığı pekiştirildi.

## BÖLÜM 1:
### İHA Türleri, Gövde Yapıları (Airframe) ve Uçuş Dinamiği
* **Döner Kanat (Multirotor) Sistemler:** Motor sayısına ve dizilimine göre isimlendirilir (3 motorlu *Tricopter*, 4 motorlu *Quadcopter*, 6 motorlu *Hexacopter*, 8 motorlu *Octocopter* ve çift katmanlı *X8*). 
Motor sayısı arttıkça taşıma kapasitesi (itki) artar ancak batarya tüketimi ve ağırlık da büyüdüğü için göreve göre denge kurulmalıdır. Döner kanatlarda sağlıklı uçuş ve manevra kabiliyeti için toplam itki kuvvetinin araç ağırlığının en az **2 katı (1:2 oranı)** olması gerekir (X8 gibi tasarımlarda bu oran 1:3'e çıkar).
* **Sabit Kanatlı (Fixed-Wing) Sistemler:** Havada tutunmak için motor gücü yerine kanatların aerodinamik kaldırma kuvvetini kullanır. Tek motorla çok daha az enerji harcayarak uzun mesafeler uçabilir; ancak iniş ve kalkış için **piste ihtiyaç duyar** ve yüksek hızda (yaklaşık 20 m/s) piste inmesi kontrol açısından daha hassastır.
* **VTOL (Dikey İniş-Kalkış) ve Hibrit Sistemler:** Döner kanadın pist gerektirmeyen dikey iniş-kalkış yeteneği ile sabit kanadın uzun menzil avantajını birleştirir. Standart VTOL (4 dikey motor + 1 itici arka motor), motorları öne katlanabilen **Tilt-Rotor** ve 2 motorlu **Tailsitter** gibi türleri bulunur.
* **QGroundControl Airframe (Gövde) Seçimi:** Uçuş kontrolcüsüne (FC) yazılım yüklerken aracın fiziksel yapısına (motor dizilimi, X veya + yönelimi, kontrol yüzeyi sayısı) uygun hazır *Airframe* şablonu seçilir. Hazır şablonlar uzun mühendislik ve kontrol algoritması testlerinden geçtiği için özel bir tasarım yapılmadıkça bu standart gövdelerin seçilmesi uçuş kararlılığı sağlar.
## BÖLÜM 2:
### İHA Uçuş Dinamiği, Eksen Hareketleri (Roll, Pitch, Yaw) ve Aerodinamik (DönerKanat ve SabitKanat İHA Nasıl Uçar?)
- **Döner Kanatlarda Uçuş ve Eksen Kontrolü:** Multirotor İHA'lar; pil voltajı ve pervane çapına bağlı olarak motorların ürettiği toplam itki kuvvetinin araç ağırlığını aşmasıyla dikey kalkış yapar. Havada yönelim üç temel eksende motor devirlerinin farklılaştırılmasıyla sağlanır:
  - **Pitch (Yunuslama):** Ön ve arka motorların devir farkı oluşturarak İHA'nın burnunu öne veya arkaya eğip ileri-geri hareket etmesini sağlar.
  - **Roll (Yalpalama / Yatış):** Sağ ve sol motorların devir farkıyla aracın sağa veya sola yatmasını sağlar.
  - **Yaw (Sapma / Dönüş):** Çapraz motorların zıt yönlerde (saat yönü ve saat yönünün tersi) dönmesiyle oluşan tork dengesinin değiştirilmesi sayesinde İHA'nın kendi dikey ekseni etrafında sağa veya sola dönmesini sağlar.
- **Tork Dengesi ve Ağırlık Merkezi (CoG):** Pervanelerin çapraz olarak zıt yönlerde dönmesi, gövdeye binen dönme torkunu sıfırlayarak aracın kendi etrafında kontrolsüzce dönmesini engeller. Ayrıca yük veya batarya yerleşimi nedeniyle ağırlık merkezi tam ortada olmadığında, bu mesafe farklarının uçuş kontrolcüsüne tanımlanması motorlara dengeli güç dağıtılmasını ve uçuş kararlılığını artırır.
- **Sabit Kanatlı İHA'larda Aerodinamik Kaldırma (Lift):** Sabit kanatlı uçaklar ileri doğru hızlandıkça, kanat profilinin (*airfoil*) üst yüzeyindeki kavisli yapıdan geçen hava alt yüzeyden geçen havaya göre daha hızlı akar ve basınç farkı (Bernoulli prensibi) oluşturur. Bu basınç farkı uçağı havada tutan kaldırma kuvvetini üretir.
## BÖLÜM 3-4-5:
### Temel Avyonik Bileşenler ve Motor Yapısı
- **Uçuş Kontrolcüsü (Flight Controller – FC):** Pixhawk veya Cube Orange gibi donanımlardan oluşan İHA'nın ana kontrol birimidir. Üzerinde gerçek zamanlı gömülü yazılım koşar; GPS, ivmeölçer ve hava hızı gibi sensörlerden gelen verileri işleyerek aracı havada dengede tutar ve üst seviyeden gelen "konuma git" gibi komutları motorlara ve servolara gidecek fiziksel sinyallere dönüştürür.
- **Görev Bilgisayarı (Companion Computer):** Raspberry Pi veya NVIDIA Jetson gibi Linux tabanlı mini bilgisayarlardır. Yer istasyonu ile İHA arasındaki iletişim gecikmesini ortadan kaldırmak için doğrudan aracın üzerinde bulunur; görüntü işleme ve otonom karar algoritmalarını anlık çalıştırarak uçuş kontrolcüsüne hızlı komut iletir.
- **Sensörler ve Telemetri:**
  - **GPS:** İHA'nın küresel konum bilgisini sağlar.
  - **Airspeed (Hava Hızı) Sensörü:** Özellikle sabit kanatlı İHA'larda havanın araca göre akış hızını ölçerek havada tutunma (stall olmama) güvenliği sağlar.
  - **Telemetri Modülü:** İHA ile yer kontrol istasyonu (Ground Control Station) arasındaki kablosuz veri ve parametre alışverişini kurar.
- **Fırçasız (Brushless) İHA Motorları ve KV Değeri:** Motor kodlarındaki 4 haneli sayılar (örneğin `2212`) iç stator bobininin çapını ve yüksekliğini ifade eder. **KV değeri** ise motorun yüksüz halde **1 Volt başına dakikada yapacağı devir sayısını (RPM)** gösterir; çok yüksek KV değerleri hızı artırsa da enerjiyi ısıya dönüştürerek uçuş verimliliğini düşürür.
### Güç Dağıtımı, ESC, Sensör Füzyonu (EKF) ve Kontrol Algoritmaları
- **ESC (Electronic Speed Controller) ve Güç Dağıtımı (PDB):** ESC, uçuş kontrolcüsünden aldığı sinyal doğrultusunda motora giden üç fazlı (A, B, C) akımı düzenleyerek motor devrini kontrol eder. LiPo bataryalardan (3S, 4S, 6S vb.) gelen yüksek akım **PDB (Power Distribution Board)** ve güç modülleri aracılığıyla güvenli şekilde dağıtılır; ayrıca pil voltajı ve anlık akım bilgisi uçuş kontrolcüsüne aktarılır.
  - **Güvenlik Payı ve BEC:** ESC seçimi yapılırken motorun çekebileceği maksimum akımın üzerinde (örneğin 10A çeken bir motor için 15A–20A) bir değer seçilmelidir. Bazı ESC'lerde bulunan **BEC (Battery Eliminator Circuit)** devresi uçuş kontrolcüsüne ve sensörlere ekstra 5V güç beslemesi sağlarken, *Opto ESC*'lerde BEC bulunmaz.
- **Uçuş Kontrolcüsü Donanımı ve İşlem Hızı:** Pixhawk, CUAV V5 ve Cube Orange gibi kontrolcüler STM32 tabanlı işlemciler kullanır. İşlemci frekansının (MHz) yüksek olması sensör verilerinin saniyede daha fazla döngüde işlenmesini ve İHA'nın havadaki sarsıntılara çok daha hızlı tepki vermesini sağlar. Kritik uçuşlarda gürültülü verileri elemek için birden fazla yedekli IMU kullanılır.
- **Gelişmiş Sensörler ve RTK GPS:**
  - **IMU (İvmeölçer + Jiroskop):** X, Y, Z eksenlerindeki doğrusal ivmeyi ve açısal dönüş hızını ölçer.
  - **Barometre, Manyetometre ve LiDAR:** Barometre hava basıncından tahmini irtifa üretirken, uçağın altına yerleştirilen **LiDAR** kızılötesi ışınlarla yere olan gerçek mesafeyi hassas şekilde ölçer. Manyetometre ise pusula görevi görerek yön sapmalarını engeller.
  - **RTK GPS:** Standart GPS'teki 1–1.5 metrelik hata payını sabit bir yer referans istasyonu üzerinden düzelterek **1–2 cm hassasiyete** düşüren yüksek doğruluklu konumlandırma sistemidir.
- **PID Kontrol ve Sensör Füzyonu (EKF):**
  - **PID (Proportional – Integral – Derivative):** Sensörlerden gelen anlık hataya (P), zamanla biriken hataya (I) ve hatanın değişim hızına (D) göre motorlara veya kontrol yüzeylerine ne şiddette tepki verileceğini belirleyen temel kararlılık algoritmasıdır.PID,drone'un dengesini sürekli koruyan matematiksel kontrol sistemidir.
  - **EKF (Extended Kalman Filter):** GPS, IMU, barometre ve hava hızı sensörlerinden gelen gürültülü verileri birleştirip filtreleyerek İHA'nın gerçek konumunu, hızını ve yönelim açılarını en doğru şekilde tahmin eden matematiksel sensör füzyonu algoritmasıdır.
- **Telemetri Haberleşmesi:** Yer istasyonu ile İHA arasındaki kablosuz veri ve komut iletişimini sağlar. Kısa-orta menzilli görevlerde 433/915 MHz modüller (Holybro vb.), uzun menzilli (40 km'ye kadar) ve yüksek çıkış güçlü (mW) görevlerde ise RFD900 gibi şifreli haberleşme modülleri kullanılır.
### Görüntü Aktarım Sistemleri, Görev Bilgisayarları ve Yer Kontrol İstasyonu (GCS)
- **Görüntü Aktarım Sistemleri (Analog vs. Dijital):** İHA üzerindeki kameradan alınan görüntünün operatöre (FPV gözlük veya yer ekranına) aktarılmasını sağlar ve acil durumlarda manuel müdahaleyi kolaylaştırır.
  - **Analog Sistemler:** Daha düşük maliyetlidir ve gecikmesi (latency) çok düşüktür, ancak görüntü çözünürlüğü sınırlıdır.
  - **Dijital Sistemler (DJI vb.):** 2K–4K seviyesinde yüksek çözünürlüklü ve net görüntü aktarımı sunar.
- **Görev Bilgisayarı (Companion Computer) ve Yapay Zeka İşleme:** NVIDIA Jetson (özellikle Orin Nano serisi) veya yapay zeka hızlandırıcılı Raspberry Pi 5 gibi mini bilgisayarlardır. Uçuşun temel dengesini uçuş kontrolcüsüne (Pixhawk) bırakırken; doğrudan bağlı kameradan (gimbal veya derinlik kamerası) aldığı görüntüyü 40–150 FPS hızlarında işleyerek **nesne tespiti, hedef takibi (tracking), rota optimizasyonu ve otonom it dalaşı (dogfight)** kararları üretir ve USB üzerinden uçuş kontrolcüsüne anlık komut iletir.
- **Yer Kontrol İstasyonu (Ground Control Station – GCS) Özellikleri:** Açık kaynaklı (özelleştirilebilir) operasyon merkezidir. Uçuş öncesi *Takeoff – Waypoint – Landing* görev planlaması yapılmasını, canlı telemetri ve kamera görüntüsünün izlenmesini, *Failsafe* (acil durum/eve dönüş) davranışlarının yönetilmesini ve uçuş sonrası hata analizi için **uçuş günlüklerinin (log)** kaydedilmesini sağlar. Ayrıca Wi-Fi veya 4G/LTE (SIM kart) modülleri üzerinden yerdeki bilgisayar ile İHA üzerindeki görev bilgisayarı arasında kablosuz ağ ve **SSH bağlantısı** kurulabilir.
## BÖLÜM 6:
### Otopilot Yazılımları (PX4 vs. ArduPilot) ve PX4 Uçuş Modları
- **Otopilot Yazılımının Temel Görevleri:** Sensör füzyonu ile durum tahmini (*State Estimation*), gelen komutları motor/servo sinyallerine dönüştüren uçuş kontrolü, görev yönetimi (*Takeoff – Waypoint – RTL/Land*) ve batarya düşüşü ya da sensör tutarsızlığında devreye giren **Failsafe** (güvenli kurtarma/iniş) mekanizmalarını yönetir.
- **PX4 ve ArduPilot Karşılaştırması:**
  - **Lisans ve Ticari Kullanım:** ArduPilot (GPL lisansı nedeniyle) kaynak kodunda yapılan değişikliklerin açık kaynak paylaşılmasını zorunlu kılarken; **PX4 (BSD lisansı)** geliştirilen özel algoritmaların kapalı tutulmasına ve ticari ürünlere entegre edilmesine izin verir.
  - **Topluluk ve Geliştirme:** ArduPilot hobi ve DIY (kendin yap) tarafında çok geniş bir topluluğa sahipken, PX4 kontrol mühendisleri ve Ar-Ge projeleri için daha güncel ve modüler bir mimari sunar. PX4 ağırlıklı olarak *QGroundControl*, ArduPilot ise *Mission Planner* ile kullanılsa da günümüzde her iki yer istasyonu da birbirini desteklemektedir.
- **PX4 Uçuş Modları (Manuel Yardımlı ve Otonom):**
  - **Stabilized:** İHA'nın sadece yatay dengesini (Roll/Pitch açısını) korur; irtifa ve konum kontrolü tamamen pilottadır.
  - **Altitude:** IMU ve barometre kullanarak aracın yerden yüksekliğini (irtifasını) otomatik sabitler; GPS gerektirmez.
  - **Position:** GPS, barometre ve IMU'yu birlikte kullanır. Döner kanatlarda kumanda bırakıldığında aracı 3 boyutlu konumda havada sabitler; sabit kanatlarda ise belirlenen irtifa ve yön doğrultusunda düz uçuşu korur.
  - **Hold (Loiter):** Bekleme ve güvenlik modudur. Döner kanatlar bulunduğu noktada havada asılı kalırken, sabit kanatlar havada tutunmak için belirlenen nokta etrafında dairesel dönüş (*Loiter*) yapar.
  - **Mission & Return (RTL):** Önceden planlanan kalkış, ara nokta (*Waypoint*) ve iniş rotasını otonom uygular. Sabit kanatlı İHA'lar iniş (*Land*) öncesinde piste hizalanmak için *Loiter* dönüşü yapar; *Return* modu ise aracı kalkış noktasına (*Home*) geri döndürür.
  - **Offboard Modu:** Otopilotun kontrolü harici bir sisteme (görev bilgisayarı üzerinde çalışan **ROS 2** veya MAVSDK kodlarına) devrettiği gelişmiş otonom moddur. Doğrudan hız, ivme, yönelim (*Attitude*) veya itki komutları gönderilerek engel kaçınma, görsel takip ve sürü (*Swarm*) görevleri yürütülür. Komut akışı kesilirse veya sabit kanatlı araç kaldırma kuvvetini kaybedeceği kritik hız sınırının (*Stall*) altına düşmeye zorlanırsa PX4 güvenlik korumasını devreye sokar.
## BÖLÜM 7:
### İHA Haberleşme Protokolleri (MAVLink vs. DDS) ve Yazılım Kütüphaneleri
- **MAVLink ve DDS (Data Distribution Service) Karşılaştırması:**
  - **MAVLink:** İHA ile yer kontrol istasyonu arasındaki uzun mesafeli haberleşmelerde kullanılan çok hafif, düşük bant genişliği tüketen ve bayt bazlı paketler (sistem ID, komut, *checksum* vb.) taşıyan standart haberleşme protokolüdür. Uzak mesafede sinyal zayıflasa bile veri bütünlüğünü korur.
  - **DDS ve Micro XRCE-DDS:** Özellikle İHA üzerindeki görev bilgisayarı (Jetson/Raspberry Pi) ile uçuş kontrolcüsü arasındaki yüksek hızlı ve düşük gecikmeli veri aktarımı için kullanılır. Bant genişliği tüketimi yüksek olduğu için uzun menzilli telsiz bağlantıları yerine dahili donanımlar arasında **ROS 2** ile birlikte çalışır (PX4 içindeki dahili haberleşme olan *uORB* ile karıştırılmamalıdır).
- **İHA Programlama Kütüphaneleri:**
  - **MAVSDK:** Özellikle **PX4** ile tam uyumlu, modern ve güncel bir kütüphanedir. Python ve C++ gibi dillerde `takeoff()`, `arm()` gibi yüksek seviyeli ve okunaklı hazır fonksiyonlar sunarak otonom görev geliştirmeyi hızlandırır.
  - **Pymavlink:** Doğrudan alt seviye MAVLink mesaj paketlerini (Message ID ve Payload) manuel olarak oluşturup göndermeyi sağlayan Python kütüphanesidir. Kullanımı MAVSDK'ya göre daha zordur ancak gimbal kontrolü gibi özel/ince ayar gerektiren komutlarda yüksek esneklik sunar.
  - **ROS 2 (Robot Operating System 2):** Yalnızca uçuş kontrolü için değil; 360° LiDAR, derinlik kamerası ve sonar gibi harici sensörleri tek bir mimaride (*Publisher/Subscriber* topic yapısı) birleştirmek için kullanılır. Savaşan İHA (*dogfight*) veya anlık engel kaçınma gibi milisaniyelik tepki gerektiren karmaşık görevlerde tercih edilir.
  - **DroneKit:** Geçmişte ArduPilot projelerinde yaygın kullanılan ancak günümüzde aktif geliştirilmesi durdurulduğu için yerini MAVSDK ve Pymavlink'e bırakan eski bir kütüphanedir.
## BÖLÜM 8:
### İHA Simülasyon Ortamları ve Karşılaştırması
- **Simülasyon Kullanım Amacı:** Gerçek saha uçuşlarından önce kontrol algoritmalarını, sensör tepkilerini ve otonom görev senaryolarını sıfır kırım riski ve sıfır donanım maliyetiyle sanal ortamda test etmek için kullanılır.
- **Gazebo:** Hem PX4 hem de ArduPilot ekosisteminde en yaygın kullanılan açık kaynaklı fizik ve 3B robotik simülatörüdür. İçerisinde çok sayıda hazır araç modeli (*X500 multirotor*, *RC Cessna / Advanced Plane sabit kanat*, *Standard VTOL*, *Quad Tailsitter*, *Tilt-rotor* vb.) barındırır ve kamera/sensör entegrasyonu ile kapsamlı görev testleri sunar.
- **jMAVSim:** Kurulumu ve kullanımı hafif olan temel bir PX4 simülatörüdür. Kamera veya karmaşık çevre etkileşimi gerektirmeyen durumlarda sadece `arm`, `takeoff` ve temel rota (*waypoint*) kodlarını hızlıca test etmek için tercih edilir.
- **AirSim (Unreal Engine 4):** Yüksek görsel gerçekçiliğe sahip çevre modelleri (binalar, ışık-gölge, şehir dokusu) sunan ve özellikle görüntü işleme tabanlı teslimat/navigasyon testlerinde kullanılan simülatördür; ancak aktif geliştirilmesi durduğu için topluluk desteği sınırlıdır.
- **MATLAB / Simulink (UAV Toolbox):** Kontrol mühendisliği ve akademik çalışmalarda; sensör füzyonu (EKF) parametrelerini, uçuş kontrol algoritmalarını ve matematiksel modelleri derinlemesine analiz etmek için kullanılır.
- **NVIDIA Isaac Sim (Pegasus Simulator):** RTX ekran kartları üzerinde çalışan, özellikle **pekiştirmeli öğrenme (Reinforcement Learning)** tabanlı robotik ve ROS 2 / PX4 yapay zeka simülasyonları için geliştirilmiş yeni nesil bir ortamdır.
## BÖLÜM 12:
### QGroundControl (QGC) Arayüzü, Görev Planlama ve Güvenlik (GeoFence)
- **Uçuş Öncesi Sağlık Kontrolü (Health Check) ve Telemetri Paneli:** Uçuşa başlamadan önce GPS uydu sayısı, HDOP (konum doğruluk oranı) ve IMU kalibrasyonu gibi sensör kontrollerinin tamamlanıp **"Ready to Fly"** durumunun görülmesi gerekir. Alt gösterge paneli özelleştirilerek anlık *Roll, Pitch, Yaw (Heading)* açıları, hava hızı (*Airspeed*), batarya voltajı/akımı ve *Rangefinder (LiDAR)* mesafesi canlı izlenebilir.
- **Görev Planlama (Mission) ve Alan Tarama (Survey):**
  - *Plan* sekmesinden kalkış (*Takeoff*), ara noktalar (*Waypoint*) ve eve dönüş (*Return to Launch – RTL*) adımları oluşturularak İHA'ya yüklenir (*Upload*). Sabit kanatlı İHA'lar keskin dönüşler yapamadığı için ara noktalar geniş açılı/yumuşak geçişlerle planlanmalıdır.
  - **Survey (Pattern) Özelliği:** 3B haritalama (*Drone Mapping*) görevlerinde seçilen bir poligon alanını otomatik tarama hatlarına böler ve belirli mesafe aralıklarıyla kamera tetikleme (*camera trigger*) komutları üretir.
- **Analyze Tools (MAVLink Inspector ve Uçuş Logları):**
  - **MAVLink Inspector:** İHA'dan akan ham MAVLink mesajlarını (*HEARTBEAT*, *ATTITUDE*, *GLOBAL_POSITION_INT*, *BATTERY_STATUS*) gerçek zamanlı denetleyerek yeni takılan sensörlerin doğru çalışıp çalışmadığını test etmeyi sağlar.
  - **Uçuş Logları (.ulog):** Uçuş sırasındaki tüm sensör ve motor verilerini kaydeder; uçuş sonrasında *PX4 Flight Review* gibi araçlarla motor itkisi, kararlılık ve kırım analizi yapılmasına imkan tanır.
- **Parametre Yönetimi ve GeoFence (Sanal Çit):**
  - *Parameters* menüsünden aracın uçuş karakteristiği ve güvenlik sınırları ayarlanır (örneğin sabit kanatlı İHA'larda maksimum hava hızını sınırlayan `FW_AIRSPD_MAX` parametresi).
  - **GeoFence:** İHA'nın görev yapabileceği güvenli hava sahasını poligon veya daire şeklinde GPS koordinatlarıyla sınırlar. Sınır ihlali (*Breach*) durumunda *Safety* ayarlarından belirlenen aksiyon (uyarı, *Hold*, *Return*, *Land* veya motorları kesen *Terminate*) otomatik tetiklenir.
## BÖLÜM 13:
### Gazebo Simülasyon Ortamı Özelleştirme (Dünya, Sensör ve Konum Ayarları)
- **Simülasyon Dünyası (World) ve Pist Ekleme:** Varsayılan boş zemin yerine gerçekçi iniş-kalkış testleri yapabilmek için `~/PX4-Autopilot/Tools/simulation/gz/models/` dizinine özel model dosyaları (`runway` vb.) eklenir ve `worlds/default.sdf` dosyasına `<include>` etiketiyle tanımlanarak ortama dahil edilir.
- **Araç Modeline Sensör Ekleme (SDF Yapısı):** Sabit kanatlı İHA modellerinin (`advanced_plane` vb.) `model.sdf` dosyasına `<link>`, `<sensor>` ve `<joint>` blokları eklenerek araca ön veya alt kamera/LiDAR sensörleri entegre edilebilir. Üretilen görüntü verisi Gazebo arayüzündeki *Image Display* eklentisi veya ROS 2 köprüsü üzerinden OpenCV ile işlenebilir.
- **Başlangıç GPS Koordinatları ve Yönelim:** Gerçek saha uçuşu öncesinde simülasyonu ilgili uçuş alanına taşımak için terminal üzerinden `PX4_HOME_LAT`, `PX4_HOME_LON` ve `PX4_HOME_ALT` ortam değişkenleri tanımlanır; aracın pist üzerindeki başlangıç açısı ise modelin `pose` parametresi üzerinden ayarlanır.
### KISA YOLLAR-Hızlı Başvuru Rehberi: Temel Terminal Komutları ve Model Dosya Yolları
cat << 'EOF' >> ~/astron-fixed-wing-mission/teknik_rapor.md

| İşlem | Komut / Dosya Yolu | Ne İşe Yarar? |
| :--- | :--- | :--- |
| **Sabit Kanat Simülasyonunu Başlat** | `cd ~/PX4-Autopilot && make px4_sitl gz_advanced_plane` | Gazebo'da pist ve sabit kanatlı uçağı açar. |
| **Arka Plandaki Simülasyonu Kapat** | `pkill -f px4; pkill -f gz` | Takılı kalan simülasyon süreçlerini anında kapatır. |
| **Tanımlı Kısayolları Görüntüle** | `tail -n 15 ~/.bashrc` | Terminalde tanımlı özel kısayolları listeler. |
| **Dünya / Pist Dosyası** | `~/PX4-Autopilot/Tools/simulation/gz/worlds/default.sdf` | Sahneye pist, bina veya zemin eklenen dosya. |
| **Sabit Kanat Model Dosyası** | `~/PX4-Autopilot/Tools/simulation/gz/models/advanced_plane/model.sdf` | Uçağa kamera, LiDAR veya sensör eklenen dosya. |
| **Başlangıç GPS Konumunu Değiştir** | `export PX4_HOME_LAT=...` / `LON` / `ALT` | Uçağın başlangıç koordinatını değiştirir. |
EOF
## BÖLÜM 14:
### MAVSDK ve Python ile Otonom İHA Programlama
- **Paket ve Ortam Yönetimi (Miniconda / Conda):** Kütüphane sürüm çakışmalarını (ör. ASIO asenkron altyapısı ve MAVLink paket sürümleri) önlemek amacıyla izole sanal ortamlar (`conda create -n <ortam> python=3.10`, `conda activate`) oluşturularak `mavsdk` kütüphanesi kurulur.
- **Asenkron Mimari (`asyncio`) ve Bağlantı:** MAVSDK, farklı frekanslarda (10 Hz – 20 Hz) veri üreten sensörleri bloklamadan dinleyebilmek için Python `asyncio` altyapısını kullanır. Simülasyon ortamında araç bağlantısı yerel UDP portu (`udp://:14540`), gerçek telemetri donanımında ise seri port (`/dev/ttyUSB0`) üzerinden `drone.connect()` ile sağlanır.
- **Telemetri ve Durum İzleme:** `drone.telemetry` modülü üzerinden uçuş öncesi sağlık kontrolleri (*Health Check*), GPS konumu (*Position*), yönelim açıları (*Attitude* — Roll/Pitch/Yaw), hız ve uçuş modu verileri gerçek zamanlı çekilir; hedef noktalara varış kontrolü GPS mesafe hesaplamalarıyla denetlenir.
- **Temel Otonom Uçuş Komutları:** Uçuşa hazırlık onayının ardından motor yetkilendirme (`drone.action.arm()`), hedef irtifa belirleme (`set_takeoff_altitude()`), kalkış (`takeoff()`), bekleme (*Hold*) ve iniş (`land()`) komutları asenkron döngülerle yürütülür.
EOF