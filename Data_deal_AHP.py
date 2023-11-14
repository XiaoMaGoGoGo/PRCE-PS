"""
    本部分代码实现：
         1.Blast结果整理
         2.计算三指标权重并进行一致性检验
         后续单菌种风险和综合风险于excel中完成
"""
import numpy as np
import pandas as pd
import os
from pandas.errors import EmptyDataError

def blast_sort(sheet_name):
    """
    1.读取Blast结果并处理数据，统计数据库中识别到的基因个数
    :param sheet_name:CARD：固有耐药；ResFinder：获得性耐药；VFDB：毒力因子；Vrprofile：可移动序列及耐药基因
    """
    df = pd.read_excel('data_sample/Blast_result.xlsx', sheet_name=sheet_name)
    gene_count = df.groupby('SEQUENCE')['GENE'].nunique().reset_index()
    gene_count.columns = ['SEQUENCE', 'CARD_Count']

    # 统计每个样本中检出基因的名称
    gene_names = df.groupby('SEQUENCE')['GENE'].apply(list).reset_index()
    gene_names.columns = ['SEQUENCE', 'CARD_Names']

    # 合并结果
    result_df = pd.merge(gene_count, gene_names, on='SEQUENCE')

    # 将结果写入Excel的"sort"工作表
    with pd.ExcelWriter('data_sample/Blast_result.xlsx', engine='openpyxl', mode='a') as writer:
        result_df.to_excel(writer, sheet_name='sort', index=False)


def vrprofile_sort(folder_path='VRprofile_Download/'):
    """
    处理VRprofile下载的MGE结果
    :return:
    """
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # 读取所有文件并合并数据
    dataframes = []
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_csv(file_path, sep='\t')
            if not df.empty:
                dataframes.append(df)
        except pd.errors.EmptyDataError:
            print(f"文件 {file_name} 为空，跳过处理")
    filtered_df = dataframes[dataframes["Antibiotic_Resistance_Genes"].notnull()]
    # 将数据合并到一个DataFrame
    data = pd.concat(filtered_df)
    with pd.ExcelWriter('data_sample/Blast_result.xlsx', engine='openpyxl', mode='a') as writer:
       data.to_excel(writer, sheet_name='Vrprofile', index=False)


def calculate_ahp():
    A = np.array([[1, 5, 3],
                  [1/5, 1, 1/3],
                  [1/3, 3, 1]])                 # 重要性矩阵
    n = len(A[0])
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51]
#    R= np.linalg.matrix_rank(A)                #求判断矩阵的秩
    V,D = np.linalg.eig(A)                       #求判断矩阵的特征值和特征向量，V特征值，D特征向量；
    list1 = list(V)
    λ = np.max(list1)                           #最大特征值
    index = list1.index(λ)
    C = D[:, index]                            #对应特征向量
    CI = (λ-n)/(n-1)                             #计算一致性检验指标CI
    CR=CI/RI[n]
    if CR<0.10:
        print("CI=", CI)
        print("CR=", CR)
        print('重要性矩阵通过一致性检验，各向量权重向量Q为：')
        sum=np.sum(C)
        Q=C/sum                               #特征向量标准化
        print(Q)                              #  输出权重向量
    else:
        print("重要性A未通过一致性检验，需对对比矩阵A重新构造")
