import sys
import os
import re
import argparse
import datetime
import markdown
import subprocess
import tempfile
import hashlib

DATA_FOLDER = "data"
HTML_FOLDER = "docs"
DELETE_FILES = (".DS_Store",)
IGNORED_FILES = (
  "CNAME",
  "robots.txt",
  "sitemap.xml",
  "favicon.ico",
  "apple-touch-icon.png",
  "apple-touch-icon-precomposed.png",
  "images/",
  "css/",
  "js/",
)
IGNORED_FILES += ("ads.txt", "seobilityverify_6966967.html")

DEFAULT_PARAMS = {}
CMDLINE_ARGS = None
ALL_PAGES = []


# NOTES
# external links icon via css https://stackoverflow.com/questions/5379752/css-style-external-links


def process_file_if_changed(
  data_root, html_root, data_folder, data_file, html_folder, html_file
):
  global CMDLINE_ARGS
  if not CMDLINE_ARGS.force:
    data_path = os.path.join(data_root, data_folder, data_file)
    html_path = os.path.join(html_root, html_folder, html_file)
    if os.path.exists(html_path):
      data_mtime = os.stat(data_path)
      html_mtime = os.stat(html_path)
      if data_mtime.st_mtime == html_mtime.st_mtime:
        return 0

  return process_file(
    data_root, html_root, data_folder, data_file, html_folder, html_file
  )


def parse_data(data, params=DEFAULT_PARAMS):
  new_data = []
  new_params = {}
  allow_more_params = True
  for line in data:
    if re.match("^\s*$", line) and len(new_params):  # empty line after data
      allow_more_params = False
    if allow_more_params:
      if re.match("^\s*#\s", line):  # comment
        continue
      m = re.match("^\s*([^:]+)\s*:\s*(.+?)\s*(#.*)?$", line)
      if m:
        new_params[m.group(1).strip()] = m.group(2).strip()
        continue
      allow_more_params = False
    new_data.append(line)
  new_data = "\n".join(new_data)
  params = params.copy()
  params.update(new_params)
  return new_data, params

def param_is(params, key, value):
    if value is True:
      return key in params
    #return value in [x.strip() for x in params.get(key,"").strip().lower().split(",")]
    return params.get(key,"").strip().lower() == value


def get_files(data_folder=DATA_FOLDER, folder=""):
  """html_path, last-updated, folder, params"""
  files = []
  for file in os.listdir(os.path.join(data_folder, folder)):
    data_path = os.path.join(data_folder, folder, file)
    if os.path.isdir(data_path):
      files += get_files(data_folder, os.path.join(folder, file))
    elif not folder and file == "index.md":
      continue
    elif file.endswith(".md"):
      with open(data_path, "r") as f:
        data = f.readlines()
      data, params = parse_data(data, params=DEFAULT_PARAMS)
      if "type" in params and params["type"] == "draft":
        continue
      if "redirect" in params:
        continue
      if param_is(params, "no-index", True):
        continue
      html_path = os.path.join(folder, f"{file[:-3]}.html")
      mtime = os.stat(data_path)
      last_updated = datetime.datetime.fromtimestamp(mtime.st_mtime).strftime(
        "%Y-%m-%d %H:%M:%S"
      )
      files.append(
        (
          html_path,
          params.get("last-updated", last_updated),
          folder,
          params,
        )
      )
  # end for
  files.sort(key=lambda x: x[1], reverse=True)
  return files

CACHE_HASHES = {}

def hash_string(s):
  m = hashlib.sha256()
  m.update(s.encode("utf-8"))
  return m.hexdigest()


def get_hash(file, key=None, html=None):
  global CACHE_HASHES

  data = ''
  data_hash = ''
  if file.startswith("http"):
    filename = file
  elif file.startswith("/"):
    filename = f"docs{file}"
    if not os.path.exists(filename):
      raise Exception(f"File not found '{filename}")
  elif file.startswith("text"):
    regexp = ".*" + re.escape("{{{" + key + "}}}") + "[^>]*>([^<]+)<.*"
    matches = re.match(regexp, html, re.DOTALL)
    data = matches[1]
    data_hash = hash_string(data)
    if data_hash in CACHE_HASHES:
      return CACHE_HASHES[data_hash]
    filename = tempfile.mktemp()
    with open(filename, "w+") as f:
      f.write(data)
  else:
    raise Exception(f"Unknown file '{file}")

  if filename in CACHE_HASHES:
    return CACHE_HASHES[filename]
  #print(f"Generating hash for '{data or filename}'")
  p = subprocess.run([ 'scripts/integrity', filename], stdout=subprocess.PIPE, check=True, text=True)
  hash = p.stdout.strip()
  hash = f"sha384-{hash}"
  if data:
    CACHE_HASHES[data_hash] = hash
  else:
    CACHE_HASHES[filename] = hash
  return hash


def get_index(filter_year=None, limit=0, params=DEFAULT_PARAMS):
  global ALL_PAGES
  # print(files)
  # return f"{files}"
  cur_year = None
  res = """      <div class="index">"""
  for file in ALL_PAGES:
    type = file[3].get("type", "")
    if type in ["home", "archive", "error"] :
      continue
    if type != "article" or param_is(file[3], "no-index", True):
      print(f"SKIP INDEX {file}")
      continue
    if filter_year and filter_year != file[1][0:4]:
      continue
    limit -= 1
    if limit == 0:
      break

    year = file[1][:4]
    if year != cur_year:
      if cur_year:
        res += """          </ul>\n"""
      if not filter_year:
        res += f"""<h2>{year}</h2>"""
      res += f"""\n        <ul>\n"""
      cur_year = year
    section = file[2]
    section = params.get(f"alias-{section}", section)
    last_updated = file[1]
    last_updated_machine = last_updated.replace(" ", "T")
    last_updated = last_updated[:10]
    res += f"""          <li>
            <p>
              <span class="folder"><a href="/{canonical_link(file[0])}">{file[3]['title']}</a> [{section}]</span>
              (<time datetime="{last_updated_machine}" class="last-updated">{last_updated}</time>)
            </p>
          </li>\n"""
  res += """          </ul>\n        </div>\n"""
  return res


def get_lazy_param(key, html=None):
  if key == "index":
    return get_index(datetime.datetime.now().strftime("%Y"))
  if key.startswith("index-"):
    return get_index(key[6:])
  if key.startswith("integrity-"):
    return get_hash(key[10:], key, html)
  return None


def get_next_prev(html_path):
  if html_path.endswith(".md"):
    html_path = html_path[:-3] + ".html"
  prev, cur, next = None, None, None
  global ALL_PAGES
  for page in ALL_PAGES:
    if page[3].get("type", "") != "article":
      continue
    # print(f"html_path={html_path} page={page[0]}")
    if html_path == page[0]:
      cur = page
    elif cur:
      next = page
      break
    else:
      prev = page
  return (prev, next) if cur else (None, None)


def canonical_link(link):
  if link.startswith("/"):
    link = link[1:]
  if link == "index.html":
    return ""
  if link.endswith("index.html"):
    return link[:-10]
  if link.endswith(".html"):
    return link[:-5]  # no .html
  return link


def generate_html(data, params, data_path=None, link=None):
  html = ""
  params["last-updated-machine"] = params["last-updated"].replace(" ", "T")
  params["last-updated-nice"] = params["last-updated"][:16]
  if params["last-updated-nice"][-6:] == " 00:00":
    params["last-updated-nice"] = params["last-updated-nice"][:10]
  elif params["last-updated-nice"][-6:] == " 23:59":
    params["last-updated-nice"] = params["last-updated-nice"][:10]
  type = params.pop("type", None)
  params["canonical-link"] = f"{params['site-link']}/{canonical_link(link)}"
  params["robots-index"] = "noindex,follow" if "no-index" in params else "index,follow"

  if type == "redirect" or "redirect" in params:
    if not params["redirect"].startswith("/"):
      print(
        f"FIX NEED absolute path on redir for {data_path} with redirect={params['redirect']}"
      )
      sys.exit(1)
    with open(f"templates/redirect.html", "r") as f:
      template = f.read()
    params[
      "canonical-link"
    ] = f"{params['site-link']}/{canonical_link(params['redirect'])}"
    html = placeholders(template, params)
  elif type == "error":
    with open(f"templates/error.html", "r") as f:
      template = f.read()
    params['data'] = data
    html = placeholders(template, params)
  else:
    with open("templates/header.html", "r") as f:
      html += f.read()
    if not html.endswith("\n"):
      html += "\n"

    if type:
      if type == "draft":
        type = "article"  # FIXME
      if not os.path.exists(f"templates/{type}.html"):
        print(f"FIX BROKEN {data_path} invalid template '{type}'")
        sys.exit(1)

      with open(f"templates/{type}.html", "r") as f:
        template = f.read()
      params['data'] = data
      template = placeholders(template, params)
      template = re.sub(re.escape("{{{" + type + "}}}"), data, template)
      if type == "article":
        nav = ""
        next, prev = get_next_prev(link)
        if prev or next:
          # print(prev, next)
          nav += f"""
            <div class="nav">
              <span class="prev">"""
          if prev:
            if "title" not in prev[3]:
              print(f"ERROR: MISSING TITLE ON {prev}")
              sys.exit(1)
            nav += f"""Previous: <a rel="prev" href="/{canonical_link(prev[0])}">{prev[1][0:10]}: {prev[3]['title']}</a>"""
          nav += f"""</span>
            <span class="next">"""
          if next:
            if "title" not in next[3]:
              print(f"ERROR: MISSING TITLE ON {next}")
              sys.exit(1)
            nav += f"""Next: <a rel="next" href="/{canonical_link(next[0])}">{next[1][0:10]}: {next[3]['title']}</a>"""
          nav += f"""</span>
          </div>
          """
        template = re.sub(re.escape("{{{nav}}}"), nav, template)
      html += template
    else:
      html += data

    if not html.endswith("\n"):
      html += "\n"

    if type != "article" or "no-comments" in params:
      params["comments"] = ""
    else:
      with open("templates/comments.html", "r") as f:
        comments = f.read()
      if not html.endswith("\n"):
        comments += "\n"
      params["comments"] = placeholders(comments, params)

    with open("templates/footer.html", "r") as f:
      html += f.read()
    if not html.endswith("\n"):
      html += "\n"
    html = placeholders(html, params)

  keys_phases = [ [], [] ]
  m = re.findall("{{{(.*?)}}}", html)
  for key in m:
    if key.startswith("integrity-"):
      keys_phases[1].append(key)
    else:
      keys_phases[0].append(key)

  for keys in keys_phases:
    for key in keys:
        val = get_lazy_param(key, html)
        if not val:
          print(f"FIX BROKEN {data_path} no val for '{key}'")
          print(html)
          sys.exit(1)
        html = re.sub(re.escape("{{{" + key + "}}}"), val, html)

  return html


def preparse(body):
  body = re.sub(
    re.escape(r"{{{image:") + "(.+?):(.+?)" + re.escape(r"}}}"),
    r"""<img src="/images/\1" alt="\2" />""",
    body,
  )
  return body


def generate_description(html):
  # 160 chars > 1000px
  html = re.sub(r"<h[1-6].*?>.*?</h[1-6]>", "", html)
  html = re.sub(r"<.+?>", "", html)
  html = re.sub(r"\\\"", r"\\\\\"", html)
  html = re.sub(r"\s+", r" ", html)
  html = html.strip()
  if len(html) > 148:
    html = html[0:147] + "…"
  return html


def process_file(data_root, html_root, data_folder, data_file, html_folder, html_file):
  data_path = os.path.join(data_root, data_folder, data_file)
  html_path = os.path.join(html_root, html_folder, html_file)

  mtime = os.stat(data_path)
  with open(data_path, "r") as f:
    data = f.readlines()
  body, params = parse_data(data, DEFAULT_PARAMS)
  if "last-updated" not in params:
    mtime = os.stat(data_path)
    params["last-updated"] = datetime.datetime.fromtimestamp(
      mtime.st_mtime
    ).strftime("%Y-%m-%d %H:%M:%S")

  # https://python-markdown.github.io/extensions/
  body = preparse(body)
  body = markdown.markdown(
    body,
    extensions=[
      "fenced_code",
      # "codehilite",
      "tables",
      "footnotes",
      "sane_lists",
    ],
  )
  body = re.sub(r">nofollow:", r' rel="nofollow">', body)
  body = re.sub(r"(<ul>\s*<li>\s*)(.*?)(\s*</li>\s*</ul>)", r"\1<p>\2</>\3", body)
  body = re.sub(r"\n\n+", r"\n", body)
  body = re.sub(r"<code>\n", r"<code>", body)
  body = re.sub(r'(href="https://web.archive.org)', r'rel="nofollow" \1', body)
  body = re.sub(
    r"(<a[^>]*)href=([^>]*)>strike:([^<]*</a>)",
    r'<strike>\1rel="nofollow" href=\2>\3</strike>',
    body,
  )

  if "description" not in params:
    description = generate_description(body)
    if "{{{" in description:
      print(f"FAIL {data_path} description has placeholders")
      sys.exit(1)
    params["description"] = description
  html = generate_html(
    body, params, data_path, link=os.path.join(html_folder, html_file)
  )

  html_path_folder = os.path.join(html_root, html_folder)
  if not os.path.isdir(html_path_folder):
    os.makedirs(html_path_folder)
  with open(html_path, "w") as f:
    f.write(html)
  os.utime(html_path, (mtime.st_atime, mtime.st_mtime))
  print(f"Processed {data_path} into {html_path}")
  return 1


def process_data(data_root, html_root=HTML_FOLDER):
  return _process_data(data_root, html_root, "", "")


def _process_data(data_root, html_root, data_folder, html_folder):
  processed = 0
  data_path = os.path.join(data_root, data_folder)
  for file in os.listdir(data_path):
    if os.path.isdir(os.path.join(data_path, file)):
      processed += _process_data(
        data_root,
        html_root,
        os.path.join(data_folder, file),
        os.path.join(html_folder, file),
      )
    elif file.endswith(".md"):
      processed += process_file_if_changed(
        data_root,
        html_root,
        data_folder,
        file,
        html_folder,
        f"{file[:-3]}.html",
      )
  # end for
  return processed


# def _generate_sitemap_from_file(f, html_folder, html_path):
#   f.write("""  <url>\n""")
#   real_path = canonical_link(html_path)

#   loc = os.path.join(params['site-link'], real_path)
#   if loc.endswith(".html"):
#     loc = loc[:-5] # no .html
#   f.write(f"""  <loc>{loc}</loc>\n""")

#   mtime = os.stat(os.path.join(html_folder, html_path))
#   mday = datetime.datetime.fromtimestamp(mtime.st_mtime).strftime(
#     "%Y-%m-%dT%H:%M:%S+00:00"
#   )
#   f.write(f"""  <lastmod>{mday}</lastmod>\n""")
#   f.write(f"""  <changefreq>always</changefreq>\n""")
#   f.write(f"""  <priority>0.5</priority>\n""")
#   f.write("""  </url>\n""")


# def _generate_sitemap_from_folder(f, html_folder=HTML_FOLDER, folder=""):
#   for file in os.listdir(os.path.join(html_folder, folder)):
#     if os.path.isdir(os.path.join(html_folder, folder, file)):
#       _generate_sitemap_from_folder(f, html_folder, os.path.join(folder, file))
#     elif file.endswith(".html"):
#       _generate_sitemap_from_file(f, html_folder, os.path.join(folder, file))


def generate_sitemap(html_folder=HTML_FOLDER, params=DEFAULT_PARAMS):
  sitemap_file = os.path.join(html_folder, "sitemap.xml")
  sitemap_mtime = None
  with open(sitemap_file, "w") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
    f.write("""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n""")
    # _generate_sitemap_from_folder(f, html_folder)
    global ALL_PAGES
    pages = [("index.html", params["site-name"], "", {})] + ALL_PAGES
    for page in pages:
      # f.write(f"{page}\n\n")
      if param_is(page[3], "no-index", True):
        continue
      real_path = canonical_link(page[0])
      loc = os.path.join(params["site-link"], real_path)
      # redir = os.path.join(params["site-link"], page[0])
      mtime = os.stat(os.path.join(html_folder, page[0]))
      mday = datetime.datetime.fromtimestamp(mtime.st_mtime).strftime(
        "%Y-%m-%dT%H:%M:%S+00:00"
      )
      if not sitemap_mtime or sitemap_mtime < mtime:
        sitemap_mtime = mtime
      freq = 'daily'
      priority = '1.0' if page[0] == "index.html" else '0.5'
      f.write("""  <url>\n""")
      f.write(f"""  <loc>{loc}</loc>\n""")
      f.write(f"""    <lastmod>{mday}</lastmod>\n""")
      f.write(f"""    <changefreq>{freq}</changefreq>\n""")
      f.write(f"""    <priority>{priority}</priority>\n""")
      f.write("""  </url>\n""")
      # # FIXME TEMP
      # if loc != redir:
      #   f.write("""  <url>\n""")
      #   f.write(f"""  <loc>{redir}</loc>\n""")
      #   f.write(f"""  <lastmod>{mday}</lastmod>\n""")
      #   f.write(f"""  <changefreq>always</changefreq>\n""")
      #   f.write(f"""  <priority>0.5</priority>\n""")
      #   f.write("""  </url>\n""")
    f.write("""</urlset>\n""")
  os.utime(sitemap_file, (sitemap_mtime.st_atime, sitemap_mtime.st_mtime))
  print(f"Processed sitemap.xml for {len(pages)} pages")


def clean_cruft(data_folder=DATA_FOLDER, html_folder=HTML_FOLDER):
  return _clean_cruft(data_folder, html_folder, "")


def _clean_cruft(data_folder=DATA_FOLDER, html_folder=HTML_FOLDER, folder=""):
  processed = 0
  for file in os.listdir(os.path.join(html_folder, folder)):
    file_path = os.path.join(folder, file)
    if file_path in IGNORED_FILES:
      continue

    data_path = os.path.join(data_folder, folder, file)
    html_path = os.path.join(html_folder, folder, file)
    if file in DELETE_FILES:
      os.unlink(os.path.join(html_folder, folder, file))
    elif os.path.isdir(html_path):
      if f"{file_path}/" in IGNORED_FILES:
        continue
      if not os.path.isdir(data_path):
        print(f"REMOVE CRUFT FOLDER {html_path}")
      else:
        processed += clean_cruft(data_path, html_path)
    elif file.endswith(".html"):
      md = f"{file[:-5]}.md"
      if not os.path.exists(os.path.join(data_folder, folder, md)):
        os.remove(html_path)
        print(f"REMOVING CRUFT FILE {html_path}")
        processed += 1
    else:
      print(f"REMOVE CRUFT UNKNOWN {os.path.join(html_folder, file)}")
      processed += 1
  return processed


def load_params():
  params = {}

  # default params
  params["type"] = "article"

  # configurable params
  with open("templates/params.yaml", "r") as f:
    data = f.readlines()
  for line in data:
    kv = line.split(":")
    kv = [k.strip() for k in kv]
    params[kv[0]] = ":".join(kv[1:])

  # dynamic params
  params["current-year"] = datetime.datetime.now().strftime("%Y")
  params["copyright-line"] = placeholders(params["copyright-line"], params)
  # params["last-updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return params


def placeholders(value, params={}):
  for key, val in params.items():
    value = re.sub(re.escape("{{{" + key + "}}}"), val, value)
  return value


def load_args():
  parser = argparse.ArgumentParser(
    description=f"{sys.argv[0]} command", add_help=True
  )
  parser.add_argument(
    "--force", "-f", dest="force", action=argparse.BooleanOptionalAction
  )
  args = parser.parse_args(sys.argv[1:])
  return args


def main():
  global CMDLINE_ARGS
  CMDLINE_ARGS = load_args()

  global DEFAULT_PARAMS
  DEFAULT_PARAMS.update(load_params())

  global ALL_PAGES
  ALL_PAGES = get_files()

  processed_data = process_data(DATA_FOLDER)
  processed_cruft = clean_cruft(DATA_FOLDER, HTML_FOLDER)
  if processed_data or processed_cruft:
    generate_sitemap(HTML_FOLDER)


if __name__ == "__main__":
  main()
