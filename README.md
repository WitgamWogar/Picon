Picon
=====

An open source tool for configuring network settings on raspberry pi.
The main use for this tool is to customize your raspberry pi settings without having to hook it up to a tv. This works well when configuring many Raspberries in a short period of time. 

===================
Version 0.2 release

- Fixed Bug: Not working for WPA2 networks. Now the scripts asks for your security type and handles it appropriately.

- Included libraries so the end user does not have to install them such as paramiko

- Moved autoexec and video uploading code from main script to text document as this is a niche feature.

- Cleaned up how variables are handled.

===================

Version 0.3 planned features:
- Compatibility with all possible Raspberry Pi operating systems
- Validation on all inputs
- Customize the advancedsettings.xml file from the program itself, enabling alteration of things like screensaver, airplay, passwords, webservers, zeroconf, staytime ext...


==================

Version 0.4 planned features:
- GUI
- Web GUI
- .exe version


