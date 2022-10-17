import os
import pandas as pd

os.chdir("C:\\Users\\10532\\Desktop\\paper")
DATA_PATH = "C:\\Users\\10532\\Desktop\\paper\\data"


def rename_files(data_path):
    dirlist = os.listdir(data_path)
    for i in range(len(dirlist)):
        old = os.path.join(data_path, dirlist[i])
        idloc = dirlist[i].find('2')
        dirlist[i] = os.path.join(data_path, dirlist[i][:idloc])
        os.rename(old, dirlist[i])


def rename_csv(data_path):
    dirlist = os.listdir(data_path)
    for i in range(len(dirlist)):
        path = os.path.join(data_path, dirlist[i])
        for file in os.listdir(path):
            if file.endswith("csv"):
                os.rename(os.path.join(path, file), os.path.join(path, 'data.csv'))
            elif file.endswith("pdf"):
                os.remove(os.path.join(path, file))
            else:
                os.rename(os.path.join(path, file), os.path.join(path, '字段说明.txt'))


def read_ratio_fixed_asset():
    ratio_fixed_asset = pd.read_csv('./data/比率结构/data.csv')
    ratio_fixed_asset = ratio_fixed_asset[ratio_fixed_asset["Typrep"] == "A"]
    ratio_fixed_asset['month'] = ratio_fixed_asset["Accper"].apply(lambda x: str(x)[5:7])
    ratio_fixed_asset = ratio_fixed_asset[ratio_fixed_asset["month"] == '12']
    ratio_fixed_asset = ratio_fixed_asset.rename(columns={"F030801A": "fixed_asset_ratio"})
    return ratio_fixed_asset


def read_tobin():
    tobin = pd.read_csv("./data/融资约束—KZ指数/data.csv")
    tobin = tobin[tobin.STPT == 1]  # 剔除ST
    tobin = tobin[tobin.IsNewOrSuspend == 1]  # 上市不满一年
    tobin = tobin.rename(columns={"Symbol": "Stkcd", "Enddate": "Accper"})
    return tobin


def read_ratio_cash_asset():
    ratio_cash_asset = pd.read_csv("./data/偿债能力/data.csv")
    ratio_cash_asset = ratio_cash_asset[ratio_cash_asset["Typrep"] == "A"]
    ratio_cash_asset = ratio_cash_asset.rename(columns={"F010401A": "cash_ratio", "F011201A": "ratio_al"})
    ratio_cash_asset["month"] = ratio_cash_asset.Accper.apply(lambda x: str(x)[5:7])
    ratio_cash_asset = ratio_cash_asset[ratio_cash_asset["month"] == '12']
    return ratio_cash_asset


def read_base_info():
    base_info = pd.read_csv("./data/管理层治理能力/data.csv")
    base_info = base_info.rename(columns={"Symbol": 'Stkcd', "Enddate": "Accper"})
    base_info = base_info[["Stkcd", "Accper", "IndustryName", "InsInvestorProp", "IndDirectorRatio", "StaffNumber"]]
    return base_info


def read_roa():
    roa = pd.read_csv("./data/盈利能力/data.csv")
    roa = roa[roa["Typrep"] == "A"]
    roa['month'] = roa["Accper"].apply(lambda x: str(x)[5:7])
    roa = roa[roa["month"] == '12']
    roa = roa.rename(columns={"F050101B": "roa", "F053401B": "rd"})
    roa.rd.fillna(0, inplace=True)
    roa = roa[["Stkcd", "Accper", "roa", "rd"]]
    return roa


def read_age():
    age = pd.read_csv("./data/融资约束—FC指数/data.csv")
    age = age[age.STPT == 1]
    age = age[age.IsNewOrSuspend == 1]
    age = age.rename(columns={"Symbol": "Stkcd", "Enddate": "Accper"})
    age = age[["Stkcd", "Accper", "ListingAge", "FC"]]
    return age


def read_mb():
    mb = pd.read_csv("./data/相对价值指标/data.csv")
    mb = mb.rename(columns={"F101001A": "mb"})
    mb['month'] = mb.Accper.apply(lambda x: str(x)[5:7])
    mb = mb[mb['month'] == '12']
    mb = mb[["Stkcd", "Accper", 'mb']]
    return mb


def read_ceo():
    ceo = pd.read_csv("./data/治理综合信息文件/data.csv")
    ceo = ceo.rename(columns={"Reptdt": "Accper"})
    ceo["Y1001b"] = ceo["Y1001b"].map({2: "否", 1: "是"})
    ceo["Y0501b"] = ceo["Y0501b"].map({1: "否", 2: "是", 3: "不确定"})
    ceo["Y1801b"] = ceo["Y1801b"].map({1: "同", 2: "不同", 3: "不确定"})
    return ceo


def read_assets():
    assets = pd.read_csv("./data/资产负债表/data.csv")
    assets = assets[assets["Typrep"] == "A"]
    assets["month"] = assets['Accper'].apply(lambda x: int(x[5:7]))
    assets = assets[assets["month"] == 12]
    assets = assets.rename(columns={"A001000000": "tassets", "A002101000": "short_loan", "A002201000": "long_loan"})
    assets = assets[["Stkcd", "Accper", "tassets", "short_loan", "long_loan"]]
    return assets


def read_profit():
    profit = pd.read_csv("./data/利润表/data.csv")
    profit = profit.rename(columns={"B001101000": "income", "B001201000": "cost", "Bbd1102203": "interest"})
    profit = profit[profit["Typrep"] == "A"]
    profit["month"] = profit['Accper'].apply(lambda x: int(x[5:7]))
    profit = profit[profit["month"] == 12]
    profit = profit[["Stkcd", "Accper", "income", "cost", "interest"]]
    return profit


def read_invent():
    invent = pd.read_csv("./data/国内外专利申请获得情况表/data.csv")
    invent = invent[invent["ApplyType"] == "已申请"]
    invent.drop_duplicates(subset=["Symbol", "EndDate"], keep='first', inplace=True)
    invent["Invention"].fillna(0, inplace=True)
    invent["UtilityModel"].fillna(0, inplace=True)
    invent["invent"] = invent["Invention"] + invent["UtilityModel"]
    invent = invent.rename(columns={"Symbol": "Stkcd", "EndDate": "Accper"})
    invent = invent[["Stkcd", "Accper", "invent"]]
    return invent


def read_invest_env():
    invest_env = pd.read_csv("./data/上市公司环境投资统计表/data.csv")
    invest_env = invest_env.rename(columns={"Symbol": "Stkcd", "EndDate": "Accper"})
    return invest_env


def merge_features():
    ratio_fixed_asset = read_ratio_fixed_asset()
    tobin = read_tobin()
    ratio_cash_asset = read_ratio_cash_asset()
    base_info = read_base_info()
    roa = read_roa()
    age = read_age()
    mb = read_mb()
    ceo = read_ceo()
    assets = read_assets()
    profit = read_profit()
    analysis = pd.read_csv("./data/上市公司基本信息特色指标表/data.csv")
    invent = read_invent()
    invest_env = read_invest_env()
    data = pd.merge(ratio_fixed_asset, tobin[["Stkcd", "Accper", "TobinQ", "KZ"]], on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, ratio_cash_asset[["Stkcd", "Accper", "cash_ratio", "ratio_al"]], on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, base_info, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, roa, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, age, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, mb, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, ceo, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, assets, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, profit, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, analysis, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, invent, on=["Stkcd", "Accper"], how="left")
    data = pd.merge(data, invest_env, on=["Stkcd", "Accper"], how="left")
    return data


def fill_nan(data):
    data["fixed_asset_ratio"].fillna(data["fixed_asset_ratio"].mean(), inplace=True)
    data["TobinQ"].fillna(data["TobinQ"].mean(), inplace=True)
    data["KZ"].fillna(data["KZ"].mean(), inplace=True)
    data["FC"].fillna(data["FC"].mean(), inplace=True)
    data['cash_ratio'].fillna(data['cash_ratio'].mean(), inplace=True)
    data['ratio_al'].fillna(data['ratio_al'].mean(), inplace=True)
    data['IndustryName'].fillna("未知", inplace=True)
    data['InsInvestorProp'].fillna(data['InsInvestorProp'].mean(), inplace=True)
    data['IndDirectorRatio'].fillna(data['IndDirectorRatio'].mean(), inplace=True)
    data['StaffNumber'].fillna(data['StaffNumber'].mean(), inplace=True)
    data['roa'].fillna(data['roa'].mean(), inplace=True)
    data['rd'].fillna(data['rd'].mean(), inplace=True)
    data['ListingAge'].fillna(-1, inplace=True)
    data['mb'].fillna(data['mb'].mean(), inplace=True)
    data['Y0501b'].fillna(-1, inplace=True)
    data['Y1001b'].fillna(-1, inplace=True)
    data['Y1801b'].fillna(-1, inplace=True)
    data['ChairmanHoldsharesRatio'].fillna(data['ChairmanHoldsharesRatio'].mean(), inplace=True)
    data['tassets'].fillna(data['tassets'].mean(), inplace=True)
    data.short_loan.fillna(data.short_loan.mean(), inplace=True)
    data.long_loan.fillna(data.long_loan.mean(), inplace=True)
    data['income'].fillna(data['income'].mean(), inplace=True)
    data['cost'].fillna(data['cost'].mean(), inplace=True)
    data['interest'].fillna(data['interest'].mean(), inplace=True)
    data['Stknmec'].fillna("未知", inplace=True)
    data.AnaAttention.fillna(0, inplace=True)
    data.ReportAttention.fillna(0, inplace=True)
    data.invent.fillna(0, inplace=True)
    data["EPInvest"].fillna(0, inplace=True)
    return data


def save_data(data):
    new_data = data.dropna()
    limit_ind_set = {
        '电力、热力生产和供应业', '石油加工、炼焦及核燃料加工业', "有色金属矿采选业",
        '有色金属冶炼及压延加工业', "黑色金属矿采选业", '黑色金属冶炼及压延加工业',
        "煤炭开采和洗选业", "石油和天然气开采业", "非金属矿采选业", '水上运输业',
        '水的生产和供应业', '铁路、船舶、航空航天和其它运输设备制造业', '化学纤维制造业'}
    new_data["treat"] = new_data.loc[:, 'IndustryName'].apply(lambda x: 1 if x in limit_ind_set else 0)
    new_data["year"] = new_data.loc[:, "Accper"].apply(lambda x: int(x[0:4]))
    new_data.drop(columns=["Typrep", "Accper", "month"], inplace=True)
    new_data.columns = list(pd.DataFrame(new_data.columns)[0].apply(lambda x: x.lower()))
    new_data_order = new_data[[
        'stkcd', 'year', 'treat', 'fixed_asset_ratio', 'tobinq', 'kz',
        'cash_ratio', 'ratio_al', 'industryname', 'insinvestorprop',
        'inddirectorratio', 'staffnumber', 'roa', 'rd', 'listingage', 'fc',
        'mb', 'y0501b', 'y1001b', 'y1801b', 'chairmanholdsharesratio', 'tassets', 'short_loan', 'long_loan',
        'income', 'cost', 'interest', 'stknmec', 'anaattention',
        'reportattention', 'invent', 'epinvest', ]]
    new_data_order.to_csv("./data/format_data/data.csv", index=False)


if __name__ == "__main__":
    # rename操作只能运行一次
    # rename_files(DATA_PATH)
    # rename_csv(DATA_PATH)
    data = merge_features()
    data = fill_nan(data)
    save_data(data)
