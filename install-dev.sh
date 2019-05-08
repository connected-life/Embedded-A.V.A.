#!/bin/bash
OPTS=`getopt -o n --long no-model -- "$@"`
if [[ $? != 0 ]] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi
eval set -- "${OPTS}"

NO_MODEL=false
while true; do
  case "$1" in
    -n | --no-model ) NO_MODEL=true; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done
NO_MODEL=${NO_MODEL}

apt-get update
apt-get -y install debhelper python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev && \
apt-get -y install dpkg python3-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip python3-setuptools python3-wheel libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool libgtk2.0-0 gir1.2-gtk-3.0 && \

pip3 install -e .

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
CHECKSUM="21198f6b6f24ef1f45082aebc6fd452e"

DRAGONFIRE_DIR=/usr/share/ava
if [[ ! -d "$DRAGONFIRE_DIR" ]]; then
  mkdir ${DRAGONFIRE_DIR}
fi

DEEPSPEECH_DIR=/usr/share/ava/deepspeech
if [[ "$NO_MODEL" = false ]] ; then
    if [[ ! -d "$DEEPSPEECH_DIR" ]]; then
      mkdir ${DEEPSPEECH_DIR}
    fi
    cd ${DEEPSPEECH_DIR}
    verified=$(md5sum models/* | md5sum)
    if [[ ! ${verified::-3} = "$CHECKSUM" ]]; then
      wget -nc -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz | tar xvfz -
    fi
fi

pip3 install --upgrade tinydb==3.9.0.post1 pyowm==2.9.0 tensorflow==1.0.0 deepspeech==0.4.1 SpeechRecognition metadata_parser==0.9.20 requests==2.20.0 msgpack==0.5.6 psutil>=5.4.2 paho-mqtt>=1.4.0 && \
pip3 install --upgrade flake8 sphinx sphinx_rtd_theme recommonmark m2r pytest && \
echo -e "\n\n${GREEN}Embedded-A.V.A. is successfully installed to your computer.${NC}\n"

