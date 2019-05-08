#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of Embedded-A.V.A. that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import argparse  # Parser for command-line options, arguments and sub-commands
import datetime  # Basic date and time types
import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces
import subprocess  # Subprocess managements
import sys  # System-specific parameters and functions
import threading
import requests

try:
    import thread  # Low-level threading API (Python 2.7)
except ImportError:
    import _thread as thread  # Low-level threading API (Python 3.x)
import time  # Time access and conversions
import uuid  # UUID objects according to RFC 4122
from multiprocessing import Event, Process  # Process-based “threading” interface
from os.path import expanduser  # Common pathname manipulations
from random import choice  # Generate pseudo-random numbers
import shutil  # High-level file operations
import readline #GNU readline Interface

from embedded_ava.utilities import TextToAction, nostdout, nostderr  # Submodule of Dragonfire to provide various utilities

from embedded_ava.augmented import Augmenter
from embedded_ava.augmented.mqtt import MqttReceimitter

from tinydb import Query, TinyDB  # TinyDB is a lightweight document oriented database optimized for your happiness

__version__ = '0.0.1'

DRAGONFIRE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
FNULL = open(os.devnull, 'w')
GENDER_PREFIX = {'male': 'Sir', 'female': 'My Lady'}
CONVERSATION_ID = uuid.uuid4()
userin = None

try:
    raw_input  # Python 2
except NameError:
    raw_input = input  # Python 3


def start(args, userin):
    """Function that starts the virtual assistant with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
        userin:     :class:`ava.utilities.TextToAction` instance.
    """

    # if 'TRAVIS' in os.environ or args["db"] == "mysql":
    #     engine = create_engine('mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASS + '@' + Config.MYSQL_HOST + '/' + Config.MYSQL_DB)
    # else:
    #     engine = create_engine('sqlite:///ava.db', connect_args={'check_same_thread': False}, echo=True)
    # Base.metadata.create_all(engine)
    # Base.metadata.bind = engine
    # DBSession = sessionmaker(bind=engine)
    # db_session = DBSession()
    # learner.db_session = db_session

    # global user_full_name
    # global user_prefix
    # global ava_name
    # global email_manager
    if args["cli"]:
        her = EmbeddedVA(args, userin, user_full_name, user_prefix, ava_name)
        while True:
            com = raw_input("Enter your command: ")
            thread.start_new_thread(her.command, (com,))
            time.sleep(0.5)
    elif args["gspeech"]:
        from embedded_ava.sr.gspeech import GspeechRecognizer

        her = EmbeddedVA(args, userin, user_full_name, user_prefix, ava_name)
        recognizer = GspeechRecognizer()
        recognizer.recognize(her)
    else:
        from embedded_ava.sr.deepspeech import DeepSpeechRecognizer

        her = EmbeddedVA(args, userin, user_full_name, user_prefix, ava_name)
        recognizer = DeepSpeechRecognizer()
        recognizer.recognize(her)


class EmbeddedVA:
    """Class to define a portable virtual assistant.

    This class provides necessary initiations and a function named :func:`ava.VirtualAssistant.command`
    as the entry point for each one of the user commands.

    .. note::

        This class is not used in the API.

    """

    def __init__(self, args, userin, user_full_name="John Doe", user_prefix="sir", ava_name="A.V.A.", tw_user=None, testing=False):
        """Initialization method of :class:`embedded_ava.EmbeddedVA` class.

        Args:
            args:       Command-line arguments.
            userin:     :class:`embedded_ava.utilities.TextToAction` instance.

        Keyword Args:
            user_full_name (str):       User's full name  to answer some basic questions
            user_prefix (str):          Prefix to address/call user when answering
            tw_user (str):              Twitter username of the person querying DragonfireAI Twitter account with a mention
        """

        self.args = args
        self.userin = userin
        self.user_full_name = user_full_name
        self.user_prefix = user_prefix
        self.ava_name = ava_name
        self.userin.twitter_user = tw_user
        self.testing = testing
        self.inactive = True
        if self.testing:
            home = expanduser("~")
            dot_ava_dir = home + "/.ava"
            self.config_file = TinyDB(dot_ava_dir + '/config.json')

        if self.args["augmented"]:
            self.augmenter = Augmenter('192.168.1.21', self)
        # thread_ = threading.Thread(target=email_manager.passive_check, args=(self.userin, self.user_prefix))
        # thread_.start()
        # thread.start_new_thread(reminder.remind, (note_taker, userin, user_prefix, user_answering_note))

    def command(self, com):
        """Function that serves as the entry point for each one of the user commands.

        This function goes through these steps for each one of user's commands, respectively:

         - Search across the built-in commands via a simple if-else control flow.
         - Try to get a response from remote user's own A.V.A. server.

        Args:
            com (str):  User's command.

        Returns:
            str:  Response.
        """
        args = self.args
        userin = self.userin
        user_full_name = self.user_full_name
        user_prefix = self.user_prefix
        ava_name = self.ava_name
        if args["augmented"]:
            augmenter = self.augmenter
        if self.testing:
            config_file = self.config_file

        if isinstance(com, str) and com:
            com = com.strip()
        else:
            return False

        print("You: " + com.upper())
        # doc = nlp(com)
        # h = Helper(doc)

        # if args["verbose"]:
        #     userin.pretty_print_nlp_parsing_results(doc)

        if check_network_connection():
            if args["augmented"]:
                augmenter.forward_com(com)
                return ''
        else:
            return userin.say(choice(["Sorry, ", "I'm sorry, ", "Bad situation, ", ""]) + choice([".", ", " + user_prefix + "."]) + choice(["I could not reach my servers.",
                                                                                                                                            "I have no connection with my servers.",
                                                                                                                                            "I lose my internet connection.",
                                                                                                                                            "I can't connect my database.",
                                                                                                                                            "I can not reach the servers."]))


def tts_kill():
    """The top-level method to kill/end the text-to-speech output immediately.
    """

    subprocess.call(["pkill", "flite"], stdout=FNULL, stderr=FNULL)


def greet(args, userin):
    """The top-level method to greet the user with message like "*Good morning, sir.*".

    Args:
        args:  Command-line arguments.
        userin:  :class:`embedded_ava.utilities.TextToAction` instance.

    Returns:
        str:  Response.
    """

    global user_full_name
    global user_prefix
    global config_file
    global ava_name
    global email_manager

    command = "getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1"
    user_full_name = os.popen(command).read()
    user_full_name = user_full_name[:-1]  # .decode("utf8")

    home = expanduser("~")
    dot_ava_dir = home + "/.ava"
    if not os.path.exists(dot_ava_dir):
        os.mkdir(dot_ava_dir)

    config_file = TinyDB(dot_ava_dir + '/config.json')

    if args['augmented'] and check_network_connection():
        her = EmbeddedVA(args, userin)

        if not her.augmenter.mqtt_receimitter.get_is_connected():
            user_prefix, ava_name = prepare_config(config_file)
        else:
            gender = her.augmenter.reach_config('gender')
            callme = her.augmenter.reach_config('callme')
            if callme:
                config_file.update({'title': callme}, Query().datatype == 'callme')
                user_prefix = callme
            else:
                config_file.update({'gender': gender}, Query().datatype == 'gender')
                user_prefix = GENDER_PREFIX[gender]
            ava_name = her.augmenter.reach_config('ava_name')
            config_file.update({'name': ava_name}, Query().datatype == 'name')
    else:
        user_prefix, ava_name = prepare_config(config_file)

        # email_manager = EmailManager()

    (columns, lines) = shutil.get_terminal_size()
    print(columns * "_" + "\n")
    time = datetime.datetime.now().time()

    if datetime.time(4) < time < datetime.time(12):
        time_of_day = "morning"
    elif datetime.time(12) < time < datetime.time(18):
        time_of_day = "afternoon"
    elif datetime.time(18) < time < datetime.time(22):
        time_of_day = "evening"
    else:
        time_of_day = "night"

    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "To activate say 'Dragonfire!' or 'Wake Up!'")
    return userin.say(" ".join(["Good", time_of_day, user_prefix]))


def prepare_config(config_file):
    """The top-level method to managing information to/from configuration file.

    Args:
        config_file:  .json file for holding config infos.
    """

    callme_config = config_file.search(Query().datatype == 'callme')
    name_config = config_file.search(Query().datatype == 'name')
    if callme_config:
        user_prefix = callme_config[0]['title']
    else:
        gender_config = config_file.search(Query().datatype == 'gender')
        if gender_config:
            user_prefix = GENDER_PREFIX[gender_config[0]['gender']]
        else:
            # gender = Classifier.gender(user_full_name.split(' ', 1)[0])
            gender = 'male'
            config_file.insert({'datatype': 'gender', 'gender': gender})
            user_prefix = GENDER_PREFIX[gender]

    if name_config:
        ava_name = name_config[0]['name']
    else:
        config_file.insert({'datatype': 'name', 'name': 'A.V.A.'})
        ava_name = 'A.V.A.'

    return user_prefix, ava_name


def check_network_connection():
    """The top-level method to checking network connection.

    Returns:
        bool:  status.
    """
    url = 'http://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        # userin.say("Internet connection could not be established.")
        pass
    return False


def speech_error():
    """The top-level method to indicate that there is a speech recognition error occurred.

    Returns:
        str:  Response.
    """
    cmds = [{'distro': 'All', 'name': ["echo"]}]
    userin.execute(cmds, "An error occurred")
    return userin.say("I couldn't understand, please repeat again.")


def initiate():
    """The top-level method to serve as the entry point of Embedded-A.V.A..

    This method is the entry point defined in `setup.py` for the `embedded_ava` executable that
    placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cli", help="Command-line interface mode. Give commands to Dragonfire via command-line inputs (keyboard) instead of audio inputs (microphone).", action="store_true")
    ap.add_argument("-s", "--silent", help="Silent mode. Disable Text-to-Speech output. Dragonfire won't generate any audio output.", action="store_true")
    ap.add_argument("-j", "--headless", help="Headless mode. Do not display an avatar animation on the screen. Disable the female head model.", action="store_true")
    ap.add_argument("-v", "--verbose", help="Increase verbosity of log output.", action="store_true")
    ap.add_argument("-g", "--gspeech", help="Instead of using the default speech recognition method(Mozilla DeepSpeech), use Google Speech Recognition service. (more accurate results)", action="store_true")
    ap.add_argument("-a", "--augmented", help="Augmented mode. Reach A.V.A. remotely and use its features.", action="store_true")
    ap.add_argument("--version", help="Display the version number of Dragonfire.", action="store_true")
    args = vars(ap.parse_args())

    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("ava").version)
        sys.exit(1)
    try:
        global dc
        userin = TextToAction(args)
        greet(args, userin)
        start(args, userin)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    initiate()
