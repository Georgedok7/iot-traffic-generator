RANDOM_SEED = 42

TOTAL_FLOWS = 10000

ATTACK_RATIO = 0.20

DNS_RATIO = 0.40
HTTP_RATIO = 0.30
MQTT_RATIO = 0.30

PORT_SCAN_RATIO = 0.25
MQTT_FLOOD_RATIO = 0.25
DNS_EXFILTRATION_RATIO = 0.25
MIRAI_RATIO = 0.25

ATTACK_BURST_MIN = 5
ATTACK_BURST_MAX = 15

NORMAL_DELAY_MIN = 0.05
NORMAL_DELAY_MAX = 0.50

PORT_SCAN_DELAY_MIN = 0.005
PORT_SCAN_DELAY_MAX = 0.03

MQTT_FLOOD_DELAY_MIN = 0.001
MQTT_FLOOD_DELAY_MAX = 0.01

DNS_EXFIL_DELAY_MIN = 0.05
DNS_EXFIL_DELAY_MAX = 0.20

MIRAI_DELAY_MIN = 0.003
MIRAI_DELAY_MAX = 0.02

DEVICE_PROFILES = {
    "temperature_sensor": {
        "ip": "192.168.1.10",
        "protocol_weights": {
            "mqtt": 0.80,
            "dns": 0.20
        }
    },

    "smart_camera": {
        "ip": "192.168.1.20",
        "protocol_weights": {
            "http": 0.80,
            "dns": 0.20
        }
    },

    "thermostat": {
        "ip": "192.168.1.30",
        "protocol_weights": {
            "mqtt": 0.60,
            "http": 0.25,
            "dns": 0.15
        }
    },

    "gateway": {
        "ip": "192.168.1.40",
        "protocol_weights": {
            "http": 0.40,
            "mqtt": 0.35,
            "dns": 0.25
        }
    }
}