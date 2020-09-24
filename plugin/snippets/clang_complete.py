import re
import vim

def snippetsInit():
  python_cmd = vim.eval('s:py_cmd')
  vim.command("noremap <silent> <buffer> <tab> :{} updateSnips()<CR>".format(python_cmd))
  vim.command("snoremap <silent> <buffer> <tab> <ESC>:{} updateSnips()<CR>".format(python_cmd))
  if int(vim.eval("g:clang_conceal_snippets")) == 1:
    vim.command("syntax match placeHolder /\$`[^`]*`/ contains=placeHolderMark")
    vim.command("syntax match placeHolderMark contained /\$`/ conceal")
    vim.command("syntax match placeHolderMark contained /`/ conceal")

# The two following function are performance sensitive, do _nothing_
# more that the strict necessary.

def snippetsFormatPlaceHolder(word):
  return "$`%s`" % word

def snippetsAddSnippet(fullname, word, abbr):
  return word

r = re.compile('\$`[^`]*`')

def snippetsTrigger():
  if r.search(vim.current.line) is None:
    return
  vim.command('call feedkeys("\<esc>^\<tab>")')

def snippetsReset():
  pass

def utf8_position_from_byte_index(utf8_string, byte_index):
  by = bytearray(utf8_string, 'utf-8', 'ignore')
  return len(by[0:byte_index].decode('utf-8','ignore'))

def byte_index_from_utf8_position(utf8_string, position):
  return len(utf8_string[0:position].encode('utf-8','ignore'))

def updateSnips():
  line = vim.current.line
  row, column_byte_index = vim.current.window.cursor
  col = utf8_position_from_byte_index(line, column_byte_index)

  result = r.search(line, col)
  if result is None:
    result = r.search(line)
    if result is None:
      vim.command('call feedkeys("\<c-i>", "n")')
      return

  startb, endb = result.span()
  start = byte_index_from_utf8_position(result.string, startb)
  end = byte_index_from_utf8_position(result.string, endb)
  vim.current.window.cursor = row, start
  isInclusive = vim.eval("&selection") == "inclusive"
  vim.command('call feedkeys("\<ESC>\<C-V>%dl\<C-G>", "n")' % (end - start - isInclusive))

# vim: set ts=2 sts=2 sw=2 expandtab :
