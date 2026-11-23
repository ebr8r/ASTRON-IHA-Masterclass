"""
ASTRON İHA Masterclass — Sabit Kanatlı İHA Otonom Görev ve Canlı Telemetri Betiği

PX4 SITL ve Gazebo ortamında simüle edilen sabit kanatlı İHA'ya (gz_rc_cessna)
MAVSDK-Python üzerinden bağlanır, QGroundControl ile yüklenen görevi doğrular,
uçuş öncesi sağlık kontrollerini yaparak aracı ARM eder, otonom görevi başlatır
ve uçuş boyunca canlı telemetri verilerini terminalde görüntüler.
"""

import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.mission import MissionError
from mavsdk.mission_raw import MissionRawError


async def monitor_telemetry(drone):
    """Bonus: Uçuş sırasında konum, irtifa, yer hızı, uçuş modu ve ARM durumunu canlı görüntüler."""
    lat, lon, alt, speed, mode, armed_status = 0.0, 0.0, 0.0, 0.0, "BİLİNMİYOR", "DISARMED"

    async def read_position():
        nonlocal lat, lon, alt
        async for pos in drone.telemetry.position():
            lat = pos.latitude_deg
            lon = pos.longitude_deg
            alt = pos.relative_altitude_m

    async def read_velocity():
        nonlocal speed
        async for vel in drone.telemetry.velocity_ned():
            speed = (vel.north_m_s**2 + vel.east_m_s**2) ** 0.5

    async def read_mode():
        nonlocal mode
        async for flight_mode in drone.telemetry.flight_mode():
            mode = flight_mode.name if hasattr(flight_mode, "name") else str(flight_mode)

    async def read_armed():
        nonlocal armed_status
        async for is_armed in drone.telemetry.armed():
            armed_status = "ARMED" if is_armed else "DISARMED"

    tasks = [
        asyncio.create_task(read_position()),
        asyncio.create_task(read_velocity()),
        asyncio.create_task(read_mode()),
        asyncio.create_task(read_armed()),
    ]

    try:
        while True:
            print(
                f"[TELEMETRİ] Durum: {armed_status:<8} | Mod: {mode:<10} | "
                f"Konum: ({lat:.6f}, {lon:.6f}) | "
                f"İrtifa: {alt:5.1f} m | Hız: {speed:4.1f} m/s"
            )
            await asyncio.sleep(1.0)
    finally:
        for task in tasks:
            task.cancel()


async def run():
    drone = System()
    print("[1/5] PX4 SITL simülasyonuna bağlanılıyor (udp://:14540)...")
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("[OK] Sabit kanatlı İHA bağlantısı kuruldu.")
            break

    print("[2/5] Uçuş öncesi sensör, GPS ve ARM edilebilirlik kontrolleri bekleniyor...")
    async for health in drone.telemetry.health():
        if (
            health.is_global_position_ok
            and health.is_home_position_ok
            and health.is_armable
        ):
            print("[OK] GPS, Home konumu ve sistem sağlığı uçuşa hazır.")
            break

    print("[3/5] QGroundControl üzerinden yüklenen mission kontrol ediliyor...")
    try:
        mission_plan = await drone.mission.download_mission()
        total_items = len(mission_plan.mission_items)
    except MissionError:
        try:
            raw_items = await drone.mission_raw.download_mission()
            total_items = len(raw_items)
        except MissionRawError as e:
            print(f"[HATA] Görev planı okunamadı: {e}")
            return

    if total_items == 0:
        print("[HATA] Yüklü mission bulunamadı! Önce QGroundControl'den 'Upload' yapın.")
        return
    print(f"[OK] Yüklü rota doğrulandı (Toplam {total_items} görev öğesi).")

    telemetry_task = asyncio.create_task(monitor_telemetry(drone))

    try:
        print("[4/5] İHA ARM ediliyor...")
        try:
            await drone.action.arm()
        except ActionError as e:
            print(f"[HATA] ARM işlemi reddedildi: {e}")
            return

        await asyncio.sleep(1)

        print("[5/5] Otonom sabit kanat görevi (Mission) başlatılıyor...")
        try:
            await drone.mission.start_mission()
        except MissionError as e:
            print(f"[HATA] Görev başlatılamadı: {e}")
            return

        async for progress in drone.mission.mission_progress():
            print(f"--> [GÖREV İLERLEMESİ] Tamamlanan Nokta: {progress.current} / {progress.total}")
            if progress.current == progress.total and progress.total > 0:
                print("[OK] Tüm waypoint'ler tamamlandı, iniş prosedürü izleniyor...")
                break

        async for in_air in drone.telemetry.in_air():
            if not in_air:
                print("[TAMAMLANDI] Sabit kanatlı İHA piste iniş yaptı ve görev sona erdi.")
                break
    finally:
        telemetry_task.cancel()


if __name__ == "__main__":
    asyncio.run(run())
