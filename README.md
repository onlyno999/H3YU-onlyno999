# H3YU-onlyno999

歌曲全自动生产 Agent（YU＝音乐）。用户只给故事/主题的大白话，Agent 包办：

- 风格转译（大白话 → 专业音乐语言）
- 官方技能 music-caption-rewriter 三段式 Caption（Global Metadata / Vocal Details / Arrangement）
- 完整歌词写作（原案例块重复格式，靠重复撑满时长，结尾 outro 必须落地）
- 时长决策（按故事完整度定，3–5 分钟，最长 300 秒）
- RunningHub MiniMax Music 3 工作流 2108276969036148738 派发（Standard）
- 带时间戳 ASR 质检（逐段核对＋结尾验收，不达标不交付）
- 交付：聊天附件＋ Google Drive「MP3」文件夹（最多 10 首）

核心铁律：派发时 42.max_duration 与 46.seconds 必须同值覆盖——该参数在画布上被写死 120 秒，是长歌后段自续/卡句/哼唱的根因（2026-10-09 实证，见 references/census.md）。

成功案例：《满城妖魔》完整版（190s）、《你的良心不会痛吗》（240s），见 references/cases.md。

本地技能目录：~/workspace/skills/h3yu-onlyno999/（与本仓同步）。

依赖说明：写词与审词方法依赖 `chinese-songwriter-skill` 技能包（本地 ~/workspace/skills/chinese-songwriter-skill/，源 github.com/coinluu/chinese-songwriter-skill）——五分析、副歌先行、五维审词与对唱设计皆走它的方法文件；Caption 依赖官方 `music-caption-rewriter` 技能。两个依赖均按路径引用，内容不在本仓复制。
