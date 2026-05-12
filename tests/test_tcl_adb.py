import unittest
from unittest.mock import patch, MagicMock
from tv.tcl_adb import TclAdbTV

class TestTclAdbTV(unittest.TestCase):
    def test_init(self):
        config = {
            'IP': '192.168.1.100',
            'HDMI': 1,
            'PlayStopUri': 'app=emby'
        }
        tv = TclAdbTV(config)
        self.assertEqual(tv._ip, '192.168.1.100')

    @patch('tv.tcl_adb.AdbDeviceTcp')
    def test_connect(self, mock_adb_tcp):
        mock_device = MagicMock()
        mock_adb_tcp.return_value = mock_device
        
        config = {'IP': '192.168.1.100'}
        tv = TclAdbTV(config)
        tv._connect()
        
        mock_adb_tcp.assert_called_with('192.168.1.100', 5555, default_transport_timeout_s=9)
        mock_device.connect.assert_called()

    @patch('tv.tcl_adb.AdbDeviceTcp')
    def test_play_begin_hdmi1(self, mock_adb_tcp):
        mock_device = MagicMock()
        mock_device.available = True
        mock_adb_tcp.return_value = mock_device
        
        config = {'IP': '192.168.1.100', 'HDMI': 1}
        tv = TclAdbTV(config)
        tv.play_begin(None)
        
        # targetSourceId 8 for HDMI 1
        expected_cmd = "am start -n com.tcl.tv/.TVActivity --ei targetSourceId 8 --es referer adb"
        mock_device.shell.assert_called_with(expected_cmd)

    @patch('tv.tcl_adb.AdbDeviceTcp')
    def test_play_end_default_emby(self, mock_adb_tcp):
        mock_device = MagicMock()
        mock_device.available = True
        mock_adb_tcp.return_value = mock_device
        
        # Test default behavior when PlayStopUri is None
        config = {'IP': '192.168.1.100', 'PlayStopUri': None}
        tv = TclAdbTV(config)
        tv.play_end(None)
        
        expected_cmd = "am start -n com.mb.android/com.mb.android.MainActivity"
        mock_device.shell.assert_called_with(expected_cmd)

    @patch('tv.tcl_adb.AdbDeviceTcp')
    def test_play_end_kodi(self, mock_adb_tcp):
        mock_device = MagicMock()
        mock_device.available = True
        mock_adb_tcp.return_value = mock_device
        
        config = {'IP': '192.168.1.100', 'PlayStopUri': 'app=kodi'}
        tv = TclAdbTV(config)
        tv.play_end(None)
        
        expected_cmd = "am start -n org.xbmc.kodi/org.xbmc.kodi.Main"
        mock_device.shell.assert_called_with(expected_cmd)
