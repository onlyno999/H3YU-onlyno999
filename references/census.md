# 工作流普查 · 2108276969036148738（音乐/音频生成 · ACE-Step 系指纹）

- 链接：https://www.runninghub.cn/workflow/2108276969036148738
- 普查：2026-10-09 两段：首探全回 810 未激活；用户在网页界面手动运行一次后复探，workflow 端点转 **803 已激活**、ai-app 端点 901 不存在（普通 workflow，非 AI 应用）。零扣费哨兵法，**全程建任务 0、扣费 0**。
- 节点全扫 1–2000：**仅 17 个节点，全部落在 35–59**：35, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59（301–2000 全空）。
- 字段普查：核心轮 206 词 × 17 节点（命中 39、未决 0）＋补充轮 642 词 × 6 个关键节点 35/42/45/46/49/51（新增命中 3、未决 0）。

## 定性

**音乐/音频生成流（写歌词＋风格描述 → 生成一首带时长的音频）**，指纹与 ACE-Step 系一致：提示节点带 caption＋lyrics 双文本栏＋cfg_scale/top_k，空 latent 以 seconds 定时长，出口为 SaveAudio。全流无任何 image/video 输入输出字段命中，不是视频流、不是 RVC（无 speaker_id/f0/index_rate/训练字段）。

## 节点全表（实测字段指纹）

| 节点 | 命中字段 | 归属 |
| :--- | :--- | :--- |
| 35 | audio, filename_prefix, format | **SaveAudio 出口**（唯一落盘点） |
| 41 | unet_name, weight_dtype | UNET 加载（主模型） |
| **42** | **caption, lyrics, cfg_scale, seed, top_k**, clip(连线) | **提示/文本编码核心节点**：caption＝风格描述栏、lyrics＝歌词栏 |
| 43 | clip_name, type, device | CLIP 加载 |
| 44 | vae_name | VAE 加载 |
| 45 | conditioning | 条件汇聚/加工（单 conditioning 口） |
| 46 | seconds, batch_size | 空音频 latent：seconds 定时长、batch_size 定条数 |
| **47** | model/positive/negative/latent_image(连线), **steps, cfg, denoise, seed, sampler_name, scheduler** | **KSampler 采样器（全流心脏）** |
| 48 | samples, vae | VAEDecode ① |
| 49 | seed | 独立种子节点 |
| 50 | samples, vae | VAEDecode ②（与 51 switch 构成解码分支） |
| 51 | switch, on_true, on_false | 分支开关节点 |
| 55–59 | value（×5） | 五个原始值节点（喂数值参数，连线去向须画布/实派确认） |

## 怎么用（派发视角）

链路：41/43/44 装模型 → **42 写 caption（曲风/乐器/情绪/人声描述）＋ lyrics（歌词正文）**、定 cfg_scale/top_k/seed → 45 汇条件 → 46 定 seconds/batch_size → 47 KSampler（steps/cfg/denoise/seed/sampler/scheduler）→ 48/50 解码（51 switch 选支）→ 35 存音频。

- **最关键的一对：42（写什么）＋47（怎么采）**。42 是全流唯一文本入口——没有第二个 prompt 节点；提示词写法＝双栏制：caption 栏写风格描述、lyrics 栏写歌词，不要把歌词和风格混在一栏。
- 可写口（字段命中含连线口，widget/连线之分须实派回片元数据确认）：42.caption / 42.lyrics / 42.cfg_scale / 42.seed / 42.top_k、46.seconds / 46.batch_size、47.steps / 47.cfg / 47.denoise / 47.seed / 47.sampler_name / 47.scheduler、49.seed、51.switch、55–59.value、35.filename_prefix / 35.format，以及模型三件 41.unet_name / 43.clip_name / 44.vae_name。
- 探针读不到的：各字段现存默认值与 **42 里现存的 caption/lyrics 原文**（API 探针只能验字段存在、读不到内容）——原文须进画布看（浏览器登录被旋转滑块验证码挡住，用户未授权解题/未接管，故未读到），或用户导出工作流 JSON。

## 原始数据（同目录）
- step1.py ＋ step1_endpoints.log（首探 810）／step1_after_run.log（激活后 803）
- spotcheck.py ＋ spotcheck.log（首探 12 节点抽查全 810）
- census.py ＋ census_results_1_300 / 301_1000 / 1001_2000.json（节点全扫：17 个）
- field_census_core.py ＋ fields_hits_core.json（39 命中、未决 0）
- field_census_supp.py ＋ fields_hits_supp.json（新增 42.caption、51.on_true/on_false、未决 0）

## 画布实证补钉（2026-10-09 用户截图）

- **真身：MiniMax Music 3 音乐生成工作流**（画布标题与 Note 原文；此前按字段指纹猜的「ACE-Step 系」作废）。
- Note 原文要点：模型由 Caption＋Lyrics 两项输入驱动，时长最长 5 分钟。
  - **Caption 必须分三部分撰写：全局元数据 → 人声细节 → 编曲**；描述越具体越贴合预期。（我此前写的扁平标签串不符合此式——用户所指「没严格按提示词写」即此。）
  - **Lyrics：段落标签（[intro]/[verse]/[chorus]/[bridge]/[outro]）是唯一可执行的结构指令，歌词文本本身仅用于传达情绪。**
  - **max_duration＝目标时长（秒），默认 120，模型最长约 300**（对应本流 46.seconds 的角色）。
  - seed 固定可复现、改 seed 得不同版本；Tiled decode 是 48/50 双解码＋51 switch 的来历（低显存分块解码，高显存建议关）。
  - 官方 Caption 改写技能在 GitHub（MiniMax-AI 仓，Note 内链）。
- 原始文本存放处：**#58 STRING＝原 Lyrics、#59 STRING＝原 Caption**（截图可见片段：原歌为英文女声，lyrics 含 [pre-chorus] 段，caption 以 "…guitar, female vocal" 收尾）。55–59 五个原始值节点的角色至此对上：字符串/数值喂给 42/46/47 的参数位。我经 API 直填 42.caption/42.lyrics 实测可覆盖生效。

## 画布原文抄录（2026-10-09 浏览器登录实抄，短信验证码登录）

- **42 号 caption 原文**（出厂默认，扁平标签串 8 组）：`nu-disco, funk pop, electropop, hyperpop, electronica, funk bass, electric guitar, female vocal`——注意：出厂默认并非三段式；三段式是 Note＋官方技能的推荐写法，两式并存。
- **42 号 lyrics 原文结构**：共 72 行（61 非空行：9 个标头＋52 行正文、约 308 英文词）；标头仅四种（verse/pre-chorus/chorus/instrumental），顺序 verse→pre-chorus→chorus→verse→pre-chorus→chorus→instrumental→pre-chorus→chorus；pre-chorus 整段原样 ×3；chorus 四行块共出现 5 次（后两段为双块连唱＋各多两行单字感叹）；段间空一行，唯 [instrumental] 后紧贴下一标头不空行；**无 intro/bridge/outro**。
- **★根因钉死：42 号另有 `max_duration` 输入口，由 #55 FLOAT 节点供给＝120.0；46.seconds 同样由 #55 供给 120.0。** 我历次 API 派发只覆盖了 46.seconds、从未覆盖 42.max_duration——于是模型永远只按 120 秒规划歌曲内容，46 给的 180 秒 latent 后 60 秒只能自续/卡句/哼唱。**以后派发必须同时覆盖 42.max_duration 与 46.seconds 为同一目标值。**（普查词表漏了 max_duration 一词，故未探到此字段。）
- 其余现值：42 cfg_scale=1.7、top_k=50、seed 由 #49 Seed 节点供给（527731791462746、control=fixed）；47 KSampler steps=30、cfg=1.7、sampler=euler、scheduler=simple、denoise=1.0；46 batch_size=1。
- 事件如实记：浏览器抄录过程中误触一次外层运行键，随即取消（任务 21083837 开头、约 6 秒被取消），是否产生少量计费页面无法确认。
