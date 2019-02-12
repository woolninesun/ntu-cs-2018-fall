---
export_on_save:
  phantomjs: "pdf"
---

# [hw0x03] writeup
莊翔旭, woolninesun, b04902083

## De-de-deobfuscation

1. 通靈解：拿 secret code 前 4 個去和 flag 做 xor 發現結果都是 4，就直接將 secret code 的每個字元都 xor 4，就拿到 flag 了。 

2. 先用 idapro 找 main 的位置，在拿 x32dbg 去一步一步 trace code，trace 到一半就找到 flag 了！
