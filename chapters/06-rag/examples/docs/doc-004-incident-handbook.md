# 萤火协作平台故障处理手册

本文档仅限运维团队使用（access_level: ops-only）。

## 数据库连接超时

**告警条件：** 数据库连接超时超过 30 秒。

**排查步骤：**

1. 检查数据库服务器 CPU 和内存使用率。如果 CPU 持续超过 80%，考虑扩容或优化慢查询。
2. 检查连接池配置。默认最大连接数为 200，如果活跃连接数持续接近上限，需要增加连接池大小。
3. 检查是否有未提交的长事务。执行 `SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction'` 查看。
4. 检查网络延迟。使用 `ping` 和 `traceroute` 确认应用服务器到数据库服务器之间的网络状态。

**临时缓解：** 重启应用服务器的连接池。

## Redis 内存满

**告警条件：** Redis 使用内存超过 `maxmemory` 的 90%。

**排查步骤：**

1. 检查当前内存使用：`INFO memory`。
2. 检查淘汰策略：`CONFIG GET maxmemory-policy`。当前默认 `allkeys-lru`。
3. 检查大 Key：`redis-cli --bigkeys`。

**恢复：** 如果内存持续满，临时增加 `maxmemory` 或手动清理过期 Key。长期方案是增加 Redis 节点或拆分缓存数据。

## 消息队列堆积

**告警条件：** 消息队列未消费消息数超过 10,000 条。

**排查步骤：**

1. 检查消费者是否在线：`rabbitmqctl list_consumers`。
2. 检查消费者日志是否有异常。
3. 检查死信队列是否增长。

**恢复：** 重启消费者进程。如果消费者处理能力不足，增加消费者实例数。

## 磁盘空间不足

**告警条件：** 数据盘使用率超过 95%。

**排查步骤：**

1. 检查各目录占用：`du -sh /* | sort -h`。
2. 检查日志文件大小：`journalctl --disk-usage`。
3. 清理超过 30 天的日志：`find /var/log -name "*.log" -mtime +30 -delete`。

**恢复：** 扩容磁盘或迁移历史数据到对象存储。
