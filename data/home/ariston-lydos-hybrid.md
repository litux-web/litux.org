title: Ariston Lydos Hybrid Wi-Fi Water Heater
last-updated: 2023-10
meta-keywords: Ariston, Lydos, Ariston Lydos, HomeKit, Termoaccumulator, Termoacumulador, Hybrid, Híbrido, Heat-Pump, Bomba de calor


{{{image:home/ariston-lydos-hybrid.jpg:Ariston Lydos Hybrid}}} The Ariston Lydos Hybrid Wi-Fi water heater is an excellent choice for those looking for an energy-efficient and convenient way to heat their water.

With its hybrid heating technology, the Lydos can save up to 50% on energy bills. And with its Wi-Fi connectivity, you can control the heater from anywhere using your smartphone or tablet.

## Features and Benefits of the Ariston Lydos Hybrid Wi-Fi Water Heater
The Ariston Lydos Hybrid Wi-Fi water heater has a number of features and benefits that make it a great choice for your home. These include:

* Hybrid heating technology: The Lydos uses a combination of a heat pump and a traditional heating element to heat water. This allows the heater to be very energy-efficient, as the heat pump can provide up to 50% of the heating power.
* Wi-Fi connectivity: The Lydos can be connected to your home Wi-Fi network, which allows you to control the heater from anywhere using your smartphone or tablet.
* Multiple heating modes: The Lydos has three different heating modes: Eco, Comfort, and Boost. Eco mode is the most energy-efficient, while Comfort mode provides a faster heating time. Boost mode is the fastest heating mode, but it is also the least energy-efficient.
* Easy to use: The Lydos is very easy to use. The control panel is simple and straightforward, and the Wi-Fi connectivity makes it easy to control the heater from anywhere.

## How to Use the Ariston Lydos Hybrid Wi-Fi Water Heater
To use the Ariston Lydos Hybrid Wi-Fi water heater, follow these steps:

1. Install the heater according to the manufacturer's instructions.
2. Connect the heater to the home Wi-Fi network.
3. Download the Ariston Net app on a smartphone or tablet.
4. Create an account and log in to the app.
5. Select the heater from the list of available devices.
6. You can now control the heater using the app.

## Conclusion
The Ariston Lydos Hybrid Wi-Fi water heater is an excellent choice for those looking for an energy-efficient and convenient way to heat their water. With its hybrid heating technology, the Lydos can save you up to 50% on your energy bills. And with its Wi-Fi connectivity, you can control the heater from anywhere using your smartphone or tablet.



With an average of 190W consumption when using the heat pump and 1.200W when using the resistor, it also supports a mixed mode with a maximum consumption of 1.420W.

The heat pump can heat the water only up to 53°C, with the resistor mode used to reach higher temperatures.

I prefer to adjust the heating to a lower temperature to open the hot tap without mixing cold water. For me, it means keeping the heater around 45ºC.

In heat pump mode, the pump only starts when the temperature is more than 5° below the intended temperature. Wi-Fi connectivity allows one to program it in detail by using, for example, Home Assistant as the bridge and itself or HomeKit as the central programming system.

* Ariston Net at Apple Store: https://apps.apple.com/app/ariston-net/id980286873
* Ariston Net at Google Play Store: https://play.google.com/store/apps/details?id=com.remotethermo.aristonnet


## Problem Resolution

Q: My app doesn't start aymore and only shows "connecting".
Q: HomeAssistant connects to Ariston servers and times out without an response.

* On the heater screen, long press the Wi-Fi button until "AP" appears on the screen
* Uninstall Ariston Net just in case to fully reset the state of the app
* Reinstall Ariston Net and log in with the current account
* When the app states it can't get information from the heater, reset the heater
* Follow the standard connectivity process - approve local network discovery, allow to connect to the heater's temporary Wi-Fi network, select the home network, and enter its password.
* Double-check that the app starts properly again and can manage the heater.
* Restart the HomeAssistant daemon to force it to reconnect to Ariston's servers if it doesn't do it automatically.
* Confirm that HomeKit sees the heater again.
