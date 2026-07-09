-- 创建数据库 (如果尚未创建)
CREATE DATABASE IF NOT EXISTS quant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE quant_db;

-- -----------------------------------------------------
-- 1. 用户表 (user)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码(MD5)',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
  `status` TINYINT(1) DEFAULT 1 COMMENT '状态: 0禁用 1启用',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- -----------------------------------------------------
-- 2. 日线行情表 (stock_daily)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `stock_daily`;
CREATE TABLE `stock_daily` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `ts_code` VARCHAR(20) NOT NULL COMMENT '股票代码，格式：XXXXXX.SH/XXXXXX.SZ',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `open` DECIMAL(10, 4) DEFAULT NULL COMMENT '开盘价',
  `high` DECIMAL(10, 4) DEFAULT NULL COMMENT '最高价',
  `low` DECIMAL(10, 4) DEFAULT NULL COMMENT '最低价',
  `close` DECIMAL(10, 4) DEFAULT NULL COMMENT '收盘价',
  `pre_close` DECIMAL(10, 4) DEFAULT NULL COMMENT '昨收价',
  `change` DECIMAL(10, 4) DEFAULT NULL COMMENT '涨跌额',
  `pct_chg` DECIMAL(10, 4) DEFAULT NULL COMMENT '涨跌幅%',
  `vol` DECIMAL(20, 2) DEFAULT NULL COMMENT '成交量(手)',
  `amount` DECIMAL(30, 4) DEFAULT NULL COMMENT '成交额(千元)',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  
  UNIQUE KEY `uk_code_date` (`ts_code`, `trade_date`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票日线行情表';

-- -----------------------------------------------------
-- 3. 财务指标表 (stock_financial)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `stock_financial`;
CREATE TABLE `stock_financial` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `ts_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
  `ann_date` DATE NOT NULL COMMENT '公告日期',
  `end_date` DATE DEFAULT NULL COMMENT '报告期结束日期',
  `pe_ttm` DECIMAL(12, 4) DEFAULT NULL COMMENT '市盈率TTM',
  `pb` DECIMAL(12, 4) DEFAULT NULL COMMENT '市净率',
  `ps_ttm` DECIMAL(12, 4) DEFAULT NULL COMMENT '市销率TTM',
  `dv_ratio` DECIMAL(12, 4) DEFAULT NULL COMMENT '股息率%',
  `dv_ttm` DECIMAL(12, 4) DEFAULT NULL COMMENT '股息率TTM%',
  `total_share` DECIMAL(20, 4) DEFAULT NULL COMMENT '总股本',
  `float_share` DECIMAL(20, 4) DEFAULT NULL COMMENT '流通股本',
  `free_share` DECIMAL(20, 4) DEFAULT NULL COMMENT '自由流通股本',
  `total_mv` DECIMAL(30, 4) DEFAULT NULL COMMENT '总市值',
  `circ_mv` DECIMAL(30, 4) DEFAULT NULL COMMENT '流通市值',
  `roe` DECIMAL(12, 4) DEFAULT NULL COMMENT '净资产收益率ROE%',
  `eps` DECIMAL(12, 4) DEFAULT NULL COMMENT '每股收益',
  `bps` DECIMAL(12, 4) DEFAULT NULL COMMENT '每股净资产',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',

  UNIQUE KEY `uk_code_ann` (`ts_code`, `ann_date`),
  INDEX `idx_ann_date` (`ann_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票财务指标表';

-- -----------------------------------------------------
-- 4. 股票基本信息表 (stock_basic_info)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `stock_basic_info`;
CREATE TABLE `stock_basic_info` (
  `ts_code` VARCHAR(20) PRIMARY KEY COMMENT '股票代码',
  `symbol` VARCHAR(10) DEFAULT NULL COMMENT '股票代码符号部分',
  `name` VARCHAR(50) DEFAULT NULL COMMENT '股票名称',
  `area` VARCHAR(20) DEFAULT NULL COMMENT '地域',
  `industry` VARCHAR(50) DEFAULT NULL COMMENT '所属行业',
  `fullname` VARCHAR(100) DEFAULT NULL COMMENT '全称',
  `enname` VARCHAR(100) DEFAULT NULL COMMENT '英文全称',
  `market` VARCHAR(20) DEFAULT NULL COMMENT '市场类别',
  `list_status` CHAR(1) DEFAULT NULL COMMENT '上市状态 L上市 D退市 P暂停',
  `list_date` DATE DEFAULT NULL COMMENT '上市日期',
  `delist_date` DATE DEFAULT NULL COMMENT '退市日期',
  `is_hs` CHAR(1) DEFAULT NULL COMMENT '是否沪深港通标的',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票基本信息表';

-- -----------------------------------------------------
-- 5. 股票ma日线行情表 (stock_ma_daily)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `stock_ma_daily`;
CREATE TABLE `stock_ma_daily` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `ts_code` VARCHAR(20) NOT NULL COMMENT '股票代码，格式：XXXXXX.SH/XXXXXX.SZ',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `ma5` decimal(10,4) DEFAULT NULL COMMENT '5日均线',
  `ma10` decimal(10,4) DEFAULT NULL COMMENT '10日均线',
  `ma20` decimal(10,4) DEFAULT NULL COMMENT '20日均线',
  `ma30` decimal(10,4) DEFAULT NULL COMMENT '30日均线',
  `ma60` decimal(10,4) DEFAULT NULL COMMENT '60日均线',
  `ma120` decimal(10,4) DEFAULT NULL COMMENT '120日均线',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  
  UNIQUE KEY `uk_code_date` (`ts_code`, `trade_date`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票ma日线行情表';

-- -----------------------------------------------------
-- 6. 回溯测试结果主表 (backtest_result)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `backtest_result`;
CREATE TABLE `backtest_result` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `ts_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
  `stock_name` VARCHAR(50) DEFAULT NULL COMMENT '股票名称',
  `strategy_type` VARCHAR(50) NOT NULL COMMENT '策略类型: dual_ma/triple_ma/four_line',
  `strategy_params` JSON DEFAULT NULL COMMENT '策略参数JSON',
  `initial_capital` DECIMAL(15, 2) NOT NULL COMMENT '初始资金',
  `final_capital` DECIMAL(15, 2) NOT NULL COMMENT '最终资金',
  `total_return` DECIMAL(10, 4) DEFAULT NULL COMMENT '总收益率%',
  `annualized_return` DECIMAL(10, 4) DEFAULT NULL COMMENT '年化收益率%',
  `max_drawdown` DECIMAL(10, 4) DEFAULT NULL COMMENT '最大回撤%',
  `max_drawdown_duration` INT DEFAULT NULL COMMENT '最大回撤天数',
  `sharpe_ratio` DECIMAL(10, 4) DEFAULT NULL COMMENT '夏普比率',
  `sortino_ratio` DECIMAL(10, 4) DEFAULT NULL COMMENT '索提诺比率',
  `calmar_ratio` DECIMAL(10, 4) DEFAULT NULL COMMENT '卡玛比率',
  `win_rate` DECIMAL(10, 4) DEFAULT NULL COMMENT '胜率%',
  `profit_factor` DECIMAL(10, 4) DEFAULT NULL COMMENT '盈亏比',
  `total_trades` INT DEFAULT NULL COMMENT '总交易次数',
  `winning_trades` INT DEFAULT NULL COMMENT '盈利次数',
  `losing_trades` INT DEFAULT NULL COMMENT '亏损次数',
  `average_win` DECIMAL(15, 2) DEFAULT NULL COMMENT '平均盈利',
  `average_loss` DECIMAL(15, 2) DEFAULT NULL COMMENT '平均亏损',
  `data_start_date` DATE DEFAULT NULL COMMENT '数据开始日期',
  `data_end_date` DATE DEFAULT NULL COMMENT '数据结束日期',
  `test_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '测试时间',
  
  INDEX `idx_ts_code` (`ts_code`),
  INDEX `idx_strategy` (`strategy_type`),
  INDEX `idx_test_date` (`test_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='回溯测试结果主表';

-- -----------------------------------------------------
-- 7. 资金曲线表 (backtest_equity_curve)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `backtest_equity_curve`;
CREATE TABLE `backtest_equity_curve` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `result_id` INT NOT NULL COMMENT '关联backtest_result.id',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `equity` DECIMAL(15, 2) NOT NULL COMMENT '账户总权益',
  `cash` DECIMAL(15, 2) DEFAULT NULL COMMENT '现金',
  `position_value` DECIMAL(15, 2) DEFAULT NULL COMMENT '持仓市值',
  
  INDEX `idx_result_id` (`result_id`),
  INDEX `idx_trade_date` (`trade_date`),
  UNIQUE KEY `uk_result_date` (`result_id`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资金曲线表';

-- -----------------------------------------------------
-- 8. 交易记录表 (backtest_trade)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `backtest_trade`;
CREATE TABLE `backtest_trade` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `result_id` INT NOT NULL COMMENT '关联backtest_result.id',
  `trade_date` DATE NOT NULL COMMENT '交易日期',
  `action` VARCHAR(10) NOT NULL COMMENT '交易方向: BUY/SELL',
  `price` DECIMAL(10, 4) NOT NULL COMMENT '交易价格',
  `quantity` INT NOT NULL COMMENT '交易数量(股)',
  `commission` DECIMAL(10, 4) DEFAULT NULL COMMENT '佣金',
  `slippage` DECIMAL(10, 4) DEFAULT NULL COMMENT '滑点',
  `amount` DECIMAL(15, 2) DEFAULT NULL COMMENT '交易金额',
  
  INDEX `idx_result_id` (`result_id`),
  INDEX `idx_trade_date` (`trade_date`),
  INDEX `idx_action` (`action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录表';

-- -----------------------------------------------------
-- 9. 策略类型数据字典 (strategy_type)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `strategy_type`;
CREATE TABLE `strategy_type` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `code` VARCHAR(50) NOT NULL UNIQUE COMMENT '策略编码: dual_ma/triple_ma/four_line',
  `name` VARCHAR(100) NOT NULL COMMENT '策略名称',
  `description` TEXT DEFAULT NULL COMMENT '策略描述',
  `category` VARCHAR(50) DEFAULT NULL COMMENT '策略分类: 均线策略/动量策略/均值回归等',
  `params` JSON DEFAULT NULL COMMENT '默认参数配置(JSON)',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  
  INDEX `idx_code` (`code`),
  INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='策略类型数据字典';

-- 初始化策略类型数据
INSERT INTO `strategy_type` (`code`, `name`, `description`, `category`, `params`) VALUES
('dual_ma', '双均线交叉策略', '基于两条均线交叉产生买卖信号的经典策略。短期均线上穿长期均线为金叉(买入)，下穿为死叉(卖出)。', '均线策略', '{"short_window": 5, "long_window": 20, "volume_filter": false, "volume_ratio": 1.5}'),
('triple_ma', '三重均线策略', '在双均线基础上增加一条更长周期均线作为过滤器，只有多头信号出现在最长均线上方才可做多。', '均线策略', '{"short_window": 5, "mid_window": 20, "long_window": 60, "volume_filter": false, "volume_ratio": 1.5}'),
('four_line', '四线多头策略', '四条均线呈多头排列(MA5>MA20>MA60>MA120)时趋势确认向上，顺势做多。', '均线策略', '{"windows": [5, 20, 60, 120]}');