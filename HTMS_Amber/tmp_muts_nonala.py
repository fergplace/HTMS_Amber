import os 
import subprocess
import glob
import shutil

########################### MULTI-MUTATION SETUP ###########################

make_model_str = "python mutate_model_multi.py 6m0j_noHet"

E417N = [("417", amino_acids["N"])]
E417T = [("417", amino_acids["T"])]
S477N = [("477", amino_acids["N"])]
E484K = [("484", amino_acids["K"])]
N501Y = [("501", amino_acids["Y"])]
K417N_E484K = [("484", amino_acids["K"]), ("417", amino_acids["N"])]
K417T_E484K = [("484", amino_acids["K"]), ("417", amino_acids["T"])]
E484K_N501Y = [("484", amino_acids["K"]), ("501", amino_acids["Y"])]

mutations_dict ={"E417N": E417N, 
                 "E417T": E417T, 
                 "S477N": S477N, 
                 "E484K": E484K, 
                 "N501Y": N501Y,
                 "K417N_E484K": K417N_E484K,
                 "K417T_E484K": K417T_E484K,
                 "E484K_N501Y": E484K_N501Y}

for mutation , mut_input_list in mutations_dict.items() :
	#turn our arr of tuples into a input for sys.argv (kinda dumb, but will work)
	flattened_list = [str(item) for tup in mut_input_list for item in tup] 

	formatted_string_mut_in = ' '.join(flattened_list)

	# modeller_str = make_model_str + " " + mut_input_list + "asdasd" + " A"
	dir_str = "_" + mutation

	if not os.path.exists(dir_str):
		os.makedirs(dir_str)

	subprocess.run(f"{make_model_str} {mutation} A {formatted_string_mut_in}")


	#move the file into the dir. 
	pdb_file = f"6m0j_noHet{mutation}.pdb"
	subprocess.run(["move", pdb_file, dir_str], shell=True)

	os.chdir(dir_str) #step into dir, makes passing outputs easier 
	print(os.getcwd())
	sim_set_up_str = ["python", "../sim_set_up.py",  pdb_file]
	subprocess.run(sim_set_up_str)

	#subprocess.run(['sed', '-i', 's/\r$//', 'all_process.sh'])
	subprocess.run(["C:/Program Files/Git/usr/bin/sed", "-i", "s/\r$//", "all_process.sh"])
	#subprocess.run(['dos2unix', 'all_process.sh'])
	subprocess.run(["C:/Program Files/Git/usr/bin/sed", "-i", "s/\r$//", "'run_MMPBSA.sh'"])

	os.chdir("..")
	print(os.getcwd())
	#place in files into dir 
	for in_file in glob.glob("gen_in_files\*.in"):
		shutil.copy(in_file, dir_str)
  


####################### Single Mutation Setup ###########################

binding_site_idx = np.array([417, 439, 446, 453, 455, 475, 486, 487, 489, 493, 494, 496, 498, 500, 501, 502, 503, 505])

mkae_model_str = "python mutate_model.py 6m0j_noHet"



for idx in binding_site_idx :
    
    #lowest del_G
	#get row in DF
	# tmp_row = df_exp_data.loc[np.where(df_exp_data["site_SARS2"] == idx)].sort_values("bind_avg").iloc[0]
 
	#highest del G w/o wildtype 
	df_sorted = df_exp_data.loc[np.where(df_exp_data["site_SARS2"] == idx)].sort_values("bind_avg", ascending = False)
	df_no_wild= df_sorted.iloc[np.where(df_sorted["wildtype"] != df_sorted["mutant"])]
 
	tmp_row = df_no_wild.iloc[0]
 
	
	#get three letter code 
	tmp_three_letter_code = amino_acids[tmp_row["mutant"] ]
	# want this : subprocess.run("python mutate_model.py 6m0j_noHet 505 GLY A")
	dir_str = "_" +str(idx) +tmp_three_letter_code
	modeller_str = make_model_str + " " + str(idx) + " " + tmp_three_letter_code + " A"

	#subprocess.run(f"os cwd {dir_str}")

	if not os.path.exists(dir_str):
		os.makedirs(dir_str)

	#modeller command and place output in the directory
	subprocess.run(modeller_str)

	#move the file into the dir. 
	pdb_file = f"6m0j_noHet{tmp_three_letter_code}{idx}.pdb"
	subprocess.run(["mv", pdb_file, dir_str])
	
	os.chdir(dir_str) #step into dir, makes passing outputs easier 
	print(os.getcwd())
	sim_set_up_str = ["python", "../sim_set_up.py",  pdb_file]
	subprocess.run(sim_set_up_str)
 
	subprocess.run(['sed', '-i', 's/\r$//', 'all_process.sh'])
	#subprocess.run(['dos2unix', 'all_process.sh'])
	subprocess.run(['sed', '-i', 's/\r$//', 'run_MMPBSA.sh'])
	#subprocess.run(['dos2unix', 'run_MMPBSA.sh'])
	os.chdir("..")
	print(os.getcwd())
	#place in files into dir 
	for in_file in glob.glob("gen_in_files\*.in"):
		shutil.copy(in_file, dir_str)
    