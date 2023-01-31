# TrimLog 使用指南
（2023/1/25 版本）

本仓库使用Apache2.0协议开源

## Part1 简介

TriMO组织的python项目log和项目管理框架库。

包含Logger和ObjectConstant（后简称OC）两部分。

Logger负责日志，OC负责控制项目整体变量，例如是否启用日志，是否启用debug模式等，也可以管理版本号等基础信息。


## Part2 Logger部分

### 2.1 logger基础
首先感谢**乐观的辣条(FedDragon)** 手写本项目的logger框架，太强了，万分感谢！

logger使用起来非常简单，首先需要import。

`from loggerT import log__init__, logger`

