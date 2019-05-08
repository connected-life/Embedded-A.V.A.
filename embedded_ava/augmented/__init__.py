#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of Embedded-A.V.A.'s.augmented that contains the classes related to Embedded-A.V.A.'s simple if-else struct of Augmented abilities.

.. moduleauthors:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from multiprocessing import Event, Process  # Process-based “threading” interface
import time  # Time access and conversions

from embedded_ava.augmented.mqtt import MqttReceimitter


class Augmenter:
    """Class to define a send orders ability to remote devices.

        This class provides necessary initiations and a function named :func:`embedded_ava.augmented.Augmenter.check`
        as top-level function to checking users built-in commands.

        """

    def __init__(self, ip_addr, her):
        """Initialization method of :class:`embedded_ava.augmented.Augmenter` class.

        Args:
                ip_addr:       	        Ip address of the host.
                userin:                 :class:`ava.utilities.TextToAction` instance.


        """

        # Note to author: ip_addr = '10.42.0.151'
        self.her = her
        self.mqtt_receimitter = MqttReceimitter(ip_addr, self.her)

        mqtt_proc = Process(target=self.mqtt_receimitter.subscribe('Augmented/Portable_A.V.A.'))
        mqtt_proc.start()

    def check(self, doc, h, user_answering, userin, user_prefix):
        """Method to ava's command structures of controlling ability of remote IoT devices.

        Args:
            doc:                       doc of com from __init__.py
            h:                         doc helper from __init__.py
            user_answering:            User answering string array.
            userin:                    :class:`ava.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        # response = t_system.check(doc, h, self.mqtt_receimitter, user_answering, userin, user_prefix)
        # if response:
        #     return response

        return None

    def reach_config(self, reason):
        """The top-level method to provide remotely reaching information inside of config file of Embedded-A.V.A..

        Args:
            reason (str):              Reason of the reaching query, information type which is going to be from config file.
        """

        flag = {'from': 'Portable_A.V.A.', 'status': True, 'for': 'config_info', 'reason': reason, 'options': ''}
        self.mqtt_receimitter.publish('Augmented/A.V.A.', flag)
        # time.sleep(1)  # some check for waiting the result code will be here.

        return self.check_config_response(reason)

    def forward_com(self, com):
        """The top-level method to provide Embedded-A.V.A.'s incoming commands from the user, forward to the A.V.A..

        Args:
            com (str):                 User's command.
        """

        flag = {'from': 'Portable_A.V.A.', 'status': True, 'for': 'remote_com', 'reason': '', 'options': com}
        self.mqtt_receimitter.publish('Augmented/A.V.A.', flag)
        # time.sleep(1)  # some check for waiting the result code will be here.

    def check_config_response(self, reason):
        """The low-level method to checking response from remote A.V.A. for config information query.

        Args:
            reason (str):              Reason of the config information query. either 'gender', 'callme' or 'ava_name'.
        """
        while True:
            msgs = self.mqtt_receimitter.get_incoming_messages()

            for msg in msgs:
                if msg['from'] == 'A.V.A.':
                    if msg['for'] == 'config_info':
                        if msg['reason'] == reason:
                            self.mqtt_receimitter.incoming_messages['messages'].remove(msg)
                            return msg['options']

    def check_com_response(self, msgs):
        """The low-level method to checking response from remote A.V.A. when any message was came inside to :func:'mqtt_receimitter.client.on_message'.

        Args:
            msgs (list):               Incoming messages to the subscribing topic.
        """
        for msg in msgs:
            if msg['from'] == 'A.V.A.':
                if msg['for'] == 'remote_com':
                    self.mqtt_receimitter.incoming_messages['messages'].remove(msg)
                    self.her.userin.say(msg['options'])
