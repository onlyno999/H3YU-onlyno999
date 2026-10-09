# 工作流原案例格式（2026-10-09 画布实抄的结构记录）

## 原 caption（#59→42 出厂默认）
扁平英文标签串 8 组：nu-disco / funk pop / electropop / hyperpop / electronica / funk bass / electric guitar / female vocal。
注：这是出厂示例值，不是生产标准；生产 Caption 按官方技能 music-caption-rewriter 的三段式产出（SKILL.md 铁律 3）。

## 原 lyrics（#58）结构
- 全文 72 行：61 非空行 ＝ 9 个段落标头 ＋ 52 行正文，约 308 个英文单词，按默认 120 秒唱完（唱速参照：约 0.43 行/秒、2.6 词/秒）。
- 标头只有四种，全小写方括号：[verse]、[pre-chorus]、[chorus]、[instrumental]。**原案例没有 intro/bridge/outro**（这三种 Note 允许用，本 Agent 的故事歌需要 bridge/outro 时可加，已实证可唱）。
- 顺序：verse → pre-chorus → chorus → verse → pre-chorus → chorus → instrumental → pre-chorus → chorus。
- 重复法：pre-chorus 整段（2 行同句钩子）原样出现 3 次；chorus 四行块共出现 5 次——后两次出现时是整块连唱两遍，且段尾各加两行单字感叹。
- 版式：小节之间空一行；唯一例外是 [instrumental] 标头后紧贴下一标头、不空行（器乐段本身无正文行）。
- 每段 verse 为两小节各 4 行；verse 的第二小节以同一句收尾句式结尾（回环感来自结构重复，不是新词）。

## 对写词的含义
撑时长靠「整块原样重复」（pre-chorus×N、chorus 双连唱、[instrumental] 间奏），不靠往后堆新段落——超出模型规划容量的新段会被丢弃或导致卡句（v4 实证）。
