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
2. kccj/main.page 的 URL
3. Cookies - JSESSIONID、iPlanetDirectoryPro、acw_tc
4. kccjData” 的 请求头数据、Payload数据
### What should I do?
1. 将以上准备好的数据填写到check_grades.py中
2. 修改.github/workflows/check_grades.yml中的成绩检查周期
3. Repository的设置 - Actions - General - Workflow permissions - 修改为 Read repository contents and packages permissions
4. 手动在 Actions - Check Grades 中运行一下工作链,检查能够是否正常工作

## Final
**心想事成!**