# Embedded-A.V.A.

the embedded access point to A.V.A. remotely for raspberry pi distributions


<br>

#### Supported Environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | Raspbian                                |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
|                         |                                         |

### Requirements

##### Hardware
  
- Raspberry Pi zero, 2,3 B, B + or higher
- An audio I/O unit

##### Software

Enable a larger swap file size (so the deepspeech compile won't fail due to limited memory)
```Shell
sudo nano /etc/dphys-swapfile

< change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024 and save / exit nano >

sudo /etc/init.d/dphys-swapfile restart
```
<sup> After installation, it can be reverted. </sup>

### Installation

Clone the GitHub repository and run

```Shell
sudo ./install.sh
```

in the repository directory.

for development mode: `sudo ./install-dev.sh`


<sup><i>If there is a failure try `sudo -H ./install-dev.sh`</i></sup>

### Usage <a href="https://t-system.readthedocs.io/en/latest/t_system.html"><img src="https://media.readthedocs.com/corporate/img/header-logo.png" align="right" height="25px" /></a>


```
usage: embedded_ava [-h] [-c] [-s] [-j] [-v] [-g] [-a] [--version]

optional arguments:
  -h, --help       show this help message and exit
  -c, --cli        Command-line interface mode. Give commands to Dragonfire
                   via command-line inputs (keyboard) instead of audio inputs
                   (microphone).
  -s, --silent     Silent mode. Disable Text-to-Speech output. Dragonfire
                   won't generate any audio output.
  -j, --headless   Headless mode. Do not display an avatar animation on the
                   screen. Disable the female head model.
  -v, --verbose    Increase verbosity of log output.
  -g, --gspeech    Instead of using the default speech recognition
                   method(Mozilla DeepSpeech), use Google Speech Recognition
                   service. (more accurate results)
  -a, --augmented  Augmented mode. Reach A.V.A. remotely and use its features.
  --version        Display the version number of Dragonfire.

```

<br>

### Augmented

Augmented mode is necessary for forwarding commands to [A.V.A.](https://github.com/MCYBA/A.V.A.) to controlling the assistant remotely.

<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

<sup><i>this code based from [here](https://github.com/DragonComputer/Dragonfire).</i></sup>