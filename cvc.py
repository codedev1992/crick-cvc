import pandas as pd
import random 
from io import BytesIO 
import streamlit as st 


input_txt = st.text_area("C and VC combination Details", height=300)
opt_fname = st.text_input("Output File Name")
btn_process = st.button("process")

occurrence_pairs = {}

def repeat_names(occurrences):
    repeated_names = []
    for name, count in occurrences:
        # Ensure the count is an integer, and ignore if count is zero
        count = int(count) if count else 0
        # Extend the list with the name repeated 'count' times
        repeated_names.extend([name] * count)
    return repeated_names

if btn_process:
    local = {}
    lines = input_txt.split("\n")
    for line in lines:
        values = line.split("\t")
        if len(values) == 3:
            if values[1].lower() == "c" or values[1].lower() == "vc":
                pass 
            else:
                name = values[0]
                C = 0 if values[1] == "" else  int(values[1])
                VC = 0 if values[2] == "" else  int(values[2])

                occurrence_pairs[name] = (C, VC)
    
    
    # Repeat names for the C column
    names_repeated_by_first_occurrence = repeat_names([(name, occurrences[0]) for name, occurrences in occurrence_pairs.items()])

    # Repeat names for the VC column
    names_repeated_by_second_occurrence = repeat_names([(name, occurrences[1]) for name, occurrences in occurrence_pairs.items()])

    # print(names_repeated_by_first_occurrence, names_repeated_by_second_occurrence)

    result = []
    
    iter_count = len(names_repeated_by_first_occurrence)
    for itr in range(iter_count):
        is_element_found = True
        c = random.choice(names_repeated_by_first_occurrence)
        names_repeated_by_first_occurrence.remove(c)

        while is_element_found:
            vc = random.choice(names_repeated_by_second_occurrence)
            if c != vc:
                is_element_found = False
                names_repeated_by_second_occurrence.remove(vc)

                result.append([c,vc])
            
    # file_path = r"./BAN_NZ_CVC_Listing-output.xlsx"

    df = pd.DataFrame(result, columns=['C', 'VC'])

    data = BytesIO(df.to_csv(index=False).encode('utf-8'))

    st.download_button(label="Click to Download Result",
                        data=data,
                        file_name=f"{opt_fname}.csv",
                        mime='application/octet-stream')
