import unittest

from bridgecrew.terraformscanner.scanner_registry import ResourceScannerRegistry


class TestScannerRegistry(unittest.TestCase):

    def test_num_of_scanners(self):
        registry = ResourceScannerRegistry()
        scanners_counter = 0
        for key in list(registry.scanners.keys()):
            scanners_counter+=len(registry.scanners[key])

        self.assertEqual(41,scanners_counter)




if __name__ == '__main__':
    unittest.main()
