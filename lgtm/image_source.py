import requests

class LocalImage:
  """ファイルから画像を取得"""
  def __init__(self, path):
    self._path = path

  def get_image(self):
    return open(self._path, 'rb')