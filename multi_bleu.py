import sacrebleu
import linecache
from sacremoses import MosesDetokenizer
md =  MosesDetokenizer()

gen_file = open("endeoursgen.out", 'r')
src_dict = {}
sys_dict = {}
for line in gen_file:
    line = line.strip()
    line_type = line.split("-")[0]
    if ( line_type == "S" ):
        line_id = line.split("-")[1].split("\t")[0]
        line_content = line.split("\t")[1]
        src_dict[md.detokenize(line_content.split(" "))] = line_id
        if(line_id=='2355'):
            print(md.detokenize(line_content.split(" ")))
    if ( line_type == "H" ):
        line_id = line.split("-")[1].split("\t")[0]
        line_content = line.split("\t")[1]
        sys_dict[line_id] = md.detokenize(line_content.replace("&quot;", "\"").split(" "))

ref_list_0 = []
ref_list_1 = []
ref_list_2 = []
ref_list_3 = []
ref_list_4 = []
ref_list_5 = []
ref_list_6 = []
ref_list_7 = []
ref_list_8 = []
ref_list_9 = []

ori_ref = []
sys = []
multi_ref = open("wmt14-en-de.extra_refs", 'r')
varaible = locals()

# extra_map = {407: 2355, 438, 2332, 804, 2571, 134, 1926, 1928, 1930, 2717, 930, 941, 2008}
extra_map = {}
extra_map[407] = 2355
extra_map[799] = 438
extra_map[821] = 2332
extra_map[971] = 804
extra_map[1034] = 2571
extra_map[1133] = 134
extra_map[1206] = 1926
extra_map[1208] = 1928
extra_map[1210] = 1930
extra_map[2098] = 2717
extra_map[2266] = 930
extra_map[2277] = 941
extra_map[2532] = 2008
extra_map[2561] = 708

for line in multi_ref:
    line = line.strip()
    line_type = line.split("-")[0]
    line_id = line.split("-")[1].split("\t")[0]
    line_content = line.split("\t")[1]
    if (line_type == 'S'):
        try:
            sys.append(sys_dict[src_dict[line_content]])
        except:
            sys.append(sys_dict[str(extra_map[int(line_id)])])
            # print(line_id)
            # print(line_content)
            # print(sys_dict[str(extra_map[int(line_id)])])
            # print()
        count = 0
    elif (line_type == 'T'):
        ori_ref.append(line_content)
    else:
        varaible["ref_list_" + str(count)].append(line_content)
        count += 1

ref = [ref_list_0, ref_list_1, ref_list_2, ref_list_3, ref_list_4,ref_list_5, ref_list_6, ref_list_7, ref_list_8, ref_list_9]

bleu = sacrebleu.corpus_bleu(sys, ref)
print("multi-ref max bleu")
print(bleu.score)

bleu = sacrebleu.corpus_bleu(sys, [ori_ref])
print("ori-ref bleu")
print(bleu.score)
