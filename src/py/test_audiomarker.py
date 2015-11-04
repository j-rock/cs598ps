import unittest
from audiomarker import AudioMarker

# utility method for testing invalid argument values
# for AudioMarker
def init_throws_exception(min,sec):
    try:
        m = AudioMarker(min,sec);
    except ValueError:
        return True
    return False

class TestAudioMarker(unittest.TestCase):
    """
    Tests for the AudioMarker class
    """

  def test_string(self):
      m = AudioMarker(3,4);
      self.assertEqual(str(m), '03:04')
      m = AudioMarker(13,4);
      self.assertEqual(str(m), '13:04')

  def test_init_invalidvalues(self):
      """
      AudioMarker should only be created with min and sec in range
      [0,59]
      """
      self.assertEqual(init_throws_exception(0,59), False)
      self.assertEqual(init_throws_exception(-13,4), True)
      self.assertEqual(init_throws_exception(13,-4), True)
      self.assertEqual(init_throws_exception(-13,-4), True)
      self.assertEqual(init_throws_exception(0,60), True)
      self.assertEqual(init_throws_exception(60,0), True)
      self.assertEqual(init_throws_exception(60,60), True)

  def test_getters(self):
      m = AudioMarker(3,4);
      self.assertEqual(m.getMin(), 3)
      self.assertEqual(m.getSec(), 4)
