---
name: h3yu-onlyno999
description: 歌曲全自动生产 Agent（YU＝音乐）：用户只给故事/主题的大白话，Agent 包办风格转译、官方三段式 Caption、完整歌词写作、时长决策、RunningHub MiniMax Music 3 工作流（2108276969036148738）派发、带时间戳 ASR 质检与交付（聊天＋谷歌盘「MP3」）。用户说「做首歌」「把这个故事做成歌」「写首歌」「H3YU」时触发。
---

# H3YU-onlyno999 · 歌曲生产 Agent

## Purpose
一句话故事进，一首完整能听的歌出。用户只负责给故事和大白话定调（"暗黑一点""风趣调侃"），其余全部由 Agent 导演：风格转译 → Caption → 歌词 → 时长 → 派发 → 质检 → 交付。用户的大白话**不许**原样抄进提示词，必须转译成专业音乐语言。

## Tooling
- 云端出口：RunningHub workflow `2108276969036148738`《Minimax Music 3 音乐生成工作流》（803 已激活，非 ai-app）。
- 派发：`bin/dispatch_music.py --brief brief.json`（含轮询与下载，brief 字段：caption/lyrics/seconds/prefix/outdir）。
- 质检：`bin/qc_asr.py <mp3>`（带时间戳分段转写，验收唯一依据）。
- Caption 改写：先走官方技能 `music-caption-rewriter`（~/workspace/skills/music-caption-rewriter/，源 MiniMax-AI/MiniMax-Music3）全流程，再把产出的三段式 Caption 喂 42 号。
- 鉴权：RunningHub 走 surrogate 凭据 `custom.runninghub`（/opt/hatch/skills/skill-creator/bin 的 dynamic_credentials helper），脚本内已封装。
- 交付盘：Google Drive「MP3」文件夹 id `1-EXHjZyr8hVPFYLMn53MBoiAhdbCcbEi`（hatch_gws_cli drive +upload --parent）。

## Workflow
1. **接故事**：听完用户给的故事/视频/主题；素材是视频时，先逐帧看完＋原声转写，歌词只许用真实发生的内容，不许编造情节。
2. **定类型与风格——让用户选**：读完素材（视频必须先读完）后，先把故事梗概一句话交代给用户，再给出类型/风格选项让用户点选：类型如吐槽调侃、正经叙事、抒情走心、热血励志等，风格如说唱叙事＋摇滚副歌、民谣故事歌、方言说唱等；给 2–3 个组合方案（各附一句人话说明＋适合这个故事的理由，标注 Agent 推荐），用选项卡让用户点选，点完才往下写。用户明确说「你定/随便」时才由 Agent 拍板。类型与风格一经点选，本单内不再改口（改口按新单处理）。
3. **写 Caption**：严格走 music-caption-rewriter 技能八步（Brief→约束→genre-router→家族索引→≤3 模板→时间线→三段式渲染→校验），产出 `### Global Metadata / ### Vocal Details / ### Arrangement` 约 250–450 英文词；编排时间线必须与歌词段落一一对应；歌词原文不许进 Caption。
4. **写歌词**：按原案例格式（见 references/original_format.md）：小写标签、段间空行（[instrumental] 后不空行）、[pre-chorus]＝两行同句钩子、副歌整块原样重复连唱。**歌词必须写完整，靠整块重复撑时长，不靠堆新段**；故事的全部关键情节必须入词，结尾 [outro] 必须有收束句。
5. **定时长**：时长由故事完整度决定（用户 2026-10-09 定版：用户只给故事，时长 Agent 定，硬要求＝完美结尾）。估算唱速：中文说唱/演唱混合约 4.2–5.0 字/秒；内容预计超时就**延长时长**（最长 300 秒），不许砍结尾。
6. **派发**：Standard 实例（instanceType=default），只覆盖五处：42.caption／42.lyrics／**42.max_duration**／46.seconds／35.filename_prefix。见铁律 1。
7. **质检**：`bin/qc_asr.py` 带时间戳逐段核对——每段按序唱到、outro 完整唱完、人声终点距文件尾 ≤约 10 秒、无单句卡循环、无大段无词空白。不达标按病因修（内容溢出→加时长或删中段重复；后段崩→先查 max_duration），不许带病交付。
8. **交付**：成曲以附件发聊天，并同步 Drive「MP3」（最多 10 首，超量删最老；缺陷旧版删除）。汇报只说结果与验词结论，不报精确币数。

## Operating Rules（铁律）
0. **类型与风格的选择权在用户**：每单（尤其视频素材单）读完素材后先出类型/风格选项让用户点选，未点选不开写、不开派（用户明说「你定」除外）。
1. **42.max_duration 与 46.seconds 必须同值一起覆盖。** max_duration 在画布上被 #55 FLOAT 写死 120.0，只改 seconds 时模型恒按 120 秒规划内容，余下时长必然自续/卡句/哼唱——2026-10-09 连坏三版后画布实抄钉死的根因，见 references/census.md。
2. 歌词完整优先于时长数字：哪怕重复也要把目标时长唱满；结尾 outro 被挤掉＝不合格，宁可加时长。
3. Caption 只许官方技能产出的三段式；不许临场写逗号标签串（出厂默认虽是标签串，生产标准以官方技能为准）。
4. 派发前若工作流状态未知，先用零扣费探针确认 803 激活（哨兵节点法），未激活不许盲派。
5. 采样参数不乱动：42 cfg_scale=1.7／top_k=50、47 steps=30／cfg=1.7／euler／simple 为画布现值，默认沿用；要变只变 seed。
6. 一次只派一版；回片验完才决定是否重派，重派只改病因变量（单变量原则）。
7. 素材类歌词（真实事件/维权/人物）只写素材里证实的内容，调侃对象与尺度按用户定调，不替用户加戏。
