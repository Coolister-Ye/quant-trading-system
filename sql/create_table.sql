drop table if exists quant.all_stock_code;
create table quant.all_stock_code (
	code varchar(32),
    tradeStatus varchar(32),
    code_name varchar(32),
	update_date date not null
);

drop table if exists quant.all_history_k;
create table quant.all_history_k (
	date varchar(32),
    time varchar(32),
    code varchar(32),
    open varchar(32),
    high varchar(32),
    low varchar(32),
    close varchar(32),
    preclose varchar(32),
    volume varchar(32),
    amount varchar(32),
    adjustflag varchar(32),
    turn varchar(32),
    tradestatus varchar(32),
    pctChg varchar(32),
    isST varchar(32),
    update_date date not null
);