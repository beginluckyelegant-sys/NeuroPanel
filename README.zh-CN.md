# NeuroPanel

神经科语言模型研究的推理架构与复现材料。

[English](README.md) · [架构详解](docs/inference_architecture.md) · [运行指南](docs/run_reference.md)

## 已补充可运行的参考实现

本次新增：固定向量余弦检索、多 agent 生成、同模型 critic、有限轮次定向修正、硬票与软票汇总、单 agent 对照模式，以及完整调用日志。支持无需模型的合成演示，也提供真实模型 HTTP 接口适配器。

**这是 2026 年 10 月根据补充材料重新构建的可运行参考实现。** 提供可配置的角色、提示词、温度、阈值及失败处理；版本来源和配置记录见模型说明及 `configs/study.template.json`。

## 快速运行

需要 Python 3.10 及以上版本，在仓库根目录执行：

```sh
PYTHONPATH=src python3 -m neuropanel \
  --config configs/reference.demo.json \
  --case examples/reference_case.json \
  --bank examples/reference_bank.json \
  --output outputs/demo-run-001
```

演示使用固定的合成回复，完整走通检索、2 个 agent、critic、修正与投票，共 8 次模拟调用。得到的 Candidate A 只是测试标签，不代表临床诊断或模型表现。

真实模型接入见[运行指南](docs/run_reference.md)：使用已有的 OpenAI 兼容服务，填写实际模型名及服务地址。此仓库不负责启动模型服务或加载权重。

## 验证与边界

已执行离线流程及软件测试，覆盖检索排除、向量版本一致性、修正停止条件、投票去重与并列、截断和无效输出，以及本地 HTTP 接口契约。本版本验证范围为合成数据执行及本地 HTTP 接口。

模型自报分数明确标为未校准分数。模型、配置及评价材料的提供状态见模型说明和数据开放清单。先前准备的 DeepSeek Q8_0 是公开基座参数，不等同于最终 NeuroPanel。

所有真实病例与调用日志应保留在受控环境中，不要提交到公共仓库。软件许可证和正式论文引用信息仍待确认。
