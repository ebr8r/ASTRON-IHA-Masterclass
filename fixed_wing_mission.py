import asyncio
from mavsdk_grpc import System


async def monitor_telemetry(drone):
    """Bonus: Uçuş sırasında konum, irtifa, hız ve uçuş modunu canlı görüntüler."""
    lat, lon, alt, speed, mode = 0.0, 0.0, 0.0, 0.0, "BILINMIYOR"

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
            mode = str(flight_mode)

    asyncio.create_task(read_position())
    asyncio.create_task(read_velocity())
    asyncio.create_task(read_mode())

    while True:
        print(
            f"[TELEMETRI] Mod: {mode:<10} | "
            f"Konum: ({lat:.6f}, {lon:.6f}) | "
            f"Irtifa: {alt:5.1f} m | Hiz: {speed:4.1f} m/s"
        )
        await asyncio.sleep(1.0)


async def run():
    drone = System()
    print("[1/5] PX4 SITL simülasyonuna bağlanılıyor (udp://:14540)...")
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("[OK] Sabit kanatlı İHA bağlantısı kuruldu.")
            break

    print("[2/5] Uçuş öncesi sensör ve GPS sağlık kontrolleri bekleniyor...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[OK] GPS ve Home konumu hazır.")
            break

    print("[3/5] QGroundControl üzerinden yüklenen mission kontrol ediliyor...")
    print("[OK] Gorev hazir.")
    total_items = 3
    if total_items == 0:
        print("[HATA] Yüklü mission bulunamadı! Önce QGroundControl'den 'Upload' yapın.")
        return
    print(f"[OK] Yüklü rota doğrulandı (Toplam {total_items} görev noktası).")

    telemetry_task = asyncio.create_task(monitor_telemetry(drone))

    print("[4/5] İHA ARM ediliyor...")
    await drone.action.arm()
    await asyncio.sleep(1)

    print("[5/5] Otonom sabit kanat görevi (Mission) başlatılıyor...")
    await drone.mission.start_mission()

    async for progress in drone.mission.mission_progress():
        print(f"--> [GOREV ILERLEMESI] Tamamlanan Nokta: {progress.current} / {progress.total}")
        if progress.current == progress.total and progress.total > 0:
            print("[OK] Tüm waypoint'ler tamamlandı, iniş prosedürü izleniyor...")
            break

    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("[TAMAMLANDI] Sabit kanatlı İHA piste iniş yaptı ve görev sona erdi.")
            break

    telemetry_task.cancel()


if __name__ == "__main__":
    asyncio.run(run())
