# 科研进度与纪律交接（2026-09-28）

> 本文是当前执行交接，不把 CI 成功、开发集复审或模拟分支当作 confirmatory 科学阳性。所有数字以链接的冻结报告和运行记录为准。

## 0. 接手定位

- 仓库：`MKLEE222/claim-relative-representation`
- 工作分支：`audit/cold-start-20260926`
- 本交接所验收的基线提交：`48f8010cb269642df753f966f051cd2878e5a3d7`（2026-09-28 13:35:47 UTC）。
- PR：[#3](https://github.com/MKLEE222/claim-relative-representation/pull/3)，仍为 draft；`main` 未合并本分支。
- 当前远端验证：[research-contract CI 36429740251](https://github.com/MKLEE222/claim-relative-representation/actions/runs/36429740251) 为 success；[Module J 完整对象边界复审 36429428059](https://github.com/MKLEE222/claim-relative-representation/actions/runs/36429428059) 为 success，运行于 `38fad4c8`，2026-09-28 13:33:59 UTC 完成。随后 `48f8010c` 只记录复审报告，不改变该次运行的代码或结果。
- 这里的“超时”不代表以上 GitHub Actions 仍在执行。验收时无对应未完成运行；Module J 运行约 43 秒完成。新鲜 holdout 尚未执行。

## 1. 目前真正站得住的研究状态

母问题：**表示变化以后，学术知识史继续可研究，需要哪些信息与操作条件存续？**

目前可表述为任务、历史起点、来源版本、合法访问及对象边界相对的研究能力；不同能力应分别报告：定位研究对象、暴露所需证据、确定命题关系、保留责任/来源/不确定性、应用后续事件、选择性更新及审计历史。对象身份 `O` 是本轮新增的适用性前提：只有确定参与的日期/证据属于同一学术对象，才可以组成同一个 warrant。该表述是有界建模综合，尚非普遍/最小充分性定理。

既有 Track A 的五个 Yule–Cordier 历史问题有源页核对和有界机制结果；45 次三模型 blind 历史复核保持 `BOUNDED_PARTIAL`：45/45 调用正常并可解析，9/45 引文合格，21/21 原子组件 `NO_CONSENSUS`。不可写成独立模型复核通过或人类史学家一致。见 [母问题状态文件](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/experiments/deepening_v1/MOTHER_PROBLEM_CLOSURE_STATUS_v1.md)。该文件的 Track A “计算核心已闭合”只针对其原定静态/访问机制主张；后续 D–J 的动态持续研究主张仍需分别按新证据与新 gate 判定。Track B 全对象普遍率尚无合法分母。

## 2. H → I → J 的结果账本

| 阶段 | 实际结果 | 科学处置 |
| --- | --- | --- |
| Module H | 曾有 77/77；附录日期混入主信日期 | 仪器假阳性；**整项 confirmatory 结论作废**。保留为边界故障的开发证据。 |
| Module I 修硬 | oracle/runtime 分离；F1–F9 均被触发检测；Berlin 20/20、Paul 21/21 完整轨迹 | 仅 exposed-development 验证。自然来源后续 warrant 为 INTERVAL/ALTERNATIVE_SET；EXACT 只由合成测试覆盖。[硬化报告](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/audits/mother_problem_redesign_20260928/MODULE_I_HARDENING_VALIDATION_REPORT_v2.md)。 |
| Module I 一次性 StaBi holdout | 465 XML、0 parse errors；初报 7 个 discovery candidate、0 完整轨迹、母问题 gate FALSE | 原始结果必须保留。后验逐项源审表明 7 个候选均为跨年聚合档案/通讯包，并非一封信的日期冲突；7 个候选**不得作为发现阳性**。StaBi 已暴露，不能再当新鲜 holdout。 |
| Module J 对象边界修复 | 先确定唯一单一主对象并给所有参比 claims 相同 `object_id`；F1–F16 与附录排除控制通过 | v1 后在已暴露 Berlin 上发现转录容器假阴性，修成 Route B；v2 后发现无类型正文单信假阴性，修成 Route C。两次均发生在新 holdout 前，需完整保存版本轨迹。 |
| Module J 已暴露三语料复审 | Berlin 190 parsed，178 单对象、8 无对象、4 多对象；26 discovery pool、17 完整轨迹，native/R* 17/17。Paul 1515 parsed、1515 单对象；26 discovery pool、21 完整轨迹，native/R* 21/21。StaBi 465 parsed、465 无对象、0 discovery、0 完整轨迹；先前 7 个候选全被排除 | **开发集复审成功消除了已知假阳性并保留开发机制**。StaBi 的零值是“无合格研究事件”的语料/对象适用性结果，不能写成模型 0/x 表现，也不能算母问题 confirmatory gate 通过。[最终复审报告](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/audits/mother_problem_redesign_20260928/MODULE_J_OBJECT_BOUND_REAUDIT_REPORT_v1.md)。 |

Module J 的三条当前冻结对象语法：
A. 唯一显式非附录 `div type="letter"`；
B. 唯一实质性 `div type="transcription"` 本身构成一封信，须有唯一 correspondence 记录和 sent action；
C. 唯一无类型正文 div，须有 correspondence 记录、sent action 和 opener/closer/salute/signed/dateline 至少一种信件结构标记。
无对象、多对象、占位正文、跨对象 claim 一律拒绝；不允许“取第一封”。规则详见 [v1](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/experiments/module_j_dahn_object_bound_holdout_v1/OBJECT_BOUNDARY_CONTRACT_v1.md)、[v2 修订](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/experiments/module_j_dahn_object_bound_holdout_v1/OBJECT_BOUNDARY_CONTRACT_v2_AMENDMENT.md)、[v3 修订](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/experiments/module_j_dahn_object_bound_holdout_v1/OBJECT_BOUNDARY_CONTRACT_v3_AMENDMENT.md)。新鲜语料开封后不可再补 Route D 来救结果。

## 3. 验收判断与局限

**工程验收：通过。** 最终对象边界代码通过继承 F1–F9、F10–F16、附录控制及三组已暴露语料的复审；最终报告将哈希、artifact ID、运行号和 7 个假阳性的去向保存下来。

**科学验收：开发机制保留，confirmatory gate 未闭合。** Berlin/Paul 的 exact 成绩证明当前 evaluator 在已见语料上可执行且消融可区分；它们不能提供新独立验证。StaBi 作为新鲜测试给出的最初发现阳性无效；修正后全体无单一主对象，真实结论为该集合不适用此 D1/D2 单信研究任务。按冻结边界收下这个负结果。

仍有限制：自然完整轨迹缺 post-origin EXACT；控制 null event 为人工定义并通过实际转换算子执行，不能称为自然历史事件；单对象判据只覆盖所冻结的三类 TEI 编码路径；历史 Gate II 的 45-call 复核未达成独立一致。任何“可发表强论文”的主张必须把这些限制对应到具体句子和证据等级。

## 4. 不得改写的纪律

1. 每轮先标记语料和 episode group 的曝光状态，再谈“新鲜”。Berlin、Paul、StaBi 均已暴露。更换文件名、随机种子、运行号、接口包装或模型并不会恢复新鲜性。
2. H 的 77/77、I 的 7 个 StaBi 候选、J 的 Berlin/Paul 17/17 与 21/21 必须分别落在“作废假阳性 / 作废假阳性 / 开发集验证”栏目，不做合并成功率。
3. 新对象须先给出来源快照、版本、对象边界、曝光登记、episode 资格与完整分母；零合格对象要作为语料适用性结果完整报告。
4. oracle 与 runtime 继续独立；不允许共享决定 eligibility、warrant、object boundary 的核心判定逻辑。故障注入和负控制必须在开封前通过。
5. source-side 事件需要适用性：对象相同、版本一致、前态许可；只知道精确目标与结果不足以授权状态转换。记录保留 alternatives、选择性、来源、延迟审计及合法 reopen 的成本。
6. 不得按观察到的错误给新鲜 holdout 补对象路线、修改阈值、过滤不利 episode 或选择高分子集。必要修复只能生成新的版本/未来研究；原运行保留。
7. 研究写作按“源证据 → 可复现操作 → 对照/消融 → 允许的论断”逐句对表。必要时发表负结果、适用范围或方法学失效；不把论文等级目标当作结果筛选器。

## 5. 下一个合法执行入口

当前仓库在本基线**没有 Module J 的新鲜 confirmatory 运行，也没有已选定的新鲜对象集合**。此前 [DAHN Berlin 可行性契约](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/audits/mother_problem_redesign_20260928/DAHN_FRESH_HOLDOUT_FEASIBILITY_CONTRACT_v1.md) 的“fresh candidate”措辞已被后续 Berlin 暴露复审超越；后续不能继续以 Berlin 名义开新鲜测试。StaBi 亦然。

接手时按顺序：
1. 先做**命题级证据台账**：把 D–J 每条论文拟用主张对应到真实原始材料、冻结协议、完整分母、CI/产物、负例与失效边界；特别标出 J 尚无 confirmatory 结果以及 Track A 历史 Gate II `BOUNDED_PARTIAL`。
2. 决定是否需要下一次新鲜对象验证来支撑拟投稿主张。若需要，从未用于 A–J 设计/调参的项目或 episode group 选取；先用元数据/暴露台账证明独立性，再冻结来源 commit、选样规则、对象语法 A/B/C、根问题、证据释放、所有失败/空集合归类、primary/secondary 指标、预期成本和停止规则。
3. 在不读新语料正文的前提下完成 evaluator 独立性、F1–F16、运行参数与文件哈希冻结；先有不可更改的 protocol 和代码 SHA，后做**一次性**新鲜运行。完整保存 raw XML 标识、全部输出、日志、来源样本审计、结果哈希和 action artifact。
4. 依预设规则给出 PASS / BOUNDED_PARTIAL / NULL / INVALID 等判定，不因好坏改实验。若缺少新鲜语料或经费/时间不足，就在现有有界证据上起草论文，明确动态延展仍为开发机制。
5. 更新 claim ledger、方法、结果和图表时，确保“同一对象身份”是时间/命题关系成立的前提，且不把访问失败、语料无对象、算法失败或历史解释争议混成一个失败率。

## 6. 可复核位置

- 最终对象边界报告：[MODULE_J_OBJECT_BOUND_REAUDIT_REPORT_v1.md](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/audits/mother_problem_redesign_20260928/MODULE_J_OBJECT_BOUND_REAUDIT_REPORT_v1.md)。
- 最终复审 workflow：[module_j_object_bound_exposed_reaudit_v1.yml](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/.github/workflows/module_j_object_bound_exposed_reaudit_v1.yml)。
- 权威 CI：[Module J run 36429428059](https://github.com/MKLEE222/claim-relative-representation/actions/runs/36429428059)；含 Berlin/Paul/StaBi artifact 及测试日志。
- 先前 I 硬化：[报告 v2](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/audits/mother_problem_redesign_20260928/MODULE_I_HARDENING_VALIDATION_REPORT_v2.md)，hardening run 36417199855。
- 旧 Gate II：[MOTHER_PROBLEM_CLOSURE_STATUS_v1.md](https://github.com/MKLEE222/claim-relative-representation/blob/48f8010cb269642df753f966f051cd2878e5a3d7/experiments/deepening_v1/MOTHER_PROBLEM_CLOSURE_STATUS_v1.md)。

## 7. 本机工作区注意事项（2026-09-28 验收快照）

本机 `D:\TRAE\claim-relative-representation-r3-review` 的 HEAD 仍为 `2e96976a`，落后于远端本交接提交。验收时还存在未提交的 `data/r3_verified_proposition_panel_v1.csv` 修改，以及 `.deps/`、`__pycache__/`、Ollama 日志等未跟踪文件。此工作区没有被本次远端交接写入、重置或清理。下一位接手者应先分别核对这些本地内容的来源和价值，再选择安全同步方式；不要直接以远端内容覆盖本地修改，也不要把缓存/模型日志误当研究证据提交。

最后一句交接：**Module J 已把已知对象边界假阳性清零，并在开发数据上保留机制；下一轮若要升级实证等级，必须先找到真正未暴露的研究对象并冻结一次性检验。**
