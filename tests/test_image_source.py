import unittest
import os
from io import BytesIO
from unittest.mock import patch, MagicMock

from lgtm.image_source import (
  LocalImage,
  RemoteImage,
  KeywordImage,
  ImageSource,
  get_image
)


class TestLocalImage(unittest.TestCase):

  def setUp(self):
    self.test_file = "test_local_img.txt"
    with open(self.test_file, "wb") as f:
      f.write(b"dummy-data")


  def testDown(self):
    if os.path.exists(self.test_file):
      os.remove(self.test_file)


  def test_local_image_source(self):
    img = LocalImage(self.test_file)
    f = img.get_image()
    self.assertTrue(hasattr(f, "read"))
    self.assertEqual(f.read(), b"dummy-data")
    f.close()


  def test_local_image_not_found(self):
    img = LocalImage("not_exist_file.jpg")
    with self.assertRaises(FileNotFoundError):
      img.get_image()


class TestRemoteImage(unittest.TestCase):

  @patch("lgtm.image_source.requests.get")
  def test_keyword_image_url_build(self, mock_get):
    mock_response = MagicMock()
    mock_response.content = b"keyword-image"
    mock_get.return_value = mock_response

    img = KeywordImage("dog")
    f = img.get_image()

    expected_url = "https://loremflicker.com/800/600/dog"
    mock_get.assert_called_once_with(expected_url)

    self.assertEqual(f.read(), b"keyword-image")


class TestKeywordImage(unittest.TestCase):

  @patch("lgtm.image_source.requests.get")
  def test_keyword_image_url_build(self, mock_get):
    mock_response = MagicMock()
    mock_response.content = b"keyword-image"
    mock_get.return_value = mock_response

    img = KeywordImage("dog")
    f = img.get_image()

    expected_url = "https://loremflicker.com/800/600/dog"
    mock_get.assert_called_once_with(expected_url)

    self.assertEqual(f.read(), b"keyword-image")

class TestImageSourceSelector(unittest.TestCase):

  def setUp(self):
    self.test_file = "sample.txt"
    with open(self.test_file, "wb") as f:
      f.write(b"sample")


  def tearDown(self):
    if os.path.exists(self.test_file):
      os.remove(self.test_file)


  def test_select_remote(self):
    result = ImageSource("https://example.com")
    self.assertIsInstance(result, RemoteImage)


  def test_select_local(self):
    result = ImageSource(self.test_file)
    self.assertIsInstance(result, LocalImage)


  def test_select_keyword(self):
    result = ImageSource("keyword")
    self.assertIsInstance(result, KeywordImage)


class TestGetImage(unittest.TestCase):

  @patch("lgtm.image_source.requests.get")
  def test_get_image_from_url(self, mock_get):
    mock_response = MagicMock()
    mock_response.content = b"url-image"
    mock_get.return_value = mock_response

    f = get_image("https://example.com/test.png")
    self.assertEqual(f.read(), b"url-image")


if __name__ == "__main__":
  unittest.main()