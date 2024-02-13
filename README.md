Configs for a esp32-based [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy.html) that can also control an [AutoSlide sliding door opener](https://autoslide.com/how-it-works/) over its modbus pin header (marked "RS485"), by way of an additional RS485-to-TTL converter module.

![Home Assistant screenshot](/screenshot.png)

Once discovered in Home Assistant, you can remotely trigger sensors & buttons that come with the kit, observe the state of the door opeining, and change its mode (Auto/Pet/Stacker/Security).

# wiring from the autoslide

My autoslide has a "V2" control board and the unit was manufactured in 2022.  
I had to remove both the external cover and the interior electronics cover to expose its [RS485](https://en.wikipedia.org/wiki/RS-485) pin header (top right corner), and then wirewrapped its three left-most pins to 5 inches of 30AWG going to the RS485 module.  

* pin 1: B (D-)
* pin 2: A (D+)
* pin 3: ground
* pin 4: 12V (I don't use this one & shorting it to ground will reset the autoslide!)

# RS485-to-TTL converters / Modbus transievers

I could not get this working with the "automatic" flow-controlling modules, they would corrupt the initial bytes of the reply.

A simpler module with DE & RE pins (hardware flow control) worked fine. Bridge them together with some solder and hook up one pin to a GPIO on the ESP32.

you will have to play with flip flopping the TX/RX and A/B connections until you get both correct. the labels on any particular module don't inherently mean much without a full text description or maybe a direction arrow in their product picture.

you can set logs to VERBOSE to see individual send/reply bytes, the autoslide PDF linked in the yaml has examples of what you should be seeing.

if your module has RX/TX leds, seeing both flash at the same time is also a good sign you've got the wiring correct.

# building

fill in `network.yaml.sample` and remove the `.sample` extension

for first run, plug in the esp32 over USB and run
```
pip3 install esphome
esphome run sliding_door_controller.yaml
```

once its flashed and successfully associated to wifi, `run` or `logs` will use OTA to manage the device.

# sample log

```
[21:33:20][I][app:102]: ESPHome version 2023.12.9 compiled on Feb 12 2024, 19:58:08
[21:33:20][I][app:104]: Project esphome.bluetooth-proxy version 1.0
[21:33:20][C][wifi:573]: WiFi:
[21:33:20][C][wifi:405]:   Local MAC: 44:17:93:59:4E:AC
[21:33:20][C][wifi:410]:   SSID: 'xxxxxxx'
[21:33:20][C][wifi:411]:   IP Address: 10.2.0.151
[21:33:20][C][wifi:413]:   BSSID: xx:xx:xx:xx:xx:xx
[21:33:20][C][wifi:414]:   Hostname: 'sliding-door-ctl'
[21:33:20][C][wifi:416]:   Signal strength: -47 dB ▂▄▆█
[21:33:20][C][wifi:420]:   Channel: 11
[21:33:20][C][wifi:421]:   Subnet: 255.255.255.0
[21:33:20][C][wifi:422]:   Gateway: 10.2.0.1
[21:33:20][C][wifi:423]:   DNS1: 10.2.0.1
[21:33:20][C][wifi:424]:   DNS2: 0.0.0.0
[21:33:20][C][logger:439]: Logger:
[21:33:20][C][logger:440]:   Level: DEBUG
[21:33:20][C][logger:441]:   Log Baud Rate: 115200
[21:33:20][C][logger:443]:   Hardware UART: UART0
[21:33:20][C][uart.idf:139]: UART Bus 1:
[21:33:20][C][uart.idf:140]:   TX Pin: GPIO21
[21:33:20][C][uart.idf:141]:   RX Pin: GPIO22
[21:33:20][C][uart.idf:143]:   RX Buffer Size: 256
[21:33:20][C][uart.idf:145]:   Baud Rate: 9600 baud
[21:33:20][C][uart.idf:146]:   Data Bits: 8
[21:33:20][C][uart.idf:147]:   Parity: NONE
[21:33:20][C][uart.idf:148]:   Stop bits: 1
[21:33:20][C][modbus:143]: Modbus:
[21:33:20][C][modbus:144]:   Flow Control Pin: GPIO23
[21:33:20][C][modbus:145]:   Send Wait Time: 700 ms
[21:33:20][C][modbus:146]:   CRC Disabled: NO
[21:33:20][C][bluetooth_proxy:088]: Bluetooth Proxy:
[21:33:20][C][bluetooth_proxy:089]:   Active: YES
[21:33:20][C][modbus_controller.text_sensor:012]: Modbus Controller Text Sensor 'opener status'
[21:33:20][C][modbus_controller.select:009]: modbus_controller.selectModbus Controller Select 'select mode'
[21:33:20][C][modbus_controller.switch:068]: modbus_controller.switchModbus Controller Switch 'door button'
[21:33:20][C][modbus_controller.switch:091]: modbus_controller.switch  Restore Mode: disabled
[21:33:20][C][modbus_controller.switch:068]: modbus_controller.switchModbus Controller Switch 'pet sensor'
[21:33:20][C][modbus_controller.switch:091]: modbus_controller.switch  Restore Mode: disabled
[21:33:20][C][esp32_ble:374]: ESP32 BLE:
[21:33:20][C][esp32_ble:376]:   MAC address: 44:17:93:59:4E:AE
[21:33:20][C][esp32_ble:377]:   IO Capability: none
[21:33:20][C][esp32_ble_tracker:645]: BLE Tracker:
[21:33:20][C][esp32_ble_tracker:646]:   Scan Duration: 300 s
[21:33:20][C][esp32_ble_tracker:647]:   Scan Interval: 320.0 ms
[21:33:20][C][esp32_ble_tracker:648]:   Scan Window: 30.0 ms
[21:33:20][C][esp32_ble_tracker:649]:   Scan Type: ACTIVE
[21:33:20][C][esp32_ble_tracker:650]:   Continuous Scanning: True
[21:33:20][C][mdns:115]: mDNS:
[21:33:20][C][mdns:116]:   Hostname: sliding-door-ctl
[21:33:20][C][ota:097]: Over-The-Air Updates:
[21:33:20][C][ota:098]:   Address: sliding-door-ctl.lan:3232
[21:33:20][C][ota:101]:   Using Password.
[21:33:20][C][api:139]: API Server:
[21:33:20][C][api:140]:   Address: sliding-door-ctl.lan:6053
[21:33:20][C][api:142]:   Using noise encryption: YES
[21:33:20][C][modbus_controller:298]: ModbusController:
[21:33:20][C][modbus_controller:299]:   Address: 0x01
[21:33:24][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:24][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:24][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:29][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:29][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:29][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:34][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:34][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:34][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:39][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:39][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:39][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:44][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:44][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:44][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:45][D][esp32_ble_tracker:266]: Starting scan...
[21:33:49][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:49][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:49][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:54][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:54][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:54][D][text_sensor:064]: 'opener status': Sending state 'closed'
[21:33:59][D][modbus_controller.select:014]: New select value 0 from payload
[21:33:59][D][select:015]: 'select mode': Sending state Auto (index 0)
[21:33:59][D][text_sensor:064]: 'opener status': Sending state 'closed'

[21:36:38][D][select:062]: 'select mode' - Setting
[21:36:38][D][select:115]: 'select mode' - Set selected option to: Pet
[21:36:38][D][modbus_controller.select:048]: Found value 3 for option 'Pet'
[21:36:39][D][modbus_controller.select:014]: New select value 3 from payload
[21:36:39][D][select:015]: 'select mode': Sending state Pet (index 3)
[21:36:39][D][text_sensor:064]: 'opener status': Sending state 'closed & locked'
```
