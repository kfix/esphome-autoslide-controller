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

you will have to play with flip flopping the TX/RX and A/B connections until you you get both correct. the labels on any particular module don't inherently mean much without a full text description or maybe a direction arrow in their product picture.

# building

fill in `network.yaml.sample` and remove the `.sample` extension

for first run, plug in the esp32 over USB and run
```
pip3 install esphome
esphome run sliding_door_controller.yaml
```

once its flashed and successfully associated to wifi, `run` or `logs` will use OTA to manage the device.


