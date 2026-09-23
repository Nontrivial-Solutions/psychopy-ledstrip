"""Marks the package containing the Psychopy Ledstrip plugin hardware wrapper."""

from lib2to3.pytree import Base
from pathlib import Path

from psychopy import constants, logging
from psychopy.experiment import Experiment
from psychopy.hardware import DeviceManager
from psychopy.hardware.listener import BaseListener
from psychopy_fastrak.hardware import FastrakHardwareDevice

from ..hardware import LedstripHardwareDevice


class LedFastrakListner(BaseListener):
    def __init__(self):
        BaseListener.__init__(self)

    def receiveMessage(self, message):
        """
        Method defining what to do when receiving a message. Must be implemented by subclasses.

        Parameters
        ----------
        message
            Message received.
        """
        with open('./data/out.log', 'a') as file:
            file.write(f'{message}\n=============\n\n')


class LedstripWrapper:
    """Wraps a Psychopy Ledstrip hardware device for use in a Psychopy component.

    Attributes
    ----------
    _device : LedstripHardwareDevice
        The Ledstrip device to wrap.
    _outputPath : Path
        The path (relative to the data directory) to store a data file.
        >[!note]
        > Also serves as an "ID" when logging.
    _status : int
        The Base device status. The values are derived from consts in a [SimpleNamespace which is essentially a
        Dict](https://docs.python.org/3/library/types.html#types.SimpleNamespace).
        > [!warning]
        > This is **NOT** an [Enum](https://docs.python.org/3/library/enum.html).
    _hasDeviceLock : bool
        Indicates if this instance of the wrapper believes it holds the lock on its hardware device.
    _counter : int
        The number of times this wrapper has run. 1 indexed.
    """

    _ledDevice: LedstripHardwareDevice
    _fastrakDevice: FastrakHardwareDevice
    _listener: LedFastrakListner
    _outputPath: Path
    _status: int
    _hasDeviceLock: bool
    _counter: int

    def __init__(
        self, ledDevice: str, fastrakDevice: str, outputDir: str = '.'
    ) -> None:
        """Initialize the wrapper object.

        Parameters
        ----------
        device : str
            The name of the hardware device to wrap.

        outputDir : str
            The path (relative to the data directory) to store a data file.
        """
        if not isinstance(ledDevice, str) or ledDevice not in DeviceManager.devices:
            raise ValueError(
                f"Could not find device named '{ledDevice}', make sure it has been set up in DeviceManager."
            )  # TODO: Add specific exception object

        self._outputPath = Path(outputDir)
        self._ledDevice = DeviceManager.getDevice(ledDevice)
        self._fastrakDevice = DeviceManager.getDevice(fastrakDevice)
        self._listener = LedFastrakListner()
        self._fastrakDevice.addListener(self._listener)
        self._status = constants.NOT_STARTED

    @property
    def status(self) -> int:
        """Wrapper Status attribute.

        Returns
        -------
        int
            Indicates the status of the wrapper.
            > [!warning]
            > This is **NOT** an [Enum](https://docs.python.org/3/library/enum.html).

        """
        return self._status

    @status.setter
    def status(self, status: int) -> None:
        """Set the wrapper Status attribute."""
        self._status = status