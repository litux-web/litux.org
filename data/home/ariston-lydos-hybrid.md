title: Ariston Lydos Hybrid Wi-Fi
last-updated: 2023-10
meta-keywords: Ariston, Lydos, Ariston Lydos, HomeKit, Termoaccumulator, Termoacumulador, Hybrid, Híbrido, Heat-Pump, Bomba de calor


{{{image:home/ariston-lydos-hybrid.jpg:Ariston Lydos Hybrid}}}The Ariston Lydos Hybrid Wi-Fi is a water heater with hybrid heating technology and Wi-Fi connectivity, with 80 and 100L capacities.

The heater supports a typical resistor heating as well as a heat pump, with configurable options via the mobile app as well as buttons on the device.

Although many heat pumps have an efficiency of more than 300%, the Lydos have, in my experience, an efficiency just slightly above 200%, which correlates with Ariston's claim of "50% savings".

With an average of 190W consumption when using the heat pump and 1.200W when using the resistor, it also supports a mixed mode with a maximum consumption of 1.420W.

The heat pump can heat the water only up to 53°C, with the resistor mode used to reach higher temperatures.

I prefer to adjust the heating to a lower temperature to open the hot tap without mixing cold water. For me, it means keeping the heater around 45ºC.

In heat pump mode, the pump only starts when the temperature is more than 5° below the intended temperature. Wi-Fi connectivity allows one to program it in detail by using, for example, Home Assistant as the bridge and itself or HomeKit as the central programming system.

* Ariston Net at Apple Store: https://apps.apple.com/app/ariston-net/id980286873
* Ariston Net at Google Play Store: https://play.google.com/store/apps/details?id=com.remotethermo.aristonnet


## Problem Resolution

Q: My app doesn't start aymore and only shows "connecting".
Q: HomeAssistant connects to Ariston servers and times out without an response.

On the heater screen, long press the Wi-Fi button until "AP" appears on the screen
Uninstall Ariston Net just in case to fully reset the state of the app
Reinstall Ariston Net and log in with the current account
When the app states it can't get information from the heater, reset the heater
Follow the standard connectivity process - approve local network discovery, allow to connect to the heater's temporary Wi-Fi network, select the home network, and enter its password.
Double-check that the app starts properly again and can manage the heater.
Restart the HomeAssistant daemon to force it to reconnect to Ariston's servers if it doesn't do it automatically.
Confirm that HomeKit sees the heater again.