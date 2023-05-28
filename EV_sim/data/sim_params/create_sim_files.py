import pickle


sim_dict = {
    "air_density [kg/m3]": 1.225,
    "road grade [in rad]": 0.003
}

a_file = open("sim_param.pkl", "wb")
pickle.dump(sim_dict, a_file)
a_file.close()