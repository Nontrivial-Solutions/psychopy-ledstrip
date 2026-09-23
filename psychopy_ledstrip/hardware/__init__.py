"""Marks the package containing the Psychopy Ledstrip plugin hardware objects."""

from fastrakSerialDriver.fastrakPosition import FastrakPostion
from psychopy import logging
from psychopy.hardware.base import BaseDevice
from serial.tools import list_ports
from slasd.fastrakAnimator import FastrakAnimationDevice


class LedstripHardwareDevice(BaseDevice):
    """Psychopy hardware object for a Ledstrip.

    Attributes
    ----------
    _ftd : LedstripDevice
        Ledstrip serial driver object.

    _name : str
        The name of hardware object.

    _is_locked : bool
        Indicates if the object is locked. A hardware object can only be accessed by one experiment
        object at a time.

        - Locked when `True`
        - Unlocked when `False`

    _is_setup : bool
        The setup routine only needs to be called once per hardware device. This flag indicates when
        the setup has already been run.
    """

    _name: str
    _is_locked: bool
    _is_setup: bool
    _ledStrip: FastrakAnimationDevice
    _angleToLight: int
    _colorR: int
    _colorG: int
    _colorB: int

    def __init__(self, *args, **kwargs):
        """Initialize a Psychopy hardware object for a Ledstrip."""
        super().__init__()

        port = kwargs.get('port')
        if not isinstance(port, str):
            raise Exception(
                'Port input for Fastrak is not a string.'
            )  # TODO: Add specific Exception

        baudrate = kwargs.get('baudrate')
        if not isinstance(baudrate, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception

        ledCount = kwargs.get('ledCount')
        if not isinstance(ledCount, int):
            raise Exception(
                'Baudrate for Fastrak is not valid.'
            )  # TODO: Add specific Exception

        # Create a driver instance for the device.
        self._name = f'Ledstrip-{port}_{baudrate}KHz'
        self._is_setup = False
        self._baud = baudrate
        self._ledStrip = FastrakAnimationDevice(
            COMport=port, baud=baudrate, ledCount=ledCount, setup=False
        )

    def isSameDevice(self, other: 'LedstripHardwareDevice') -> bool:
        """Determine whether this object represents the same physical device as a given `other` object.

        > [!note]
        > This is a `BaseResponseDevice` interface.

        Parameters
        ----------
        other : LedstripHardwareDevice
            Other device object to compare against.

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        return (
            isinstance(other, LedstripHardwareDevice)
            and other._ledStrip == self._ledStrip
        )

    @staticmethod
    def getAvailableDevices() -> list[dict]:
        """Get all available Ledstrip Hardware Devices.

        > [!note]
        > This is a `BaseResponseDevice` interface.

        -------
        list[dict]
            List of dictionaries containing the parameters needed to initialize each device.
        """
        ports = list_ports.comports()
        ledstripDevices = []
        for device in ports:
            ledstrip = {
                'deviceName': f'Ledstrip@{device.device}',
                'deviceClass': 'psychopy_ledstrip.hardware.LedstripHardwareDevice',
                'port': device.device,
            }
            ledstripDevices.append(ledstrip)
        return ledstripDevices

    @property
    def name(self) -> str:
        """Name attribute of the object.

        Returns
        -------
        str
            The name attribute of the object.


        """
        return self._name

    def setLedState(self, pos: FastrakPostion) -> None:

        self._ledStrip.compNSndState(
            posData=pos,
            angleToLight=self._angleToLight,
            colorR=self._colorR,
            colorG=self._colorG,
            colorB=self._colorB,
        )
