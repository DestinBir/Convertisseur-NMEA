import random
import time

def calcul_checksum(check):
    checksum = 0
    for char in check:
        checksum ^= ord(char)
    return f"{checksum:02X}"

def analyser_gpgga(gpgga):
    parties = gpgga.split(',')
    temps = parties[1]
    latitude = parties[2]
    direction_latitude = parties[3]
    longitude = parties[4]
    direction_longitude = parties[5]
    qualite = parties[6]
    satellites = parties[7]
    altitude = parties[9]
    
    return {
        'temps': temps,
        'latitude': latitude,
        'direction_latitude': direction_latitude,
        'longitude': longitude,
        'direction_longitude': direction_longitude,
        'qualite': qualite,
        'satellites': satellites,
        'altitude': altitude
    }

def generer_gpgsa(gpgga):
    donnees_gpgga = analyser_gpgga(gpgga)
    mode = "A"
    fix_type = '3'
    prns = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    prns = prns[:int(donnees_gpgga['satellites'])]
    while len(prns) < 12:
        prns.append('')
    pdop = '1.0'
    hdop = '1.0'
    vdop = '1.0'
    gpgsa = f"$GPGSA,{mode},{fix_type}," + ",".join(prns) + f",{pdop},{hdop},{vdop}*30"
    return gpgsa

def generer_gprmc(gpgga):
    donnees_gpgga = analyser_gpgga(gpgga)
    maintenant = time.strftime("%H%M%S", time.gmtime())
    status = 'A'
    latitude = f"{donnees_gpgga['latitude']},{donnees_gpgga['direction_latitude']}"
    longitude = f"{donnees_gpgga['longitude']},{donnees_gpgga['direction_longitude']}"
    vitesse = ""
    angle = ""
    date = time.strftime("%d%m%y", time.gmtime())
    variationMagn = "000.0,W"
    gprmc = f"GPRMC,{maintenant},{status},{latitude},{longitude},{vitesse},{angle},{date},{variationMagn}"
    checksum = calcul_checksum(gprmc)
    return f"${gprmc}*{checksum}"
