import urllib.request
import urllib.parse
import urllib.error
import urllib.robotparser
import re
import sys
import imghdr
import os
from urllib.parse import urlparse

def extract_images(seed):
  links = extract_links(seed, get_page(seed))
  return links


def get_page(url):
    page = ""
    try:
        with urllib.request.urlopen(url) as page:
            page = page.read().decode('UTF-8')
    except:
        raise sys.exc_info()[0]
    finally:
        return page

def extract_links(base_url, page):
    urls = set()

    captured = set(re.findall(r'<img[^>]*\ssrc="(.*?)"', page))

    for img_src in captured:
        img_src_parsed = urlparse(img_src)
        if not img_src_parsed.netloc:
            img_src = urllib.parse.urljoin(base_url, img_src)
        if not img_src_parsed.scheme and not img_src.startswith("http"):
            print("img_src has no scheme, adding http:", img_src)
            img_src = "http:" + img_src
        urls.add(img_src)

    return urls

def download_image(link, file_path, name):
  print("downloading:",link)
  try:
    image_bytes = urllib.request.urlopen(link).read()
    image_extension = imghdr.what("", h=image_bytes)
    if not image_bytes or not image_extension:
      raise NameError("No image was downloaded!")
  except:
    raise sys.exc_info()[0]
  else:
    file_path = os.path.join(file_path, str(name) + "." + image_extension)

    f = open(file_path, 'wb')
    f.write(image_bytes)

    f.close()

def main():

    args = sys.argv

    seed_url = args[1]
    folder = os.path.expanduser(args[2])
    crawl_path = extract_images(seed_url)

    counts = len(crawl_path)

    
    count = 1
    for image_path in crawl_path:
      print("Downloading ({:d}/{:d}): {:s}".format(count, counts, image_path))
      try:
        download_image(image_path, folder, count)
        count += 1
      except:
        print("Cannot download", image_path)

    print("Finished operation")


if __name__ == '__main__':
    main()