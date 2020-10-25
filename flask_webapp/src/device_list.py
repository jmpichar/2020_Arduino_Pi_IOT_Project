"""
File:
    device_list.py
Description:
    Describes bluetooth device container for managing device instances.
Classes:
    BtDevContainer
Author:
    Adoany Berhe
"""
import __init__
import bluetooth
from bluetooth.ble import DiscoveryService
from device import Bt_Ble_Device, Bt_Device

class BtDevContainer(object):
    """
    Brief:
        BtDevContainer(): Container class for holding all bt device instances and apis
    Description:
        This class will discover all peripheral devices and provide APIs for sending and receiving
            commands.
    Methods:
        _scan_for_bt_regular_devices, _scan_for_bt_ble_devices, _is_verified_bt_dev, get_device
    """
    def __init__(self):
        """

        """
        self._bt_name_dev_dict = {}     # name -> device

    def _scan_for_bt_regular_devices(self):
        """
        Brief:
            _scan_for_bt_regular_devices(): scan for regular bluetooth devices and collect into a list.
        Description:
            The following function will be used to scan for bt devices within a 30m radius of
                the raspberry pi.
        """
        devices = bluetooth.discover_devices(lookup_names=True)
        for device in devices:
            addr, name = device
            if self._is_verified_bt_dev(name):
                self._bt_name_dev_dict[name] = Bt_Device(addr)

    def _scan_for_bt_ble_devices(self):
        """
        Brief:
            _scan_for_bt_ble_devices():  scan for ble devices and collect into a list.
        Description:
            The following function will be used to scan for bt devices within a 30m radius of
                the raspberry pi.
        """
        service = DiscoveryService()
        devices = service.discover(2)
        for addr, name in zip(devices.keys(), devices.values()):
            if self._is_verified_bt_dev(name):
                self._bt_name_dev_dict[name] = Bt_Ble_Device(addr)

    def _is_verified_bt_dev(self, name):
        """
        Brief:
            _is_verified_bt_dev(name): verify the dev object is desired device under test.
        Description:
            This function will be used for issuing a test to identify desired arduino devices
                in the bluetooth range.
        Param(s):
            name: name of the device that appeared in a bluetooth scan.
        Return:
            True on verified device, False on every other component.
        """
        return "arduino" in name.lower()

    def scan(self):
        """
        Brief:
            scan(): public api for issuing a bluetooth device scan.
        Description:
            This api issues a scan for smart bluetooth and ble bluetooth devices; performs
                a verification test for filtering non-arduino devices and returns device names.
        Return:
            list of device name strings.
        """
        self._scan_for_bt_ble_devices()
        #self._scan_for_bt_regular_devices()
        active_dev_list = list(self._bt_name_dev_dict.keys())
        print(f"Discovered {len(active_dev_list)} valid bluetooth devics.")
        return active_dev_list

    def send_bluetooth_msg(self, name, msg_name):
        """
        Brief:
            send_bluetooth_msg(addr, msg): generic message sending api.
        Description:
            This function will be used to issue any commands to the peripheral device and return
                values if any.
        Param:
            name: bluetooth device name.
        Param(s):
            msg_name: bluetooth message name string to be sent to the peripheral device.
        Return:
             True on success, False on failure.
        """
        retVal = False
        try:
            retVal = self._bt_name_dev_dict[name].send_message(msg_name)
        except ValueError as error:
            print(f"Device {name} does not exist.")
            retVal = False

        # Todo: Figure out a way to propagate error message
        return retVal

    def get_device(self, name):
        """
        Brief:
            get_device(name): returns a bluetooth device objects.
        Description:
            This function takes a name string of the desired device, checks if object instance
                exists (checks for key-value exceptions) and returns either object or None with message.
        Param(s):
            name: string value of the device name.
        Return
            Bt_Device or Bt_Ble_Device device instance on success; None on failure.
        """
        try:
            return self._bt_name_dev_dict[name]
        except KeyError:
            print(f"Device name: {name} is not found. Raising exception.\n{KeyError}")
            raise KeyError



