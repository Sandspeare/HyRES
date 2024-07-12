# %%
from transformers import AutoTokenizer, AutoModel
from datasets import load_from_disk
import json
import torch
import json
from tqdm import tqdm
import re
import torch.nn.functional as F
device = torch.device("cuda")


def mean_pooling(model_output, attention_mask):
    # First element of model_output contains all token embeddings
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(
        -1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def check_useless_name(name):
    pattern = r"mem\d+_\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"zero\d+"
    if re.search(pattern, name) != None:
        return True
    
    pattern = r"author\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"value\d+"
    if re.search(pattern, name) != None:
        return True
    
    pattern = r"value_\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"field\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"field_\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"zero_padding\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"zero_byte\d+"
    if re.search(pattern, name) != None:
        return True

    pattern = r"input_value\d+"
    if re.search(pattern, name) != None:
        return True
    
    if "unused" in name:
        return True
    
    if "data" == name:
        return True
    
    if "value" == name:
        return True
    
    return False


if __name__ == "__main__":

    text_tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
    text_encoder = AutoModel.from_pretrained("thenlper/gte-large").cuda()

    data = json.load(open("data.json"))
    similarity = open("similarity.facts", "w")
    fieldtype = open("fieldtype.facts", "w")
    
    structs = list(data.keys())

    names = set()
    for i in range(len(structs)):
        for key in data[structs[i]]:
            for name in data[structs[i]][key][1]:
                names.add(name)
                field = key.replace("mem_", "")
                fieldtype.write(f"{structs[i]};{field};{data[structs[i]][key][0]}\n")
    names = list(names)

    namembeding = {}
    with torch.no_grad():
        for i in range(len(names) // 128 + 1):
            batch_dict = text_tokenizer(names[i*128 : (i+1)*128], max_length=1024, padding=True, truncation=True, return_tensors='pt')
            batch_dict = batch_dict.to(device)
            output = text_encoder(**batch_dict)
            output = mean_pooling(output, batch_dict['attention_mask'])
            for j in range(len(output)):
                namembeding[names[i*128 : (i+1)*128][j]] = output[j:j+1]

    result = {}
    for i in tqdm(range(len(structs))):
        for j in range(len(structs)):
            if j == i:
                continue
            structA = data[structs[i]]
            structB = data[structs[j]]

            for field in range(4096):
                if f"mem_{field}" in structA and f"mem_{field}" in structB: 

                    for m in structA[f"mem_{field}"][1]:
                        for n in structB[f"mem_{field}"][1]:
                            logits = int(F.cosine_similarity(namembeding[m], namembeding[n])[0] * 100)
                            pattern = r"mem\d+_\d+"
                            if check_useless_name(m) or check_useless_name(n):
                                logits = -1
                            # similarity.write(f"{logits};{m};{n};{field};{structs[i]};{structs[j]}\n")

                            if f"{field};{structs[i]};{structs[j]}" not in result:
                                result[f"{field};{structs[i]};{structs[j]}"] = [f"{m};{n}", logits]
                            
                            if result[f"{field};{structs[i]};{structs[j]}"][1] < logits:
                                result[f"{field};{structs[i]};{structs[j]}"] = [f"{m};{n}", logits]
    
    for key in result:
        similarity.write(f"{result[key][1]};{key};{result[key][0]}\n")
                            
    fieldtype.close()
    similarity.close()