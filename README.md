# NENU-GradeCHECKER
You'll be notificated by BARK

## What’s this?

期末周,既要忍受考试的痛苦,又要忍受等分数的痛苦

这是一个**Python脚本**,来自于Chat老师和Gemini老师

它能够实时监控教务系统的成绩变化动态

将此**Python脚本**配合**GitHub Action**和**Bark** 使用

当成绩变化时,你的手机会接收到通知

## How to use?
### What should I prepare?
1. BARK_TOKEN
2. Cookies - JSESSIONID、iPlanetDirectoryPro、acw_tc
### What should I do?
1. 在 Repository 的设置中 Secrets and Variables - Actions - 添加四个 Repository secrets

  名称分别是  a. ACW_TC
            b. BARK_TOKEN
            c. IPLANETDIRECTORYPRO
            d. JSESSIONID
  并填写对应字段

2. Repository的设置 - Actions - General - Workflow permissions - 修改为 Read and write permissions
3. 手动在 Actions - Check Grades 中运行一下工作链,检查能够是否正常工作

## Final
**心想事成!**
