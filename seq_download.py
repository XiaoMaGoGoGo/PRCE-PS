"""
在NCBI的核酸数据库中下载益生菌的完整基因组数据，Accession Number来源于NCBI的菌种索引
"""
from Bio import Entrez


def getFasta(Accession_number):
    Entrez.email = '646542773@qq.com'
    print(str(Accession_number) + "  正在加载中...")
    hd_efetch_fa = Entrez.efetch(db='nucleotide', id=Accession_number, rettype="fasta")  ## 里面保存的时下载的fasta文件
    read_efetch_fa = hd_efetch_fa.read()
    return read_efetch_fa

if __name__ == '__main__':
    f = open('data_sample/Accession_ID.txt')
    for accession_number in f:
        Accession_number = accession_number.replace('\n', '')
        f_ = open('data_sample/data/'+str(Accession_number)+'.fasta', 'a')
        f_.write(getFasta(Accession_number))