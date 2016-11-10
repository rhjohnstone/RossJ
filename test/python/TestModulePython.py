import unittest
import rossj

class TestRossManualClass(unittest.TestCase):

    def test_rossj(self):
        message = 'hello world'
        ross = rossj.RossManual(message)

if __name__ == '__main__':
    unittest.main()
