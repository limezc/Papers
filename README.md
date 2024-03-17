# Papers
<p align="center">
    <p align="center">
        <a href="https://github.com/limezc/Papers/actions"><img alt="GitHub Workflow Status (main)" src="https://img.shields.io/github/actions/workflow/status/limezc/Papers/paper.yml?branch=main&style=round-square"></a>
        <a href="https://packagist.org/packages/limezc/Papers"><img alt="Total Downloads" src="https://img.shields.io/packagist/dt/limezc/Papers"></a>
        <a href="https://packagist.org/packages/limezc/Papers"><img alt="Latest Version" src="https://img.shields.io/packagist/v/limezc/Papers"></a>
        <a href="https://packagist.org/packages/limezc/Papers"><img alt="License" src="https://img.shields.io/github/license/limezc/Papers"></a>
    </p>
</p>

这个项目用于爬取CVPR等相关会议的期刊论文。我们收集并整理了相关的论文代码和文章链接，以便于研究者和开发者更方便地获取和利用这些资源。

## 功能

- **论文爬取**：我们的爬虫会定期爬取CVPR等相关会议的最新论文。
- **代码收集**：对于开源的论文实现，我们会收集其代码链接，方便读者直接查看和使用。
- **文章链接**：我们提供每篇论文的直接链接，你可以通过这些链接直接阅读原文。
- **论文分类**：我们对论文进行了分类，你可以根据你的兴趣和需求，快速找到你需要的论文。
- **中英文摘要**：我们提供每篇论文的中英文摘要，帮助你快速理解论文的主要内容和贡献。

## 使用方法

1. 克隆这个仓库到你的本地机器。
2. 安装必要的依赖：`pip install -r requirements.txt`。
3. 运行爬虫：`python main.py`。
4. 查看结果：打开位于output下生成的文件。

## 待办列表
- [x] 获取网页所有论文列表
- [ ] 获取论文的中英文摘要
- [ ] 获取论文的pdf链接
- [ ] 获取论文的github链接
- [ ] 根据论文的abstract对论文进行分类
- [ ] 使用connect paper拓展相关方向论文


## 贡献

如果你有任何问题，或者有任何改进的建议，欢迎提交issue或者pull request。

## 开发人员

<p float="left">
  <a href="https://github.com/limezc"><img src="https://github.com/limezc.png" width="100" height="100" style="border-radius:50%"></a>
  <a href="https://github.com/liukongqau"><img src="https://github.com/liukongqau.png" width="100" height="100" style="border-radius:50%"></a>
</p>

## 许可

这个项目遵循MIT许可，详情请见[LICENSE](LICENSE)文件。
