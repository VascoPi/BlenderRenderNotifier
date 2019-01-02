# BlenderRenderNotifier

## Manual

#### Download

* Download [BlenderRenderNotifier for Blender 2.79](https://github.com/VascoPi/BlenderRenderNotifier/tree/master) or [BlenderRenderNotifier for Blender 2.80](https://github.com/VascoPi/BlenderRenderNotifier/tree/2.80) from my github repository.
* Stable release can be found in the [link](https://github.com/VascoPi/BlenderRenderNotifier/releases).
* Nightly release can be downloaded from the [master for Blender 2.79](https://github.com/VascoPi/BlenderRenderNotifier/archive/master.zip) or [brunch for Blender 2.80](https://github.com/VascoPi/BlenderRenderNotifier/archive/2.80.zip), only basic functionality is tested working.

#### Install

In preferences window choose Addon tab and press "Install Add-on from File...". Choose "blender_render_notifier.py".
It'll apper in Testing/Render category, enable it and set preferences.
After installation, you can find the the add-on at Properties section on Render tab.

#### Usage

Telegram notifies user about render status.
All you need, is to create Telegram Bot with [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot). You will get Token. Then get your User_id via [userinfobot](https://telegram.me/userinfobot) (just send message and you receive your info).
Paste your Token and User_id into addon preferences.

![](https://github.com/VascoPi/BlenderRenderNotifier/raw/master/help/Addon_preferences.jpg)


Aslo you can change them later.

![](https://github.com/VascoPi/BlenderRenderNotifier/raw/master/help/Addon_settings.jpg)

That's it! Next time you render, will get render info message from your bot.

Message example.

![](https://github.com/VascoPi/BlenderRenderNotifier/raw/master/help/Message_example.jpg)


## Support

* send render start info
* send render finish info


## Todo

* update manual
* send render image thumbnail
* set frame interval
