# passgen

本地密码 / 密码短语生成器。小而专：只做一件事——用密码学安全的随机数生成强密码。

## 安装

```bash
python3 -m passgen
```

纯标准库（`secrets` / `argparse` / `math`），Python 3.10+，零依赖。

## 用法

```bash
passgen                        # 20 位密码（大小写+数字+符号，每类至少一个）
passgen --length 32            # 32 位密码
passgen --no-symbols           # 去掉符号（某些网站不允许）
passgen --pin 6                # 6 位纯数字 PIN
passgen --passphrase           # 5 个单词的密码短语，如 correct-horse-…
passgen --passphrase --words 7 # 7 个词
passgen --count 5              # 一次生成 5 个
passgen --entropy              # 同时显示熵（bits）
```

## 熵（诚实说明）

- 密码熵 = 长度 × log2(字符集大小)。默认 20 位、字符集约 88 个字符 → 约 **129 bits**。
- 密码短语熵 = 单词数 × log2(词表大小)。内置词表 1768 个常见英文单词，
  5 个词 → 约 **53.9 bits**；7 个词 → 约 **75.4 bits**。
- 词表是精选的常见短词（不是 EFF 7776 大词表），所以同样词数下熵更低——
  想要更高强度就加单词数（`--words 8` ≈ 86 bits）。

## 安全说明（请读）

- 用 `secrets` 模块（CSPRNG），**不用** `random`。
- 本工具**不联网、不存储**生成的任何密码。生成完请立刻放进密码管理器
  （1Password / Bitwarden / iCloud 钥匙串等），不要留在终端历史或截图里。
- 密码短语方便人记，但 5 词短语（~54 bits）不适合保护高价值账户——
  重要账户用 20+ 位随机密码 + 密码管理器。

## 已知局限

- 密码短语是英文单词，中文用户手打稍麻烦（复制粘贴即可）。
- `--pin` 的数字 PIN 熵很低（6 位 ≈ 20 bits），只适合做设备解锁码等第二因素，
  不要当主密码。
- 本工具只生成、不校验已有密码强度。

## License

MIT，Copyright (c) 2026 ljiang9。
