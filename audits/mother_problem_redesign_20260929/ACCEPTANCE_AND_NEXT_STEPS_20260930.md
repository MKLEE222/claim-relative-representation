# 2026-09-30 验收与下一步执行交接

状态：**研究证据有界可用；主论文尚未成文；下一优先级是人文学主线与证据压缩。**  
本记录验收基线：`audit/cold-start-20260926` 的 `60391ea79036a9374e86a9102a459efda193f68f`。后续提交须重新核对本记录的状态，不自动继承“完成”。

## 1. 本轮验收

| 项目 | 验收状态 | 依据与界限 |
| --- | --- | --- |
| 动态理论的注册模型闭包 | **通过，有界** | `Sigma(g)=(Beta(g),Kappa(g))` 区分事件/关系绑定与当前状态/历史资格。Action-relative equivalent-state 120/120；REQUIRED witness 393/393；NOT_REQUIRED witness 19/19；Formalization Papers sequence 52/52、Yule–Cordier sequence 2/2。[证据图](DYNAMIC_MOTHER_PROBLEM_EVIDENCE_MAP_v1.md)；[运行 36661636458](https://github.com/MKLEE222/claim-relative-representation/actions/runs/36661636458)。这些数字只覆盖注册的动作、扰动和模型；不推出普遍最小表示定理。 |
| 人文学经验主线 | **证据已具备，叙述尚未合并** | Yule–Cordier 的 Paper Money 可作历史序列主例，Arbre Sec 可作未决/仅历史动作的对照。早期五案仍受历史 Gate II `BOUNDED_PARTIAL` 约束；不可写成独立史学复核成功。 |
| 独立生态机制检验 | **已具备有界复现** | Formalization Papers 有 52 条连接链、源材料独立复核和反例；其首次 fresh run 为 `INVALID`，后续成功是 `POST_FRESH_CORRECTED_REPRODUCTION_PASS`。在主文中担当外部机制验证，不充当人文学研究对象。 |
| 真实发表案例对照 | **结构性初审完成** | [领域偏移与强论文缺口审计](DOMAIN_DRIFT_AND_STRONG_PAPER_GAP_AUDIT_v1.md)核对了数字校勘、版本、provenance 方向的已发表论文，指出主文身份和写作缺口。此审计是定位材料，尚非逐论点的完整新颖性综述。 |
| 现有稿件 | **未通过成文验收** | `manuscript_v0_1_core.md` 与 2026-09-27 的 humanities-first architecture 早于 qualified generator / composition 结果。主文仍以前一代的“表示是否足够/静态恢复”为重心，需要整合重写。 |
| eLife prospective 候选 | **仅预数据准备，未获科学结果** | [候选协议](ELIFE_CLEAN_PROSPECTIVE_CONFIRMATION_PROTOCOL_v1.md)已冻结来源、抽样和判定；repo 有 source manifest、两套解析/资格代码、20 个合成 XML、独立 documentary auditor、finalizer。验收基线尚无完整 synthetic coverage/scientific manifest、候选专用 DATA_OPEN workflow、exact-path artifact round-trip 报告或自然 XML 结果。通用 research-contract CI 成功仅证明仓库常规检查成功。eLife 是可选外部技术验证，不能替代主论文的人文学锚点。 |
| TMLR/OpenReview | **退出下一轮选择** | 文档筛选发现决定性评分历史对公共研究者不可见；亦有明显领域偏移风险。不得用其公开决定结果反推私有资格历史。[筛选台账](CLEAN_PROSPECTIVE_TYPED_CONFIRMATION_SCREENING_LEDGER_v1.md)。 |

已核对的已发表邻近论文原文入口：[Birnbaum & Spadini 2020](https://www.digitalhumanities.org/dhq/vol/14/3/000489/000489.html)、[Bleeker 等 2022](https://www.digitalhumanities.org/dhq/vol/16/1/000583/000583.html)、[Broyles 2020](https://www.digitalhumanities.org/dhq/vol/14/2/000455/000455.html)、[Vancisin 等 2023](https://academic.oup.com/dsh/article/38/3/1322/7140400)、[Williamson 2026](https://academic.oup.com/dsh/article/41/3/1705/8703430)。这些论文说明数字校勘、版本与数字 provenance 已有坚实研究传统；我们的差异主张须逐句证明，不能以“前人忽略历史/来源”概括。

## 2. 距离 strong paper 的四个工作包

### 工作包 A：冻结论文身份与三条贡献（下一步，先做）

交付一个短文件，逐字固定：
1. 一句人文学母问题：学术知识经过编辑、数字化和表示变化后，后来的研究者怎样继续判断哪些源于历史证据的研究动作有资格进行。
2. 主经验现象：Yule–Cordier 的跨版知识史；Paper Money 主序列、Arbre Sec 对照。
3. 三条贡献：① 当前结论相同仍可有不同的后续研究可能性；② 所需保留的绑定、状态、历史条件依动作而异；③ 学术动作通过写入后续动作所需的状态/历史而组成序列。
4. 其他语料的指定职责及排除规则：Formalization Papers 只作独立机制检验；AAD/VGW/Frankenstein/Whitman/Faust 等按单个审稿问题择用；TMLR/OpenReview/eLife 不定义论文的经验领域。

完成标准：摘要、引言首段、结果标题能不用 `Sigma/Beta/Kappa` 先说清历史现象与新发现；三条贡献各有直接证据，且无第四条“搭系统”式贡献。

### 工作包 B：证据裁剪与真实邻近研究定位（与 A 连续）

建立一张**主张—源证据—比较—允许措辞**矩阵，逐项指定：原始页/记录、冻结任务、实验与 artifact、负例、局限、主文或补充材料。至少处理：
- Paper Money 与 Arbre Sec 的人文学解释及对应 source anchor；
- 自然序列、相同当前投影/不同未来资格的见证；
- Formalization Papers 的首次 `INVALID` 与修正复现；
- Module H/I/J 的对象边界负结果在主文的最小必要作用；
- 45-call Gate II `BOUNDED_PARTIAL`；
- 120/393/19 等注册模型数字的有限外推范围。

与邻近论文的对话应逐一说明：版本可引、校勘建模、provenance 可见性已经解决了什么；本研究新增的是“具体后续研究动作的资格条件”以及“前一动作改变后一动作”的可检验机制。A/B 的完整矩阵和论文目录确认后才开始正文重写。

完成标准：主文只留一条历史脊柱、一个独立验证和必要的反例；工程修复、候选筛选、freshness 日志移入补充材料。每个 headline claim 至少有一条可回到原始对象的链。

### 工作包 C：整篇整合重写

从新论文架构起稿，停止逐段修补 `manuscript_v0`。顺序建议：
1. 历史/编辑问题；
2. 与已有数字校勘、版本与 provenance 研究的精确缺口；
3. 源对象、研究任务和合法访问契约；
4. Yule–Cordier 自然历史序列；
5. 以人文学语言解释动作相对的条件，再给有界形式化；
6. 独立生态机制检验及负结果；
7. 对数字学术版本/档案研究可继续性的含义；
8. 限制。

完成标准：读者在第一页看到历史研究问题、源对象、现象与贡献；主文每张图解释一个学术推理关系；稿件不按仓库模块字母或执行时间排序。

### 工作包 D：投稿前红队验收

逐项检查：
- 第一页是否仍像 DH / scholarly editing 论文；
- 对五篇已发表邻近作品的定位是否准确、有引用、无虚构新颖性；
- 每条主张的源页与运行结果是否直达；
- `INVALID`、`BOUNDED_PARTIAL`、开发集、修正复现、自然 null 是否按原等级出现；
- 对照是否足以排除“只保存更多元数据就行”或“只是检索失败”的简化解释；
- 图和补充材料是否支撑而不淹没历史叙述。

完成标准：每个 MAJOR/CRITICAL 问题有修复或明确降级措辞，然后才决定额外实验是否会改变主张等级。

## 3. eLife 的停/走纪律

目前**不执行 DATA_OPEN**。eLife 预数据包可保留并继续检查，但它是可选技术确认，不能代替 A–D。若之后明确决定执行，必须先满足 [master protocol](PROSPECTIVE_CONFIRMATION_MASTER_EXECUTION_PROTOCOL_v1.md)：完整 scientific/source/coverage manifests、全部注册分支合成覆盖、独立 oracle/runtime 和第三审计、同一权威栈 exact-path 合成通跑、finalizer、artifact 上传下载及哈希复核、代码/依赖冻结。全部通过后才写入 `DATA_OPEN_EVENT_v1.json` 并一次性开启预先指定的 297 manuscript / 568 XML 范围。数据开封后任何失败按原类别保留，不能改选记录或增加解析路线来取得 fresh PASS。

做论文成文的 A–D 期间，可以继续在已暴露资料上复核证据；不要为了等待 eLife PASS 而拖延主文。若 eLife 最终执行，无论结果如何都按其预注册判定记录，它的论文角色仍为外部技术边界/补充材料。

## 4. 下一位接手者的第一小时

1. 核对当前分支 HEAD、PR #3 和本文件的基线差异；保护本机旧检出的未提交内容。
2. 阅读 [证据图](DYNAMIC_MOTHER_PROBLEM_EVIDENCE_MAP_v1.md)、[领域/成文审计](DOMAIN_DRIFT_AND_STRONG_PAPER_GAP_AUDIT_v1.md)、旧[manuscript architecture](../../manuscript/MANUSCRIPT_ARCHITECTURE_HUMANITIES_FIRST.md) 与 [稿件 v0.1](../../manuscript/manuscript_v0_1_core.md)。
3. 直接开始 A 的一页 claim freeze，再做 B 的证据矩阵；不要再搜索便利的 peer-review 语料来代替历史研究对象。
4. 任何拟写“强论文已经完成”“fresh PASS”或“普遍必要”之句，先回到对应运行与源证据；证据达不到则降级措辞。

**当前明确结论：四个成文工作包尚待完成；A+B 是下一轮立即执行项。eLife 一次性实证是有条件的可选分支，尚未越过 PRE_DATA gate。**
